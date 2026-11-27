"""Teacher-forced scoring of AgenticPPL trajectories: span BPB, observation breakdown,
role-switch mass, temperature grid, prompted prediction, Yes/No error question.

usage: score.py MODEL_PATH NAME [--limit N]
"""
import argparse, gzip, hashlib, json, math, os, time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache

LN2 = math.log(2)
MAXLEN = 32768
CHUNK = 2048
NGRAM = 8
FIRSTN = 16
CAP = 2.0
TGRID = [round(0.5 + 0.1 * i, 2) for i in range(26)]  # 0.5 .. 3.0
TYPES = ["task", "thought", "action", "observation", "markup", "wrap"]
TID = {t: i for i, t in enumerate(TYPES)}
PRED_ASK = "Predict the exact terminal output the commands above will produce. Reply with the output only."
Q_ASK = "Will the output of the commands above contain an error? Answer Yes or No."


def headers(fmt, role, i):
    if fmt == "native":
        return f"<|im_start|>{role}\n", "<|im_end|>\n"
    if i == 0:
        return "### Task\n", "\n\n"
    return ("### Agent\n" if role == "assistant" else "### Terminal\n"), "\n\n"


class Enc:
    def __init__(self, tok):
        self.tok = tok

    def plain(self, text):  # wrapper text: special tokens recognised
        return self.tok(text, add_special_tokens=False)["input_ids"]

    def content(self, text):  # content: literal, with offsets
        e = self.tok(text, add_special_tokens=False, return_offsets_mapping=True, split_special_tokens=True)
        ids, offs = e["input_ids"], e["offset_mapping"]
        nbytes = [len(text[s:t].encode("utf-8")) for s, t in offs]
        return ids, offs, nbytes


def build(enc, msgs, fmt):
    ids, typ, nb, turnstart, msg_start, msg_of, turn = [], [], [], [], [], [], []
    for i, m in enumerate(msgs):
        h, f = headers(fmt, m["role"], i)
        msg_start.append(len(ids))
        hid = enc.plain(h)
        ids += hid; typ += [TID["wrap"]] * len(hid); nb += [0] * len(hid); turnstart += [0] * len(hid)
        msg_of += [i] * len(hid); turn += [-2] * len(hid)
        cid, offs, cb = enc.content(m["content"])
        parts = m["parts"]
        for k, ((s, _), b) in enumerate(zip(offs, cb)):
            t, tn = "markup", parts[0][1] if parts else -2
            for p in parts:
                if p[2] <= s < p[3]:
                    t, tn = p[0], p[1]; break
            turn.append(tn)
            typ.append(TID[t]); nb.append(b)
            turnstart.append(1 if k < FIRSTN else 0)
            msg_of.append(i)
        ids += cid
        fid = enc.plain(f)
        ids += fid; typ += [TID["wrap"]] * len(fid); nb += [0] * len(fid); turnstart += [0] * len(fid)
        msg_of += [i] * len(fid); turn += [-2] * len(fid)
    msg_start.append(len(ids))
    # truncate whole trailing messages
    nmsg = len(msgs)
    while msg_start[nmsg] > MAXLEN and nmsg > 1:
        nmsg -= 1
    L = msg_start[nmsg]
    return dict(ids=ids[:L], typ=typ[:L], nb=nb[:L], first=turnstart[:L], msg_start=msg_start[: nmsg + 1],
                nmsg=nmsg, msg_of=msg_of[:L], turn=turn[:L])


def copy_flags(ids, start=0, seen=None):
    """flag[i]=1 if ids[i-NGRAM+1..i] occurred entirely before position i (in ids or seen set)."""
    seen = set() if seen is None else seen
    flags = [0] * len(ids)
    for i in range(len(ids)):
        if i >= NGRAM - 1:
            g = tuple(ids[i - NGRAM + 1: i + 1])
            if i >= start and g in seen:
                flags[i] = 1
            seen.add(g)
    return flags, seen


def crop_to(cache, L):
    n = cache.get_seq_length() - L
    if n > 0:
        cache.crop(-n)
    assert cache.get_seq_length() == L, (cache.get_seq_length(), L)


class Scorer:
    def __init__(self, path):
        self.tok = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, attn_implementation="sdpa",
                                                          device_map="cuda")
        self.model.eval()
        self.W = self.model.lm_head.weight
        V = self.W.shape[0]
        first_special = self.tok.convert_tokens_to_ids("<|endoftext|>")
        self.special = torch.zeros(V, dtype=torch.bool, device="cuda")
        self.special[first_special:] = True
        self.sid = {k: self.tok.convert_tokens_to_ids(k) for k in ["<|im_start|>", "<|im_end|>", "<think>"]}
        hm = torch.zeros(V, dtype=torch.bool)
        for i in range(min(V, len(self.tok))):
            s = self.tok.decode([i])
            if s.lstrip().startswith("###"):
                hm[i] = True
        self.hash = hm.cuda()
        self.yes = self.tok("Yes", add_special_tokens=False)["input_ids"]
        self.no = self.tok("No", add_special_tokens=False)["input_ids"]
        assert len(self.yes) == 1 and len(self.no) == 1
        self.enc = Enc(self.tok)

    @torch.inference_mode()
    def stats(self, h, tgt, tmask):
        """h: (n,d) hidden predicting tgt (n,). returns dict of cpu arrays; T-grid only where tmask."""
        out = {k: [] for k in ["bits", "spec", "hash", "im_start", "im_end", "think", "ent", "rank", "top1"]}
        tg = []
        for a in range(0, h.shape[0], CHUNK):
            z = (h[a:a + CHUNK] @ self.W.T).float()
            t = tgt[a:a + CHUNK]
            lse = torch.logsumexp(z, -1)
            zt = z.gather(1, t[:, None])[:, 0]
            out["bits"].append(((lse - zt) / LN2).cpu())
            out["rank"].append((z > zt[:, None]).sum(-1).clamp(max=1000).cpu())
            out["top1"].append(torch.exp(z.max(-1).values - lse).cpu())
            p = torch.softmax(z, -1)
            out["ent"].append((lse - (p * z).sum(-1)).cpu())
            out["spec"].append((p * self.special).sum(-1).cpu())
            out["hash"].append((p * self.hash).sum(-1).cpu())
            for k, tk in [("im_start", "<|im_start|>"), ("im_end", "<|im_end|>"), ("think", "<think>")]:
                out[k].append(p[:, self.sid[tk]].cpu())
            del p
            m = tmask[a:a + CHUNK]
            if m.any():
                zm, tm = z[m], zt[m]
                tg.append(torch.stack([(torch.logsumexp(zm / T, -1) - tm / T) / LN2 for T in TGRID], 1).cpu())
            del z
        res = {k: torch.cat(v).numpy() for k, v in out.items()}
        res["tgrid"] = torch.cat(tg).numpy() if tg else np.zeros((0, len(TGRID)), np.float32)
        return res

    @torch.inference_mode()
    def forward(self, ids, cache):
        x = torch.tensor([ids], device="cuda")
        hs = []
        for a in range(0, len(ids), CHUNK):
            o = self.model.model(input_ids=x[:, a:a + CHUNK], past_key_values=cache, use_cache=True)
            hs.append(o.last_hidden_state[0])
        return torch.cat(hs)

    @torch.inference_mode()
    def run_traj(self, traj, fmt, items, run_items=True):
        b = build(self.enc, traj["messages"], fmt)
        ids = b["ids"]
        N = len(ids)
        typ = np.array(b["typ"])
        cflags, _ = copy_flags(ids)
        # boundaries at selected item messages (prefix = tokens before message j)
        cuts = sorted({b["msg_start"][it["msg"]] for it in items if it["msg"] < b["nmsg"]})
        bounds = [0] + cuts + [N]
        cutset = set(cuts)
        cache = DynamicCache()
        prev = None
        allstats = []
        item_res = []
        for si in range(len(bounds) - 1):
            a, e = bounds[si], bounds[si + 1]
            if e > a:
                h = self.forward(ids[a:e], cache)
                hp = h[:-1] if prev is None else torch.cat([prev[None], h[:-1]])
                tg = ids[a + 1:e] if prev is None else ids[a:e]
                tm = typ[a + 1:e] if prev is None else typ[a:e]
                allstats.append(self.stats(hp, torch.tensor(tg, device="cuda"),
                                           torch.ones(len(tg), dtype=torch.bool, device="cuda")))
                prev = h[-1]
                del h, hp
            if e in cutset and run_items:
                for it in items:
                    if it["msg"] < b["nmsg"] and b["msg_start"][it["msg"]] == e:
                        item_res.append(self.run_item(it, fmt, ids[:e], cache, e))
        # concat stats (positions 1..N-1)
        st = {k: np.concatenate([s[k] for s in allstats]) for k in allstats[0]}
        return dict(b=b, st=st, copy=np.array(cflags[1:]), items=item_res)

    @torch.inference_mode()
    def run_item(self, it, fmt, prefix_ids, cache, L):
        enc = self.enc
        if fmt == "native":
            ask = f"<|im_start|>user\n{PRED_ASK}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
            qs = f"<|im_start|>user\n{Q_ASK}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        else:
            ask = f"### User\n{PRED_ASK}\n\n### Prediction\n"
            qs = f"### Question\n{Q_ASK}\n\n### Answer\n"
        rid, _, rnb = enc.content(it["reply"])
        rid, rnb = rid[:512], rnb[:512]
        aid = enc.plain(ask)
        suf = aid + rid
        # prediction
        h = self.forward(suf, cache)
        crop_to(cache, L)
        n0 = len(aid)
        hp = h[n0 - 1: n0 - 1 + len(rid)]
        s = self.stats(hp, torch.tensor(rid, device="cuda"), torch.zeros(len(rid), dtype=torch.bool, device="cuda"))
        flags, _ = copy_flags(list(prefix_ids) + suf, start=L + n0)
        cf = np.array(flags[L + n0:])
        # question
        qid = enc.plain(qs)
        hq = self.forward(qid, cache)
        crop_to(cache, L)
        z = (hq[-1] @ self.W.T).float()
        lp = torch.log_softmax(z, -1)
        ly, ln_ = lp[self.yes[0]].item(), lp[self.no[0]].item()
        return dict(traj=it["traj"], msg=it["msg"], bits=s["bits"], nb=np.array(rnb), copy=cf,
                    spec0=float(s["spec"][0]), logp_yes=ly, logp_no=ln_,
                    label_raw=it["label_raw"], label_new=it["label_new"])


def agg_traj(r):
    """per-trajectory sufficient statistics."""
    b, st, cp = r["b"], r["st"], r["copy"]
    typ = np.array(b["typ"][1:]); nb = np.array(b["nb"][1:]); first = np.array(b["first"][1:])
    bits = st["bits"]
    out = {}
    for t in TYPES[:-1]:
        m = typ == TID[t]
        out[f"type/{t}"] = [float(bits[m].sum()), int(nb[m].sum()), int(m.sum())]
    ob = typ == TID["observation"]
    subsets = {"all": ob, "first16": ob & (first == 1), "body": ob & (first == 0),
               "novel": ob & (cp == 0), "copy": ob & (cp == 1)}
    for name, m in subsets.items():
        rec = dict(bits=float(bits[m].sum()), bytes=int(nb[m].sum()), n=int(m.sum()),
                   capped=float(np.minimum(bits[m], CAP).sum()), prob=float(np.exp2(-bits[m]).sum()),
                   spec=float(st["spec"][m].sum()), hash=float(st["hash"][m].sum()),
                   im_start=float(st["im_start"][m].sum()), im_end=float(st["im_end"][m].sum()),
                   think=float(st["think"][m].sum()))
        rec["tgrid"] = st["tgrid"][m].sum(0).tolist()
        out[f"obs/{name}"] = rec
    # non-observation tokens special mass for reference
    nonob = (typ != TID["observation"]) & (typ != TID["wrap"])
    out["nonobs_spec"] = [float(st["spec"][nonob].sum()), int(nonob.sum())]
    nw = typ != TID["wrap"]
    out["nonwrap_tgrid"] = st["tgrid"][nw].sum(0).tolist()
    return out


def save_tok(a, ev, tokbuf, tstar):
    shared = f"{a.tokdir}/_shared"; mine = f"{a.tokdir}/{a.name}"
    os.makedirs(shared, exist_ok=True); os.makedirs(mine, exist_ok=True)
    for fmt, tb in tokbuf.items():
        lens = np.array([len(x) for x in tb["lp"]]); off = np.concatenate([[0], np.cumsum(lens)])
        meta = dict(ids=np.concatenate(tb["ids"]), typ=np.concatenate(tb["typ"]), turn=np.concatenate(tb["turn"]),
                    first=np.concatenate(tb["first"]), copy=np.concatenate(tb["copy"]), offsets=off,
                    traj=np.array(ev), hash=np.array(tb["hash"]), types=np.array(TYPES))
        sp = f"{shared}/{fmt}.npz"
        match = True
        if os.path.exists(sp):
            ref = np.load(sp)
            match = list(ref["hash"]) == list(meta["hash"]) and list(ref["traj"]) == list(meta["traj"])
            if not match:
                print(f"WARNING token hash mismatch vs shared for {fmt}; saving own meta", flush=True)
        else:
            np.savez_compressed(sp, **meta)
        per = dict(lp=np.concatenate(tb["lp"]), ent=np.concatenate(tb["ent"]), lp_Tobs=np.concatenate(tb["lp_Tobs"]),
                   lp_Tall=np.concatenate(tb["lp_Tall"]), hash=meta["hash"],
                   rank=np.concatenate(tb["rank"]), top1=np.concatenate(tb["top1"]), spec=np.concatenate(tb["spec"]),
                   lp_tgrid=np.concatenate(tb["lp_tgrid"]), tgrid=np.array(TGRID), version=3,
                   T_obs=tstar[fmt]["T_obs"], T_all=tstar[fmt]["T_all"], hash_match=match)
        if not match:
            per.update({f"meta_{k}": v for k, v in meta.items()})
        np.savez(f"{mine}/{fmt}.npz", **per)
    print("saved per-token", mine, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("name")
    ap.add_argument("--prep", default="prep.json"); ap.add_argument("--data", default="data/trajectories.jsonl.gz")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", default="results")
    ap.add_argument("--tf-only", action="store_true"); ap.add_argument("--tokdir", default="tok")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    prep = json.load(open(a.prep))
    rows = {r["id"]: r for r in map(json.loads, gzip.open(a.data, "rt"))}
    ev, cal = prep["eval"], prep["cal"]
    if a.limit:
        ev, cal = ev[: a.limit], cal[: max(1, a.limit // 4)]
    items_by = {}
    for it in prep["items"]:
        items_by.setdefault(it["traj"], []).append(it)
    t0 = time.time()
    sc = Scorer(a.model)
    tload = time.time() - t0
    res = dict(name=a.name, model=a.model, tgrid=TGRID, eval={}, cal={}, items={}, tstar={})
    ntok = 0
    tokbuf = {f: {k: [] for k in ["lp", "ent", "lp_Tobs", "lp_Tall", "rank", "top1", "spec", "lp_tgrid",
                                  "ids", "typ", "turn", "first", "copy", "hash"]}
              for f in ["neutral", "native"]}
    for split, ids in [("cal", cal), ("eval", ev)]:
        if split == "eval":
            for fmt in ["neutral", "native"]:
                d = res["cal"][fmt]
                go = np.sum([d[t]["obs/all"]["tgrid"] for t in d], 0); ga = np.sum([d[t]["nonwrap_tgrid"] for t in d], 0)
                res["tstar"][fmt] = dict(k_obs=int(np.argmin(go)), T_obs=TGRID[int(np.argmin(go))],
                                         k_all=int(np.argmin(ga)), T_all=TGRID[int(np.argmin(ga))])
            print("tstar", res["tstar"], flush=True)
        for k, tid in enumerate(ids):
            for fmt in ["neutral", "native"]:
                its = items_by.get(tid, []) if split == "eval" else []
                r = sc.run_traj(rows[tid], fmt, its, run_items=not a.tf_only)
                if split == "eval":
                    tb, st, ts = tokbuf[fmt], r["st"], res["tstar"][fmt]
                    bid = r["b"]["ids"]
                    tb["lp"].append((-st["bits"] * LN2).astype(np.float16))
                    tb["ent"].append(st["ent"].astype(np.float16))
                    tb["rank"].append(st["rank"].astype(np.int16))
                    tb["top1"].append(st["top1"].astype(np.float16))
                    tb["spec"].append(st["spec"].astype(np.float16))
                    tb["lp_tgrid"].append((-st["tgrid"] * LN2).astype(np.float16))
                    tb["lp_Tobs"].append((-st["tgrid"][:, ts["k_obs"]] * LN2).astype(np.float16))
                    tb["lp_Tall"].append((-st["tgrid"][:, ts["k_all"]] * LN2).astype(np.float16))
                    tb["ids"].append(np.array(bid[1:], np.int32))
                    tb["typ"].append(np.array(r["b"]["typ"][1:], np.int8))
                    tb["turn"].append(np.array(r["b"]["turn"][1:], np.int16))
                    tb["first"].append(np.array(r["b"]["first"][1:], np.int8))
                    tb["copy"].append(r["copy"].astype(np.int8))
                    tb["hash"].append(hashlib.sha1(np.array(bid, np.int32).tobytes()).hexdigest()[:16])
                ntok += len(r["b"]["ids"]) + sum(len(x["bits"]) + 60 for x in r["items"])
                res[split].setdefault(fmt, {})[tid] = agg_traj(r)
                for x in r["items"]:
                    res["items"].setdefault(fmt, []).append(dict(
                        traj=x["traj"], msg=x["msg"], bits=float(x["bits"].sum()), bytes=int(x["nb"].sum()),
                        n=int(len(x["bits"])), novel_bits=float(x["bits"][x["copy"] == 0].sum()),
                        novel_bytes=int(x["nb"][x["copy"] == 0].sum()), novel_n=int((x["copy"] == 0).sum()),
                        capped=float(np.minimum(x["bits"], CAP).sum()), spec0=x["spec0"],
                        logp_yes=x["logp_yes"], logp_no=x["logp_no"],
                        label_raw=x["label_raw"], label_new=x["label_new"]))
            if k % 10 == 0:
                print(f"{split} {k}/{len(ids)} {time.time()-t0:.0f}s tok={ntok}", flush=True)
    save_tok(a, ev, tokbuf, res["tstar"])
    res["timing"] = dict(load_s=tload, total_s=time.time() - t0, tokens=ntok,
                         gpu=torch.cuda.get_device_name(), max_mem_gb=torch.cuda.max_memory_allocated() / 1e9)
    out = a.out if not a.tf_only else a.out + "_tf"
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(f"{out}/{a.name}.json", "w"))
    print("done", res["timing"], flush=True)


if __name__ == "__main__":
    main()
