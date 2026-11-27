"""Preliminary size-equivalent analysis of agentic post-training on terminal observation tokens.

For each post-trained model m with starting checkpoint s, Δ = metric(m) - metric(s) (paired, same tokens), and
n = 2^(Δ/b), b = OLS slope of the metric on log2(total params) along a Qwen3 ladder. Joint trajectory bootstrap:
resample the 200 eval trajectories once per replicate, recompute every model's metric (incl. cross-fitted T and
rank-recalibration q), refit b, recompute n.

CPU analysis of saved token scores and token-class arrays.
usage: python size_equiv.py [--boot 2000] [--out size_equiv/recomputed]
"""
import argparse, json, os, sys
import numpy as np
np.seterr(over="ignore", divide="ignore", invalid="ignore")

ap = argparse.ArgumentParser()
ap.add_argument("--tok", default="tok")
ap.add_argument("--cls", default="token_classes")
ap.add_argument("--prep", default="prep.json")
ap.add_argument("--boot", type=int, default=2000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--splits", type=int, default=10, help="extra 2-fold split seeds for split-sensitivity of cross-fit point estimates")
ap.add_argument("--out", default="size_equiv/recomputed")
a = ap.parse_args()
LN2 = np.log(2)

# ---------------------------------------------------------------- parameter counts (Qwen3 configs; no biases)
CFG = {  # hidden, layers, intermediate, q heads, kv heads, tied ; head_dim 128, vocab 151936 for all
    "0.6B": (1024, 28, 3072, 16, 8, True), "1.7B": (2048, 28, 6144, 16, 8, True), "4B": (2560, 36, 9728, 32, 8, True),
    "8B": (4096, 36, 12288, 32, 8, False), "14B": (5120, 40, 17408, 40, 8, False), "32B": (5120, 64, 25600, 64, 8, False)}


def nparams(h, L, I, nq, nkv, tied, hd=128, V=151936):
    attn = h * nq * hd + 2 * h * nkv * hd + nq * hd * h + 2 * hd
    return V * h * (1 if tied else 2) + L * (attn + 3 * h * I + 2 * h) + h


PARAMS = {k: nparams(*v) for k, v in CFG.items()}


def size_of(m):
    for k in CFG:
        if f"-{k}" in m:
            return k
    raise ValueError(m)


# ---------------------------------------------------------------- models present
prep = json.load(open(a.prep))
models = sorted(d for d in os.listdir(a.tok) if not d.startswith("_") and os.path.exists(f"{a.tok}/{d}/native.npz"))
BASE_LADDER = [m for m in ["Qwen3-0.6B-Base", "Qwen3-1.7B-Base", "Qwen3-4B-Base", "Qwen3-8B-Base", "Qwen3-14B-Base"] if m in models]
INST_LADDER = [m for m in ["Qwen3-4B", "Qwen3-8B", "Qwen3-14B", "Qwen3-32B"] if m in models]
PAIRS = [  # (start, post, ladder)
    ("Qwen3-8B", "Nemotron-Terminal-8B", "inst"), ("Qwen3-14B", "Nemotron-Terminal-14B", "inst"),
    ("Qwen3-32B", "Nemotron-Terminal-32B", "inst"),
    ("Qwen3-4B-Base", "Qwen3-4B", "base"), ("Qwen3-8B-Base", "Qwen3-8B", "base"), ("Qwen3-14B-Base", "Qwen3-14B", "base")]
PAIRS = [p for p in PAIRS if p[0] in models and p[1] in models]
LADDERS = {"base": BASE_LADDER, "inst": INST_LADDER}

# rank buckets (rank = #logits strictly above the true token, clamped at 1000) and top-1-prob buckets
R_EDGES = np.array([0, 1, 2, 4, 8, 16, 32, 100, 1000, 1001])          # 9 buckets; last = rank>=1000 (clamped)
P_EDGES = np.array([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99, 1.01])  # 12 buckets
NR, NP = len(R_EDGES) - 1, len(P_EDGES) - 1

rng = np.random.default_rng(a.seed)
NT = 200
W = np.vstack([np.ones(NT), rng.multinomial(NT, np.full(NT, 1 / NT), size=a.boot)]).astype(np.float64)  # row 0 = point
def split(seed):
    p = np.random.default_rng(1000 + seed).permutation(NT); A = np.zeros(NT, bool); A[p[:NT // 2]] = True
    return A
SPLIT0 = split(0)

log = open(f"{a.out}/run.log", "w")
def say(*x):
    s = " ".join(str(v) for v in x); print(s, flush=True); log.write(s + "\n"); log.flush()

say("models in tok/:", models)
say("params:", {k: f"{v/1e9:.3f}B" for k, v in PARAMS.items()})
say("base ladder:", BASE_LADDER, "| instruct ladder:", INST_LADDER)


def crossfit_grid(G, A, Wm):
    """G: per-traj (NT, K) summed loss for each grid value (fit set); returns per-rep chosen index for fold A and B."""
    GA = Wm[:, A] @ G[A]; GB = Wm[:, ~A] @ G[~A]
    return GA.argmin(1), GB.argmin(1)


def eval_grid(Ge, kA, kB, A, Wm):
    """evaluate fold B with index fitted on A and vice versa; Ge (NT,K) evaluation sums. returns (R,) summed loss."""
    EB = Wm[:, ~A] @ Ge[~A]; EA = Wm[:, A] @ Ge[A]; r = np.arange(len(Wm))
    return EB[r, kA] + EA[r, kB]


def rankrecal(Cfit, Ceval, A, Wm):
    """Cfit/Ceval: per-traj (NT, NP*NR) counts. q fitted (Laplace) on fold A content, evaluated on fold B, and vice versa."""
    out = np.zeros(len(Wm))
    for F in (A, ~A):
        cf = (Wm[:, F] @ Cfit[F]).reshape(-1, NP, NR)
        q = (cf + 1) / (cf.sum(2, keepdims=True) + NR)
        ce = (Wm[:, ~F] @ Ceval[~F]).reshape(-1, NP, NR)
        out += (ce * -np.log2(q)).sum((1, 2))
    return out


RES = {}  # RES[fmt][metric][mask][model] = (R,) array of metric values
INFO = {}
for fmt in ["neutral", "native"]:
    meta = np.load(f"{a.tok}/_shared/{fmt}.npz"); cz = np.load(f"{a.cls}/cls_{fmt}.npz")
    assert len(cz["cls"]) == len(meta["ids"]), "class file does not match tok/_shared"
    trajs = list(meta["traj"]); assert len(trajs) == NT
    cal_in_tok = len(set(trajs) & set(prep["cal"]))
    typ, copy, off = meta["typ"], meta["copy"], meta["offsets"]
    OBS = list(meta["types"]).index("observation"); CLS = list(cz["names"]); cls = cz["cls"]; cid = {c: i for i, c in enumerate(CLS)}
    ob = typ == OBS; tix = np.repeat(np.arange(NT), np.diff(off))
    rand = ob & np.isin(cls, [cid["rand_hash"], cid["rand_time"], cid["rand_misc"]])
    output = ob & np.isin(cls, [cid[c] for c in ["err_line", "test_line", "number", "path", "other"]])
    novel = ob & (copy == 0)
    content = output & novel
    outcome = content & np.isin(cls, [cid["err_line"], cid["test_line"], cid["number"]])
    MASKS = {"content": content, "outcome": outcome, "random": rand, "random_novel": rand & novel, "hash_novel": ob & (cls == cid["rand_hash"]) & novel,
             "boiler": ob & (cls == cid["boiler"]), "prompt_echo_ws": ob & np.isin(cls, [cid["prompt"], cid["cmd_echo"], cid["ws"]])}
    INFO[fmt] = dict(cal_trajs_in_tok=cal_in_tok, ntok={k: int(v.sum()) for k, v in MASKS.items()}, obs=int(ob.sum()))
    say(f"\n[{fmt}] cal trajectories present in tok/: {cal_in_tok} (so T and q are cross-fitted on eval halves); token counts",
        INFO[fmt]["ntok"])
    cnt = {k: np.bincount(tix[v], minlength=NT).astype(float) for k, v in MASKS.items()}
    Ncnt = {k: W @ c for k, c in cnt.items()}
    R = {}
    for m in models:
        z = np.load(f"{a.tok}/{m}/{fmt}.npz")
        assert bool(z["hash_match"]) and list(z["hash"]) == list(meta["hash"]), f"token hash mismatch {m} {fmt}"
        v3 = "lp_tgrid" in z.files
        bits = -z["lp"].astype(np.float64) / LN2
        bT = -z["lp_Tobs"].astype(np.float64) / LN2
        per = {"raw": bits, "capped2": np.minimum(bits, 2.0), "prob": np.exp2(-bits), "T_obs_cal": bT}
        for met, x in per.items():
            for mk, M in MASKS.items():
                s = np.bincount(tix[M], weights=x[M], minlength=NT)
                R.setdefault(met, {}).setdefault(mk, {})[m] = (W @ s) / Ncnt[mk]
        INFO[fmt].setdefault("T_obs_cal", {})[m] = float(z["T_obs"])
        INFO[fmt].setdefault("v3", {})[m] = v3
        if not v3:
            continue
        tg = z["tgrid"]; grid = {}
        for mk in ["content", "outcome", "random", "random_novel"]:
            M = MASKS[mk]; g = -z["lp_tgrid"][M].astype(np.float64) / LN2
            grid[mk] = np.stack([np.bincount(tix[M], weights=g[:, k], minlength=NT) for k in range(len(tg))], 1)
        kA, kB = crossfit_grid(grid["content"], SPLIT0, W)
        INFO[fmt].setdefault("T_cf", {})[m] = dict(A=float(tg[kA[0]]), B=float(tg[kB[0]]),
                                                   full=float(tg[grid["content"].sum(0).argmin()]))
        for mk in ["content", "outcome", "random", "random_novel"]:
            R.setdefault("T_cf_content", {}).setdefault(mk, {})[m] = eval_grid(grid[mk], kA, kB, SPLIT0, W) / Ncnt[mk]
        # split sensitivity of point estimate
        sens = []
        for sd in range(1, a.splits + 1):
            A2 = split(sd); kA2, kB2 = crossfit_grid(grid["content"], A2, W[:1])
            sens.append(float(eval_grid(grid["content"], kA2, kB2, A2, W[:1])[0] / Ncnt["content"][0]))
        INFO[fmt].setdefault("T_cf_split_sd", {})[m] = float(np.std(sens))
        rb = np.clip(np.searchsorted(R_EDGES, z["rank"].astype(np.int64), side="right") - 1, 0, NR - 1)
        pb = np.clip(np.searchsorted(P_EDGES, z["top1"].astype(np.float64), side="right") - 1, 0, NP - 1)
        cell = pb * NR + rb
        C = {}
        for mk in ["content", "outcome", "random", "random_novel"]:
            M = MASKS[mk]; C[mk] = np.zeros((NT, NP * NR)); np.add.at(C[mk], (tix[M], cell[M]), 1)
        for mk in ["content", "outcome", "random", "random_novel"]:
            R.setdefault("rankrecal", {}).setdefault(mk, {})[m] = rankrecal(C["content"], C[mk], SPLIT0, W) / Ncnt[mk]
        sens = []
        for sd in range(1, a.splits + 1):
            A2 = split(sd); sens.append(float(rankrecal(C["content"], C["content"], A2, W[:1])[0] / Ncnt["content"][0]))
        INFO[fmt].setdefault("rr_split_sd", {})[m] = float(np.std(sens))
        say(f"  {m}: v3 T_cf(content) A/B/full = {INFO[fmt]['T_cf'][m]}  T_obs(cal)={float(z['T_obs'])}")
    RES[fmt] = R

# ---------------------------------------------------------------- slopes and size equivalents
METRICS = ["raw", "T_obs_cal", "T_cf_content", "capped2", "prob", "rankrecal"]
HIGHER_BETTER = {"prob"}
pct = lambda x: (float(np.nanpercentile(x, 2.5)), float(np.nanpercentile(x, 97.5)))


def fit(R, ladder):
    x = np.array([np.log2(PARAMS[size_of(m)]) for m in ladder]); xc = x - x.mean()
    Y = np.stack([R[m] for m in ladder], 1)  # (reps, k)
    b = (Y - Y.mean(1, keepdims=True)) @ xc / (xc @ xc)
    yhat = Y.mean(1, keepdims=True) + b[:, None] * xc[None]
    ss_res = ((Y - yhat) ** 2).sum(1); ss_tot = ((Y - Y.mean(1, keepdims=True)) ** 2).sum(1)
    r2 = 1 - ss_res / np.where(ss_tot > 0, ss_tot, np.nan)
    return b, r2, (Y - yhat)[0]


OUT = {"info": INFO, "params": PARAMS, "ladders": LADDERS, "boot": a.boot, "slopes": {}, "pairs": {}, "ladder_values": {}}
for fmt in RES:
    for met in METRICS:
        if met not in RES[fmt]:
            continue
        for mk in RES[fmt][met]:
            R = RES[fmt][met][mk]
            for ln, lad in LADDERS.items():
                lad = [m for m in lad if m in R]
                key = f"{fmt}|{met}|{mk}|{ln}"
                OUT["ladder_values"][key] = {m: [float(R[m][0]), *pct(R[m])] for m in lad}
                if len(lad) < 2:
                    continue
                b, r2, resid = fit(R, lad)
                ys = np.stack([R[m] for m in lad], 1); sgn = 1 if met in HIGHER_BETTER else -1
                mono = np.all(np.diff(sgn * ys, axis=1) > 0, axis=1)  # strictly improving with size
                lo, hi = pct(b)
                OUT["slopes"][key] = dict(models=lad, b=float(b[0]), ci=[lo, hi], r2=float(r2[0]), resid=resid.tolist(),
                                          monotone=bool(mono[0]), p_monotone=float(mono[1:].mean()),
                                          crosses0=bool(lo <= 0 <= hi), npts=len(lad))
            for s, p, ln in PAIRS:
                if s not in R or p not in R:
                    continue
                lad = [m for m in LADDERS[ln] if m in R]
                d = R[p] - R[s]; dlo, dhi = pct(d)
                rec = dict(start=s, post=p, ladder=ln, delta=float(d[0]), delta_ci=[dlo, dhi], start_val=float(R[s][0]),
                           post_val=float(R[p][0]))
                if len(lad) >= 2:
                    b, _, _ = fit(R, lad)
                    dbl = d / b; n = np.exp2(dbl)
                    rec.update(b=float(b[0]), doublings=float(dbl[0]), doublings_ci=list(pct(dbl)), n=float(n[0]),
                               n_ci=list(pct(n)), b_crosses0=OUT["slopes"][f"{fmt}|{met}|{mk}|{ln}"]["crosses0"],
                               frac_b_wrong_sign=float(np.mean((b[1:] >= 0) if met not in HIGHER_BETTER else (b[1:] <= 0))),
                               npts=len(lad))
                    # robustness: local slope from the ladder points bracketing the start size
                    xs = [PARAMS[size_of(m)] for m in lad]; x0 = PARAMS[size_of(s)]
                    lo_ = [m for m, x in zip(lad, xs) if x < x0]; hi_ = [m for m, x in zip(lad, xs) if x > x0]
                    loc = ([lo_[-1]] if lo_ else []) + ([s] if s in lad and not (lo_ and hi_) else []) + ([hi_[0]] if hi_ else [])
                    if len(loc) >= 2:
                        bl, _, _ = fit(R, loc); dl = d / bl
                        rec.update(local_ladder=loc, b_local=float(bl[0]), n_local=float(np.exp2(dl[0])), n_local_ci=list(pct(np.exp2(dl))))
                OUT["pairs"][f"{fmt}|{met}|{mk}|{s}->{p}"] = rec

# ================================================================ PRIMARY (method v2): inverse piecewise-linear interpolation
# x = log2(non-embedding params); ladder points joined piecewise-linearly; the post model's metric value is located on the
# ladder by walking outward from the start model's own ladder point (start is on the ladder => anchored exactly).
# Values beyond the ladder ends are censored (never extrapolated). Joint bootstrap: same trajectory resample for ladder,
# start and post. Validity gate: every adjacent ladder step must improve with its paired 95% CI excluding 0.
# non-embedding params (B) from the Qwen3 configuration files; base and instruct share them. Cross-checked vs configs.
NONEMB = {k: v * 1e9 for k, v in {"0.6B": 0.440, "1.7B": 1.409, "4B": 3.634, "8B": 6.946, "14B": 13.212, "32B": 31.206}.items()}
for k, v in CFG.items():
    calc = nparams(*v) - 151936 * v[0] * (1 if v[5] else 2)
    assert abs(calc / NONEMB[k] - 1) < 2e-3, (k, calc, NONEMB[k])
XN = lambda m: np.log2(NONEMB[size_of(m)])
PRIMARY = ["rankrecal", "T_cf_content", "T_obs_cal"]
SECONDARY = ["raw", "capped2", "prob"]


def locate(G, gp, xs, j):
    """G: (k,) goodness (higher better) of ladder; gp: post goodness; j: start index. returns log2 n (±inf if censored)."""
    if gp >= G[j]:
        for i in range(j, len(G) - 1):
            if G[i + 1] >= gp:
                t = (gp - G[i]) / (G[i + 1] - G[i]) if G[i + 1] != G[i] else 0.0
                return xs[i] + t * (xs[i + 1] - xs[i]) - xs[j]
        return np.inf
    for i in range(j, 0, -1):
        if G[i - 1] <= gp:
            t = (G[i] - gp) / (G[i] - G[i - 1]) if G[i] != G[i - 1] else 0.0
            return xs[i] - t * (xs[i] - xs[i - 1]) - xs[j]
    return -np.inf


q = lambda x, p: float(np.quantile(x, p, method="inverted_cdf"))
OUT["interp"] = {}; OUT["gate"] = {}
for fmt in RES:
    for met in PRIMARY + SECONDARY:
        if met not in RES[fmt]:
            continue
        sgn = 1.0 if met in HIGHER_BETTER else -1.0
        for mk in ["content", "outcome"]:
            R = RES[fmt][met][mk]
            for ln, lad0 in LADDERS.items():
                lad = [m for m in lad0 if m in R]
                if len(lad) < 2:
                    continue
                G = sgn * np.stack([R[m] for m in lad], 1)
                steps = []
                for i in range(len(lad) - 1):
                    d = G[:, i + 1] - G[:, i]
                    steps.append(dict(frm=lad[i], to=lad[i + 1], step=float(d[0]), ci=[pct(d)[0], pct(d)[1]], ok=bool(pct(d)[0] > 0)))
                gate = all(s["ok"] for s in steps)
                OUT["gate"][f"{fmt}|{met}|{mk}|{ln}"] = dict(models=lad, passes=gate, steps=steps)
            for s, p, ln in PAIRS:
                lad = [m for m in LADDERS[ln] if m in R]
                if s not in lad or p not in R or len(lad) < 2:
                    continue
                xs = np.array([XN(m) for m in lad]); j = lad.index(s)
                G = sgn * np.stack([R[m] for m in lad], 1); gp = sgn * R[p]
                l2 = np.array([locate(G[r], gp[r], xs, j) for r in range(len(G))])
                gk = f"{fmt}|{met}|{mk}|{ln}"
                OUT["interp"][f"{fmt}|{met}|{mk}|{s}->{p}"] = dict(
                    start=s, post=p, ladder=lad, gate=OUT["gate"][gk]["passes"],
                    delta=float(R[p][0] - R[s][0]), delta_ci=list(pct(R[p] - R[s])),
                    log2n=float(l2[0]), lo=q(l2, .025), hi=q(l2, .975),
                    cens_lo=float(xs[0] - xs[j]), cens_hi=float(xs[-1] - xs[j]),
                    p_gain=float(np.mean(l2[1:] > 0)), p_cens_hi=float(np.mean(np.isinf(l2[1:]) & (l2[1:] > 0))),
                    p_cens_lo=float(np.mean(np.isinf(l2[1:]) & (l2[1:] < 0))))

json.dump(OUT, open(f"{a.out}/results.json", "w"), indent=1)

# ---------------------------------------------------------------- markdown tables
L = []
w = L.append
w(f"models in tok/: {', '.join(models)}\n")
w(f"v3 (rank/top1/T-grid present): {', '.join(m for m in models if INFO['neutral']['v3'][m])}\n")
w(f"bootstrap: {a.boot} joint trajectory resamples over {NT} eval trajectories; cal trajectories in tok/: "
  f"{INFO['neutral']['cal_trajs_in_tok']} -> T and q are 2-fold cross-fitted on eval halves (split seed 0)\n")
w("token counts: " + "; ".join(f"{f}: " + ", ".join(f"{k}={v}" for k, v in INFO[f]['ntok'].items()) for f in INFO) + "\n")
def fmt_l2(v, x):
    if np.isinf(x):
        return f">{v['cens_hi']:+.2f}" if x > 0 else f"<{v['cens_lo']:+.2f}"
    return f"{x:+.2f}"


def fmt_n(v):
    x = v["log2n"]
    if x <= 0:
        return "no gain" + (f" (<{2**v['cens_lo']:.2f}x)" if np.isinf(x) else f" ({2**x:.2f}x)")
    return f">{2**v['cens_hi']:.2f}x" if np.isinf(x) else f"{2**x:.2f}x"


w("\n## PRIMARY: size-equivalent by inverse piecewise-linear interpolation (x = log2 non-embedding params)\n")
w("non-embedding params: " + ", ".join(f"{k} {v/1e9:.3f}B" for k, v in NONEMB.items()) + "\n")
w("Validity gate: each adjacent ladder step improves with paired 95% CI excluding 0. n is reported only when the gate passes.\n")
w("| rendering | metric | mask | ladder | models | steps (improvement, 95% CI) | gate |")
w("|---|---|---|---|---|---|---|")
for k, v in OUT["gate"].items():
    fmt, met, mk, ln = k.split("|")
    st = "; ".join(f"{size_of(x['frm'])}→{size_of(x['to'])} {x['step']:+.4f} [{x['ci'][0]:+.4f},{x['ci'][1]:+.4f}]{'' if x['ok'] else ' ✗'}" for x in v["steps"])
    w(f"| {fmt} | {met} | {mk} | {ln} | {len(v['models'])} | {st} | {'PASS' if v['passes'] else 'FAIL'} |")
w("\n| rendering | metric | mask | pair | Δ post−start [95% CI] | log2 n [95% CI] | n | P(gain) | P(cens. hi/lo) | ladder range (log2) |")
w("|---|---|---|---|---|---|---|---|---|---|")
for tier in (PRIMARY, SECONDARY):
    for k, v in OUT["interp"].items():
        fmt, met, mk, _ = k.split("|")
        if met not in tier:
            continue
        pr = f"{v['post'].replace('Nemotron-Terminal', 'Nemo')} vs {v['start']}"
        d = f"{v['delta']:+.4f} [{v['delta_ci'][0]:+.4f}, {v['delta_ci'][1]:+.4f}]"
        rng_ = f"[{v['cens_lo']:+.2f}, {v['cens_hi']:+.2f}] ({len(v['ladder'])} pts)"
        if not v["gate"]:
            w(f"| {fmt} | {met} | {mk} | {pr} | {d} | gate FAIL – not reported | – | – | – | {rng_} |")
            continue
        w(f"| {fmt} | {met} | {mk} | {pr} | {d} | {fmt_l2(v, v['log2n'])} [{fmt_l2(v, v['lo'])}, {fmt_l2(v, v['hi'])}] | {fmt_n(v)} | "
          f"{v['p_gain']:.2f} | {v['p_cens_hi']:.2f}/{v['p_cens_lo']:.2f} | {rng_} |")
w("\n## SECONDARY (superseded): global OLS slopes b (metric per doubling of total params)\n")
w("| rendering | metric | mask | ladder | pts | b | 95% CI | R² | residuals | monotone | P(monotone) |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for k, v in OUT["slopes"].items():
    fmt, met, mk, ln = k.split("|")
    w(f"| {fmt} | {met} | {mk} | {ln} | {v['npts']} | {v['b']:+.4f} | [{v['ci'][0]:+.4f}, {v['ci'][1]:+.4f}]{' **crosses 0**' if v['crosses0'] else ''} | "
      f"{v['r2']:.3f} | {', '.join(f'{x:+.4f}' for x in v['resid'])} | {'yes' if v['monotone'] else 'NO'} | {v['p_monotone']:.2f} |")
w("\n## SECONDARY (superseded): global-slope n = 2^(Δ/b) — fragile, ladder is concave\n")
w("| rendering | metric | mask | pair | start | post | Δ [95% CI] | doublings [95% CI] | n [95% CI] | n, local slope [95% CI] | flags |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for k, v in OUT["pairs"].items():
    fmt, met, mk, _ = k.split("|")
    if mk not in ("content", "outcome"):
        continue
    pr = f"{v['post'].replace('Nemotron-Terminal', 'Nemo')} vs {v['start']}"
    if "n" in v:
        fl = []
        if v["b_crosses0"]: fl.append("b CI crosses 0")
        if v["npts"] == 2: fl.append("2-pt slope")
        w(f"| {fmt} | {met} | {mk} | {pr} | {v['start_val']:.4f} | {v['post_val']:.4f} | {v['delta']:+.4f} [{v['delta_ci'][0]:+.4f}, {v['delta_ci'][1]:+.4f}] | "
          f"{v['doublings']:+.2f} [{v['doublings_ci'][0]:+.2f}, {v['doublings_ci'][1]:+.2f}] | {v['n']:.2f} [{v['n_ci'][0]:.2f}, {v['n_ci'][1]:.2f}] | "
          + (f"{v['n_local']:.2f} [{v['n_local_ci'][0]:.2f}, {v['n_local_ci'][1]:.2f}] ({'/'.join(size_of(m) for m in v['local_ladder'])})" if 'n_local' in v else "–")
          + f" | {'; '.join(fl)} |")
    else:
        w(f"| {fmt} | {met} | {mk} | {pr} | {v['start_val']:.4f} | {v['post_val']:.4f} | {v['delta']:+.4f} [{v['delta_ci'][0]:+.4f}, {v['delta_ci'][1]:+.4f}] | – | – | – | no ladder for this metric |")
w("\n## Ladder values (point [95% CI])\n")
for k, v in OUT["ladder_values"].items():
    fmt, met, mk, ln = k.split("|")
    if mk in ("content", "outcome", "random", "random_novel", "hash_novel"):
        w(f"- {k}: " + "; ".join(f"{m} {x[0]:.4f} [{x[1]:.4f},{x[2]:.4f}]" for m, x in v.items()))
w("\n## Temperatures\n")
for f in INFO:
    w(f"- {f}: T_obs(cal, all obs tokens, 50 real cal trajs) = {INFO[f]['T_obs_cal']}")
    w(f"- {f}: T_cf(content; fold A / fold B / full-data) = {INFO[f].get('T_cf', {})}")
    w(f"- {f}: split-seed SD of cross-fit point estimates: T_cf {INFO[f].get('T_cf_split_sd', {})}; rankrecal {INFO[f].get('rr_split_sd', {})}")
open(f"{a.out}/tables.md", "w").write("\n".join(L) + "\n")
say("wrote", f"{a.out}/results.json", f"{a.out}/tables.md")
