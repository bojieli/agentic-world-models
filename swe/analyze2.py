"""CPU analysis of phase-2 measures M1-M4 from results/raw/<model>/<ds>_{m1.npz,br.pkl}.
usage: analyze2.py [--models a,b,...] [--B 1000]   -> results/summary.json, results/tables.md
"""
import argparse, collections, json, math, os, pickle, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2)
TGRID = [round(0.7 + 0.1 * i, 2) for i in range(19)]
CLS = ["ws", "boiler", "prompt", "cmd_echo", "rand_hash", "rand_time", "rand_misc", "err_line", "test_line",
       "number", "path", "other", "lineno"]
CI = {c: i for i, c in enumerate(CLS)}
CONTENT = [CI[c] for c in ["err_line", "test_line", "number", "path", "other", "lineno"]]
OUTCOME = [CI[c] for c in ["err_line", "test_line", "number"]]
EXEC = {"test_run", "python_exec", "shell_other"}
V = 151936
# rank buckets: 0, 1, [2,4), [4,8), ..., [1024, V)
RB_LO = [0, 1] + [2 ** k for k in range(1, 11)]
RB_HI = [1, 2] + [2 ** (k + 1) for k in range(1, 10)] + [V]
RB_W = np.log2(np.array(RB_HI) - np.array(RB_LO))
CB = np.array([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99, 1.0001])

GROUPS = {  # size -> role -> model
    "0.6B": {"base": "Qwen3-0.6B-Base", "instruct": "Qwen3-0.6B"},
    "1.7B": {"base": "Qwen3-1.7B-Base", "instruct": "Qwen3-1.7B"},
    "4B": {"base": "Qwen3-4B-Base", "instruct": "Qwen3-4B"},
    "8B": {"base": "Qwen3-8B-Base", "instruct": "Qwen3-8B", "nonagentic SFT+RL (Light-IF)": "Light-IF-8B",
           "nonagentic distill (Klear-SFT)": "Klear-Reasoner-8B-SFT", "agentic SFT (Nemotron-T)": "Nemotron-Terminal-8B",
           "agentic SFT (tmax-sft)": "tmax-sft-8b", "agentic RL (tmax)": "tmax-8b", "world model (WebWorld)": "WebWorld-8B"},
    "14B": {"base": "Qwen3-14B-Base", "instruct": "Qwen3-14B", "nonagentic SFT+RL (Light-IF)": "Light-IF-14B",
            "agentic SFT (Nemotron-T)": "Nemotron-Terminal-14B", "agentic RL (CodeScout)": "CodeScout-14B"},
    "32B": {"instruct": "Qwen3-32B", "agentic SFT (Nemotron-T)": "Nemotron-Terminal-32B",
            "agentic SFT (OpenThinkerAgent)": "OpenThinkerAgent-32B"},
}


def size_of(m):
    for s, g in GROUPS.items():
        if m in g.values():
            return s
    if m.startswith("lora") or m.startswith("ckpt"):
        return "8B"
    return None


# ---------------------------------------------------------------- stats helpers
class Boot:
    def __init__(self, n, B, idx, seed=0):
        """resample the trajectories in idx (eval split) with replacement; W[b, traj] = multiplicity"""
        r = np.random.default_rng(seed); idx = np.asarray(idx)
        self.W = np.stack([np.bincount(idx[r.integers(0, len(idx), len(idx))], minlength=n) for _ in range(B)]).astype(np.float64)

    def ratio(self, num, den):
        return (self.W @ num) / np.maximum(self.W @ den, 1e-12)

    def mean(self, x):
        return (self.W @ x) / self.W.sum(1)


def ci(a):
    a = np.asarray(a); a = a[np.isfinite(a)]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else [np.nan, np.nan]


def auroc(s, y, w=None):
    s, y = np.asarray(s, float), np.asarray(y).astype(bool)
    w = np.ones(len(s)) if w is None else np.asarray(w, float)
    if y.all() or (~y).all():
        return np.nan
    o = np.argsort(s, kind="mergesort"); s, y, w = s[o], y[o], w[o]
    # rank with ties
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    wn = np.bincount(inv, weights=w * ~y); wp = np.bincount(inv, weights=w * y)
    cum_n = np.cumsum(wn) - wn
    return float(((cum_n + 0.5 * wn) * wp).sum() / (wp.sum() * wn.sum()))


def logreg(X, y, l2=1.0, w=None, iters=50):
    X = np.asarray(X, float); y = np.asarray(y, float)
    w = np.ones(len(y)) if w is None else w
    b = np.zeros(X.shape[1])
    R = l2 * np.eye(X.shape[1]); R[0, 0] = 1e-6  # column 0 = intercept
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        g = X.T @ (w * (p - y)) + R @ b
        H = (X * (w * p * (1 - p))[:, None]).T @ X + R
        step = np.linalg.solve(H, g); b -= step
        if np.abs(step).max() < 1e-8:
            break
    return b


def sig(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


# ---------------------------------------------------------------- loading
_META = {}
SUB = {}  # ds -> set of trajectory indices kept (None = all); set by --subset


def insub(ds, ti):
    return SUB.get(ds) is None or ti in SUB[ds]


WORKDIR = os.environ.get("P2_WORK", os.path.join(HERE, "work"))
RAWDIR = os.environ.get("P2_RAW", os.path.join(HERE, "results", "raw"))


def meta(ds):
    if ds not in _META:
        p = os.path.join(WORKDIR, f"{ds}_meta.pkl")
        if not os.path.exists(p):
            W = pickle.load(open(os.path.join(WORKDIR, f"{ds}.pkl"), "rb"))
            pickle.dump(dict(m1=W["m1"], items=W["items"], trajs=W["trajs"]), open(p, "wb"), protocol=4)
        _META[ds] = pickle.load(open(p, "rb"))
        _META[ds]["ds"] = ds
    return _META[ds]


def loadm(model, ds):
    d = os.path.join(RAWDIR, model)
    if not os.path.exists(os.path.join(d, f"{ds}.done")):
        return None
    z = np.load(os.path.join(d, f"{ds}_m1.npz"))
    m1 = {k: z[k] for k in z.files}
    # map processed segments back onto the token metadata (subset runs score only some segments)
    sel = np.isin(meta(ds)["m1"]["seg"], m1["seg_ids"]) if "seg_ids" in m1 else np.ones(len(m1["lp"]), bool)
    assert sel.sum() == len(m1["lp"]), (model, ds, sel.sum(), len(m1["lp"]))
    act = os.path.join(d, f"{ds}_act.npz")
    return dict(m1=m1, sel=sel, br=pickle.load(open(os.path.join(d, f"{ds}_br.pkl"), "rb")),
                act=np.load(act)["lp"] if os.path.exists(act) else None)


# ---------------------------------------------------------------- M1
def m1_fit(R, M):
    """per-model recalibration fitted on the calibration split; returns per-token eval code lengths (bits)."""
    m = {k: v[R["sel"]] for k, v in M["m1"].items()}; z = R["m1"]
    cls, cp, split = m["cls"], m["copy"], m["split"]
    content = np.isin(cls, CONTENT) & (cp == 0)
    outcome = np.isin(cls, OUTCOME) & (cp == 0)
    cal, ev = split == "cal", split == "eval"
    bits = -z["lp"] / LN2
    bitsT = -z["lpT"].astype(np.float64) / LN2
    rank, top1, ent = z["rank"], z["top1"].astype(float), z["ent"].astype(float) / LN2
    rb = np.searchsorted(np.array(RB_LO), rank, side="right") - 1
    cb = np.clip(np.searchsorted(CB, top1, side="right") - 1, 0, len(CB) - 2)
    out = {}
    for sname, smask in [("content", content), ("outcome", outcome)]:
        c, e = smask & cal, smask & ev
        kT = int(np.argmin(bitsT[c].mean(0)))
        Q = np.full((len(CB) - 1, len(RB_LO)), 0.5)
        np.add.at(Q, (cb[c], rb[c]), 1)
        Q /= Q.sum(1, keepdims=True)
        hist = -np.log2(Q[cb, rb]) + RB_W[rb]
        out[sname] = dict(mask=e, T=TGRID[kT], kT=kT, bits=bits, bitsT=bitsT[:, kT], hist=hist,
                          top1hit=(rank == 0).astype(float), ent=ent)
    out["exec_content"] = dict(out["content"], mask=content & ev & np.isin(m["kind"], list(EXEC)))
    for k in ["test_run", "python_exec", "shell_other", "file_view", "search", "edit_ack"]:
        out[f"kind={k}"] = dict(out["content"], mask=content & ev & (m["kind"] == k))
    for c in ["err_line", "test_line", "number"]:
        out[f"cls={c}"] = dict(out["content"], mask=content & ev & (cls == CI[c]))
    out["traj"] = m["traj"]
    if SUB.get(M.get("ds")) is not None:
        keep = np.isin(m["traj"], list(SUB[M["ds"]]))
        for k in out:
            if k != "traj":
                out[k]["mask"] = out[k]["mask"] & keep
    return out


def m1_summary(F, ntraj, boot):
    res = {}
    for s in [k for k in F if k not in ("traj",)]:
        d = F[s]; e = d["mask"]
        if e.sum() == 0:
            continue
        tr = F["traj"][e]
        n = np.bincount(tr, minlength=ntraj).astype(float)
        r = dict(n_tok=int(e.sum()), T=d["T"])
        for k in ["bits", "bitsT", "hist", "top1hit", "ent"]:
            r[k] = float(d[k][e].mean())
        r["gap"] = r["bits"] - r["ent"]
        res[s] = r
        res[s]["_sums"] = {k: np.bincount(tr, weights=d[k][e], minlength=ntraj) for k in ["bits", "bitsT", "hist"]}
        res[s]["_n"] = n
    return res


# ---------------------------------------------------------------- M2
def m2_summary(R, M, kT, ntraj, boot):
    items = [it for it in M["items"]["m2"] if f"{it['key']}:true" in R["br"] and insub(M["ds"], it["traj"])]
    rows = []
    for it in items:
        c = it["content"].astype(bool); o = it["outcome"].astype(bool)
        r = {nm: R["br"][f"{it['key']}:{nm}"] for nm in ["true", "swapA", "swapB"]}
        for T, get in [("raw", lambda x: -x["lp"] / LN2), ("T", lambda x: -x["lpT"][:, kT].astype(float) / LN2)]:
            for sub, mk in [("content", c), ("outcome", o)]:
                v = {nm: float(get(r[nm])[mk].sum()) for nm in r}
                rows.append((it["traj"], T, sub, it["kind"], it["src"], v["true"], v["swapA"], v["swapB"], int(mk.sum())))
    res = {}
    for T in ["raw", "T"]:
        for sub in ["content", "outcome"]:
            for grp, f in [("all", lambda r: True), ("exec", lambda r: r[3] in EXEC), ("nonexec", lambda r: r[3] not in EXEC),
                           ("src=same", lambda r: r[4] == "same"), ("src=other", lambda r: r[4] == "other")] + \
                          [(f"kind={k}", (lambda k: lambda r: r[3] == k)(k)) for k in ["test_run", "python_exec", "shell_other", "file_view", "search", "edit_ack"]]:
                rr = [r for r in rows if r[1] == T and r[2] == sub and f(r) and r[8] > 0]
                if len(rr) < 5:
                    continue
                tr = np.array([r[0] for r in rr])
                t = np.bincount(tr, [r[5] for r in rr], ntraj); a = np.bincount(tr, [r[6] for r in rr], ntraj)
                b = np.bincount(tr, [r[7] for r in rr], ntraj); nt = np.bincount(tr, [r[8] for r in rr], ntraj)
                sw = (a + b) / 2
                g = 1 - boot.ratio(t, sw); ctl = boot.ratio(a - b, sw)
                res[f"{T}/{sub}/{grp}"] = dict(n_items=len(rr), n_tok=int(nt.sum()), gain=float(1 - t.sum() / sw.sum()), gain_ci=ci(g),
                                               control=float((a - b).sum() / sw.sum()), control_ci=ci(ctl),
                                               bits_true=float(t.sum() / nt.sum()), bits_swap=float(sw.sum() / nt.sum()),
                                               abs_gain=float((sw.sum() - t.sum()) / nt.sum()), abs_gain_ci=ci(boot.ratio(sw - t, nt)),
                                               _t=t, _sw=sw, _nt=nt)
    return res


# ---------------------------------------------------------------- reading test
def read_sums(R, M, ntraj):
    """per-trajectory sums of next-action bits with the observation hidden / shown, and token counts (eval items)."""
    if R.get("act") is None or not M["items"].get("read"):
        return None
    hid, sho, n = np.zeros(ntraj), np.zeros(ntraj), np.zeros(ntraj)
    kinds = {}
    for it in M["items"]["read"]:
        r = R["br"].get(f"{it['key']}:hidden")
        if r is None or not insub(M["ds"], it["traj"]):
            continue
        h = -r["lp"].sum() / LN2; s_ = -R["act"][it["act_off"]:it["act_off"] + it["n_act"]].sum() / LN2
        hid[it["traj"]] += h; sho[it["traj"]] += s_; n[it["traj"]] += it["n_act"]
        k = kinds.setdefault(it["kind"], [np.zeros(ntraj), np.zeros(ntraj), np.zeros(ntraj)])
        k[0][it["traj"]] += h; k[1][it["traj"]] += s_; k[2][it["traj"]] += it["n_act"]
    return dict(all=(hid, sho, n), **{f"kind={k}": tuple(v) for k, v in kinds.items()})


# ---------------------------------------------------------------- M3
def m3_scores(R, it, cond):
    r = R["br"].get(f"{it['key']}:{cond}")
    if r is None:
        return None
    return np.array([float(x.sum()) for x in r])


AF_REFS = {"af": "Qwen3-0.6B-Base", "af2": "Qwen3-1.7B-Base"}  # adversarial-filter references (excluded from M3 conclusions)
AF_MAX = 0.40                 # keep a 4-way item only if the reference's leak-context posterior on the truth <= this
_AF = {}


def af_keep(ds, it, ref):
    if (ds, ref) not in _AF:
        p = os.path.join(HERE, "results", "raw", ref, f"{ds}_br.pkl")
        _AF[(ds, ref)] = pickle.load(open(p, "rb")) if os.path.exists(p) else None
    r = _AF[(ds, ref)]
    if r is None or f"{it['key']}:leak" not in r:
        return None
    s = np.array([float(x.sum()) for x in r[f"{it['key']}:leak"]])
    p = np.exp(s - s.max()); p /= p.sum()
    return bool(p[0] <= AF_MAX)


def m3_summary(R, M, ntraj, boot, ds=None):
    """4-way items (err_class, number, pytest counts): accuracy, pairwise AUROC; binary items (first pytest status
    fail-vs-pass, printed bool False-vs-True, grep no-hit): AUROC of the model's log-odds and balanced accuracy at 0.
    Each in the full context and in the leak-check context (current action + preceding turn masked)."""
    rows = []
    for it in M["items"]["m3"]:
        if not insub(M["ds"], it["traj"]):
            continue
        for cond in ["full", "leak"]:
            s = m3_scores(R, it, cond)
            if s is None:
                continue
            t = it["type"]
            if t in ("grep", "bool", "pytest_first"):
                if t == "grep":
                    sc, y = s[0] - np.log1p(-min(np.exp(s[0]), 1 - 1e-9)), it["nohit"]
                else:
                    cands = [it["true"]] + list(it["foils"])
                    bad = [k for k, c in enumerate(cands) if c in ("FAILED", "ERROR", "F", "E", "False")]
                    good = [k for k, c in enumerate(cands) if c in ("PASSED", ".", "True")]
                    sc = np.logaddexp.reduce(s[bad]) - np.logaddexp.reduce(s[good])
                    y = int(it["true"] in ("FAILED", "ERROR", "F", "E", "False"))
                rows.append(dict(traj=it["traj"], cond=cond, type=t, err=y, score=float(sc), y=y, bin=True))
                continue
            mx = s.max(); win = np.isclose(s, mx)
            acc = float(win[0] / win.sum())
            pair = float(np.mean([(s[0] > x) + 0.5 * (s[0] == x) for x in s[1:]]))
            fl = {k: af_keep(ds, it, ref) for k, ref in AF_REFS.items()}
            fl["afboth"] = None if None in fl.values() else (fl["af"] and fl["af2"])
            rows.append(dict(traj=it["traj"], cond=cond, type=t, err=it["outcome_err"], acc=acc, pair=pair, n=len(s), bin=False,
                             kind=it["kind"], **fl))
    res = {}
    types4 = ["err_class", "number", "pytest"]
    for cond in ["full", "leak"]:
        for grp, f in [("4way", lambda r: r["type"] in types4)] + \
                      [("4way_" + a, (lambda a: lambda r: r["type"] in types4 and r[a])(a)) for a in ["af", "af2", "afboth"]] + \
                      [(t, (lambda t: lambda r: r["type"] == t)(t)) for t in types4] + \
                      [(t + "_af", (lambda t: lambda r: r["type"] == t and r["af"])(t)) for t in types4] + \
                      [("4way_kind=" + k, (lambda k: lambda r: r["type"] in types4 and r["kind"] == k)(k)) for k in ["test_run", "python_exec", "shell_other", "search"]] + \
                      [("4way_af_kind=" + k, (lambda k: lambda r: r["type"] in types4 and r["af"] and r["kind"] == k)(k)) for k in ["test_run", "python_exec", "shell_other", "search"]]:
            rr = [r for r in rows if r["cond"] == cond and f(r)]
            if not rr:
                continue
            tr = np.array([r["traj"] for r in rr]); acc = np.array([r["acc"] for r in rr]); err = np.array([r["err"] for r in rr])
            pr = np.array([r["pair"] for r in rr])
            wb = np.where(err == 1, 0.5 / max((err == 1).sum(), 1), 0.5 / max((err == 0).sum(), 1))
            if (err == 1).all() or (err == 0).all():
                wb = np.ones(len(rr)) / len(rr)
            nn = np.bincount(tr, None, ntraj).astype(float)
            res[f"{cond}/{grp}"] = dict(n=len(rr), n_err=int(err.sum()), chance=float(np.mean([1 / r["n"] for r in rr])),
                                        acc=float(acc.mean()), acc_bal=float((wb * acc).sum()),
                                        acc_ci=ci(boot.ratio(np.bincount(tr, acc, ntraj), nn)), auroc=float(pr.mean()),
                                        auroc_ci=ci(boot.ratio(np.bincount(tr, pr, ntraj), nn)),
                                        _acc=np.bincount(tr, acc, ntraj), _n=nn)
        for t in ["pytest_first", "bool", "grep"]:
            rr = [r for r in rows if r["cond"] == cond and r["type"] == t]
            if len(rr) < 10:
                continue
            sc = np.array([r["score"] for r in rr]); y = np.array([r["y"] for r in rr]); tr = np.array([r["traj"] for r in rr])
            au = auroc(sc, y)
            bs = []
            for w in boot.W[:300]:
                ww = w[tr]
                if ww.sum() > 0:
                    bs.append(auroc(sc, y, ww))
            pred = (sc > 0).astype(int)
            bal = 0.5 * ((pred[y == 1] == 1).mean() if (y == 1).any() else np.nan) + 0.5 * ((pred[y == 0] == 0).mean() if (y == 0).any() else np.nan)
            res[f"{cond}/{t}"] = dict(n=len(rr), n_pos=int(y.sum()), auroc=au, auroc_ci=ci(bs), acc_bal=float(bal), _sc=sc, _y=y, _tr=tr)
    full4 = [r for r in rows if r["cond"] == "full" and r["type"] in types4]
    if full4 and all(r["af"] is not None and r["af2"] is not None for r in full4):
        a = np.array([r["af"] for r in full4]); b = np.array([r["af2"] for r in full4])
        res["af_overlap"] = dict(n=len(full4), n_af=int(a.sum()), n_af2=int(b.sum()), n_both=int((a & b).sum()),
                                 jaccard=float((a & b).sum() / max((a | b).sum(), 1)))
    for grp in list(res):
        if grp.startswith("full/") and "leak/" + grp[5:] in res and "_acc" in res[grp]:
            f, l = res[grp], res["leak/" + grp[5:]]
            res["delta/" + grp[5:]] = dict(acc=f["acc"] - l["acc"],
                                           acc_ci=ci(boot.ratio(f["_acc"], f["_n"]) - boot.ratio(l["_acc"], l["_n"])))
    return res


# ---------------------------------------------------------------- M4
def feats(items, vocab):
    X = []
    for it in items:
        x = [1.0] + [float(it["kind"] == k) for k in vocab["kind"]] + [float(it["prog"] == p) for p in vocab["prog"]] + \
            [float(it["prev_error"] == v) for v in (-1, 1)]
        X.append(x)
    return np.array(X)


def m4_summary(R, M, ntraj, boot):
    items = [it for it in M["items"]["m4"] if insub(M["ds"], it["traj"])]
    cal = [it for it in items if it["split"] == "cal"]
    vocab = dict(kind=sorted({it["kind"] for it in cal}),
                 prog=[p for p, _ in collections.Counter(it["prog"] for it in cal).most_common(10)])
    res = {}
    for q, lab in [("succ", lambda it: 1 - it["error"]), ("test", lambda it: None if it["tests_pass"] is None else int(it["tests_pass"]))]:
        for var in ["n", "p"]:
            def get(split):
                out = []
                for it in items:
                    if it["split"] != split or lab(it) is None:
                        continue
                    r = R["br"].get(f"{it['key']}:{q}:{var}")
                    if r is None:
                        continue
                    out.append((it, lab(it), float(r[0] - r[1]), float(np.exp(r).sum())))
                return out
            C, E = get("cal"), get("eval")
            if len(E) < 20:
                continue
            cov = float(np.mean([e[3] >= 0.5 for e in E]))
            Cg = [c for c in C if c[3] >= 0.5]; Eg = [e for e in E if e[3] >= 0.5]
            d = dict(n_eval=len(E), coverage=cov, mass=float(np.mean([e[3] for e in E])),
                     base_rate=float(np.mean([e[1] for e in E])))
            if len(Eg) >= 20 and len(Cg) >= 10 and len({c[1] for c in Cg}) == 2:
                yc = np.array([c[1] for c in Cg]); ye = np.array([e[1] for e in Eg])
                sc = np.array([c[2] for c in Cg]); se = np.array([e[2] for e in Eg])
                ab = logreg(np.c_[np.ones(len(sc)), sc], yc, l2=1e-3)
                pm = sig(ab[0] + ab[1] * se)
                # baseline: logistic on command type / previous error / kind base rate, fit on ALL cal items
                Call = [c for c in C]
                bb = logreg(feats([c[0] for c in Call], vocab), np.array([c[1] for c in Call]), l2=1.0)
                pb = sig(feats([e[0] for e in Eg], vocab) @ bb)
                # stacked: baseline features + model logit
                Xs = np.c_[feats([c[0] for c in Cg], vocab), sc]
                bs = logreg(Xs, yc, l2=1.0)
                ps = sig(np.c_[feats([e[0] for e in Eg], vocab), se] @ bs)
                tr = np.array([e[0]["traj"] for e in Eg])
                bm, bbase, bst = (pm - ye) ** 2, (pb - ye) ** 2, (ps - ye) ** 2
                Sm, Sb, Ss = [np.bincount(tr, x, ntraj) for x in (bm, bbase, bst)]
                d.update(n_gated=len(Eg), auroc=auroc(se, ye), auroc_base=auroc(pb, ye), brier=float(bm.mean()),
                         brier_base=float(bbase.mean()), bss=float(1 - bm.sum() / bbase.sum()), bss_ci=ci(1 - boot.ratio(Sm, Sb)),
                         bss_stack=float(1 - bst.sum() / bbase.sum()), bss_stack_ci=ci(1 - boot.ratio(Ss, Sb)),
                         platt=[float(ab[0]), float(ab[1])])
            res[f"{q}:{var}"] = d
    # error class (6-way letters), error items only
    for var in ["n", "p"]:
        E, C = [], []
        for it in items:
            if not it.get("ecls"):
                continue
            r = R["br"].get(f"{it['key']}:cls:{var}")
            if r is None:
                continue
            (C if it["split"] == "cal" else E).append((it, "ABCDEF".index(it["ecls"]), r))
        if len(E) < 10:
            continue
        mass = np.array([np.exp(e[2]).sum() for e in E])
        g = mass >= 0.5
        maj = collections.Counter([c[1] for c in C] or [e[1] for e in E]).most_common(1)[0][0]
        y = np.array([e[1] for e in E]); pred = np.array([int(np.argmax(e[2])) for e in E])
        res[f"cls:{var}"] = dict(n_eval=len(E), coverage=float(g.mean()), acc_gated=float((pred[g] == y[g]).mean()) if g.any() else np.nan,
                                 acc_all=float((pred == y).mean()), acc_majority=float((y == maj).mean()),
                                 acc_majority_gated=float((y[g] == maj).mean()) if g.any() else np.nan)
    return res


# ---------------------------------------------------------------- driver
def strip(d):
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if not k.startswith("_")}
    if isinstance(d, (np.floating, np.integer)):
        return d.item()
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=None); ap.add_argument("--B", type=int, default=1000)
    ap.add_argument("--subset", default=None, help="json {ds: [traj ids]}: restrict every measure to these trajectories")
    ap.add_argument("--out", default="summary.json")
    a = ap.parse_args()
    raw = os.path.join(HERE, "results", "raw")
    models = a.models.split(",") if a.models else sorted(os.listdir(raw))
    S = {}
    pairs_out = {}
    for ds in ["tp", "swe"]:
        M = meta(ds); ntraj = len(M["trajs"])
        if a.subset:
            keep = set(json.load(open(a.subset))[ds])
            SUB[ds] = {i for i, t in enumerate(M["trajs"]) if t["id"] in keep}
        boot = Boot(ntraj, a.B, [i for i, t in enumerate(M["trajs"]) if t["split"] == "eval" and insub(ds, i)])
        S[ds] = {}
        keep = {}
        for mname in models:
            R = loadm(mname, ds)
            if R is None:
                continue
            F = m1_fit(R, M)
            m1 = m1_summary(F, ntraj, boot)
            m2 = m2_summary(R, M, F["content"]["kT"], ntraj, boot)
            m3 = m3_summary(R, M, ntraj, boot, ds)
            m4 = m4_summary(R, M, ntraj, boot)
            S[ds][mname] = dict(m1=m1, m2=m2, m3=m3, m4=m4)
            print(ds, mname, "done", flush=True)
        # paired comparisons vs size-matched base / instruct
        pairs_out[ds] = {}
        for mname in S[ds]:
            sz = size_of(mname)
            if not sz:
                continue
            for role in ["base", "instruct"]:
                ref = GROUPS[sz].get(role)
                if not ref or ref == mname or ref not in S[ds]:
                    continue
                pr = {}
                X, Y = S[ds][mname], S[ds][ref]
                for s in [k for k in X["m1"] if k in Y["m1"]]:
                    for k in ["bits", "bitsT", "hist"]:
                        x, y = X["m1"][s]["_sums"][k], Y["m1"][s]["_sums"][k]
                        lr = np.log2(boot.ratio(x, y))
                        pr[f"m1/{s}/{k}"] = dict(log2ratio=float(np.log2(x.sum() / y.sum())), ci=ci(lr))
                for k in [k for k in X["m2"] if k in Y["m2"] and (k.startswith("raw/") or k.startswith("T/content/all"))]:
                    if k in X["m2"] and k in Y["m2"]:
                        gx = 1 - boot.ratio(X["m2"][k]["_t"], X["m2"][k]["_sw"]); gy = 1 - boot.ratio(Y["m2"][k]["_t"], Y["m2"][k]["_sw"])
                        pr[f"m2/{k}"] = dict(diff=X["m2"][k]["gain"] - Y["m2"][k]["gain"], ci=ci(gx - gy))
                for g in ["4way", "4way_af", "4way_af2", "4way_afboth", "err_class", "number", "err_class_af", "number_af"] + \
                         [f"4way{a}_kind={k}" for a in ["", "_af"] for k in ["test_run", "python_exec", "shell_other", "search"]]:
                    f, l = f"full/{g}", f"leak/{g}"
                    if f in X["m3"] and f in Y["m3"]:
                        bx = lambda Z, k: boot.ratio(Z["m3"][k]["_acc"], Z["m3"][k]["_n"])
                        pr[f"m3/full/{g}"] = dict(diff=X["m3"][f]["acc"] - Y["m3"][f]["acc"], ci=ci(bx(X, f) - bx(Y, f)))
                        if l in X["m3"] and l in Y["m3"]:
                            dd = (bx(X, f) - bx(X, l)) - (bx(Y, f) - bx(Y, l))
                            pr[f"m3/delta/{g}"] = dict(diff=(X["m3"][f]["acc"] - X["m3"][l]["acc"]) - (Y["m3"][f]["acc"] - Y["m3"][l]["acc"]), ci=ci(dd))
                pairs_out[ds][f"{mname} vs {ref}"] = pr
    json.dump(dict(models=strip(S), pairs=pairs_out), open(os.path.join(HERE, "results", a.out), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("wrote results/" + a.out)


if __name__ == "__main__":
    main()
