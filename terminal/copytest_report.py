"""Tables for the synthetic copy test: model x alphabet x length per context, Nemotron - Qwen3 instruct deltas."""
import json, os, sys
import numpy as np

R = sys.argv[1] if len(sys.argv) > 1 else "results"
ORDER = ["Qwen3-0.6B-Base", "Qwen3-1.7B-Base", "Qwen3-4B-Base", "Qwen3-8B-Base", "Qwen3-14B-Base",
         "Qwen3-0.6B", "Qwen3-1.7B", "Qwen3-4B", "Qwen3-8B", "Qwen3-14B", "Qwen3-32B",
         "Nemotron-Terminal-8B", "Nemotron-Terminal-14B", "Nemotron-Terminal-32B"]
ALPHA = ["hex", "base64", "words", "digits"]
LENGTHS = [8, 16, 32, 64]
CTX = ["bare", "term/neutral", "term/native", "traj/neutral", "traj/native"]
rng = np.random.default_rng(0)


def main():
    res = {n: json.load(open(f"{R}/copytest_{n}.json")) for n in ORDER if os.path.exists(f"{R}/copytest_{n}.json")}
    out = []
    for ctx in CTX:
        out.append(f"\n#### Copy test, context = {ctx}: bits per character on repeated occurrences (mean over strings)\n")
        out.append("| model | " + " | ".join(f"{a}/{L}" for a in ALPHA for L in LENGTHS) + " | first-tok bits | later-tok bits |")
        out.append("|---|" + "---|" * (len(ALPHA) * len(LENGTHS) + 2))
        for n, r in res.items():
            c = r["cells"].get(ctx, {})
            vals = [np.mean(c[f"{a}/{L}"]["bpc"]) if f"{a}/{L}" in c else float("nan") for a in ALPHA for L in LENGTHS]
            fi = np.nanmean([x for v in c.values() for x in v["first"]]) if c else float("nan")
            la = np.nanmean([x for v in c.values() for x in v["later"]]) if c else float("nan")
            out.append(f"| {n} | " + " | ".join(f"{v:.3f}" for v in vals) + f" | {fi:.2f} | {la:.3f} |")
    out.append("\n#### Nemotron − Qwen3 instruct, Δ bits/char (paired over strings, 95% bootstrap CI), pooled over lengths per alphabet\n")
    out.append("| size | context | " + " | ".join(ALPHA) + " | all |")
    out.append("|---|---|" + "---|" * (len(ALPHA) + 1))
    for s in ["8B", "14B", "32B"]:
        a_, b_ = f"Qwen3-{s}", f"Nemotron-Terminal-{s}"
        if a_ not in res or b_ not in res:
            continue
        for ctx in CTX:
            cells = []
            for a in ALPHA + ["all"]:
                d = []
                for al in (ALPHA if a == "all" else [a]):
                    for L in LENGTHS:
                        k = f"{al}/{L}"
                        ca, cb = res[a_]["cells"][ctx].get(k), res[b_]["cells"][ctx].get(k)
                        if not ca or not cb:
                            continue
                        ma = dict(zip(ca["idx"], ca["bpc"])); mb = dict(zip(cb["idx"], cb["bpc"]))
                        d += [mb[i] - ma[i] for i in ma if i in mb]
                d = np.array(d)
                bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(1000)]
                cells.append(f"{d.mean():+.3f} [{np.percentile(bs, 2.5):+.3f},{np.percentile(bs, 97.5):+.3f}]")
            out.append(f"| {s} | {ctx} | " + " | ".join(cells) + " |")
    txt = "\n".join(out) + "\n"
    open(f"{R}/copytest.md", "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
