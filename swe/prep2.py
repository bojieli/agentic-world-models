"""CPU prep for phase-2 measures. Builds, for both datasets, the scoring segments (windows that END at scored
observations), the M1 per-token metadata, and the branch suffixes for M2 (action swap), M3 (forced choice + leak
check) and M4 (outcome probe). Output: work/<ds>.pkl consumed by run.py (GPU) and analyze2.py.

usage: prep2.py [--W 16384] [--max-segs 2]
"""
import argparse, collections, gzip, json, pickle, random, re, os
import numpy as np
from common import *

ap = argparse.ArgumentParser()
ap.add_argument("--W", type=int, default=16384)
ap.add_argument("--max-segs", type=int, default=2)
ap.add_argument("--m2-per-traj", type=int, default=4)
ap.add_argument("--obs-cap", type=int, default=4096)
ap.add_argument("--asst-cap", type=int, default=3072)
ap.add_argument("--task_cap", type=int, default=8192)
ap.add_argument("--m2-obs-cap", type=int, default=512)
ap.add_argument("--m3-prefix-cap", type=int, default=1500)
ap.add_argument("--swe-cal", type=int, default=30)
ap.add_argument("--limit", type=int, default=0, help="debug: trajectories per split")
ap.add_argument("--out", default=os.path.join(HERE, "work"))
ap.add_argument("--datasets", default="tp,swe")
ap.add_argument("--no-m3m4", action="store_true", help="skip M3 forced-choice and M4 probe branches")
ap.add_argument("--reading", action="store_true", help="reading test: next-action NLL with the observation shown vs hidden")
ap.add_argument("--max-segs-swe", type=int, default=0, help="override --max-segs for SWE")
ap.add_argument("--hash-only", default=None, help="write per-trajectory rendered-id hashes (json) and exit")
A = ap.parse_args()
os.makedirs(A.out, exist_ok=True)
enc = Enc()
rng = random.Random(0)

# ---------------------------------------------------------------- load
def load_tp():
    prep = json.load(open(os.path.join(ROOT, "terminal", "prep.json")))
    rows = {r["id"]: r for r in map(json.loads, gzip.open(os.path.join(ROOT, "terminal", "data", "trajectories.jsonl.gz"), "rt"))}
    out = []
    for split, ids in [("cal", prep["cal"]), ("eval", prep["eval"])]:
        for tid in ids[: A.limit or None]:
            r = rows[tid]; msgs = []
            for i, m in enumerate(r["messages"]):
                parts = [[p[0], p[2], p[3]] for p in m["parts"]]
                if i == 0:
                    msgs.append(dict(role="task", content=m["content"], parts=parts)); continue
                if m["role"] == "assistant":
                    msgs.append(dict(role="asst", content=m["content"], parts=parts, ks=keystrokes_of(m))); continue
                d = dict(role="obs", content=m["content"], parts=parts)
                prev = msgs[-1]
                strip = strip_echo(m["content"])
                d["stripped"] = strip
                ks = prev.get("ks", "") if prev["role"] == "asst" else ""
                valid = bool(ks.strip()) and "Are you sure you want to mark the task as complete" not in m["content"]
                lab = label(None, ks, strip)
                d.update(valid=valid, kind=lab["obs_kind"], error=lab["error"], tests_pass=lab["tests_pass"],
                         cmd=ks, asst=len(msgs) - 1 if prev["role"] == "asst" else None)
                msgs.append(d)
            out.append(dict(id=tid, split=split, ds="tp", task=r["task_id"], teacher=r["teacher"], msgs=msgs))
    return out


def load_swe():
    rows = [json.loads(l) for l in gzip.open(os.path.join(HERE, "data", "swe_rebench.jsonl.gz"), "rt")]
    tasks = sorted({r["task_id"] for r in rows}); random.Random(1).shuffle(tasks)
    cal_tasks, n = set(), 0
    for t in tasks:  # disjoint by task calibration split of ~swe_cal trajectories
        if n >= A.swe_cal:
            break
        cal_tasks.add(t); n += sum(r["task_id"] == t for r in rows)
    out = []
    for split in ["cal", "eval"]:
        sel = [r for r in rows if (r["task_id"] in cal_tasks) == (split == "cal")][: A.limit or None]
        for r in sel:
            obs_iter = iter(r["observations"])
            text_pos = 0; msgs = []
            for i, m in enumerate(r["messages"]):
                tag = len(("<|user|>" if m["role"] == "user" else "<|assistant|>").encode())
                cstart = text_pos + tag; cend = cstart + len(m["content"].encode())
                text_pos = cend
                ps = m["parts"]
                parts = [[p[0], p[2], ps[k + 1][2] if k + 1 < len(ps) else len(m["content"])] for k, p in enumerate(ps)]
                if i == 0:
                    msgs.append(dict(role="task", content=m["content"], parts=parts)); continue
                if m["role"] == "assistant":
                    msgs.append(dict(role="asst", content=m["content"], parts=parts,
                                     n_act=sum(p[0] == "action" for p in parts))); continue
                d = dict(role="obs" if m.get("tool_result") else "other", content=m["content"], parts=parts,
                         stripped=m["content"], valid=False)
                is_obs = any(p[0] == "observation" for p in parts) or (m.get("tool_result") and not parts)
                if is_obs:
                    o = next(obs_iter)
                    assert cstart <= o["byte_start"] <= cend, (r["id"], i)
                    a = len(msgs) - 1
                    while a >= 0 and msgs[a]["role"] != "asst":
                        a -= 1
                    d.update(valid=msgs[a].get("n_act") == 1 and a == len(msgs) - 1,
                             kind=o["obs_kind"], error=o["error"], tests_pass=o["tests_pass"], cmd=o["command"] or "",
                             asst=a, exit_code=o["exit_code"], tool=o["tool"])
                else:
                    d["role"] = "other"
                msgs.append(d)
            out.append(dict(id=r["id"], split=split, ds="swe", task=r["task_id"], teacher=r["teacher"], msgs=msgs))
    return out


# ---------------------------------------------------------------- rendering
def headers(ds, m):
    if m["role"] == "asst":
        return "<|im_start|>assistant\n", "<|im_end|>\n"
    if ds == "swe" and m["role"] == "obs":
        return "<|im_start|>user\n<tool_response>\n", "\n</tool_response><|im_end|>\n"
    return "<|im_start|>user\n", "<|im_end|>\n"


def render(tr):
    """per message: ids, type per token ('wrap'/'task'/'thought'/'action'/'markup'/'observation'), obs token classes"""
    for m in tr["msgs"]:
        h, f = headers(tr["ds"], m)
        cid, offs = enc.content(m["content"])
        cap = {"task": A.task_cap, "asst": A.asst_cap}.get(m["role"], A.obs_cap)
        cid, offs = cid[:cap], offs[:cap]
        typ = []
        for s, _ in offs:
            t = "markup"
            for p in m["parts"]:
                if p[1] <= s < p[2]:
                    t = p[0]; break
            typ.append(t)
        cls = token_classes(m["content"], offs, tr["ds"] == "tp") if m["role"] == "obs" else None
        hid, fid = enc.plain(h), enc.plain(f)
        m["ids"] = hid + cid + fid
        m["typ"] = ["wrap"] * len(hid) + typ + ["wrap"] * len(fid)
        m["cls"] = None if cls is None else np.concatenate([np.full(len(hid), -1, np.int8), cls, np.full(len(fid), -1, np.int8)])
        m["hlen"] = len(hid)


def segments(tr):
    L = [len(m["ids"]) for m in tr["msgs"]]
    n = len(L); task = L[0]; segs = []
    e = n
    maxs = A.max_segs_swe if (tr["ds"] == "swe" and A.max_segs_swe) else A.max_segs
    while e > 1 and len(segs) < maxs:
        s = e
        while s > 1 and task + sum(L[s - 1:e]) <= A.W:
            s -= 1
        if s == e:  # single message larger than W: skip it
            e -= 1; continue
        ctx = task; scored = []
        for mi in range(s, e):
            if tr["msgs"][mi]["role"] == "obs" and (s == 1 or ctx >= A.W // 2):
                scored.append(mi)
            ctx += L[mi]
        segs.append(dict(s=s, e=e, scored=scored))
        if s == 1 or not scored:
            break
        e = scored[0]
    return segs[::-1]


# ---------------------------------------------------------------- copy flags
class NgramIndex:
    """first end-position of every 8-gram in a token sequence"""
    def __init__(self, ids):
        self.first = {}
        for i in range(NGRAM - 1, len(ids)):
            g = tuple(ids[i - NGRAM + 1:i + 1])
            if g not in self.first:
                self.first[g] = i
        self.ids = ids

    def copy_flags(self, start, end):
        out = np.zeros(end - start, np.int8)
        for i in range(max(start, NGRAM - 1), end):
            if self.first[tuple(self.ids[i - NGRAM + 1:i + 1])] < i:
                out[i - start] = 1
        return out

    def copy_suffix(self, ctx_len, suffix, lo):
        """flags for suffix[lo:] given context ids[:ctx_len] + suffix"""
        full = list(self.ids[max(0, ctx_len - NGRAM + 1):ctx_len]) + list(suffix)
        off = len(full) - len(suffix)
        seen = set()
        out = np.zeros(len(suffix) - lo, np.int8)
        for i in range(NGRAM - 1, len(full)):
            g = tuple(full[i - NGRAM + 1:i + 1])
            j = i - off
            if j >= lo and (g in seen or self.first.get(g, 1 << 60) < ctx_len - 0):
                out[j - lo] = 1
            seen.add(g)
        return out


# ---------------------------------------------------------------- M2 helpers
def asst_variants(tr, ai):
    """(blanked-thought content, action-region text, region bounds) of assistant message ai"""
    m = tr["msgs"][ai]; c = m["content"]
    if tr["ds"] == "tp":
        acts = [p for p in m["parts"] if p[0] == "action"]
        if not acts:
            return None
        a0, a1 = acts[0][1], acts[-1][2]
        # turns whose message holds several JSON objects / thoughts between commands (28 of ~3.6k held-out turns)
        # cannot be spliced cleanly: excluded from M2 targets and swap pools
        if any(p[0] == "thought" and a0 <= p[1] < a1 for p in m["parts"]) or c.count('"analysis"') > 1:
            return None
        return dict(content=c, a0=a0, a1=a1, thoughts=[(p[1], p[2]) for p in m["parts"] if p[0] == "thought"])
    mk = [p for p in m["parts"] if p[0] in ("markup", "action")]
    if not mk:
        return None
    return dict(content=c, a0=mk[0][1], a1=len(c), thoughts=[(p[1], p[2]) for p in m["parts"] if p[0] == "thought"])


def asst_text(tr, v, region=None):
    """assistant text with thoughts blanked and the action region optionally replaced"""
    c = v["content"]
    if tr["ds"] == "swe":
        return (region if region is not None else c[v["a0"]:v["a1"]]).lstrip("\n")
    pieces, pos = [], 0
    cuts = sorted([(s, e, "") for s, e in v["thoughts"]] + [(v["a0"], v["a1"], region if region is not None else None)])
    for s, e, rep in cuts:
        pieces.append(c[pos:s]); pieces.append(c[s:e] if rep is None else rep); pos = e
    pieces.append(c[pos:])
    return "".join(pieces)


def region_text(tr, v):
    return v["content"][v["a0"]:v["a1"]]


# ---------------------------------------------------------------- M3 helpers
PYTEST_PROGRESS = re.compile(r"PASSED|FAILED|XFAIL|XPASS|^ERROR\b|^\S+\.py\s+[.FEsxX]+|^[.FEsxX]{2,}\s*(\[\s*\d+%\])?\s*$|"
                             r"^(?:ok|FAIL|ERROR)\s*$|\.\.\. (?:ok|FAIL|ERROR)\b|^Ran \d+ tests?", re.M)
SUMMARY_RE = re.compile(r"^(=+ )?((?:\d+ (?:failed|passed|errors?|skipped|xfailed|xpassed|warnings?|deselected|rerun)(?:, )?)+)( in [\d.]+s)", re.M)
NUMTOK_RE = re.compile(r"(?<![\w.\-/:])-?\d+(?:\.\d+)?(?![\w.]*[\w/])")
PYFIRST_RE = re.compile(r"^(\S+::\S+) (PASSED|FAILED|ERROR|SKIPPED)\b|^(\S+\.py) ([.FEs])", re.M)
BOOL_RE = re.compile(r"\b(True|False)\b")


def pytest_alts(counts, rng):
    """counts: ordered list of (n, word). Returns up to 3 alternative count phrases with same total of
    passed+failed+error(s) and other parts unchanged."""
    d = {w.rstrip("s") if w.startswith("error") else w: n for n, w in counts}
    p, f, e = d.get("passed", 0), d.get("failed", 0), d.get("error", 0)
    N = p + f + e
    if N == 0:
        return None
    alts = set()
    cands = [(N, 0, 0), (N - 1, 1, 0), (0, N, 0), (N - 2, 2, 0), (N - 1, 0, 1), (max(N // 2, 1), N - max(N // 2, 1), 0)]
    for _ in range(30):
        k = rng.randint(1, N); cands.append((N - k, k, 0))
    for c in cands:
        if c != (p, f, e) and min(c) >= 0 and sum(c) == N:
            alts.add(c)
    alts = list(alts); rng.shuffle(alts)
    # prefer the canonical ones first
    alts.sort(key=lambda c: 0 if c in cands[:3] else 1)
    out = []
    for pp, ff, ee in alts[:3]:
        parts = []
        for n, w in counts:
            key = w.rstrip("s") if w.startswith("error") else w
            if key in ("passed", "failed", "error"):
                continue
            parts.append((n, w))
        new = []
        if ff: new.append(f"{ff} failed")
        if pp: new.append(f"{pp} passed")
        for n, w in counts:  # keep other entries in place (skipped, warnings...) after passed
            key = w.rstrip("s") if w.startswith("error") else w
            if key not in ("passed", "failed", "error"):
                new.append(f"{n} {w}")
        if ee: new.append(f"{ee} error" + ("s" if ee > 1 else ""))
        out.append(", ".join(new))
    return out


def same_format_numbers(num, pool, rng, exclude):
    fmt = (num.startswith("-"), len(num.lstrip("-").split(".")[0]), len(num.split(".")[1]) if "." in num else -1)
    c = [x for x in pool.get(fmt, []) if x != num and x not in exclude]
    rng.shuffle(c)
    out = []
    for x in c:
        if x not in out:
            out.append(x)
        if len(out) == 3:
            break
    tries = 0
    while len(out) < 3 and tries < 200:  # rule-based fallback: random digits in the same format
        tries += 1
        neg, ni, nd = fmt
        if ni == 1:
            ip = str(rng.randint(0, 9))
        else:
            ip = str(rng.randint(10 ** (ni - 1), 10 ** ni - 1))
        x = ("-" if neg else "") + ip + ("." + "".join(str(rng.randint(0, 9)) for _ in range(nd)) if nd >= 0 else "")
        if x != num and x not in out and x not in exclude:
            out.append(x)
    return out if len(out) == 3 else None


def num_fmt(x):
    return (x.startswith("-"), len(x.lstrip("-").split(".")[0]), len(x.split(".")[1]) if "." in x else -1)


# ---------------------------------------------------------------- questions (M4)
Q_SUCC = "Will the command(s) above run successfully, without any error? Answer with only Yes or No."
Q_TEST = "Will all of the tests run by the command(s) above pass? Answer with only Yes or No."
Q_CLS = ("The command(s) above will fail with an error. Which kind of error?\n" + ERRCLS_TEXT +
         "\nAnswer with only the letter.")
FS_SUCC = ("\n--- Quiz: predict the outcome of the last command in the transcript above ---\n"
           "Command: ls /nonexistent_dir\nRuns without error: No\n"
           "Command: echo hello\nRuns without error: Yes\n"
           "Command: python -c \"import json; print(json.dumps({'a': 1}))\"\nRuns without error: Yes\n"
           "Command: python -c \"import numpy_typo\"\nRuns without error: No\n"
           "Command: {cmd}\nRuns without error:")
FS_TEST = ("\n--- Quiz: predict the outcome of the last command in the transcript above ---\n"
           "Command: pytest tests/test_parser.py -q   (bug not yet fixed)\nAll tests pass: No\n"
           "Command: python -m pytest tests/test_utils.py   (after the fix)\nAll tests pass: Yes\n"
           "Command: pytest tests/ -x -q   (new test added for unimplemented feature)\nAll tests pass: No\n"
           "Command: pytest tests/test_io.py::test_roundtrip -q   (existing passing test)\nAll tests pass: Yes\n"
           "Command: {cmd}\nAll tests pass:")
FS_CLS = ("\n--- Quiz: which kind of error will the last command in the transcript above produce? ---\n" + ERRCLS_TEXT + "\n"
          "Command: python -c \"import numpy_typo\"\nError: A\n"
          "Command: python -c \"print('a'\"\nError: B\n"
          "Command: pytest tests/test_core.py   (bug not yet fixed)\nError: C\n"
          "Command: python -c \"x = None; x.foo()\"\nError: D\n"
          "Command: python -c \"int('abc')\"\nError: E\n"
          "Command: cat /no/such/file\nError: F\n"
          "Command: {cmd}\nError:")
NATIVE = "<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
YN_NATIVE = [enc.plain("Yes")[0], enc.plain("No")[0]]
YN_PLAIN = [enc.plain(" Yes")[0], enc.plain(" No")[0]]
LET_NATIVE = [enc.plain(x)[0] for x in ERRCLS]
LET_PLAIN = [enc.plain(" " + x)[0] for x in ERRCLS]


def short_cmd(c):
    c = (c or "").strip().replace("\n", " ⏎ ")
    return c if len(c) <= 300 else c[:300] + " …"


# ---------------------------------------------------------------- main build
def build(ds, trajs):
    for tr in trajs:
        render(tr)
    # pools for M2 swaps and M3 foils
    act_pool = collections.defaultdict(list)  # kind -> [(traj idx, asst idx, region text)]
    exc_pool = collections.Counter(); num_pool = collections.defaultdict(list)
    for ti, tr in enumerate(trajs):
        for mi, m in enumerate(tr["msgs"]):
            if m["role"] == "obs" and m.get("valid"):
                v = asst_variants(tr, m["asst"])
                if v:
                    act_pool[m["kind"]].append((ti, m["asst"], region_text(tr, v)))
                st = m["stripped"]
                for q in EXC_RE.finditer(ANSI_RE.sub("", st)):
                    if "." not in q.group(1):
                        exc_pool[q.group(1)] += 1
                if m["kind"] in EXEC_KINDS:
                    for q in NUMTOK_RE.finditer(st):
                        num_pool[num_fmt(q.group(0))].append(q.group(0))
    exc_names = [k for k, v in exc_pool.items() if v >= 2]
    exc_w = [exc_pool[k] for k in exc_names]
    print(ds, "exception pool", len(exc_names), exc_pool.most_common(12), flush=True)

    segs_out, m1_meta, items = [], collections.defaultdict(list), dict(m2=[], m3=[], m4=[], read=[])
    n_act_total = [0]
    pending = []
    stat = collections.Counter()
    for ti, tr in enumerate(trajs):
        msgs = tr["msgs"]
        m2_cands = []
        for sg in segments(tr):
            order = [0] + list(range(sg["s"], sg["e"]))
            ids, starts = [], {}
            for mi in order:
                starts[mi] = len(ids); ids += msgs[mi]["ids"]
            ng = NgramIndex(ids)
            branches = collections.defaultdict(list)  # boundary pos -> branch list
            score_pos = []
            act_pos = []
            seg_id = len(segs_out)
            for mi in sg["scored"]:
                m = msgs[mi]; p0 = starts[mi]
                cp = ng.copy_flags(p0, p0 + len(m["ids"]))
                for k, t in enumerate(m["typ"]):
                    if t == "observation":
                        score_pos.append(p0 + k)
                        for key, val in [("cls", m["cls"][k]), ("copy", cp[k]), ("traj", ti), ("msg", mi), ("seg", seg_id),
                                         ("kind", m.get("kind", "?")), ("err", int(bool(m.get("error")))),
                                         ("split", tr["split"]), ("tokpos", k - m["hlen"])]:
                            m1_meta[key].append(val)
                stat["m1_tokens"] += sum(t == "observation" for t in m["typ"])
                if not m.get("valid") or m["asst"] not in starts:
                    continue
                ai = m["asst"]
                aprev = ai - 1
                while aprev > 0 and msgs[aprev]["role"] != "asst":
                    aprev -= 1
                base = dict(traj=ti, msg=mi, split=tr["split"], kind=m["kind"], error=int(bool(m["error"])),
                            tests_pass=m["tests_pass"], task=tr["task"], teacher=tr["teacher"])
                # previous observation label (baseline feature)
                pj = mi - 1
                while pj > 0 and not (msgs[pj]["role"] == "obs" and msgs[pj].get("valid")):
                    pj -= 1
                base["prev_error"] = int(bool(msgs[pj].get("error"))) if pj > 0 else -1
                base["prog"] = (first_programs(m["cmd"]) or ["?"])[0] if m["cmd"] else "?"
                # ---------------- M4 probes at the observation boundary
                kq = f"m4:{ds}:{ti}:{mi}"
                bl = branches[p0] if not A.no_m3m4 else []
                bl.append(dict(t="next", key=kq + ":succ:n", nodes=[enc.plain(NATIVE.replace("{q}", Q_SUCC))], cands=YN_NATIVE))
                bl.append(dict(t="next", key=kq + ":succ:p", nodes=[enc.plain(FS_SUCC.replace("{cmd}", short_cmd(m["cmd"])))], cands=YN_PLAIN))
                if m["tests_pass"] is not None:
                    bl.append(dict(t="next", key=kq + ":test:n", nodes=[enc.plain(NATIVE.replace("{q}", Q_TEST))], cands=YN_NATIVE))
                    bl.append(dict(t="next", key=kq + ":test:p", nodes=[enc.plain(FS_TEST.replace("{cmd}", short_cmd(m["cmd"])))], cands=YN_PLAIN))
                ecls = error_class(m["stripped"]) if m["error"] else None
                if ecls:
                    bl.append(dict(t="next", key=kq + ":cls:n", nodes=[enc.plain(NATIVE.replace("{q}", Q_CLS))], cands=LET_NATIVE))
                    bl.append(dict(t="next", key=kq + ":cls:p", nodes=[enc.plain(FS_CLS.replace("{cmd}", short_cmd(m["cmd"])))], cands=LET_PLAIN))
                if not A.no_m3m4:
                    items["m4"].append(dict(base, key=kq, ecls=ecls))
                # ---------------- reading test: next action with this observation shown (main pass) vs hidden (branch)
                nx = mi + 1
                if A.reading and tr["split"] == "eval" and nx < sg["e"] and msgs[nx]["role"] == "asst":
                    ak = [k for k, t in enumerate(msgs[nx]["typ"]) if t == "action"]
                    if ak:
                        hh, ff = headers(ds, m)
                        pre = enc.plain(hh) + enc.content("[output omitted]")[0] + enc.plain(ff)
                        key = f"rd:{ds}:{ti}:{mi}"
                        branches[p0].append(dict(t="nll", key=key + ":hidden", nodes=[pre + msgs[nx]["ids"]],
                                                 pos=[len(pre) + k for k in ak]))
                        act_pos += [starts[nx] + k for k in ak]
                        items["read"].append(dict(base, key=key, n_act=len(ak), seg=seg_id, act_off=n_act_total[0]))
                        n_act_total[0] += len(ak)
                # ---------------- M2 candidates (decided per trajectory below)
                h, f = headers(ds, m)
                sid, soffs = enc.content(m["stripped"])
                sid, soffs = sid[:A.m2_obs_cap], soffs[:A.m2_obs_cap]
                if sid and tr["split"] == "eval":
                    m2_cands.append(dict(base, seg=seg_id, bpos=starts[ai], ai=ai, sid=sid, soffs=soffs, h=h, f=f))
                # ---------------- M3 spans (foils for number/err_class are assigned after all items are known)
                if msgs[aprev]["role"] == "asst" and aprev in starts and aprev >= sg["s"]:
                    ctx_text = "\n".join(msgs[j]["content"] for j in order if j < mi)
                    for j, it in enumerate(m3_spans(ds, tr, m, ti, mi, base) if not A.no_m3m4 else []):
                        pending.append(dict(seg=seg_id, p0=p0, pl=starts[aprev], h=h, f=f, ctx=ctx_text, j=j, base=base, it=it))
            segs_out.append(dict(traj=ti, ids=np.array(ids, np.int32), score_pos=np.array(score_pos, np.int64),
                                 act_pos=np.array(act_pos, np.int64), branches={k: v for k, v in branches.items() if v}))
            stat["main_tokens"] += len(ids)
        # ---------------- M2: choose up to K per trajectory, build swap branches
        rng.shuffle(m2_cands)
        for c in m2_cands[: A.m2_per_traj]:
            sg_ = segs_out[c["seg"]]
            v = asst_variants(tr, c["ai"])
            if v is None:
                stat["m2_drop_unspliceable"] += 1; continue
            true_region = region_text(tr, v)
            same = [x for x in act_pool[c["kind"]] if x[0] == ti and x[1] != c["ai"] and x[2].strip() != true_region.strip()]
            src = "same"
            if len(same) < 2:
                same = [x for x in act_pool[c["kind"]] if x[0] != ti and x[2].strip() != true_region.strip()]
                src = "other"
            if len(same) < 2:
                continue
            sA, sB = rng.sample(same, 2)
            texts = [asst_text(tr, v), asst_text(tr, v, sA[2] if ds == "tp" else sA[2]), asst_text(tr, v, sB[2])]
            if ds == "tp":  # swap regions come from another message's content; splice
                texts = [asst_text(tr, v), asst_text(tr, v, sA[2]), asst_text(tr, v, sB[2])]
            ha, fa = headers(ds, dict(role="asst"))
            obs_ids = enc.plain(c["h"]) + c["sid"]
            # content mask (true condition): obs token classes + copy vs context + true suffix
            scls = token_classes(c["stripped"] if "stripped" in c else tr["msgs"][c["msg"]]["stripped"], c["soffs"], ds == "tp")
            true_suffix = enc.plain(ha) + enc.content(texts[0])[0] + enc.plain(fa) + obs_ids
            lo = len(true_suffix) - len(c["sid"])
            ngi = NgramIndex(list(sg_["ids"]))
            cpy = ngi.copy_suffix(c["bpos"], true_suffix, lo)
            content = np.isin(scls, CONTENT_CLS) & (cpy == 0)
            outcome = np.isin(scls, OUTCOME_CLS) & (cpy == 0)
            if content.sum() < 3:
                stat["m2_drop_nocontent"] += 1; continue
            key = f"m2:{ds}:{ti}:{c['msg']}"
            for nm, t in zip(["true", "swapA", "swapB"], texts):
                suf = enc.plain(ha) + enc.content(t)[0] + enc.plain(fa) + obs_ids
                lo_ = len(suf) - len(c["sid"])
                pos = (lo_ + np.nonzero(content | outcome)[0]).tolist()
                sg_["branches"].setdefault(int(c["bpos"]), []).append(dict(t="nll", key=f"{key}:{nm}", nodes=[suf], pos=pos))
            sel = content[content | outcome]
            items["m2"].append(dict({k: c[k] for k in ["traj", "msg", "split", "kind", "error", "task", "teacher"]},
                                    key=key, src=src, content=content[content | outcome].astype(np.int8),
                                    outcome=outcome[content | outcome].astype(np.int8),
                                    n_content=int(content.sum()), n_outcome=int(outcome.sum())))
    assign_m3(ds, pending, segs_out, items, stat)
    # stats on branch tokens
    for sg in segs_out:
        for bl in sg["branches"].values():
            for b in bl:
                stat["branch_tokens_" + b["key"].split(":")[0]] += sum(len(n) for n in b["nodes"])
                stat["n_branch"] += 1
        stat["n_boundaries"] += len(sg["branches"])
    m1 = {k: np.array(v) for k, v in m1_meta.items()}
    print(ds, dict(stat), {k: len(v) for k, v in items.items()}, flush=True)
    print(ds, "m3 types", collections.Counter((i["type"], i["outcome_err"]) for i in items["m3"]), flush=True)
    return dict(ds=ds, trajs=[dict(id=t["id"], split=t["split"], task=t["task"], teacher=t["teacher"]) for t in trajs],
                segs=segs_out, m1=m1, items=items, args=vars(A), stat=dict(stat))


def in_text(x, text, numeric):
    if numeric:
        return re.search(r"(?<![\d.])" + re.escape(x) + r"(?![\d])", text) is not None
    return re.search(r"\b" + re.escape(x) + r"\b", text) is not None


def assign_m3(ds, pending, segs_out, items, stat):
    """Exchangeable foils: for number and err_class items the foils are drawn (frequency-weighted) from the TRUE
    answers of the other eligible items of the same type and format, so a context-free prior cannot beat chance in
    expectation. Items whose true answer already appears in the context window (copyable) are dropped, and foils that
    appear in the context, the observation prefix or the line lead are excluded."""
    elig = []
    for p in pending:
        it = p["it"]
        if it["type"] in ("number", "err_class"):
            num = it["type"] == "number"
            if in_text(it["true"], p["ctx"], num):
                stat[f"m3_drop_true_in_ctx_{it['type']}"] += 1; continue
        elig.append(p)
    # foil pools: true answers of eligible items of the SAME TASK (all its trajectories, incl. this one), same type and
    # digit format, so the history without the action cannot tell which answer belongs to this observation; exception
    # classes fall back to the dataset-wide pool when the task has too few.
    pool_task = collections.defaultdict(collections.Counter); pool_all = collections.defaultdict(collections.Counter)
    for p in elig:
        it = p["it"]
        if it["type"] in ("number", "err_class"):
            key = ("number", num_fmt(it["true"])) if it["type"] == "number" else ("err_class",)
            pool_task[(p["base"]["task"],) + key][it["true"]] += 1
            pool_all[key][it["true"]] += 1
    for p in elig:
        it = dict(p["it"])
        if it["type"] in ("number", "err_class"):
            num = it["type"] == "number"
            key = ("number", num_fmt(it["true"])) if num else ("err_class",)
            seen = p["ctx"] + "\n" + it["prefix"] + it["lead"]
            r2 = random.Random(hash((p["base"]["traj"], p["base"]["msg"], p["j"])) & 0xffffffff)
            foils, src = [], None
            for src_name, pool in [("task", pool_task[(p["base"]["task"],) + key])] + ([("dataset", pool_all[key])] if not num else []):
                cand = {k: v for k, v in pool.items() if k != it["true"] and not in_text(k, seen, num)}
                if len(cand) < 3:
                    continue
                while len(foils) < 3:
                    k = r2.choices(list(cand), weights=list(cand.values()))[0]
                    foils.append(k); cand.pop(k)
                src = src_name
                break
            if len(foils) < 3:
                stat[f"m3_drop_nofoil_{it['type']}"] += 1; continue
            it["foils"] = foils; it["foil_src"] = src
            it["conts_text"] = [it["lead"] + it["true"]] + [it["lead"] + x for x in foils]
        P = enc.plain(p["h"]) + (enc.content(it["prefix"])[0] if it["prefix"] else [])
        if len(P) > A.m3_prefix_cap:
            stat["m3_drop_prefix"] += 1; continue
        conts = [enc.content(c)[0] if c else [] for c in it["conts_text"]]
        if it["type"] == "grep":
            conts = [enc.plain(p["f"])[:2]]
        if any(len(c) == 0 for c in conts):
            continue
        key = f"m3:{ds}:{p['base']['traj']}:{p['base']['msg']}:{it['type']}{p['j']}"
        sg = segs_out[p["seg"]]["branches"]
        sg.setdefault(p["p0"], []).append(dict(t="fork", key=key + ":full", nodes=[P] + conts))
        sg.setdefault(p["pl"], []).append(dict(t="fork", key=key + ":leak", nodes=[P] + conts))
        it.pop("prefix"); it.pop("conts_text")
        items["m3"].append(dict(p["base"], key=key, **it))


def m3_spans(ds, tr, m, ti, mi, base):
    """forced-choice items on the (echo-stripped) observation. Each item: prefix text (up to the start of the span's
    line), candidate line-prefixes (true first), type, outcome_err flag."""
    st = m["stripped"]; out = []
    act = m["cmd"] or ""
    # grep hit / no-hit (SWE: empty tool output)
    progs = first_programs(act)
    if ds == "swe" and m["kind"] == "search" and progs and progs[0] in ("grep", "egrep", "rg", "git-grep"):
        out.append(dict(type="grep", prefix="", conts_text=[""], nohit=int(st.strip() == ""), outcome_err=int(st.strip() == ""),
                        n_cand=1))
    if not st.strip():
        return out
    plain = st
    # error class (foils assigned later from the pool of true answers)
    for q in EXC_RE.finditer(plain):
        name = q.group(1)
        if "." in name:
            continue
        ls = plain.rfind("\n", 0, q.start(1)) + 1
        prefix = plain[:ls]; lead = plain[ls:q.start(1)]
        if not in_text(name, prefix + lead, False):
            out.append(dict(type="err_class", prefix=prefix, lead=lead, true=name, outcome_err=1, n_cand=4))
        break
    # pytest summary counts
    sm = list(SUMMARY_RE.finditer(plain))
    if sm:
        q = sm[-1]
        ls = plain.rfind("\n", 0, q.start()) + 1
        prefix = plain[:ls]
        if not PYTEST_PROGRESS.search(prefix):
            counts = [(int(a), b) for a, b in re.findall(r"(\d+) (\w+)", q.group(2))]
            alts = pytest_alts(counts, random.Random(hash((ti, mi, "py")) & 0xffffffff))
            if alts and len(alts) == 3:
                lead = plain[ls:q.start(2)]
                true = q.group(2).rstrip(", ")
                out.append(dict(type="pytest", prefix=prefix, conts_text=[lead + true] + [lead + a for a in alts], true=true,
                                foils=alts, outcome_err=int(bool(re.search(r"failed|error", true))), n_cand=4))
        else:
            STAT_DROP["pytest_progress_leak"] += 1
    # first pytest test status (verbose PASSED/FAILED or progress character); nothing before it reveals outcomes
    if m["kind"] == "test_run":
        q = PYFIRST_RE.search(plain)
        if q and not PYTEST_PROGRESS.search(plain[:q.start()]):
            ls = q.start()
            prefix = plain[:ls]
            tok = q.group(2) or q.group(4)
            opts = ["PASSED", "FAILED", "ERROR", "SKIPPED"] if q.group(2) else [".", "F", "E", "s"]
            lead = q.group(1) + " " if q.group(2) else q.group(3) + " "
            if tok in opts:
                foils = [o for o in opts if o != tok]
                out.append(dict(type="pytest_first", prefix=prefix, conts_text=[lead + tok] + [lead + f for f in foils],
                                true=tok, foils=foils, outcome_err=int(tok in ("FAILED", "ERROR", "F", "E")), n_cand=4))
    # printed numbers (execution kinds and search/listing output; up to 5 per observation, one per line)
    if m["kind"] in EXEC_KINDS or m["kind"] == "search":
        cls = char_classes(plain, ds == "tp")
        nn, lines_used = 0, set()
        for q in NUMTOK_RE.finditer(plain):
            if cls[q.start()] != C["number"]:
                continue
            num = q.group(0)
            ls = plain.rfind("\n", 0, q.start()) + 1
            if ls in lines_used:
                continue
            prefix = plain[:ls]; lead = plain[ls:q.start()]
            if num in act or in_text(num, prefix + lead, True):
                continue
            out.append(dict(type="number", prefix=prefix, lead=lead, true=num, outcome_err=int(bool(m["error"])), n_cand=4))
            lines_used.add(ls); nn += 1
            if nn == 5:
                break
    # boolean
    if m["kind"] == "python_exec":
        cls = char_classes(plain, ds == "tp")
        if True:
            for q in BOOL_RE.finditer(plain):
                ls = plain.rfind("\n", 0, q.start()) + 1
                prefix = plain[:ls]
                if cls[q.start()] in (C["err_line"],) or BOOL_RE.search(prefix + plain[ls:q.start()]) or q.group(1) in act:
                    break
                lp = plain[ls:q.start()]
                other = "False" if q.group(1) == "True" else "True"
                out.append(dict(type="bool", prefix=prefix, conts_text=[lp + q.group(1), lp + other], true=q.group(1),
                                foils=[other], outcome_err=int(q.group(1) == "False"), n_cand=2))
                break
    return out


STAT_DROP = collections.Counter()
exc_names_global, exc_w_global, num_pool_global = {}, {}, {}


def pools(ds, trajs):
    exc_pool = collections.Counter(); num_pool = collections.defaultdict(list)
    for tr in trajs:
        for m in tr["msgs"]:
            if m["role"] == "obs" and m.get("valid"):
                st = m["stripped"]
                for q in EXC_RE.finditer(ANSI_RE.sub("", st)):
                    if "." not in q.group(1):
                        exc_pool[q.group(1)] += 1
                if m["kind"] in EXEC_KINDS:
                    cls = char_classes(st, ds == "tp")
                    for q in NUMTOK_RE.finditer(st):
                        if cls[q.start()] == C["number"]:
                            num_pool[num_fmt(q.group(0))].append(q.group(0))
    names = sorted(k for k, v in exc_pool.items() if v >= 2)
    exc_names_global[ds] = names; exc_w_global[ds] = [exc_pool[k] for k in names]
    num_pool_global[ds] = num_pool


def traj_hashes(trajs):
    import hashlib
    out = {}
    for tr in trajs:
        render(tr)
        h = hashlib.sha1()
        for m in tr["msgs"]:
            h.update(np.array(m["ids"], np.int64).tobytes())
        out[tr["id"]] = h.hexdigest()[:16]
    return out


if __name__ == "__main__":
    if A.hash_only:
        res = {ds: traj_hashes(loader()) for ds, loader in [("tp", load_tp), ("swe", load_swe)] if ds in A.datasets.split(",")}
        json.dump(res, open(A.hash_only, "w"))
        print("hashes", {k: len(v) for k, v in res.items()})
        raise SystemExit
    for ds, loader in [("tp", load_tp), ("swe", load_swe)]:
        if ds not in A.datasets.split(","):
            continue
        trajs = loader()
        pools(ds, trajs)
        res = build(ds, trajs)
        print(ds, "drops", dict(STAT_DROP), flush=True)
        pickle.dump(res, open(os.path.join(A.out, f"{ds}.pkl"), "wb"), protocol=4)
        print("wrote", ds, flush=True)
