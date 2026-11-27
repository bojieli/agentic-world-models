"""Size-equivalent multipliers on the counterfactual benchmark.

PRIMARY (plan revision; matches phase-2's SWE numbers): inverse interpolation on the ladder.  Ladder points
(x_k, y_k), x_k = log2(non-embedding params), y_k = metric of Qwen3-<k> (instruct ladder for instruct starts);
y is made monotone by a running max (isotonic per bootstrap draw); x* = piecewise-linear inverse of that curve at
the post-trained model's metric y_m; log2 n = x* - x_start; censored to [x_min - x_start, x_max - x_start].
SENSITIVITY: global OLS y = a + b*x over the ladder, log2 n = (y_m - y_start) / b, same censoring.
Second reference (b): paired delta vs the same-size base model (no n; the base ladder is flat above 4B).
95% CIs from ONE joint cluster bootstrap over generated environments that drives every model (2000 draws).

Input = results/<NAME>/<render>/per_item.jsonl from score2x2.py (item ids aligned across models).  The loader
`per_item_specs()` returns {metric: (kind, num, den)} arrays over items, the same (kind, a, b) spec format that
swe/size_equiv.py's value() consumes ("ratio": sum(num)/sum(den); "gain": 1 - sum(t)/sum(sw)).

usage: size_equiv_cf.py [--render plain] [--mask nocopy] [--temp T1] [--B 1000]
"""
import argparse, collections, json, os, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(os.path.dirname(HERE), "swe")
PARAMS = {k: v["non_embedding"] for k, v in json.load(open(os.path.join(P2, "configs", "params.json"))).items()}
BASE = {s: f"Qwen3-{s}-Base" for s in ["0.6B", "1.7B", "4B", "8B", "14B"]}
INST = {s: f"Qwen3-{s}" for s in ["0.6B", "1.7B", "4B", "8B", "14B", "32B"]}
POST = {"Nemotron-Terminal-8B": ("Qwen3-8B", "inst"), "Nemotron-Terminal-14B": ("Qwen3-14B", "inst"),
        "Nemotron-Terminal-32B": ("Qwen3-32B", "inst"), "tmax-sft-8b": ("Qwen3-8B", "inst"),
        "tmax-8b": ("Qwen3-8B", "inst"), "tmax-8b|vs tmax-sft": ("tmax-sft-8b", "inst"),
        "CodeScout-14B": ("Qwen3-14B", "inst"), "Light-IF-8B": ("Qwen3-8B", "inst"), "Light-IF-14B": ("Qwen3-14B", "inst"),
        "Klear-Reasoner-8B-SFT": ("Qwen3-8B-Base", "base"), "WebWorld-8B": ("Qwen3-8B", "inst"),
        "WebWorld-8B|vs Base": ("Qwen3-8B-Base", "base"), "SERA-8B": ("Qwen3-8B", "inst"),
        "Arctic-AWM-8B": ("Qwen3-8B", "inst"), "FrogMini-14B-2510": ("Qwen3-14B", "inst"),
        "OpenThinkerAgent-32B": ("Qwen3-32B", "inst"), "Klear-Reasoner-8B-SFT|vs instruct": ("Qwen3-8B", "inst")}
for s in ["0.6B", "1.7B", "4B", "8B", "14B"]:
    POST[f"Qwen3-{s}|instruct vs base"] = (f"Qwen3-{s}-Base", "base")
STRATA = {"primary": ("S2", "S3", "S2h", "S3h"), "S2+S3": ("S2", "S3"), "S2h+S3h": ("S2h", "S3h"),
          **{s: (s,) for s in ["S1", "S2", "S3", "S4", "S2h", "S3h"]}}


def per_item_specs(name, render, mask, temp, ids, results):
    p = os.path.join(results, name, render, "per_item.jsonl")
    if not os.path.exists(p):
        return None
    R = {r["id"]: r for r in map(json.loads, open(p))}
    if not set(ids) <= set(R):
        return None
    k = f"{temp}/{mask}"
    out = {}
    for sname, sts in STRATA.items():
        w = np.array([R[i]["stratum"] in sts for i in ids], dtype=float)
        if not w.any():
            continue
        g = lambda f: np.array([R[i][k][f] for i in ids]) * w
        out[f"binding acc/{sname}"] = ("ratio", g("bind"), w)
        out[f"interaction bits/byte/{sname}"] = ("ratio", g("I_bits"), g("bytes"))
        out[f"info gain/{sname}"] = ("gain", g("ig_t"), g("ig_sw"))
        out[f"null binding/{sname}"] = ("ratio", g("null_bind"), w)
    return out


def value(spec, W=None):
    kind, a, b = spec
    S = (lambda x: x.sum()) if W is None else (lambda x: W @ x)
    if kind == "ratio":
        return S(a) / np.maximum(S(b), 1e-12)
    return 1 - S(a) / np.maximum(S(b), 1e-12)


def ci(x):
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", default="plain"); ap.add_argument("--mask", default="nocopy")
    ap.add_argument("--temp", default="T1"); ap.add_argument("--B", type=int, default=1000)
    ap.add_argument("--results", default=os.path.join(HERE, "results"))
    ap.add_argument("--items", default="items.jsonl.gz", help="comma-separated item files the results cover")
    ap.add_argument("--metrics", default=None, help="regex: only metrics matching (e.g. 'primary')")
    ap.add_argument("--out", default=os.path.join(HERE, "results", "size_equiv"))
    a = ap.parse_args()
    import gzip
    items = [json.loads(l) for f in a.items.split(",") for l in gzip.open(os.path.join(HERE, f), "rt")]
    ids = [x["id"] for x in items]
    env = [x["env_id"] for x in items]
    groups = collections.defaultdict(list)
    for k, e in enumerate(env):
        groups[e].append(k)
    groups = list(groups.values())
    rng = np.random.default_rng(0)
    W = np.zeros((a.B, len(ids)))
    for b in range(a.B):
        for g in rng.integers(0, len(groups), len(groups)):
            W[b, groups[g]] += 1
    names = set(BASE.values()) | set(INST.values()) | {k.split("|")[0] for k in POST} | {v[0] for v in POST.values()}
    D = {m: per_item_specs(m, a.render, a.mask, a.temp, ids, a.results) for m in sorted(names)}
    D = {m: v for m, v in D.items() if v}
    res = {}
    for met in sorted({k for v in D.values() for k in v}):
        if a.metrics and not re.search(a.metrics, met):
            continue
        r = dict(fits={}, models={}); bd = {}; curve = {}
        for lad, Lm in [("base", BASE), ("inst", INST)]:
            pts = [(s, m) for s, m in Lm.items() if m in D]
            if len(pts) < 3:
                continue
            x = np.log2([PARAMS[s] for s, _ in pts]); X = np.c_[np.ones(len(x)), x]
            y = np.array([value(D[m][met]) for _, m in pts])
            yb = np.stack([value(D[m][met], W) for _, m in pts], 1)
            c = np.linalg.lstsq(X, y, rcond=None)[0]; cb = np.linalg.lstsq(X, yb.T, rcond=None)[0]
            r["fits"][lad] = dict(points={s: float(v) for (s, _), v in zip(pts, y)}, a=float(c[0]), b=float(c[1]), b_ci=ci(cb[1]))
            bd[lad] = cb[1]
            curve[lad] = (x, y, yb)
        for pm, (start, lad) in POST.items():
            m = pm.split("|")[0]
            if m not in D or start not in D or lad not in r["fits"]:
                continue
            d = value(D[m][met]) - value(D[start][met]); db = value(D[m][met], W) - value(D[start][met], W)
            b = r["fits"][lad]["b"]
            # censoring: the implied size start*n must lie inside the fitted ladder's range [smallest, largest]
            xs = np.log2([PARAMS[s] for s in r["fits"][lad]["points"]])
            x0 = np.log2(PARAMS[re.search(r"(\d+(?:\.\d+)?)[Bb]", start).group(1) + "B"])
            lo, hi = xs.min() - x0, xs.max() - x0
            raw = d / b; l2d = db / bd[lad]
            cens = "" if lo <= raw <= hi else (">" if raw > hi else "<")
            l2 = float(np.clip(raw, lo, hi)); l2d = np.clip(l2d, lo, hi)
            # sensitivity: local piecewise-linear interpolation of the ladder curve (isotonic-ised) at the model's value
            cx, cy, cyb = curve[lad]
            ym, ymb = value(D[m][met]), value(D[m][met], W)
            def inv(yv, ys):
                ys = np.maximum.accumulate(ys)
                return float(np.interp(np.clip(yv, ys[0], ys[-1]), ys, cx)), (yv < ys[0]) or (yv > ys[-1])
            xi, ci_cens = inv(ym, cy)
            xib = np.array([inv(ymb[k], cyb[k])[0] for k in range(len(ymb))])
            cens_b = np.mean([inv(ymb[k], cyb[k])[1] for k in range(len(ymb))])
            loc = dict(log2n=xi - x0, log2n_ci=ci(xib - x0), censored=("" if not ci_cens else (">" if ym > cy.max() else "<")),
                       cens_frac=float(cens_b))
            r["models"][pm] = dict(start=start, ladder=lad, delta=float(d), delta_ci=ci(db), log2n=l2, log2n_raw=float(raw), local=loc,
                                   log2n_ci=ci(l2d), censored=cens, cens_frac=float(np.mean((db / bd[lad] < lo) | (db / bd[lad] > hi))),
                                   range=[float(lo), float(hi)], n=float(2 ** l2), n_ci=ci(2 ** l2d),
                                   slope_ok=bool(r["fits"][lad]["b_ci"][0] > 0))
        # (b) second reference: the same-size BASE model (no n: the base ladder is flat above 4B, so only the paired delta)
        r["vs_base"] = {}
        for pm, (start, lad) in POST.items():
            m = pm.split("|")[0]
            if "|" in pm or m not in D:
                continue
            size = re.search(r"(\d+(?:\.\d+)?)[Bb]", start).group(1) + "B"
            base = f"Qwen3-{size}-Base"
            if base not in D or met not in D[base]:
                r["vs_base"][m] = dict(base=base, available=False)
                continue
            d = value(D[m][met]) - value(D[base][met]); db = value(D[m][met], W) - value(D[base][met], W)
            lo_, hi_ = ci(db)
            r["vs_base"][m] = dict(base=base, available=True, delta=float(d), delta_ci=[lo_, hi_],
                                   verdict="above base" if lo_ > 0 else "below base" if hi_ < 0 else "n.s.")
        res[met] = r
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.render}_{a.mask}_{a.temp}"
    json.dump(res, open(os.path.join(a.out, f"size_equiv_{tag}.json"), "w"), indent=1)
    L = [f"# Size-equivalent multipliers, counterfactual benchmark ({tag}; joint env-cluster bootstrap)\n",
         "| metric | ladder | b [95% CI] | points |", "|---|---|---|---|"]
    for met, r in res.items():
        for lad, f in r["fits"].items():
            L.append(f"| {met} | {lad} | {f['b']:+.4f} [{f['b_ci'][0]:+.4f},{f['b_ci'][1]:+.4f}] | "
                     + ", ".join(f"{s}: {v:.3f}" for s, v in f["points"].items()) + " |")
    L += ["", "log2 n is censored to the ladder range (start size .. ladder end); '>'/'<' = point estimate censored; "
          "cens = share of bootstrap draws censored; slope? = ladder slope CI excludes 0.", "",
          "| metric | model | start (ladder) | Δ [95% CI] | log2 n [95% CI] | n [95% CI] | cens | slope? |", "|---|---|---|---|---|---|---|---|"]
    for met, r in res.items():
        for pm, v in r["models"].items():
            L.append(f"| {met} | {pm} | {v['start']} ({v['ladder']}) | {v['delta']:+.4f} [{v['delta_ci'][0]:+.4f},{v['delta_ci'][1]:+.4f}] | "
                     f"{v['censored']}{v['log2n']:+.2f} [{v['log2n_ci'][0]:+.2f},{v['log2n_ci'][1]:+.2f}] | "
                     f"{v['censored']}{v['n']:.2f} [{v['n_ci'][0]:.2f},{v['n_ci'][1]:.2f}] | {v['cens_frac']:.2f} | {'yes' if v['slope_ok'] else 'NO'} |")
    L += ["", "## Forest table: each post-trained model against (a) its own start (size multiplier) and (b) the same-size base", ""]
    for met, r in res.items():
        L += [f"### {met}", "", "| model | start | Δ vs start [95% CI] | (a) log2 n, ladder interpolation [95% CI] | n [95% CI] | sensitivity: log2 n, global OLS [95% CI] | n (OLS) | same-size base | (b) Δ vs base [95% CI] | vs base |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for pm, v in r["models"].items():
            if "|" in pm and not pm.endswith(("vs tmax-sft", "vs instruct")):
                continue
            m = pm.split("|")[0]; vb = r["vs_base"].get(m, {}) if "|" not in pm else {}
            bcol = (f"{vb['base']} | {vb['delta']:+.4f} [{vb['delta_ci'][0]:+.4f},{vb['delta_ci'][1]:+.4f}] | {vb['verdict']}"
                    if vb.get("available") else (f"{vb.get('base', '-')} | n/a | n/a" if vb else "- | - | -"))
            lc = v["local"]
            ncol = (f"{lc['censored']}{lc['log2n']:+.2f} [{lc['log2n_ci'][0]:+.2f},{lc['log2n_ci'][1]:+.2f}] | {lc['censored']}{2 ** lc['log2n']:.2f} [{2 ** lc['log2n_ci'][0]:.2f},{2 ** lc['log2n_ci'][1]:.2f}] | "
                    f"{v['censored']}{v['log2n']:+.2f} [{v['log2n_ci'][0]:+.2f},{v['log2n_ci'][1]:+.2f}] | {v['censored']}{v['n']:.2f}"
                    if v["ladder"] == "inst" else "not computed (base ladder flat above 4B) | - | - | -")
            L.append(f"| {pm} | {v['start']} ({v['ladder']}) | {v['delta']:+.4f} [{v['delta_ci'][0]:+.4f},{v['delta_ci'][1]:+.4f}] | {ncol} | {bcol} |")
        L.append("")
    open(os.path.join(a.out, f"size_equiv_{tag}.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
