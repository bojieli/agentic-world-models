"""Per-token log-ratio log p_post(x) - log p_base(x) (bits) by span type; raw and after per-model temperature scaling."""
import csv, os, sys
import numpy as np

TOK = sys.argv[1] if len(sys.argv) > 1 else "tok"
OUT = sys.argv[2] if len(sys.argv) > 2 else "results"
LN2 = np.log(2)
PAIRS = [(f"Qwen3-{s}-Base", f"Qwen3-{s}") for s in ["0.6B", "1.7B", "4B", "8B", "14B"]]
PAIRS += [(f"Qwen3-{s}-Base", f"Nemotron-Terminal-{s}") for s in ["8B", "14B"]]
PAIRS += [(f"Qwen3-{s}", f"Nemotron-Terminal-{s}") for s in ["8B", "14B", "32B"]]
rng = np.random.default_rng(0)


def cats(meta):
    t = meta["typ"]; T = list(meta["types"])
    ob = t == T.index("observation")
    c = {n: t == T.index(n) for n in ["task", "thought", "action", "observation", "markup", "wrap"]}
    c["obs:first16"] = ob & (meta["first"] == 1)
    c["obs:body"] = ob & (meta["first"] == 0)
    c["obs:novel"] = ob & (meta["copy"] == 0)
    c["obs:copy"] = ob & (meta["copy"] == 1)
    return c


def main():
    rows = []
    md = []
    for fmt in ["neutral", "native"]:
        meta = np.load(f"{TOK}/_shared/{fmt}.npz")
        C = cats(meta)
        off = meta["offsets"]
        tix = np.repeat(np.arange(len(off) - 1), np.diff(off))
        ntraj = len(off) - 1
        for base, post in PAIRS:
            pb, pp = f"{TOK}/{base}/{fmt}.npz", f"{TOK}/{post}/{fmt}.npz"
            if not (os.path.exists(pb) and os.path.exists(pp)):
                continue
            B, P = np.load(pb), np.load(pp)
            assert bool(B["hash_match"]) and bool(P["hash_match"]) and list(B["hash"]) == list(P["hash"])
            for var, key in [("raw", "lp"), ("T*", "lp_Tall")]:
                lr = (P[key].astype(np.float64) - B[key].astype(np.float64)) / LN2
                tot_abs = np.abs(lr[~C["wrap"]]).sum()
                lines = []
                for cn, m in C.items():
                    x = lr[m]
                    # bootstrap mean over trajectories
                    s = np.bincount(tix[m], weights=x, minlength=ntraj); n = np.bincount(tix[m], minlength=ntraj)
                    bs = []
                    for _ in range(300):
                        i = rng.integers(0, ntraj, ntraj)
                        bs.append(s[i].sum() / max(n[i].sum(), 1))
                    r = dict(fmt=fmt, base=base, post=post, var=var, cat=cn, n=int(m.sum()),
                             tok_share=float(m.sum() / (~C["wrap"]).sum()), mean=float(x.mean()),
                             ci_lo=float(np.percentile(bs, 2.5)), ci_hi=float(np.percentile(bs, 97.5)),
                             p10=float(np.percentile(x, 10)), p50=float(np.percentile(x, 50)), p90=float(np.percentile(x, 90)),
                             mean_abs=float(np.abs(x).mean()), abs_mass_share=float(np.abs(x).sum() / tot_abs),
                             frac_pos=float((x > 0).mean()),
                             T_base=float(B["T_all"]), T_post=float(P["T_all"]))
                    rows.append(r)
    keys = list(rows[0].keys())
    with open(f"{OUT}/logratio.csv", "w") as f:
        w = csv.DictWriter(f, keys, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    # markdown: one table per (fmt, var) with pairs as row groups
    for fmt in ["neutral", "native"]:
        for var in ["raw", "T*"]:
            sel = [r for r in rows if r["fmt"] == fmt and r["var"] == var]
            if not sel:
                continue
            md.append(f"\n#### log-ratio (bits/token, post − base), rendering={fmt}, {'raw' if var == 'raw' else 'after per-model temperature scaling (T fit on all non-wrapper tokens of 50 cal traj)'}\n")
            md.append("| pair | T base→post | span | tok share | mean [95% CI] | p10 / p50 / p90 | mean abs | share of abs mass |")
            md.append("|---|---|---|---|---|---|---|---|")
            for base, post in PAIRS:
                for r in [r for r in sel if r["base"] == base and r["post"] == post]:
                    md.append(f"| {base} → {post} | {r['T_base']:.1f}→{r['T_post']:.1f} | {r['cat']} | {r['tok_share']:.3f} | "
                              f"{r['mean']:+.3f} [{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}] | {r['p10']:+.2f} / {r['p50']:+.3f} / {r['p90']:+.2f} | "
                              f"{r['mean_abs']:.3f} | {r['abs_mass_share']:.3f} |")
    open(f"{OUT}/logratio.md", "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
