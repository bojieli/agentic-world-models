"""Gate check over an ordered list of scored models (e.g. the Qwen3 ladder).

Binding accuracy (nocopy mask by default) per stratum and pools (S2+S3, S2h+S3h, primary = all four), with a joint cluster bootstrap over
environments (one resample drives every model), plus paired differences between consecutive models.
PASS (ladder gate) iff accuracy rises at every step with the paired 95% CI of the step excluding 0, and the
largest model stays below --ceiling (default 0.95).

usage: gate.py NAME1 NAME2 ... [--render plain] [--mask nocopy] [--temp T1|Tstar] [--metric bind]
"""
import argparse, collections, json, os
import numpy as np
from score2x2 import POOLS, in_group

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, render, results):
    with open(os.path.join(results, name, render, "per_item.jsonl")) as f:
        return {r["id"]: r for r in map(json.loads, f)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--render", default="plain"); ap.add_argument("--mask", default="nocopy")
    ap.add_argument("--temp", default="T1"); ap.add_argument("--metric", default="bind")
    ap.add_argument("--ceiling", type=float, default=0.95); ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--results", default=os.path.join(HERE, "results")); ap.add_argument("--out", default=None)
    ap.add_argument("--id-regex", default=None, help="only item ids matching (e.g. '^S(2|3|2h|3h)-x' = extension batch)")
    a = ap.parse_args()
    R = [load(n, a.render, a.results) for n in a.names]
    ids = sorted(set.intersection(*[set(r) for r in R]))
    if a.id_regex:
        import re
        ids = [i for i in ids if re.search(a.id_regex, i)]
    meta = R[0]
    key = f"{a.temp}/{a.mask}"
    rng = np.random.default_rng(0)
    L = [f"# Gate: {' < '.join(a.names)}  (render={a.render}, mask={a.mask}, {a.temp}, metric={a.metric}, ids={a.id_regex or 'all'})\n"]
    verdict = {}
    present = sorted({meta[i]["stratum"] for i in ids})
    for st in present + [p for p, m in POOLS.items() if sum(x in present for x in m) >= 2]:
        sel = [i for i in ids if in_group(meta[i]["stratum"], st)]
        if not sel:
            continue
        V = np.array([[R[m][i][key][a.metric] for i in sel] for m in range(len(R))])     # models x items
        cl = collections.defaultdict(list)
        for k, i in enumerate(sel):
            cl[meta[i]["env_id"]].append(k)
        groups = list(cl.values())
        W = np.zeros((a.B, len(sel)))
        for b in range(a.B):
            for g in rng.integers(0, len(groups), len(groups)):
                W[b, groups[g]] += 1
        W /= W.sum(1, keepdims=True)
        mean = V.mean(1); draws = W @ V.T                                                  # B x models
        ci = np.percentile(draws, [2.5, 97.5], 0)
        L.append(f"\n## {st} (n={len(sel)})\n\n| model | {a.metric} [95% CI] | step Δ vs previous [paired 95% CI] |\n|---|---|---|")
        ok = True
        for m, n in enumerate(a.names):
            step = ""
            if m:
                d = draws[:, m] - draws[:, m - 1]; lo, hi = np.percentile(d, [2.5, 97.5])
                step = f"{mean[m] - mean[m - 1]:+.3f} [{lo:+.3f},{hi:+.3f}]"
                ok &= lo > 0
            L.append(f"| {n} | {mean[m]:.3f} [{ci[0, m]:.3f},{ci[1, m]:.3f}] | {step} |")
        ok &= mean[-1] < a.ceiling
        verdict[st] = bool(ok)
        L.append(f"\nmonotone with every step's paired CI > 0 and top < {a.ceiling}: **{'PASS' if ok else 'FAIL'}**")
    txt = "\n".join(L) + "\n"
    print(txt)
    if a.out:
        open(a.out, "w").write(txt)
        json.dump(verdict, open(a.out.rsplit(".", 1)[0] + ".json", "w"))


if __name__ == "__main__":
    main()
