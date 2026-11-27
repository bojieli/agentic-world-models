"""M5: the AgenticPPL metric (github.com/wenhaochai/AgenticPPL @ bb189cc) on our checkpoints.

Rendering, tokenisation, pick mapping and the three combines are the reference package's own functions
(agenticppl.render / agenticppl.measure, unchanged). Only the forward pass differs: the reference uses vLLM prompt
log-probs; here a Hugging Face transformers bf16 forward with an fp32 LM head (validated against `agenticppl score`
with vLLM on one model, see results/m5_validate). Extra per-token outputs: entropy (for sharpness/calibration).

usage: m5.py MODEL_PATH NAME [--split heldout] [--limit N]
writes results/m5/<NAME>.json (reference-format result + bootstrap CIs + extras) and results/m5/<NAME>_tok.npz
"""
import argparse, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
from agenticppl.data import pick_sets, trajectories  # noqa: E402
from agenticppl.measure import (agenticppl_of, gather, plain_ppl, same_spans, token_bytes, nonmarkup, CAP)  # noqa: E402
from agenticppl.render import Renderer  # noqa: E402

LN2 = math.log(2.0)
DATA = os.environ.get("AGENTICPPL_DATA", os.path.join(os.path.dirname(HERE), "terminal", "data"))
NB = 2000


def hf_forward(path, prompts):
    import torch
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, attn_implementation="sdpa", device_map="cuda")
    model.eval()
    W = model.lm_head.weight.float()
    bits, ents = [], []
    t0, ntok = time.time(), 0
    with torch.inference_mode():
        for k, p in enumerate(prompts):
            x = torch.tensor([p], device="cuda")
            h = model.model(input_ids=x).last_hidden_state[0]
            b = np.full(len(p), np.nan, np.float32); e = np.full(len(p), np.nan, np.float32)
            for a in range(0, len(p) - 1, 2048):
                z = h[a:min(a + 2048, len(p) - 1)].float() @ W.T
                t = x[0, a + 1:a + 1 + z.shape[0]]
                lse = torch.logsumexp(z, -1)
                b[a + 1:a + 1 + z.shape[0]] = ((lse - z.gather(1, t[:, None])[:, 0]) / LN2).cpu().numpy()
                pz = torch.softmax(z, -1)
                e[a + 1:a + 1 + z.shape[0]] = ((lse - (pz * z).sum(-1)) / LN2).cpu().numpy()
                del z, pz
            bits.append(b); ents.append(e); ntok += len(p)
            if k % 100 == 0:
                print(f"{k+1}/{len(prompts)} docs {ntok/(time.time()-t0):.0f} tok/s mem={torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
    return bits, ents


def per_range(docs, ps, model, bits, ents):
    """per kept range: doc index, capped value, prob_mean value, raw bits sum, n rows, entropy sum, (rows)"""
    doc_rows, rbytes, _ = gather(docs, ps["ranges"], model)
    out = dict(doc=[], capped=[], prob=[], raw=[], nrow=[], ent=[], loss=[])
    base = 0
    did = {d["id"]: i for i, d in enumerate(docs)}
    for i, rows, rid in doc_rows:
        b = np.asarray(bits[i], np.float64)[rows]; e = np.asarray(ents[i], np.float64)[rows]
        nb = (np.asarray(model[i][2])[rows] - np.asarray(model[i][1])[rows]).astype(np.float64)
        ok = ~np.isnan(b)
        r = rid - rid.min() if len(rid) else rid
        n = len(np.unique(rid)) if len(rid) else 0
        if not len(rid):
            continue
        uniq = np.unique(rid)
        loc = np.searchsorted(uniq, rid)
        m = len(uniq)
        tot = np.bincount(loc[ok], np.minimum(b[ok], CAP), m); raw = np.bincount(loc[ok], b[ok], m)
        rb = np.bincount(loc[ok], nb[ok], m); cnt = np.bincount(loc[ok], None, m)
        es = np.bincount(loc[ok], e[ok], m)
        has = cnt > 0
        rbytes_k = rbytes[uniq]
        est = raw * (rbytes_k / np.maximum(rb, 1e-9))
        out["doc"] += [did[i]] * int(has.sum())
        out["capped"] += list(np.minimum(tot[has], CAP)); out["prob"] += list(2.0 ** (-np.clip(est[has], 0, 60)))
        out["raw"] += list(raw[has]); out["nrow"] += list(cnt[has]); out["ent"] += list(es[has])
    return {k: np.array(v) for k, v in out.items()}


def boot_ci(doc, val, ndoc, f=np.mean, seed=0):
    r = np.random.default_rng(seed)
    docs_with = np.unique(doc)
    by = {d: val[doc == d] for d in docs_with}
    keys = np.array(list(by.keys()))
    sums = np.array([by[d].sum() for d in keys]); cnts = np.array([len(by[d]) for d in keys])
    bs = []
    for _ in range(NB):
        w = np.bincount(r.integers(0, len(keys), len(keys)), minlength=len(keys))
        bs.append((w * sums).sum() / (w * cnts).sum())
    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("name")
    ap.add_argument("--split", default="heldout"); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "m5"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    docs = [d for d in trajectories(DATA) if d["split"] == a.split][: a.limit or None]
    sets = pick_sets(DATA)
    rd = Renderer(a.model)
    sid = np.array(sorted(rd.special_ids()), np.int64)
    model, prompts, special, unmatched, act_rows = {}, [], [], [], {}
    for d in docs:  # == agenticppl.cli.score
        text, spans = rd(d["messages"])
        enc = rd.tok(text, add_special_tokens=False, return_offsets_mapping=True)
        s, e = token_bytes(text, enc["offset_mapping"])
        ok = same_spans(d["text"], d["spans"], text, spans)
        if not ok:
            unmatched.append(d["id"])
        hit = s[np.isin(np.asarray(enc["input_ids"]), sid)]
        if any(x0 <= h < x1 for h in hit for x0, x1, _, _ in spans):
            special.append(d["id"])
        model[d["id"]] = (spans if ok else None, s, e)
        prompts.append(enc["input_ids"])
        # tokens starting inside action spans (command positions)
        acts = [(x[0], x[1]) for x in spans if x[2] == "action"]
        m = np.zeros(len(s), bool)
        for x0, x1 in acts:
            m |= (s >= x0) & (s < x1)
        act_rows[d["id"]] = m
    print(f"{len(docs)} docs, {sum(map(len, prompts))} tokens, longest {max(map(len, prompts))}, unmatched {len(unmatched)}, special {len(special)}", flush=True)
    t0 = time.time()
    b, e = hf_forward(a.model, prompts)
    secs = time.time() - t0
    ids = [d["id"] for d in docs]
    bits = dict(zip(ids, b)); ents = dict(zip(ids, e))
    res = {"model": a.model, "name": a.name, "split": a.split, "n_docs": len(docs), "docs_unmatched": len(unmatched),
           "docs_with_special_tokens_in_content": len(special), "forward_seconds": secs, "tokens": int(sum(map(len, prompts))),
           "plain_ppl": plain_ppl(docs, model, bits), "picks": {}}
    ranges_out = {}
    for name, ps in sets.items():
        r = agenticppl_of(docs, ps["ranges"], model, bits, ps["combine"])  # reference value
        pr = per_range(docs, ps, model, bits, ents)
        val = -pr["capped"] if ps["combine"] == "capped_bits" else pr["prob"]
        r.update(ci=boot_ci(pr["doc"], val, len(docs)),
                 alt_capped_bits=float(-pr["capped"].mean()), alt_prob_mean=float(pr["prob"].mean()),
                 mean_range_bits_uncapped=float(pr["raw"].mean()), mean_range_bits_uncapped_ci=boot_ci(pr["doc"], pr["raw"], len(docs)),
                 bits_per_row=float(pr["raw"].sum() / pr["nrow"].sum()), ent_per_row=float(pr["ent"].sum() / pr["nrow"].sum()))
        r["gap_per_row"] = r["bits_per_row"] - r["ent_per_row"]
        assert abs(r["alt_" + ps["combine"]] - r["agenticppl"]) < 1e-9, (r["alt_" + ps["combine"]], r["agenticppl"])
        res["picks"][name] = r
        ranges_out[name] = pr
    # sharpness at command positions (all action tokens of the model's rendering)
    ab = np.concatenate([bits[i][act_rows[i]] for i in ids]); ae = np.concatenate([ents[i][act_rows[i]] for i in ids])
    ok = ~np.isnan(ab)
    res["action_tokens"] = dict(n=int(ok.sum()), bits=float(ab[ok].mean()), ent=float(ae[ok].mean()), gap=float(ab[ok].mean() - ae[ok].mean()))
    json.dump(res, open(os.path.join(a.out, f"{a.name}.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(a.out, f"{a.name}_tok.npz"), ids=np.array(ids),
                        bits=np.concatenate(b).astype(np.float16), ent=np.concatenate(e).astype(np.float16),
                        lens=np.array([len(x) for x in b]),
                        **{f"{n}__{k}": v for n, pr in ranges_out.items() for k, v in pr.items()})
    print(json.dumps({k: v for k, v in res.items() if k != "picks"}, indent=0))
    for n, r in res["picks"].items():
        print(n, r["combine"], f"{r['agenticppl']:.4f}", r["ci"], "uncapped", round(r["mean_range_bits_uncapped"], 3), "n", r["n_ranges"])


if __name__ == "__main__":
    main()
