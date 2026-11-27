"""Synthetic random-string copy test.

Contexts: (i) bare  S\\n<filler>\\nS ; (ii) terminal-like  root@S:/app# ls\\nfile.txt\\nroot@S:/app#  (neutral+native);
(iii) real AgenticPPL prefix (task, first assistant turn, first observation) with the container hostname replaced by S
everywhere (neutral+native). Score = bits on tokens overlapping each repeated occurrence of S (all occurrences after the
first), per character; plus first-token vs later-token split.

usage: copytest.py MODEL_PATH NAME
"""
import gzip, json, math, os, random, re, sys, time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import headers  # same wrappers as the main pipeline

LN2 = math.log(2)
LENGTHS = [8, 16, 32, 64]
ALPHA = ["hex", "base64", "words", "digits"]
N_STR = 200
N_TRAJ = 50
MAXTOK_III = 3072
BUDGET = 24576  # tokens per batch
FILLER = ("The weather in the valley had been mild for most of the season, and the farmers were cautiously optimistic "
          "about the harvest. Along the river, the willows leaned over the water while children skipped stones from "
          "the gravel bank. In the village square, a small market opened every Saturday morning, selling bread, cheese, "
          "honey, and vegetables grown in nearby gardens. The old clock tower, repaired twice in the last century, still "
          "struck the hours a few minutes late, which nobody seemed to mind. Visitors often remarked on the quiet pace of "
          "life, the narrow stone streets, and the smell of wood smoke in the evenings. A local historian had written a "
          "short book about the bridge, the mill, and the families who had lived there for generations, and copies were "
          "sold at the bakery next to the post office. When autumn arrived, the hills turned gold and red, and walkers "
          "came from the city to follow the long trail that winds past the lake and over the ridge.")


def wordlist(tok):
    out = []
    for i in range(len(tok)):
        s = tok.convert_ids_to_tokens(i)
        if s and s.startswith("Ġ") and re.fullmatch(r"[a-z]{3,8}", s[1:]):
            out.append(s[1:])
        if len(out) == 2000:
            break
    return out


def make_strings(words):
    rng = random.Random(0)
    al = {"hex": "0123456789abcdef", "digits": "0123456789",
          "base64": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"}
    S = {}
    for a in ALPHA:
        for L in LENGTHS:
            lst = []
            for _ in range(N_STR):
                if a == "words":
                    s = ""
                    while len(s) < L:
                        s += rng.choice(words)
                    lst.append(s[:L])
                else:
                    lst.append("".join(rng.choice(al[a]) for _ in range(L)))
            S[f"{a}/{L}"] = lst
    return S


def tokenize_pieces(tok, pieces):
    """pieces: list of (text, is_wrapper). returns ids, char offsets (global, None for wrappers), full text."""
    ids, offs, text = [], [], ""
    for t, wrap in pieces:
        if wrap:
            x = tok(t, add_special_tokens=False)["input_ids"]
            ids += x; offs += [None] * len(x)
        else:
            e = tok(t, add_special_tokens=False, return_offsets_mapping=True, split_special_tokens=True)
            ids += e["input_ids"]; offs += [(len(text) + a, len(text) + b) for a, b in e["offset_mapping"]]
        text += t
    return ids, offs, text


def spans_tokens(offs, spans):
    """for each char span, list of token indices overlapping it."""
    res = []
    for s, e in spans:
        res.append([i for i, o in enumerate(offs) if o is not None and o[0] < e and o[1] > s])
    return res


class M:
    def __init__(self, path):
        self.tok = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, attn_implementation="sdpa",
                                                          device_map="cuda").eval()
        self.W = self.model.lm_head.weight

    @torch.inference_mode()
    def score(self, seqs):
        """seqs: list of (ids, positions). returns list of np arrays of bits at positions (target ids[p], predicted from p-1)."""
        order = sorted(range(len(seqs)), key=lambda i: len(seqs[i][0]))
        out = [None] * len(seqs)
        batches, cur = [], []
        for i in order:
            if cur and (len(cur) + 1) * len(seqs[i][0]) > BUDGET:
                batches.append(cur); cur = []
            cur.append(i)
        batches.append(cur)
        for batch in batches:
            L = max(len(seqs[i][0]) for i in batch)
            x = torch.full((len(batch), L), 0, dtype=torch.long)
            am = torch.zeros((len(batch), L), dtype=torch.long)
            for r, i in enumerate(batch):
                n = len(seqs[i][0]); x[r, :n] = torch.tensor(seqs[i][0]); am[r, :n] = 1
            h = self.model.model(input_ids=x.cuda(), attention_mask=am.cuda()).last_hidden_state
            for r, i in enumerate(batch):
                ids, pos = seqs[i]
                pos_t = torch.tensor(pos, device="cuda")
                z = (h[r, pos_t - 1] @ self.W.T).float()
                tg = torch.tensor([ids[p] for p in pos], device="cuda")
                b = (torch.logsumexp(z, -1) - z.gather(1, tg[:, None])[:, 0]) / LN2
                out[i] = b.cpu().numpy()
        return out


def rec(bits, groups, nchar):
    """groups: list of token-index lists (one per scored occurrence), positions aligned with bits order."""
    tot = float(bits.sum())
    first = [float(bits[g[0]]) for g in groups if g]
    later = [float(x) for g in groups for x in bits[g[1:]]]
    return dict(bpc=tot / nchar, first=float(np.mean(first)) if first else float("nan"),
                later=float(np.mean(later)) if later else float("nan"), ntok=int(len(bits)))


def build_seq(tok, pieces, S, skip_first=1):
    ids, offs, text = tokenize_pieces(tok, pieces)
    occ = [(m.start(), m.end()) for m in re.finditer(re.escape(S), text)]
    occ = occ[skip_first:]
    groups = spans_tokens(offs, occ)
    pos, gidx = [], []
    for g in groups:
        gi = []
        for t in g:
            if t > 0:
                gi.append(len(pos)); pos.append(t)
        gidx.append(gi)
    return ids, pos, gidx, len(occ) * len(S)


def hostname_trajs(prep_eval, rows):
    out = []
    for tid in prep_eval:
        msgs = rows[tid]["messages"]
        if len(msgs) < 3:
            continue
        m = re.search(r"root@([0-9a-f]{12}):", msgs[0]["content"]) or re.search(r"root@([0-9a-f]{12}):", msgs[2]["content"])
        if not m:
            continue
        host = m.group(1)
        cnt = sum(x["content"].count(host) for x in msgs[:3])
        if cnt >= 2:
            out.append((tid, host))
        if len(out) == N_TRAJ:
            break
    return out


def traj_pieces(msgs, host, S, fmt, maxchars=9000):
    pieces = []
    for i, m in enumerate(msgs[:3]):
        h, f = headers(fmt, m["role"], i)
        c = m["content"].replace(host, S)
        if i == 2:
            c = c[:maxchars]
        pieces += [(h, True), (c, False), (f, True)]
    return pieces


def main():
    path, name = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else "results"
    t0 = time.time()
    mm = M(path); tok = mm.tok
    S = make_strings(wordlist(tok))
    prep = json.load(open("prep.json"))
    rows = {r["id"]: r for r in map(json.loads, gzip.open("data/trajectories.jsonl.gz", "rt"))}
    trajs = hostname_trajs(prep["eval"], rows)
    res = dict(name=name, model=path, n_traj_iii=len(trajs), cells={})
    jobs = []  # (key, cell, idx, ids, pos, gidx, nchar)
    for cell, lst in S.items():
        for k, s in enumerate(lst):
            # (i) bare
            ids, pos, g, nc = build_seq(tok, [(f"{s}\n{FILLER}\n{s}", False)], s)
            jobs.append(("bare", cell, k, ids, pos, g, nc))
            # (ii) terminal-like
            term = f"New Terminal Output:\n\nroot@{s}:/app# ls\nfile.txt\nroot@{s}:/app# "
            for fmt in ["neutral", "native"]:
                h, _ = headers(fmt, "user", 1)
                ids, pos, g, nc = build_seq(tok, [(h, True), (term, False)], s)
                jobs.append((f"term/{fmt}", cell, k, ids, pos, g, nc))
        # (iii) real prefix: one string per trajectory per cell
        for k, (tid, host) in enumerate(trajs):
            s = lst[k]
            for fmt in ["neutral", "native"]:
                ids, pos, g, nc = build_seq(tok, traj_pieces(rows[tid]["messages"], host, s, fmt), s)
                if len(ids) > MAXTOK_III:
                    ids = ids[:MAXTOK_III]
                    keep = [p < MAXTOK_III for p in pos]
                    # drop occurrences crossing the cut entirely
                    newg, newpos, nocc = [], [], 0
                    for gi in g:
                        if gi and all(keep[x] for x in gi):
                            newg.append(list(range(len(newpos), len(newpos) + len(gi)))); newpos += [pos[x] for x in gi]; nocc += 1
                    pos, g, nc = newpos, newg, nocc * len(s)
                if nc > 0:
                    jobs.append((f"traj/{fmt}", cell, k, ids, pos, g, nc))
    print(f"{name}: {len(jobs)} sequences, {sum(len(j[3]) for j in jobs)} tokens, {len(trajs)} trajs", flush=True)
    bits = mm.score([(j[3], j[4]) for j in jobs])
    for j, b in zip(jobs, bits):
        key, cell, k, ids, pos, g, nc = j
        d = res["cells"].setdefault(key, {}).setdefault(cell, {"idx": [], "bpc": [], "first": [], "later": [], "ntok": []})
        r = rec(b, g, nc)
        d["idx"].append(k)
        for f in ["bpc", "first", "later", "ntok"]:
            d[f].append(r[f])
    res["timing"] = dict(total_s=time.time() - t0, max_mem_gb=torch.cuda.max_memory_allocated() / 1e9)
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(f"{out}/copytest_{name}.json", "w"))
    print("done", res["timing"], flush=True)


if __name__ == "__main__":
    main()
