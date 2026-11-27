"""Size-equivalent multipliers by inverse interpolation on a model-size ladder.

For a metric m and a post-trained model P that started from checkpoint S (a ladder point at size x_S = log2 of its
non-embedding params), find x* where the piecewise-linear ladder curve (in log2 non-embedding params) reaches m(P);
log2 n = x* - x_S. No extrapolation: values beyond the usable range are censored, where the usable range is the ladder
range intersected with [x_S - 1, x_S + 2] (i.e. 1/2x .. 4x of the start). The instruct ladder is used for instruct-
started models and the base ladder only for base-started ones (Klear; plus a Nemotron-vs-base sensitivity row).

Validity gate (per metric): the instruct ladder must be monotone with every adjacent step's paired 95% CI excluding 0.

CIs: joint bootstrap over evaluation trajectories (one resample recomputes every ladder point and every model).

Default inputs: env P2_WORK / P2_RAW (analyze2 loaders). Reusable for another benchmark by replacing `load_metrics`
with a function returning, per model, {metric: (kind, num, den)} per-trajectory sum arrays.

usage: P2_WORK=work_m12 P2_RAW=results/raw_m12 size_equiv.py [--ds swe] [--B 2000] [--out results/size_equiv]
"""
import argparse, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze2 as A

PARAMS = {k: v["non_embedding"] for k, v in json.load(open(os.path.join(HERE, "configs", "params.json"))).items()}
SIZES = ["0.6B", "1.7B", "4B", "8B", "14B", "32B"]
LADDERS = {"inst": {s: f"Qwen3-{s}" for s in SIZES}, "base": {s: f"Qwen3-{s}-Base" for s in SIZES[:5]}}
POST = [  # (row label, model, start, ladder)
    ("Nemotron-Terminal-8B", "Nemotron-Terminal-8B", "Qwen3-8B", "inst"),
    ("tmax-sft-8b", "tmax-sft-8b", "Qwen3-8B", "inst"),
    ("tmax-8b", "tmax-8b", "Qwen3-8B", "inst"),
    ("SERA-8B", "SERA-8B", "Qwen3-8B", "inst"),
    ("OpenThinker-Agent-v1-SFT", "OpenThinker-Agent-v1-SFT", "Qwen3-8B", "inst"),
    ("Arctic-AWM-8B", "Arctic-AWM-8B", "Qwen3-8B", "inst"),
    ("Light-IF-8B (non-agentic)", "Light-IF-8B", "Qwen3-8B", "inst"),
    ("WebWorld-8B (web world model)", "WebWorld-8B", "Qwen3-8B", "inst"),
    ("Klear-Reasoner-8B-SFT (non-agentic, base start)", "Klear-Reasoner-8B-SFT", "Qwen3-8B-Base", "base"),
    ("Nemotron-Terminal-14B", "Nemotron-Terminal-14B", "Qwen3-14B", "inst"),
    ("CodeScout-14B", "CodeScout-14B", "Qwen3-14B", "inst"),
    ("SERA-14B", "SERA-14B", "Qwen3-14B", "inst"),
    ("FrogMini-14B", "FrogMini-14B-2510", "Qwen3-14B", "inst"),
    ("Light-IF-14B (non-agentic)", "Light-IF-14B", "Qwen3-14B", "inst"),
    ("Nemotron-Terminal-32B", "Nemotron-Terminal-32B", "Qwen3-32B", "inst"),
    ("OpenThinkerAgent-32B", "OpenThinkerAgent-32B", "Qwen3-32B", "inst"),
    ("sensitivity: Nemotron-Terminal-8B vs 8B-Base", "Nemotron-Terminal-8B", "Qwen3-8B-Base", "base"),
    ("sensitivity: Nemotron-Terminal-14B vs 14B-Base", "Nemotron-Terminal-14B", "Qwen3-14B-Base", "base"),
    ("sensitivity: tmax-8b vs tmax-sft-8b (RL step)", "tmax-8b", "tmax-sft-8b", "inst8B"),
] + [(f"reference: Qwen3-{s} instruct vs base", f"Qwen3-{s}", f"Qwen3-{s}-Base", "base") for s in SIZES[:5]]
KINDS = ["test_run", "python_exec", "shell_other", "file_view", "search", "edit_ack"]
HIGHER = {}  # metric -> True if higher is better


def load_metrics(model, ds, M, ntraj, boot):
    R = A.loadm(model, ds)
    if R is None:
        return None
    out = {}
    F = A.m1_fit(R, M)
    m1 = A.m1_summary(F, ntraj, boot)
    for s in ["content", "outcome"] + [f"kind={k}" for k in KINDS]:
        if s in m1:
            out[f"M1 recal content bits/tok [{s}]"] = ("ratio", m1[s]["_sums"]["hist"], m1[s]["_n"]); HIGHER[f"M1 recal content bits/tok [{s}]"] = False
    m2 = A.m2_summary(R, M, F["content"]["kT"], ntraj, boot)
    for k in ["T/content/all", "T/outcome/all"] + [f"T/content/kind={x}" for x in KINDS]:
        if k in m2:  # temperature-recalibrated (per-model T* fitted on calibration content tokens)
            nm = f"M2 abs info gain bits/tok @T* [{k[2:]}]"
            out[nm] = ("ratio", m2[k]["_sw"] - m2[k]["_t"], m2[k]["_nt"]); HIGHER[nm] = True
            nm = f"M2 NLL given true action bits/tok @T* [{k[2:]}]"
            out[nm] = ("ratio", m2[k]["_t"], m2[k]["_nt"]); HIGHER[nm] = False
    for k in ["raw/content/all", "raw/outcome/all"] + [f"raw/content/kind={x}" for x in KINDS]:
        if k in m2:
            nm = f"M2 abs info gain bits/tok [{k[4:]}]"
            out[nm] = ("ratio", m2[k]["_sw"] - m2[k]["_t"], m2[k]["_nt"]); HIGHER[nm] = True
            nm = f"M2 relative gain [{k[4:]}]"
            out[nm] = ("gain", m2[k]["_t"], m2[k]["_sw"]); HIGHER[nm] = True
    rd = A.read_sums(R, M, ntraj)
    if rd:
        for k, (h, s_, n) in rd.items():
            nm = f"Reading: next-action bits/tok saved by seeing the obs [{k}]"
            out[nm] = ("ratio", h - s_, n); HIGHER[nm] = True
    return out


def value(spec, W=None):
    kind, a, b = spec
    S = (lambda x: x.sum()) if W is None else (lambda x: W @ x)
    if kind == "ratio":
        return S(a) / np.maximum(S(b), 1e-12)
    if kind == "gain":
        return 1 - S(a) / np.maximum(S(b), 1e-12)


def inv_interp(xs, ys, v, lo, hi):
    """ys increasing in xs (already oriented so larger = better). Returns (x*, censor) with censor in {'', '<', '>'}."""
    # restrict to [lo, hi] by interpolating the curve at the window edges
    xs = np.asarray(xs, float); ys = np.asarray(ys, float)
    ylo, yhi = np.interp(lo, xs, ys), np.interp(hi, xs, ys)
    if v < ylo:
        return lo, "<"
    if v > yhi:
        return hi, ">"
    gx = np.concatenate([[lo], xs[(xs > lo) & (xs < hi)], [hi]])
    gy = np.interp(gx, xs, ys)
    for i in range(len(gx) - 1):
        if gy[i] <= v <= gy[i + 1]:
            return (gx[i] + (v - gy[i]) / (gy[i + 1] - gy[i]) * (gx[i + 1] - gx[i]) if gy[i + 1] > gy[i] else gx[i]), ""
    return hi, ">"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", default="swe"); ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "size_equiv"))
    a = ap.parse_args()
    ds = a.ds
    M = A.meta(ds); ntraj = len(M["trajs"])
    boot = A.Boot(ntraj, a.B, [i for i, t in enumerate(M["trajs"]) if t["split"] == "eval"])
    names = {m for L in LADDERS.values() for m in L.values()} | {p[1] for p in POST} | {p[2] for p in POST}
    D = {m: load_metrics(m, ds, M, ntraj, boot) for m in sorted(names)}
    D = {m: v for m, v in D.items() if v}
    metrics = sorted({k for v in D.values() for k in v})
    res = {}
    for met in metrics:
        sgn = 1.0 if HIGHER[met] else -1.0
        V = {m: (value(D[m][met]), value(D[m][met], boot.W)) for m in D if met in D[m]}
        r = dict(higher_is_better=HIGHER[met], ladders={}, rows=[])
        for lad, L in LADDERS.items():
            pts = [(s, m) for s, m in L.items() if m in V]
            if len(pts) < 3:
                continue
            steps = []
            for (s1, m1), (s2, m2) in zip(pts[:-1], pts[1:]):
                d = V[m2][0] - V[m1][0]; db = V[m2][1] - V[m1][1]
                c = A.ci(db)
                steps.append(dict(step=f"{s1}->{s2}", delta=float(d), ci=c, ok=bool(c[0] > 0) if sgn > 0 else bool(c[1] < 0)))
            r["ladders"][lad] = dict(points={s: float(V[m][0]) for s, m in pts}, steps=steps,
                                     monotone=bool(all(sgn * st["delta"] > 0 for st in steps)),
                                     gate=bool(all(st["ok"] for st in steps)))
        for label, m, start, lad in POST:
            lname = "inst" if lad == "inst8B" else lad
            if m not in V or start not in V or lname not in r["ladders"]:
                continue
            L = LADDERS[lname]; pts = [(s, mm) for s, mm in L.items() if mm in V]
            xs = np.log2([PARAMS[s] for s, _ in pts])
            ssz = "8B" if lad == "inst8B" else next(s for s, mm in L.items() if mm == start)
            xS = np.log2(PARAMS[ssz])
            lo, hi = max(xs.min(), xS - 1), min(xs.max(), xS + 2)
            d = V[m][0] - V[start][0]; db = V[m][1] - V[start][1]

            def solve(ys, vp, vs):
                ys = sgn * np.maximum.accumulate(sgn * np.asarray(ys)) if True else ys  # isotonic envelope
                yo = sgn * ys
                # anchor: the start's own ladder value is replaced by the start's measured value at xS (they coincide
                # for ladder starts); the model's value is shifted by the same amount, so log2 n depends on delta only
                anchor = np.interp(xS, xs, yo)
                return inv_interp(xs, yo, anchor + sgn * (vp - vs), lo, hi)
            ys0 = [V[mm][0] for _, mm in pts]
            x0, c0 = solve(ys0, V[m][0], V[start][0])
            xb = []; cb = []
            for k in range(a.B):
                xk, ck = solve([V[mm][1][k] for _, mm in pts], V[m][1][k], V[start][1][k])
                xb.append(xk - xS); cb.append(ck)
            cb = np.array(cb)
            l2 = float(x0 - xS)
            fmt = lambda v: f"{2 ** v:.2f}x"
            r["rows"].append(dict(label=label, model=m, start=start, ladder=lname, delta=float(d), delta_ci=A.ci(db),
                                  log2n=l2, censor=c0, log2n_ci=A.ci(np.array(xb)),
                                  n=("<" if c0 == "<" else ">" if c0 == ">" else "") + fmt(l2),
                                  frac_censored_low=float((cb == "<").mean()), frac_censored_high=float((cb == ">").mean())))
        res[met] = r
    os.makedirs(a.out, exist_ok=True)
    json.dump(res, open(os.path.join(a.out, f"size_equiv_{ds}.json"), "w"), indent=1)
    L = [f"# Size-equivalent multipliers ({ds}; inverse piecewise-linear interpolation in log2 non-embedding params; "
         f"window 1/2x..4x of the start within the ladder; joint trajectory bootstrap, {a.B} draws)\n"]
    for met, r in res.items():
        L.append(f"\n## {met} ({'higher' if r['higher_is_better'] else 'lower'} is better)\n")
        for lad, f in r["ladders"].items():
            L.append(f"- {lad} ladder: " + ", ".join(f"{s} {v:.4f}" for s, v in f["points"].items()) +
                     f"; monotone={f['monotone']}; GATE={'PASS' if f['gate'] else 'FAIL'} (" +
                     "; ".join(f"{st['step']} {st['delta']:+.4f} [{st['ci'][0]:+.4f},{st['ci'][1]:+.4f}]" for st in f["steps"]) + ")")
        if r["rows"]:
            L += ["", "| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |", "|---|---|---|---|---|---|"]
            for x in r["rows"]:
                L.append(f"| {x['label']} | {x['start']} ({x['ladder']}) | {x['delta']:+.4f} [{x['delta_ci'][0]:+.4f},{x['delta_ci'][1]:+.4f}] | "
                         f"{x['n']} | {x['log2n']:+.2f} [{x['log2n_ci'][0]:+.2f},{x['log2n_ci'][1]:+.2f}] | {x['frac_censored_low']:.2f}/{x['frac_censored_high']:.2f} |")
    open(os.path.join(a.out, f"size_equiv_{ds}.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
