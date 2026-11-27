"""Aggregate results/<model>.json -> results/summary.csv + findings tables (markdown to stdout)."""
import csv, glob, json, os, sys
import numpy as np

R = sys.argv[1] if len(sys.argv) > 1 else "results"
ORDER = ["Qwen3-0.6B-Base", "Qwen3-1.7B-Base", "Qwen3-4B-Base", "Qwen3-8B-Base", "Qwen3-14B-Base",
         "Qwen3-0.6B", "Qwen3-1.7B", "Qwen3-4B", "Qwen3-8B", "Qwen3-14B", "Qwen3-32B",
         "Nemotron-Terminal-8B", "Nemotron-Terminal-14B", "Nemotron-Terminal-32B"]
TB2 = {"Qwen3-8B": 2.47, "Qwen3-14B": 4.04, "Qwen3-32B": 3.37,
       "Nemotron-Terminal-8B": 13.0, "Nemotron-Terminal-14B": 20.2, "Nemotron-Terminal-32B": 27.4}
SUBS = ["all", "first16", "body", "novel", "copy"]
rng = np.random.default_rng(0)
B = 1000


def fam(n):
    return "base" if n.endswith("-Base") else ("nemotron" if n.startswith("Nemotron") else "instruct")


def size(n):
    return n.split("-")[-2] if n.endswith("-Base") else n.split("-")[-1]


def auroc(y, s):
    y, s = np.asarray(y), np.asarray(s)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    return float(((pos[:, None] > neg[None]).sum() + 0.5 * (pos[:, None] == neg[None]).sum()) / (len(pos) * len(neg)))


def load(name):
    return json.load(open(f"{R}/{name}.json"))


def traj_arrays(res, fmt, split="eval"):
    """per-trajectory arrays for bootstrap: dict metric -> (num array, den array)."""
    d = res[split][fmt]
    ids = sorted(d)
    out = {}
    for t in ["task", "thought", "action", "observation", "markup"]:
        out[f"bpb_{t}"] = (np.array([d[i][f"type/{t}"][0] for i in ids]), np.array([d[i][f"type/{t}"][1] for i in ids]))
    for s in SUBS:
        g = lambda k: np.array([d[i][f"obs/{s}"][k] for i in ids])
        out[f"obs_{s}_bpb"] = (g("bits"), g("bytes"))
        out[f"obs_{s}_capped"] = (g("capped"), g("n"))
        out[f"obs_{s}_prob"] = (g("prob"), g("n"))
        out[f"obs_{s}_spec"] = (g("spec"), g("n"))
        out[f"obs_{s}_hash"] = (g("hash"), g("n"))
        out[f"obs_{s}_think"] = (g("think"), g("n"))
        out[f"obs_{s}_imend"] = (g("im_end"), g("n"))
        out[f"obs_{s}_n"] = (g("n"), np.ones(len(ids)))
        out[f"obs_{s}_tgrid"] = (np.array([d[i][f"obs/{s}"]["tgrid"] for i in ids]), g("bytes"))
    out["nonobs_spec"] = (np.array([d[i]["nonobs_spec"][0] for i in ids]), np.array([d[i]["nonobs_spec"][1] for i in ids]))
    return ids, out


def ratio(nd, idx=None):
    n, d = nd
    if idx is not None:
        n, d = n[idx], d[idx]
    return float(n.sum() / d.sum())


def tfit(res, fmt):
    _, cal = traj_arrays(res, fmt, "cal")
    num, den = cal["obs_all_tgrid"]
    curve = num.sum(0) / den.sum()
    k = int(np.argmin(curve))
    return k, res["tgrid"][k]


def metrics(res, fmt):
    ids, a = traj_arrays(res, fmt)
    m = {}
    for t in ["task", "thought", "action", "observation", "markup"]:
        m[f"bpb_{t}"] = ratio(a[f"bpb_{t}"])
    for s in SUBS:
        for k in ["bpb", "capped", "prob", "spec", "hash", "think", "imend"]:
            m[f"obs_{s}_{k}"] = ratio(a[f"obs_{s}_{k}"])
    m["obs_copy_frac"] = a["obs_copy_n"][0].sum() / a["obs_all_n"][0].sum()
    m["nonobs_spec"] = ratio(a["nonobs_spec"])
    k, T = tfit(res, fmt)
    k1 = res["tgrid"].index(1.0)
    m["T_star"] = T
    for s in ["all", "novel"]:
        num, den = a[f"obs_{s}_tgrid"]
        m[f"obs_{s}_bpb_T1"] = float(num[:, k1].sum() / den.sum())
        m[f"obs_{s}_bpb_Tstar"] = float(num[:, k].sum() / den.sum())
    its = res["items"].get(fmt, [])
    if its:
        b = np.array([[x["bits"], x["bytes"], x["novel_bits"], x["novel_bytes"], x["capped"], x["n"]] for x in its])
        m["pred_bpb"] = b[:, 0].sum() / b[:, 1].sum()
        m["pred_novel_bpb"] = b[:, 2].sum() / b[:, 3].sum()
        m["pred_capped"] = b[:, 4].sum() / b[:, 5].sum()
        m["pred_spec0"] = float(np.mean([x["spec0"] for x in its]))
        ly = np.array([x["logp_yes"] for x in its]); ln_ = np.array([x["logp_no"] for x in its])
        p = 1 / (1 + np.exp(-(ly - ln_)))
        m["q_yesno_mass"] = float(np.mean(np.exp(ly) + np.exp(ln_)))
        for lab in ["label_new", "label_raw"]:
            y = np.array([x[lab] for x in its])
            m[f"q_auroc_{lab}"] = auroc(y, ly - ln_)
            m[f"q_brier_{lab}"] = float(np.mean((p - y) ** 2))
            m[f"q_acc_{lab}"] = float(np.mean((p > 0.5) == y))
        m["q_pyes_mean"] = float(p.mean())
        m["n_items"] = len(its)
    m["n_traj"] = len(ids)
    return m


def paired_ci(r1, r2, fmt, key, use_T=False):
    """bootstrap over trajectories: metric(r2) - metric(r1)."""
    ids1, a1 = traj_arrays(r1, fmt); ids2, a2 = traj_arrays(r2, fmt)
    assert ids1 == ids2
    if use_T:
        k1, _ = tfit(r1, fmt); k2, _ = tfit(r2, fmt)
        n1, d1 = a1[key]; n2, d2 = a2[key]
        f1 = lambda idx: n1[idx, k1].sum() / d1[idx].sum(); f2 = lambda idx: n2[idx, k2].sum() / d2[idx].sum()
    else:
        f1 = lambda idx: ratio(a1[key], idx); f2 = lambda idx: ratio(a2[key], idx)
    n = len(ids1); full = np.arange(n)
    diffs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        diffs.append(f2(idx) - f1(idx))
    return f2(full) - f1(full), np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)


def paired_item_ci(r1, r2, fmt, what):
    i1 = r1["items"][fmt]; i2 = r2["items"][fmt]
    assert [(x["traj"], x["msg"]) for x in i1] == [(x["traj"], x["msg"]) for x in i2]
    def f(its, idx):
        if what == "pred_novel":
            return sum(its[i]["novel_bits"] for i in idx) / sum(its[i]["novel_bytes"] for i in idx)
        y = np.array([its[i]["label_new"] for i in idx]); s = np.array([its[i]["logp_yes"] - its[i]["logp_no"] for i in idx])
        return auroc(y, s)
    n = len(i1); full = list(range(n)); diffs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        diffs.append(f(i2, idx) - f(i1, idx))
    return f(i2, full) - f(i1, full), np.nanpercentile(diffs, 2.5), np.nanpercentile(diffs, 97.5)


def main():
    names = [n for n in ORDER if os.path.exists(f"{R}/{n}.json")]
    res = {n: load(n) for n in names}
    rows = []
    for n in names:
        for fmt in ["neutral", "native"]:
            m = metrics(res[n], fmt)
            rows.append(dict(model=n, family=fam(n), size=size(n), fmt=fmt, tb2=TB2.get(n, ""),
                             gpu_s=round(res[n]["timing"]["total_s"]), **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}))
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(f"{R}/summary.csv", "w") as f:
        w = csv.DictWriter(f, keys, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    get = {(r["model"], r["fmt"]): r for r in rows}

    def table(title, cols, fmts=("neutral", "native"), models=names):
        print(f"\n### {title}\n")
        print("| model | fmt | " + " | ".join(c for c, _ in cols) + " |")
        print("|---|---|" + "---|" * len(cols))
        for n in models:
            for fmt in fmts:
                r = get.get((n, fmt))
                if r is None:
                    continue
                print(f"| {n} | {fmt} | " + " | ".join(f"{r.get(k, float('nan')):.3f}" if isinstance(r.get(k), float) else str(r.get(k, ""))
                                                    for _, k in cols) + " |")

    table("Teacher-forced BPB by span type (eval, 200 traj)",
          [("task", "bpb_task"), ("thought", "bpb_thought"), ("action", "bpb_action"), ("obs", "bpb_observation"), ("markup", "bpb_markup")])
    table("Observation breakdown",
          [("obs", "obs_all_bpb"), ("first16", "obs_first16_bpb"), ("body", "obs_body_bpb"), ("novel", "obs_novel_bpb"),
           ("copy", "obs_copy_bpb"), ("capped bits/tok", "obs_all_capped"), ("mean p", "obs_all_prob"), ("copy frac", "obs_copy_frac")])
    table("Role-switch mass at observation positions (mean prob per token)",
          [("special all", "obs_all_spec"), ("special first16", "obs_first16_spec"), ("special body", "obs_body_spec"),
           ("<think>", "obs_all_think"), ("<|im_end|>", "obs_all_imend"), ("'###' first16", "obs_first16_hash"),
           ("special @non-obs", "nonobs_spec")])
    table("Temperature scaling (T fit on 50 cal traj, obs tokens)",
          [("T*", "T_star"), ("obs T=1", "obs_all_bpb_T1"), ("obs T*", "obs_all_bpb_Tstar"), ("novel T=1", "obs_novel_bpb_T1"),
           ("novel T*", "obs_novel_bpb_Tstar")])
    table("Prompted prediction (assistant role) and Yes/No error question",
          [("pred bpb", "pred_bpb"), ("pred novel bpb", "pred_novel_bpb"), ("pred capped", "pred_capped"),
           ("AUROC new", "q_auroc_label_new"), ("Brier new", "q_brier_label_new"), ("acc new", "q_acc_label_new"),
           ("AUROC raw", "q_auroc_label_raw"), ("P(yes) mean", "q_pyes_mean"), ("Yes+No mass", "q_yesno_mass")])

    print("\n### Paired comparisons (Δ = second − first; 95% bootstrap CI over trajectories / items)\n")
    print("| comparison | fmt | Δ obs BPB | Δ novel obs BPB | Δ obs BPB @T* | Δ pred novel BPB | Δ AUROC(new) |")
    print("|---|---|---|---|---|---|---|")
    pairs = []
    for s in ["0.6B", "1.7B", "4B", "8B", "14B"]:
        pairs.append((f"Qwen3-{s}-Base", f"Qwen3-{s}"))
    for s in ["8B", "14B", "32B"]:
        pairs.append((f"Qwen3-{s}", f"Nemotron-Terminal-{s}"))
    for s in ["8B", "14B"]:
        pairs.append((f"Qwen3-{s}-Base", f"Nemotron-Terminal-{s}"))
    for a, b in pairs:
        if a not in res or b not in res:
            continue
        for fmt in ["neutral", "native"]:
            c = [paired_ci(res[a], res[b], fmt, "obs_all_bpb"), paired_ci(res[a], res[b], fmt, "obs_novel_bpb"),
                 paired_ci(res[a], res[b], fmt, "obs_all_tgrid", use_T=True),
                 paired_item_ci(res[a], res[b], fmt, "pred_novel"), paired_item_ci(res[a], res[b], fmt, "auroc")]
            print(f"| {a} → {b} | {fmt} | " + " | ".join(f"{d:+.3f} [{lo:+.3f},{hi:+.3f}]" for d, lo, hi in c) + " |")
    tot = sum(res[n]["timing"]["total_s"] for n in names)
    print(f"\nGPU time (scoring only): {tot/3600:.2f} h over {len(names)} models")


if __name__ == "__main__":
    main()
