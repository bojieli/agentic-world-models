#!/usr/bin/env python3
"""Build SWE tool-output datasets in an AgenticPPL-like schema.

Outputs (in this directory):
  swe_smith.jsonl.gz              300 SWE-smith trajectories (Claude 3.7 Sonnet, SWE-agent tool format)
  swe_rebench.jsonl.gz            150 SWE-rebench leaderboard trajectories, python_spring2026 (tasks 2026-03..05),
                                  common scaffold swelike-py, 5 non-Qwen teachers   <- contamination-controlled set
  swe_rebench_openhands.jsonl.gz  150 SWE-rebench OpenHands trajectories, tasks created >= 2024-10-01
                                  (Qwen3-Coder-480B family generator; self-family bias)
  stats.json                      summary statistics

Record schema (per line):
  id, split, source, source_revision, source_ref, licence, task_id, repo, teacher, n_turns, resolved,
  messages: [{role, content, parts:[[type, turn, char_offset_in_content], ...]}]
      roles: user (task / tool results), assistant; tool results are role "user" with "tool_result": true
  text:  canonical rendering "<|user|>...<|assistant|>...<|user|>..." (role tags are not inside any span)
  spans: [[byte_start, byte_end, type, turn], ...] over UTF-8 text; type in task|thought|action|markup|observation
  observations: [{byte_start, byte_end, turn, tool, command, obs_kind, error, error_regex_raw, exit_code,
                  tests_pass, truncated, truncation_marker, n_bytes}]
"""
import ast, glob, gzip, hashlib, json, os, random, re, sys, collections
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SEED = 0

REV_SMITH = "08e109b4a59eaeebf80e4675cd125d42e7ac99a4"
REV_LB = "ed7fa382d5a6bbdd1524a0fde184f76fc88982e8"
REV_OH = "35455389ab51bf5e2306bfd436ef72d0f98bf882"
REV_RB_META = "89cdfbab4ab1bd8f5a658bb212d1b63624f4f881"

# ---------------------------------------------------------------- labelling rules
ERROR_RE = re.compile(
    r"Traceback \(most recent call last\)|\b[A-Z][A-Za-z]*Error\b|\berror\b|command not found|"
    r"No such file or directory|\bFAILED\b|\bfatal\b|Permission denied")
# tool-level errors (used for kinds whose content is file/code text, where ERROR_RE fires on source code)
TOOL_ERROR_RE = re.compile(
    r"No such file or directory|does not exist|command not found|Permission denied|"
    r"No replacement was performed|did not appear verbatim|introduced new syntax error|have NOT been applied|has NOT been applied|Invalid `?\w+`? parameter|"
    r"is not a valid|Unrecognized command|ERROR:|^Error:|^\s*error:", re.M)
# scaffold/dataset truncation markers only (generic phrases like "too long" hit linter output)
TRUNC_MARKERS = [
    "<response clipped>", "Observations should not exceeded", "Observation truncated",
    "<... tool result truncated ...>", "[Output truncated", "output truncated",
    "<NOTE>To save on context only part of this file has been shown",
]
# strong error evidence used for the `error` label (with exit code when the source records one)
STRONG_ERROR_RE = re.compile(
    r"Traceback \(most recent call last\)|command not found|No such file or directory|\bFAILED\b|"
    r"^fatal:|Permission denied|^\w*Error: |^E\s+\w+(?:Error|Exception)\b|^error(?:\[\w+\])?: |"
    r"SyntaxError|ModuleNotFoundError|ImportError", re.M)
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
PYTEST_SUMMARY_RE = re.compile(r"^=+ (.*?) in [\d.]+s(?: \([^)]*\))? =+\s*$", re.M)
PYTEST_SHORT_RE = re.compile(r"^(\d+ (?:passed|failed|error|errors)[^\n]*) in [\d.]+s\s*$", re.M)
UNITTEST_RAN_RE = re.compile(r"^Ran \d+ tests? in [\d.]+s\s*$", re.M)
EXIT_CODE_OH_RE = re.compile(r"\[The command completed with exit code (-?\d+)\.\]")
OH_FOOTER_RE = re.compile(r"\n*\[The command (?:completed with exit code -?\d+|timed out|has no new output)[^\]]*\][\s\S]*$")

SHELL_PREFIX = {"cd", "source", "export", "set", "timeout", "env", "sudo", "time", "nice"}
VIEW_PROGS = {"cat", "head", "tail", "nl", "less", "more", "bat", "awk", "view"}
SEARCH_PROGS = {"grep", "egrep", "rg", "ag", "ack", "find", "fd", "ls", "tree", "locate", "which", "git-grep"}


def first_programs(cmd):
    """Return list of program names of each pipeline/&&-segment (skipping cd/export prefixes)."""
    progs = []
    cmd = re.sub(r"<<\s*'?(\w+)'?.*?^\1$", "", cmd or "", flags=re.S | re.M)  # drop heredoc bodies
    cmd = re.sub(r"'[^']*'|\"(?:\\.|[^\"\\])*\"", "''", cmd)  # drop quoted strings
    for seg in re.split(r"&&|\|\||;|\n|\|", cmd):
        toks = seg.strip().split()
        while toks and (toks[0] in SHELL_PREFIX or re.match(r"^\w+=", toks[0])):
            # skip "cd dir" (consume argument) / "timeout 60" / VAR=1
            t0 = toks.pop(0)
            if t0 in ("cd", "source", "timeout") and toks:
                toks.pop(0)
        if toks:
            p = os.path.basename(toks[0])
            if p == "git" and len(toks) > 1:
                p = "git-" + toks[1]
            progs.append(p)
    return progs


def classify(tool, cmd, content):
    """obs_kind rules (first match wins). See README."""
    tool = (tool or "").lower()
    cmd = cmd or ""
    c = content or ""
    head = c[:400]
    # 1 tool_ack: bookkeeping tools whose result is a fixed acknowledgement
    if tool in ("think", "task_tracker", "finish", "submit") or "Your thought has been logged" in head:
        return "tool_ack"
    _p = first_programs(cmd)
    if _p and all(p in ("echo", "printf") for p in _p):  # agent echoing its own plan/notes
        return "tool_ack"
    # 2 edit_ack: file-mutating editor commands
    editor_cmd = None
    if tool in ("str_replace_editor", "edit", "str_replace_based_edit_tool", "file_editor"):
        m = re.match(r"\s*(\w+)", cmd)
        editor_cmd = m.group(1) if m else ""
        if editor_cmd in ("create", "str_replace", "insert", "undo_edit", "edit", "replace"):
            return "edit_ack"
    if tool in ("edit", "replace", "create", "insert", "append", "edit_terminal") or \
            any(p in ("edit", "replace", "create", "insert", "append") for p in _p):
        return "edit_ack"
    if re.search(r"has been edited|File created successfully|successfully (?:created|edited|replaced|inserted)|"
                 r"The file \S+ has been (?:edited|updated)|Text replaced|Edit applied|File updated\. Please review", head):
        return "edit_ack"
    # 3 file_view (directory listings via editor view -> search)
    if "Here's the files and directories up to" in head or "directories up to 2 levels" in head:
        return "search"
    if editor_cmd == "view" or tool in ("open", "goto", "scroll_down", "scroll_up") or \
            "Here's the result of running `cat -n`" in head or re.match(r"\[File: ", head):
        return "file_view"
    progs = [p for p in _p if p not in ("echo", "printf")]  # ignore leading/trailing note echoes
    low = cmd.lower()
    # 4 test_run
    if re.search(r"\bpytest\b|py\.test|-m unittest|\bunittest\b|\btox\b|\bnox\b|manage\.py test|"
                 r"\bmake (?:test|check)\b|runtests|\bcargo test\b|\bgo test\b|\bnpm (?:run )?test\b", low) or \
            "test session starts" in c or UNITTEST_RAN_RE.search(c):
        return "test_run"
    # 5 search
    if tool in ("search_file", "search_dir", "find_file") or (progs and progs[0] in SEARCH_PROGS) or \
            "git-grep" in progs:
        return "search"
    # 6 python_exec (any segment runs python: covers "cat > t.py <<EOF ... EOF; python t.py")
    if any(re.match(r"python[\d.]*$", p) for p in progs) or re.search(r"\bpython[\d.]*\s+(?:-c|\S+\.py|-\s*<<|<<)", cmd):
        return "python_exec"
    # file_view via shell (cat/head/sed -n/nl ... on files, not cat > file)
    if progs and (progs[0] in VIEW_PROGS or (progs[0] == "sed" and re.search(r"sed\s+-n", cmd))) and \
            not re.match(r"\s*(?:cd \S+\s*&&\s*)?cat\s*>", cmd):
        return "file_view"
    return "shell_other"


def tests_pass_from(content):
    c = ANSI_RE.sub("", content or "")
    ms = PYTEST_SUMMARY_RE.findall(c) or PYTEST_SHORT_RE.findall(c)
    if ms:
        s = ms[-1].lower()
        if re.search(r"\bfailed\b|\berrors?\b", s):
            return False
        if re.search(r"\bpassed\b", s):
            return True
        return None  # e.g. "no tests ran", "5 skipped"
    if UNITTEST_RAN_RE.search(c):
        tail = c[UNITTEST_RAN_RE.search(c).end():][:300]
        if re.search(r"^FAILED \(", tail, re.M):
            return False
        if re.search(r"^OK\b", tail, re.M):
            return True
    if re.search(r"^ERROR collecting|^E\s+\w+Error", c, re.M) and "test session starts" in c:
        return False
    return None


def label(tool, cmd, content, exit_code=None, status=None):
    content = content or ""
    kind = classify(tool, cmd, ANSI_RE.sub("", content))
    plain = ANSI_RE.sub("", content)
    raw = bool(ERROR_RE.search(plain))  # pilot-compatible regex family, fires on source code too
    if kind in ("file_view", "search", "edit_ack", "tool_ack"):
        err = bool(TOOL_ERROR_RE.search(plain))
    else:
        err = bool(STRONG_ERROR_RE.search(plain))
    if exit_code not in (None, 0) and not (kind == "search" and exit_code == 1):  # grep: 1 = no match
        err = True
    if status == "error" and not (kind == "search" and exit_code == 1):
        err = True
    tm = next((m for m in TRUNC_MARKERS if m in (content or "")), None)
    return dict(obs_kind=kind, error=err, error_regex_raw=raw, exit_code=exit_code,
                tests_pass=tests_pass_from(content) if kind == "test_run" else None,
                truncated=tm is not None, truncation_marker=tm)


# ---------------------------------------------------------------- rendering
class Renderer:
    def __init__(self):
        self.text = []
        self.nbytes = 0
        self.spans = []
        self.messages = []
        self.observations = []
        self.turn = -1

    def _emit(self, s, typ=None):
        b = len(s.encode("utf-8"))
        if typ is not None and b:
            self.spans.append([self.nbytes, self.nbytes + b, typ, self.turn])
        self.text.append(s)
        self.nbytes += b
        return b

    def start(self, role, tool_result=False):
        self._emit("<|user|>" if role == "user" else "<|assistant|>")
        self.messages.append(dict(role=role, content="", parts=[], **({"tool_result": True} if tool_result else {})))

    def add(self, s, typ):
        m = self.messages[-1]
        if s:
            m["parts"].append([typ, self.turn, len(m["content"])])
            m["content"] += s
        return self._emit(s, typ)

    def task(self, s):
        self.start("user")
        self.add(s, "task")

    def assistant(self, thought, calls):
        self.turn += 1
        self.start("assistant")
        if thought:
            self.add(thought, "thought")
        for name, args in calls:
            self.add(("\n" if self.messages[-1]["content"] else "") + '<tool_call>\n{"name": ' + json.dumps(name) + ', "arguments": ', "markup")
            self.add(json.dumps(args, ensure_ascii=False) if not isinstance(args, str) else args, "action")
            self.add("}\n</tool_call>", "markup")

    def observation(self, content, prefix="", meta=None, suffix=""):
        self.start("user", tool_result=True)
        if prefix:
            self.add(prefix, "markup")
        b0 = self.nbytes
        if content:
            self.add(content, "observation")
        o = dict(byte_start=b0, byte_end=self.nbytes, turn=self.turn, n_bytes=self.nbytes - b0)
        if suffix:
            self.add(suffix, "markup")
        o.update(meta or {})
        self.observations.append(o)

    def record(self, **kw):
        text = "".join(self.text)
        assert len(text.encode("utf-8")) == self.nbytes
        r = dict(kw)
        r.update(n_turns=self.turn + 1, messages=self.messages, text=text, spans=self.spans,
                 observations=self.observations)
        r["id"] = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        return r


def norm(s):
    return (s or "").replace("\r\n", "\n")


def cmd_string(name, args):
    """Human-readable command used for classification."""
    if isinstance(args, dict):
        if "command" in args and isinstance(args["command"], str):
            c = args["command"]
            if name in ("str_replace_editor", "file_editor", "str_replace_based_edit_tool"):
                return c + " " + str(args.get("path", ""))
            return c
        return " ".join(str(v) for v in args.values())
    return str(args or "")


def parse_args(a):
    if isinstance(a, dict):
        return a
    if not isinstance(a, str):
        return a
    for f in (json.loads, ast.literal_eval):
        try:
            return f(a)
        except Exception:
            pass
    return a


def content_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "".join(x.get("text", "") if isinstance(x, dict) else str(x) for x in c)
    return "" if c is None else str(c)


# ---------------------------------------------------------------- SWE-smith
def build_smith(n=300):
    df = pd.read_parquet(os.path.join(RAW, "tool-00000.parquet"))
    df = df[df.model.str.contains("claude-3-7")].copy()
    df["repo"] = df.instance_id.str.split(".").str[0]
    df = df[df.resolved].drop_duplicates("instance_id")
    rng = random.Random(SEED)
    by_repo = collections.defaultdict(list)
    for i, r in df.sample(frac=1, random_state=SEED).iterrows():
        by_repo[r.repo].append(r)
    repos = sorted(by_repo)
    rng.shuffle(repos)
    picked = []
    while len(picked) < n and any(by_repo.values()):
        for rp in repos:
            if by_repo[rp] and len(picked) < n:
                picked.append(by_repo[rp].pop())
    out = []
    for r in picked:
        msgs = json.loads(r.messages)
        R = Renderer()
        sys_txt = next((content_text(m["content"]) for m in msgs if m["role"] == "system"), "")
        user_txt = next((content_text(m["content"]) for m in msgs if m["role"] == "user"), "")
        R.task(norm(sys_txt + "\n\n" + user_txt))
        callmap = {}
        for m in msgs:
            if m["role"] == "assistant":
                tcs = m.get("tool_calls") or []
                if isinstance(tcs, str):
                    tcs = parse_args(tcs)
                calls = []
                for tc in tcs:
                    name = tc["function"]["name"]
                    args = parse_args(tc["function"]["arguments"])
                    calls.append((name, args))
                    callmap[tc.get("id")] = (name, cmd_string(name, args))
                R.assistant(norm(m.get("thought") or content_text(m.get("content"))), calls)
            elif m["role"] == "tool":
                ids = m.get("tool_call_ids") or []
                if isinstance(ids, str):
                    ids = parse_args(ids)
                name, cmd = callmap.get(ids[0] if ids else None, ("", ""))
                c = norm(content_text(m["content"]))
                prefix = ""
                if c.startswith("OBSERVATION:\n"):
                    prefix, c = "OBSERVATION:\n", c[len("OBSERVATION:\n"):]
                meta = dict(tool=name, command=cmd[:500])
                meta.update(label(name, cmd, c))
                R.observation(c, prefix, meta)
        out.append(R.record(split="swe_smith", source="SWE-bench/SWE-smith-trajectories", source_revision=REV_SMITH,
                            source_ref=f"tool/{r.traj_id}", licence="MIT", task_id=r.instance_id, repo=r.repo,
                            teacher=r.model, resolved=bool(r.resolved)))
    return out


# ---------------------------------------------------------------- SWE-rebench leaderboard (2026 tasks)
LB_TEACHERS = ["claude-opus-4.6", "gpt-5.4", "gemini-3.1-pro-preview", "glm-5.1", "deepseek-v4-pro"]


def build_lb(per_teacher=30):
    cols = ["trajectory_id", "instance_id", "repo", "task_month", "canonical_model", "model", "scaffold", "run_index",
            "resolved", "exit_status"]
    parts = []
    for f in sorted(glob.glob(os.path.join(RAW, "lb", "*.parquet"))):
        d = pd.read_parquet(f, columns=cols + ["trajectory"])
        d["traj_bytes"] = d.trajectory.str.len()
        parts.append(d.drop(columns=["trajectory"]))
    meta = pd.concat(parts)
    meta = meta[(meta.scaffold == "swelike-py") & meta.canonical_model.isin(LB_TEACHERS) & (meta.resolved == 1)]
    # shortest resolved run per (teacher, task): keeps more trajectories under the scorer's 32k-token window
    meta = meta.sort_values(["canonical_model", "instance_id", "traj_bytes"]).drop_duplicates(["canonical_model", "instance_id"])
    rng = random.Random(SEED)
    use = collections.Counter()
    chosen = []
    for t in LB_TEACHERS:
        sub = meta[meta.canonical_model == t]
        ids = list(sub.instance_id)
        rng.shuffle(ids)
        ids.sort(key=lambda i: use[i])  # stable: least-used tasks first
        for i in ids[:per_teacher]:
            use[i] += 1
            chosen.append(sub[sub.instance_id == i].iloc[0].trajectory_id)
    chosen = set(chosen)
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, "lb", "*.parquet"))):
        d = pd.read_parquet(f)
        rows.append(d[d.trajectory_id.isin(chosen)])
    df = pd.concat(rows)
    out = []
    for _, r in df.iterrows():
        t = json.loads(r.trajectory)
        R = Renderer()
        R.task(norm("\n\n".join(p["content"] for p in t["prompts"])))
        callmap = {}
        pending_thought, pending_calls = [], []

        def flush():
            if pending_thought or pending_calls:
                R.assistant("\n\n".join(x for x in pending_thought if x), list(pending_calls))
                pending_thought.clear(); pending_calls.clear()

        for e in t["events"]:
            ty = e["type"]
            if ty in ("assistant_message", "assistant_analysis"):
                if pending_calls:
                    flush()
                pending_thought.append(norm(e.get("content")).strip())
            elif ty == "tool_call":
                name = e.get("tool") or ""
                args = parse_args(e.get("input"))
                pending_calls.append((name, args))
                callmap[e.get("tool_call_id")] = (name, cmd_string(name, args))
            elif ty == "tool_result":
                flush()
                name, cmd = callmap.get(e.get("tool_call_id"), ("", ""))
                c = e.get("content")
                if c is None:
                    er = parse_args(e.get("error"))
                    if isinstance(er, dict) and "output" in er:
                        c = er.get("output") or ""
                    else:
                        # scaffold-side failure (unparseable tool call, timeout...): the text the agent saw
                        # is not released, so keep a markup stub and no observation
                        et = er.get("type") if isinstance(er, dict) else str(er)[:80]
                        R.start("user", tool_result=True)
                        R.add(f"[scaffold error: {et}]", "markup")
                        continue
                c = norm(content_text(c))
                ec = e.get("exit_code")
                try:
                    ec = int(ec) if ec is not None else (0 if e.get("status") == "success" else None)
                except Exception:
                    ec = None
                meta = dict(tool=name, command=cmd[:500], status=e.get("status"))
                meta.update(label(name, cmd, c, ec, e.get("status")))
                if e.get("truncated"):
                    meta["truncated"] = True
                    meta["truncation_marker"] = meta["truncation_marker"] or "status:truncated"
                R.observation(c, "", meta)
            elif ty == "final_message":
                if pending_calls:
                    flush()
                pending_thought.append(norm(content_text(e.get("content"))).strip())
        flush()
        out.append(R.record(split="swe_rebench_lb2026", source="nebius/SWE-rebench-leaderboard-trajectories",
                            source_revision=REV_LB, source_ref=f"python_spring2026/{r.trajectory_id}",
                            licence="CC-BY-4.0", task_id=r.instance_id, repo=r.repo, task_month=r.task_month,
                            teacher=r.canonical_model, resolved=bool(r.resolved),
                            normalization=t.get("normalization")))
    return out


# ---------------------------------------------------------------- SWE-rebench OpenHands (old tasks; self-family generator)
def build_oh(n=150, since="2024-10-01"):
    meta = pd.concat([pq.read_table(os.path.join(RAW, f"rebench-meta-{f}.parquet"), columns=["instance_id", "created_at"]).to_pandas()
                      for f in ["test-00000-of-00002", "test-00001-of-00002", "filtered-00000-of-00001"]]).drop_duplicates("instance_id")
    pf = pq.ParquetFile(os.path.join(RAW, "rebench-traj.parquet"))
    idx = pf.read(columns=["trajectory_id", "instance_id", "repo", "resolved", "exit_status"]).to_pandas().merge(meta, on="instance_id")
    idx["created_at"] = pd.to_datetime(idx.created_at)
    idx = idx[(idx.created_at >= since) & (idx.resolved == 1) & (idx.exit_status == "submit")]
    idx = idx.sample(frac=1, random_state=SEED).drop_duplicates("instance_id")
    by_repo = collections.defaultdict(list)
    for _, r in idx.iterrows():
        by_repo[r.repo].append(r)
    repos = sorted(by_repo, key=lambda k: max(x.created_at for x in by_repo[k]), reverse=True)
    picked = []
    while len(picked) < n and any(by_repo.values()):
        for rp in repos:
            if by_repo[rp] and len(picked) < n:
                picked.append(by_repo[rp].pop())
    want = {r.trajectory_id: r for r in picked}
    out = []
    for g in range(pf.metadata.num_row_groups):
        tb = pf.read_row_group(g, columns=["trajectory_id", "trajectory"]).to_pandas()
        tb = tb[tb.trajectory_id.isin(want)]
        for _, row in tb.iterrows():
            r = want[row.trajectory_id]
            msgs = [dict(x) for x in row.trajectory]
            R = Renderer()
            sys_txt = next((m["content"] for m in msgs if m["role"] == "system"), "")
            user_i = next(i for i, m in enumerate(msgs) if m["role"] == "user")
            R.task(norm(sys_txt + "\n\n" + msgs[user_i]["content"]))
            callmap = {}
            for m in msgs[user_i + 1:]:
                if m["role"] == "assistant":
                    tcs = m.get("tool_calls")
                    if isinstance(tcs, str):
                        tcs = parse_args(tcs) if tcs != "None" else []
                    tcs = [dict(t) for t in tcs] if tcs is not None and not isinstance(tcs, str) else []
                    for t in tcs:
                        t["function"] = dict(t["function"])
                    calls = []
                    for tc in tcs or []:
                        name = tc["function"]["name"]
                        args = parse_args(tc["function"]["arguments"])
                        calls.append((name, args))
                        callmap[tc.get("id")] = (name, cmd_string(name, args))
                    c = m.get("content")
                    R.assistant(norm(c if isinstance(c, str) and c != "None" else ""), calls)
                elif m["role"] == "tool":
                    name, cmd = callmap.get(m.get("tool_call_id"), (m.get("name") or "", ""))
                    c = norm(m.get("content") or "")
                    ecm = EXIT_CODE_OH_RE.search(c)
                    meta = dict(tool=name, command=cmd[:500])
                    meta.update(label(name, cmd, c, int(ecm.group(1)) if ecm else None))
                    fm = OH_FOOTER_RE.search(c)  # scaffold status footer -> markup, not observation
                    suffix = ""
                    if fm:
                        c, suffix = c[:fm.start()], c[fm.start():]
                    R.observation(c, "", meta, suffix)
                elif m["role"] == "user":  # rare mid-trajectory user messages -> treat as task text
                    R.start("user")
                    R.add(norm(m.get("content") or ""), "task")
            out.append(R.record(split="swe_rebench_openhands", source="nebius/SWE-rebench-openhands-trajectories",
                                source_revision=REV_OH, source_ref=r.trajectory_id, licence="CC-BY-4.0",
                                task_id=r.instance_id, repo=r.repo, task_created_at=str(r.created_at.date()),
                                teacher="Qwen3-Coder-480B-A35B-Instruct or nebius fine-tune (per-row model not released)",
                                resolved=True))
    return out


# ---------------------------------------------------------------- stats
def stats(recs, tok):
    s = dict(n=len(recs), teachers=dict(collections.Counter(r["teacher"] for r in recs)),
             repos=len({r["repo"] for r in recs}), tasks=len({r["task_id"] for r in recs}))
    lens = sorted(len(tok.encode(r["text"]).ids) for r in recs)
    q = lambda p: lens[min(len(lens) - 1, int(p * len(lens)))]
    s["tokens"] = dict(p10=q(.1), p50=q(.5), p90=q(.9), max=lens[-1], frac_gt_32k=round(sum(l > 32768 for l in lens) / len(lens), 3))
    tb = collections.Counter()
    for r in recs:
        for a, b, t, _ in r["spans"]:
            tb[t] += b - a
    tot = sum(r["spans"][-1][1] if r["spans"] else 0 for r in recs)
    s["span_byte_share"] = {k: round(v / sum(tb.values()), 3) for k, v in tb.most_common()}
    obs = [o for r in recs for o in r["observations"]]
    kb, kn = collections.Counter(), collections.Counter()
    for o in obs:
        kb[o["obs_kind"]] += o["n_bytes"]; kn[o["obs_kind"]] += 1
    s["n_observations"] = len(obs)
    s["obs_kind"] = {k: dict(n=kn[k], byte_share=round(kb[k] / max(1, sum(kb.values())), 3),
                             error_rate=round(sum(o["error"] for o in obs if o["obs_kind"] == k) / kn[k], 3))
                     for k in sorted(kn, key=lambda k: -kb[k])}
    s["error_rate"] = round(sum(o["error"] for o in obs) / len(obs), 3)
    s["error_regex_raw_rate"] = round(sum(o["error_regex_raw"] for o in obs) / len(obs), 3)
    tr = [o for o in obs if o["obs_kind"] == "test_run"]
    s["test_runs"] = dict(n=len(tr), tests_pass_true=sum(o["tests_pass"] is True for o in tr),
                          tests_pass_false=sum(o["tests_pass"] is False for o in tr),
                          tests_pass_null=sum(o["tests_pass"] is None for o in tr))
    s["truncated_obs"] = dict(n=sum(o["truncated"] for o in obs), rate=round(sum(o["truncated"] for o in obs) / len(obs), 4),
                              markers=dict(collections.Counter(o["truncation_marker"] for o in obs if o["truncated"])))
    s["empty_obs"] = sum(o["n_bytes"] == 0 for o in obs)
    return s


def main():
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(os.path.join(RAW, "qwen3_tokenizer.json"))
    which = sys.argv[1:] or ["smith", "lb", "oh"]
    allstats = {}
    if os.path.exists(os.path.join(HERE, "stats.json")):
        allstats = json.load(open(os.path.join(HERE, "stats.json")))
    for name, fn, fname in [("smith", build_smith, "swe_smith.jsonl.gz"), ("lb", build_lb, "swe_rebench.jsonl.gz"),
                            ("oh", build_oh, "swe_rebench_openhands.jsonl.gz")]:
        if name not in which:
            continue
        recs = fn()
        with gzip.open(os.path.join(HERE, fname), "wt") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        allstats[fname] = stats(recs, tok)
        print(fname, json.dumps(allstats[fname], indent=1))
        json.dump(allstats, open(os.path.join(HERE, "stats.json"), "w"), indent=1)
    json.dump(allstats, open(os.path.join(HERE, "stats.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
