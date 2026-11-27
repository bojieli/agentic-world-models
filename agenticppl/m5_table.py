"""M5 tables: AgenticPPL (3 pick sets) per model with doc-bootstrap CIs, plain mean bits on the picks, sharpness at
command positions, published agentic scores, paired contrasts, and cross-model correlations. -> results/m5_tables.md"""
import json, os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "m5")
ROLE = {"Qwen3-8B-Base": "base", "Qwen3-8B": "instruct", "Light-IF-8B": "non-agentic SFT+RL", "Klear-Reasoner-8B-SFT": "non-agentic distill SFT (from Base)",
        "Nemotron-Terminal-8B": "agentic SFT", "tmax-sft-8b": "agentic SFT", "tmax-8b": "agentic RL (on tmax-sft)", "WebWorld-8B": "world model (web)",
        "Qwen3-14B-Base": "base", "Qwen3-14B": "instruct", "Light-IF-14B": "non-agentic SFT+RL", "Nemotron-Terminal-14B": "agentic SFT",
        "CodeScout-14B": "agentic RL", "Qwen3-32B": "instruct", "Nemotron-Terminal-32B": "agentic SFT", "OpenThinkerAgent-32B": "agentic SFT"}
PUB = {"Qwen3-8B": "TB2.0 2.47 (NT paper); TB-Lite 7.3 / TB2.1 1.1 (Tmax paper)", "Nemotron-Terminal-8B": "TB2.0 13.0",
       "tmax-sft-8b": "TB-Lite 11.5 / TB2.1 6.0", "tmax-8b": "TB-Lite 17.7 / TB2.1 5.2", "Qwen3-14B": "TB2.0 4.04",
       "Nemotron-Terminal-14B": "TB2.0 20.2", "CodeScout-14B": "SWE-V file-loc F1 68.6 (no TB)", "Qwen3-32B": "TB2.0 3.37",
       "Nemotron-Terminal-32B": "TB2.0 27.4", "OpenThinkerAgent-32B": "TB2.0 26.2"}
SETS = ["obsgain-easy", "obsgain-nothought", "obsgain-taskgain"]
ORDER = ["Qwen3-0.6B-Base", "Qwen3-0.6B", "Qwen3-1.7B-Base", "Qwen3-1.7B", "Qwen3-4B-Base", "Qwen3-4B",
         "Qwen3-8B-Base", "Qwen3-8B", "Light-IF-8B", "Klear-Reasoner-8B-SFT", "Nemotron-Terminal-8B", "tmax-sft-8b", "tmax-8b", "WebWorld-8B",
         "Qwen3-14B-Base", "Qwen3-14B", "Light-IF-14B", "Nemotron-Terminal-14B", "CodeScout-14B",
         "Qwen3-32B", "Nemotron-Terminal-32B", "OpenThinkerAgent-32B"]


def load():
    R = {}
    for p in glob.glob(os.path.join(D, "*.json")):
        r = json.load(open(p)); R[r["name"]] = r
    return R


def ranges(name, s):
    z = np.load(os.path.join(D, f"{name}_tok.npz"))
    if f"{s}__doc" not in z.files:
        return None
    return {k: z[f"{s}__{k}"] for k in ["doc", "capped", "prob", "raw", "nrow"]}


def val(pr, s):
    return -pr["capped"] if s == "obsgain-easy" else pr["prob"]


def paired(a, b, s, B=2000, seed=0):
    """paired doc bootstrap of value(a) - value(b) (same docs, same ranges)."""
    A, Bq = ranges(a, s), ranges(b, s)
    if A is None or Bq is None:
        return None
    va, vb = val(A, s), val(Bq, s)
    # ranges kept can differ only if renderings fail; align on (doc, order) when identical lengths
    if len(va) != len(vb) or not np.array_equal(A["doc"], Bq["doc"]):
        return None
    docs = np.unique(A["doc"]); idx = np.searchsorted(docs, A["doc"])
    sa, sb, n = np.bincount(idx, va), np.bincount(idx, vb), np.bincount(idx)
    r = np.random.default_rng(seed); out = []
    for _ in range(B):
        w = np.bincount(r.integers(0, len(docs), len(docs)), minlength=len(docs))
        out.append((w @ sa - w @ sb) / (w @ n))
    return float(va.mean() - vb.mean()), [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def spearman(x, y):
    from scipy.stats import spearmanr
    return float(spearmanr(x, y).correlation)


def main():
    R = load()
    names = [n for n in ORDER if n in R] + sorted(n for n in R if n not in ORDER)
    L = ["| model | role | AgenticPPL obsgain-easy (capped_bits) | obsgain-nothought (prob_mean) | obsgain-taskgain (prob_mean) | plain mean bits/range (easy picks, uncapped) | bits/token on easy picks | entropy / loss−entropy on easy picks | entropy / loss−entropy at all command tokens | plain PPL (bits/byte) | published agentic score |",
         "|" + "---|" * 11]
    for n in names:
        r = R[n]; p = r["picks"]
        c = lambda s: f"{p[s]['agenticppl']:.4f} [{p[s]['ci'][0]:.4f},{p[s]['ci'][1]:.4f}]"
        e = p["obsgain-easy"]; a = r["action_tokens"]
        L.append(f"| {n} | {ROLE.get(n, '')} | {c('obsgain-easy')} | {c('obsgain-nothought')} | {c('obsgain-taskgain')} | "
                 f"{e['mean_range_bits_uncapped']:.3f} [{e['mean_range_bits_uncapped_ci'][0]:.3f},{e['mean_range_bits_uncapped_ci'][1]:.3f}] | {e['bits_per_row']:.3f} | "
                 f"{e['ent_per_row']:.3f} / {e['gap_per_row']:+.3f} | {a['ent']:.3f} / {a['gap']:+.3f} | {r['plain_ppl']:.4f} | {PUB.get(n, '–')} |")
    L.append("\nunmatched renderings / docs with special tokens in content: " +
             ", ".join(f"{n}: {R[n]['docs_unmatched']}/{R[n]['docs_with_special_tokens_in_content']}" for n in names))
    # paired contrasts
    C = [("Qwen3-8B", "Qwen3-8B-Base"), ("Light-IF-8B", "Qwen3-8B"), ("Nemotron-Terminal-8B", "Qwen3-8B"), ("tmax-sft-8b", "Qwen3-8B"),
         ("tmax-8b", "tmax-sft-8b"), ("tmax-8b", "Qwen3-8B"), ("Klear-Reasoner-8B-SFT", "Qwen3-8B-Base"), ("WebWorld-8B", "Qwen3-8B"),
         ("Nemotron-Terminal-8B", "Light-IF-8B"), ("tmax-sft-8b", "Light-IF-8B"),
         ("Qwen3-14B", "Qwen3-14B-Base"), ("Nemotron-Terminal-14B", "Qwen3-14B"), ("CodeScout-14B", "Qwen3-14B"), ("Light-IF-14B", "Qwen3-14B"),
         ("Nemotron-Terminal-14B", "Light-IF-14B"), ("CodeScout-14B", "Light-IF-14B"), ("Nemotron-Terminal-32B", "Qwen3-32B"), ("OpenThinkerAgent-32B", "Qwen3-32B")]
    L += ["\n**Paired differences (A − B; higher AgenticPPL = predicted more agentic), 95% paired doc bootstrap**\n",
          "| A | B | Δ obsgain-easy | Δ obsgain-nothought | Δ obsgain-taskgain |", "|---|---|---|---|---|"]
    for a, b in C:
        if a in R and b in R:
            cells = []
            for s in SETS:
                d = paired(a, b, s)
                cells.append("–" if d is None else f"{d[0]:+.4f} [{d[1][0]:+.4f},{d[1][1]:+.4f}]")
            L.append(f"| {a} | {b} | " + " | ".join(cells) + " |")
    # correlations across models
    if len(names) >= 4:
        x = {s: [R[n]["picks"][s]["agenticppl"] for n in names] for s in SETS}
        feats = {"entropy at command tokens": [R[n]["action_tokens"]["ent"] for n in names],
                 "loss−entropy at command tokens": [R[n]["action_tokens"]["gap"] for n in names],
                 "entropy on easy picks": [R[n]["picks"]["obsgain-easy"]["ent_per_row"] for n in names],
                 "loss−entropy on easy picks": [R[n]["picks"]["obsgain-easy"]["gap_per_row"] for n in names],
                 "−plain PPL": [-R[n]["plain_ppl"] for n in names]}
        L += [f"\n**Spearman rho across the {len(names)} models scored** (sign: positive = higher AgenticPPL goes with higher feature)\n",
              "| feature | " + " | ".join(SETS) + " |", "|---|---|---|---|"]
        for k, v in feats.items():
            L.append(f"| {k} | " + " | ".join(f"{spearman(x[s], v):+.2f}" for s in SETS) + " |")
        # within-size: subtract each size group's mean (removes the scale trend)
        import re as _re
        size = [(_re.search(r"(0\.6|1\.7|4|8|14|32)[Bb]", n) or [None, "?"])[1] for n in names]
        def demean(v):
            v = np.array(v, float); out = v.copy()
            for sz in set(size):
                m = np.array([s_ == sz for s_ in size]); out[m] = v[m] - v[m].mean()
            return out
        L += [f"\n**Within-size Pearson r (size-group means removed; {len(names)} models)**\n",
              "| feature | " + " | ".join(SETS) + " |", "|---|---|---|---|"]
        for k, v in feats.items():
            L.append(f"| {k} | " + " | ".join(f"{np.corrcoef(demean(x[s]), demean(v))[0, 1]:+.2f}" for s in SETS) + " |")
        # scale trend: instruct - base per size
        L += ["\n**Scale trend (easy): base, instruct, instruct − base (paired)**\n", "| size | base | instruct | Δ [95% CI] |", "|---|---|---|---|"]
        for sz in ["0.6B", "1.7B", "4B", "8B", "14B", "32B"]:
            b, i = f"Qwen3-{sz}-Base", f"Qwen3-{sz}"
            if i in R:
                d = paired(i, b, "obsgain-easy") if b in R else None
                L.append(f"| {sz} | {R[b]['picks']['obsgain-easy']['agenticppl']:.3f} | {R[i]['picks']['obsgain-easy']['agenticppl']:.3f} | "
                         + ("–" if d is None else f"{d[0]:+.3f} [{d[1][0]:+.3f},{d[1][1]:+.3f}]") + " |" if b in R else
                         f"| {sz} | – | {R[i]['picks']['obsgain-easy']['agenticppl']:.3f} | – |")
    out = "\n".join(L)
    open(os.path.join(D, "m5_tables.md") if len(sys.argv) > 1 else os.path.join(HERE, "results", "m5_tables.md"), "w").write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
