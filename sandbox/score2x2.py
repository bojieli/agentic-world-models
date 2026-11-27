"""Teacher-forced 2x2 counterfactual scorer (no generation).

For item i with contexts c=(h,a), c'=(h,a') and real outputs o, o' (and null-partner outputs q, q' taken from another
item of the same family), 8 sequences are scored: {c, c'} x {o, o', q, q'}.  For each, the summed log-prob of the
scored output tokens is kept for 3 copy masks x a temperature grid, so every metric below can be recomputed offline.

  interaction  I = [lp(o|c) + lp(o'|c')] - [lp(o'|c) + lp(o|c')]       (bits; / (B_o + B_o') -> bits per byte)
  binding      1[I > 0]  (0.5 on exact ties), chance 0.5
  info gain    IG_o = (NLL(o|c') - NLL(o|c)) / NLL(o|c'),  item IG = mean over o and o'
  null         the same with (q, q') in place of (o, o'): contexts paired with outputs they did not produce

Scored tokens: every token overlapping the byte span of OUTPUT + terminator (render.py), minus tokens touching a
copied word (copymask.py) for masks nocopy/strict.  Byte denominators are dependent on the mask but tokenizer-independent.
Offsets come from the fast tokenizer's offset mapping, so any HF tokenizer works.

usage: score2x2.py MODEL_DIR NAME [--render plain|chat|plain,chat] [--strata S2,S3] [--tok-budget 24000]
output: results/NAME/<render>/{lp.npz, per_item.jsonl, summary.json, summary.md}
"""
import argparse, collections, gzip, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render, copymask

LN2 = math.log(2)
MASKS = ["all", "nocopy", "strict"]
TEMPS = [round(0.5 + 0.1 * i, 1) for i in range(26)]          # 0.5 .. 3.0
T1 = TEMPS.index(1.0)
POOLS = {"S2+S3": ("S2", "S3"), "S2h+S3h": ("S2h", "S3h"), "primary": ("S2", "S3", "S2h", "S3h")}


def in_group(stratum, g):
    return stratum == g or stratum in POOLS.get(g, ())


def load_items(path, strata=None):
    with gzip.open(path, "rt") as f:
        items = [json.loads(l) for l in f]
    if strata:
        items = [x for x in items if x["stratum"] in strata]
    return items


def b2c(text, b):
    return len(text.encode("utf-8")[:b].decode("utf-8", "ignore"))


def build_sequences(items, tok, rend):
    """one record per (item, ctx, out): text, scored char span, masked char ranges per mask, denominators."""
    by_id = {x["id"]: x for x in items}
    seqs, dens = [], np.zeros((len(items), 4, len(MASKS)))
    for ii, it in enumerate(items):
        P = it["prefix"]
        j = by_id.get(it.get("null_partner"))
        outs = list(it["output"]) + (list(j["output"]) if j else list(it["output"]))
        ctxw_real = copymask.context_words(*P)
        ctxw_null = copymask.context_words(*P, *(j["prefix"] if j else []))
        for oi, o in enumerate(outs):
            words = ctxw_real if oi < 2 else ctxw_null
            mranges = {m: copymask.copy_ranges(o, words, m) for m in MASKS}
            for mi, m in enumerate(MASKS):
                dens[ii, oi, mi] = render.norm_bytes(o) - copymask.masked_bytes(o, mranges[m])
            for ci in range(2):
                if rend == "plain":
                    text, span = render.compose(P[ci], o)
                else:
                    text, span = render.compose_chat(tok, P[ci], o)
                c0, c1 = b2c(text, span[0]), b2c(text, span[1])
                mch = {m: [(b2c(text, span[0] + s), b2c(text, span[0] + e)) for s, e in mranges[m]] for m in MASKS}
                seqs.append(dict(item=ii, ci=ci, oi=oi, text=text, span=(c0, c1), mask=mch))
    return seqs, dens


def encode(tok, s, rend):
    e = tok(s["text"], add_special_tokens=False, return_offsets_mapping=True)
    ids, offs = list(e["input_ids"]), [tuple(x) for x in e["offset_mapping"]]
    if rend == "plain" and tok.bos_token_id is not None and getattr(tok, "add_bos_token", False):
        ids, offs = [tok.bos_token_id] + ids, [(0, 0)] + offs
    c0, c1 = s["span"]
    sel, flags = [], []
    for k, (a, b) in enumerate(offs):
        if b <= a or k == 0 or not (b > c0 and a < c1):
            continue
        sel.append(k)
        flags.append([all(not (b > ms and a < me) for ms, me in s["mask"][m]) for m in MASKS])
    s["ids"], s["sel"], s["flags"] = ids, sel, np.array(flags, dtype=bool).reshape(-1, len(MASKS))
    s["straddle"] = int(bool(sel) and offs[sel[0]][0] < c0)
    return s


def run(model, seqs, tok_budget, device):
    import torch
    order = sorted(range(len(seqs)), key=lambda i: -len(seqs[i]["ids"]))
    base = getattr(model, model.base_model_prefix)
    head = model.get_output_embeddings()
    temps = torch.tensor(TEMPS, device=device, dtype=torch.float32)
    LP = {}
    i, t0, ntok = 0, time.time(), 0
    while i < len(order):
        L = len(seqs[order[i]]["ids"])
        bs = max(1, tok_budget // L)
        batch = [seqs[k] for k in order[i:i + bs]]
        i += bs
        ids = torch.full((len(batch), L), 0, dtype=torch.long)
        att = torch.zeros((len(batch), L), dtype=torch.long)
        for r, s in enumerate(batch):
            ids[r, :len(s["ids"])] = torch.tensor(s["ids"]); att[r, :len(s["ids"])] = 1
        ntok += int(att.sum())
        with torch.no_grad():
            h = base(input_ids=ids.to(device), attention_mask=att.to(device)).last_hidden_state
            rows = [(r, k) for r, s in enumerate(batch) for k in s["sel"]]
            if not rows:
                for s in batch:
                    LP[id(s)] = np.zeros((len(MASKS), len(TEMPS)))
                continue
            rr = torch.tensor([r for r, _ in rows], device=device)
            kk = torch.tensor([k for _, k in rows], device=device)
            y = ids.to(device)[rr, kk]
            lp = []
            for c in range(0, len(rows), 1024):                              # chunk rows: logits are rows x vocab
                z = head(h[rr[c:c + 1024], kk[c:c + 1024] - 1]).float()      # logits predicting token k
                zy = z.gather(1, y[c:c + 1024, None])[:, 0]
                lp.append(torch.stack([zy / T - torch.logsumexp(z / T, 1) for T in TEMPS], 1))
            lp = torch.cat(lp).cpu().numpy()                                 # rows x T
        p = 0
        for s in batch:
            n = len(s["sel"])
            part = lp[p:p + n]; p += n
            LP[id(s)] = (s["flags"].T.astype(np.float64) @ part) if n else np.zeros((len(MASKS), len(TEMPS)))
        if (i // max(bs, 1)) % 20 == 0:
            print(f"  {i}/{len(order)} seqs, {ntok / (time.time() - t0):.0f} tok/s", file=sys.stderr, flush=True)
    return LP


def item_metrics(lp, den):
    """lp: [2 ctx, 4 out] nats at one (mask, T); den: [4] bytes.  Returns dict of per-item metrics."""
    def block(o0, o1):
        aa, ab, ba, bb = lp[0, o0], lp[0, o1], lp[1, o0], lp[1, o1]
        I = (aa + bb - ab - ba) / LN2
        nll_t = -(aa + bb) / LN2; nll_cf = -(ba + ab) / LN2               # true vs counterfactual context, bits
        ig_o = ((-ba) - (-aa)) / (-ba) if ba < 0 else 0.0
        ig_p = ((-ab) - (-bb)) / (-ab) if ab < 0 else 0.0
        B = den[o0] + den[o1]
        return dict(I_bits=I, I_bpb=I / B if B else 0.0, bind=1.0 if I > 0 else 0.5 if I == 0 else 0.0,
                    IG=(ig_o + ig_p) / 2, ig_t=nll_t, ig_sw=nll_cf, gain_bpb=(nll_cf - nll_t) / B if B else 0.0, bytes=B)
    real, null = block(0, 1), block(2, 3)
    return {**real, **{"null_" + k: v for k, v in null.items()}}


def cluster_boot(values_by_item, clusters, B=2000, seed=0, stat=np.mean):
    rng = np.random.default_rng(seed)
    cl = sorted(set(clusters))
    idx = collections.defaultdict(list)
    for i, c in enumerate(clusters):
        idx[c].append(i)
    groups = [np.array(idx[c]) for c in cl]
    v = np.asarray(values_by_item, dtype=float)
    draws = []
    for _ in range(B):
        pick = rng.integers(0, len(groups), len(groups))
        sel = np.concatenate([groups[p] for p in pick])
        draws.append(stat(v[sel]))
    return [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]


def summarize(items, LP, dens, Tstar, B=2000):
    present = sorted({x["stratum"] for x in items})
    strata = present + [p for p, m in POOLS.items() if sum(x in present for x in m) >= 2]
    out = {}
    for tname, ti in [("T=1", T1), (f"T*={TEMPS[Tstar]}", Tstar)]:
        for mi, m in enumerate(MASKS):
            M = [item_metrics(LP[ii, :, :, mi, ti], dens[ii, :, mi]) for ii in range(len(items))]
            for st in strata:
                sel = [i for i, x in enumerate(items) if in_group(x["stratum"], st)]
                if not sel:
                    continue
                cl = [items[i]["env_id"] for i in sel]
                r = {"n": len(sel)}
                for k in ["bind", "I_bpb", "I_bits", "IG", "gain_bpb", "null_bind", "null_I_bpb", "null_IG"]:
                    v = [M[i][k] for i in sel]
                    r[k] = float(np.mean(v)); r[k + "_ci"] = cluster_boot(v, cl, B)
                out.setdefault(tname, {}).setdefault(m, {})[st] = r
    return out


def fmt_md(name, rend, S, extra):
    L = [f"# {name} ({rend})\n", extra, ""]
    for tname, bym in S.items():
        for m, bys in bym.items():
            L.append(f"\n## {tname}, mask={m}\n")
            L.append("| stratum | n | binding acc [95% CI] | interaction bits/byte [CI] | info gain [CI] | null binding | null interaction bpb [CI] |")
            L.append("|---|---|---|---|---|---|---|")
            for st, r in bys.items():
                c = lambda k: f"{r[k]:.3f} [{r[k + '_ci'][0]:.3f},{r[k + '_ci'][1]:.3f}]"
                L.append(f"| {st} | {r['n']} | {c('bind')} | {c('I_bpb')} | {c('IG')} | {c('null_bind')} | {c('null_I_bpb')} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("name")
    ap.add_argument("--items", default=os.path.join(HERE, "items.jsonl.gz"))
    ap.add_argument("--render", default="plain")
    ap.add_argument("--strata", default=None)
    ap.add_argument("--tok-budget", type=int, default=24000)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    items = load_items(a.items, a.strata.split(",") if a.strata else None)
    if a.limit:
        keep = {x["id"] for x in items[:a.limit]}
        items = [x for x in items if x["id"] in keep]
    tok = AutoTokenizer.from_pretrained(a.model)
    assert tok.is_fast, "offset mapping needs a fast tokenizer"
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16, device_map="cuda")
    model.eval()
    for rend in a.render.split(","):
        if rend == "chat" and not tok.chat_template:
            print(f"[score] {a.name}: no chat template, skipping chat", file=sys.stderr); continue
        try:
            seqs, dens = build_sequences(items, tok, rend)
        except Exception as e:                                             # e.g. a chat template that rewrites content
            print(f"[score] {a.name}: {rend} rendering failed ({e}); skipped", file=sys.stderr); continue
        for s in seqs:
            encode(tok, s, rend)
        print(f"[score] {a.name} {rend}: {len(items)} items, {len(seqs)} seqs, max len {max(len(s['ids']) for s in seqs)}",
              file=sys.stderr, flush=True)
        LPd = run(model, seqs, a.tok_budget, "cuda")
        LP = np.zeros((len(items), 2, 4, len(MASKS), len(TEMPS)))
        ntok = np.zeros((len(items), 2, 4, len(MASKS)), dtype=np.int32)
        for s in seqs:
            LP[s["item"], s["ci"], s["oi"]] = LPd[id(s)]
            ntok[s["item"], s["ci"], s["oi"]] = s["flags"].sum(0) if len(s["sel"]) else 0
        # per-model temperature: minimise NLL of the true outputs in their own contexts (mask all, S1..S4 pooled)
        nll_T = -(LP[:, 0, 0, 0, :] + LP[:, 1, 1, 0, :]).sum(0)
        Tstar = int(np.argmin(nll_T))
        od = os.path.join(a.out, a.name, rend)
        os.makedirs(od, exist_ok=True)
        np.savez_compressed(os.path.join(od, "lp.npz"), lp=LP, den=dens, ntok=ntok, temps=np.array(TEMPS),
                            masks=np.array(MASKS), ids=np.array([x["id"] for x in items]))
        with open(os.path.join(od, "per_item.jsonl"), "w") as f:
            for ii, it in enumerate(items):
                rec = dict(id=it["id"], stratum=it["stratum"], family=it["family"], env_id=it["env_id"],
                           pair_type=it["pair_type"], straddle=int(any(s["straddle"] for s in seqs[ii * 8:ii * 8 + 8])))
                for tname, ti in [("T1", T1), ("Tstar", Tstar)]:
                    for mi, m in enumerate(MASKS):
                        rec[f"{tname}/{m}"] = item_metrics(LP[ii, :, :, mi, ti], dens[ii, :, mi])
                rec["ntok_nocopy"] = ntok[ii, :, :2, 1].tolist()
                f.write(json.dumps(rec) + "\n")
        S = summarize(items, LP, dens, Tstar, a.boot)
        info = dict(model=a.model, name=a.name, render=rend, n_items=len(items), Tstar=TEMPS[Tstar],
                    nll_bits_per_byte_by_T={str(T): float(nll_T[k] / LN2 / (dens[:, 0, 0] + dens[:, 1, 0]).sum()) for k, T in enumerate(TEMPS)},
                    straddle_frac=float(np.mean([s["straddle"] for s in seqs])),
                    zero_token_nocopy_frac=float(np.mean(ntok[:, :, :2, 1] == 0)), seconds=time.time() - t0)
        json.dump(dict(info=info, summary=S), open(os.path.join(od, "summary.json"), "w"), indent=1)
        md = fmt_md(a.name, rend, S, f"T* = {TEMPS[Tstar]}; straddling first tokens: {info['straddle_frac']:.3f}; "
                                     f"(item, ctx, out) with no scored nocopy token: {info['zero_token_nocopy_frac']:.3f}")
        open(os.path.join(od, "summary.md"), "w").write(md)
        print(md)


if __name__ == "__main__":
    main()
