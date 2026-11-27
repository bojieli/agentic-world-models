"""GPU executor for phase-2 measures. Consumes work/<ds>.pkl from prep2.py.

Main pass: each segment is fed left to right with a KV cache; per-token stats (M1) are taken at scored observation
positions. At every boundary that carries branches (M2 swaps, M3 forced-choice forks incl. leak-check forks, M4
probes) all branches are evaluated in ONE forward together with the main tokens that precede the boundary, using a
tree attention mask (branch tokens see the context and their ancestors only); branch KV is cropped afterwards.

usage: run.py MODEL_PATH NAME [--ds tp,swe] [--lora DIR] [--limit-segs N] [--check]
"""
import argparse, json, math, os, pickle, sys, time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, DynamicCache

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LN2 = math.log(2)
TGRID = [round(0.7 + 0.1 * i, 2) for i in range(19)]
CH = 4096
LMCH = 1024


def merge_lora(model, d):
    from safetensors.torch import load_file
    cfg = json.load(open(os.path.join(d, "adapter_config.json")))
    sd = load_file(os.path.join(d, "adapter_model.safetensors"))
    scale = cfg["lora_alpha"] / cfg["r"]
    if cfg.get("use_rslora"):
        scale = cfg["lora_alpha"] / math.sqrt(cfg["r"])
    mods = dict(model.named_modules())
    n = 0
    for k, A in sd.items():
        if "lora_A" not in k:
            continue
        B = sd[k.replace("lora_A", "lora_B")]
        name = k.split("base_model.model.")[-1].replace(".lora_A.weight", "").replace(".lora_A.default.weight", "")
        mod = mods.get(name) or mods.get(name.replace("model.", "", 1))
        assert mod is not None, name
        with torch.no_grad():
            mod.weight += (B.to(mod.weight.device, torch.float32) @ A.to(mod.weight.device, torch.float32) * scale).to(mod.weight.dtype)
        n += 1
    print(f"merged {n} LoRA modules from {d} (scale {scale})", flush=True)


class Runner:
    def __init__(self, path, lora=None):
        self.model = AutoModelForCausalLM.from_pretrained(path, dtype=getattr(torch, os.environ.get("P2_DTYPE", "bfloat16")), attn_implementation="sdpa",
                                                          device_map="cuda")
        self.model.eval()
        if lora:
            merge_lora(self.model, lora)
        self.W = self.model.lm_head.weight.float()  # fp32 head: bf16 logits are quantised at ~0.1-0.25 nats
        self.tg = torch.tensor(TGRID, device="cuda")
        self.ntok = 0

    # ------------------------------------------------------------ logits helpers
    @torch.inference_mode()
    def tok_stats(self, h, tgt, full=True):
        """h (n,d) predicting tgt (n,). Returns lp (nats), and if full rank/top1/ent/lpT."""
        out = {k: [] for k in (["lp", "rank", "top1", "ent", "lpT"] if full else ["lp", "lpT"])}
        for a in range(0, h.shape[0], LMCH):
            z = h[a:a + LMCH].float() @ self.W.T
            t = tgt[a:a + LMCH]
            lse = torch.logsumexp(z, -1)
            zt = z.gather(1, t[:, None])[:, 0]
            out["lp"].append((zt - lse).cpu())
            out["lpT"].append(torch.stack([zt / T - torch.logsumexp(z / T, -1) for T in TGRID], 1).cpu())
            if full:
                out["rank"].append((z > zt[:, None]).sum(-1).int().cpu())
                out["top1"].append(torch.exp(z.max(-1).values - lse).cpu())
                p = torch.softmax(z, -1)
                out["ent"].append((lse - (p * z).sum(-1)).cpu())
                del p
            del z
        return {k: torch.cat(v).numpy() for k, v in out.items()}

    @torch.inference_mode()
    def logsm(self, h):
        return torch.log_softmax(h.float() @ self.W.T, -1)

    # ------------------------------------------------------------ forward with optional branch trees
    @torch.inference_mode()
    def step(self, cache, main_ids, pos, branches):
        """forward main_ids at positions pos.. plus branch trees anchored at pos+len(main_ids).
        Returns main hidden (m,d), list of per-branch node hidden lists."""
        m = len(main_ids)
        L = cache.get_seq_length()
        assert L == pos, (L, pos)
        if not branches:
            x = torch.tensor([main_ids], device="cuda")
            o = self.model.model(input_ids=x, past_key_values=cache, use_cache=True)
            self.ntok += m
            return o.last_hidden_state[0], []
        b = pos + m
        flat, posid, nodes = list(main_ids), list(range(pos, b)), []
        # node spans
        for br in branches:
            spans = []
            for gi, ids in enumerate(br["nodes"]):
                parent = -1 if gi == 0 else 0  # forks: conts hang off node 0; single-node branches have no children
                st = len(flat)
                depth0 = b if parent < 0 else b + len(br["nodes"][0])
                flat += list(ids); posid += list(range(depth0, depth0 + len(ids)))
                spans.append((st, st + len(ids), parent))
            nodes.append(spans)
        q = len(flat)
        mask = torch.zeros(q, L + q, dtype=torch.bool, device="cuda")
        mask[:, :L] = True
        ar = torch.arange(q, device="cuda")
        # main tokens: causal among main
        mask[:m, L:L + m] = ar[:m, None] >= ar[None, :m]
        for spans in nodes:
            for (st, en, parent) in spans:
                mask[st:en, L:L + m] = True
                mask[st:en, L + st:L + en] = ar[st:en, None] >= ar[None, st:en]
                if parent >= 0:
                    ps, pe, _ = spans[parent]
                    mask[st:en, L + ps:L + pe] = True
        x = torch.tensor([flat], device="cuda")
        pid = torch.tensor([posid], device="cuda")
        o = self.model.model(input_ids=x, position_ids=pid, attention_mask=mask[None, None], past_key_values=cache,
                             use_cache=True)
        self.ntok += q
        H = o.last_hidden_state[0]
        n = cache.get_seq_length() - b
        if n > 0:
            cache.crop(-n)
        assert cache.get_seq_length() == b
        return H[:m], [[H[st:en] for (st, en, _) in spans] for spans in nodes]

    @torch.inference_mode()
    def eval_branch(self, br, hs, last_h):
        t = br["t"]
        if t == "nll":
            ids = br["nodes"][0]; h = hs[0]
            hp = torch.cat([last_h[None], h[:-1]])
            pos = torch.tensor(br["pos"], device="cuda", dtype=torch.long)
            tgt = torch.tensor(ids, device="cuda")[pos]
            s = self.tok_stats(hp[pos], tgt, full=False)
            return dict(lp=s["lp"].astype(np.float32), lpT=s["lpT"].astype(np.float16))
        if t == "next":
            ls = self.logsm(hs[0][-1:])[0]
            return ls[torch.tensor(br["cands"], device="cuda")].cpu().numpy()
        if t == "fork":
            hP = hs[0]; out = []
            for ids, hc in zip(br["nodes"][1:], hs[1:]):
                hp = torch.cat([hP[-1:], hc[:-1]])
                ls = self.logsm(hp)
                lp = ls.gather(1, torch.tensor(ids, device="cuda")[:, None])[:, 0]
                out.append(lp.cpu().numpy())
            return out
        raise ValueError(t)

    @torch.inference_mode()
    def run_segment(self, seg):
        ids = seg["ids"].tolist(); N = len(ids)
        ap_ = seg.get("act_pos", np.zeros(0, np.int64))
        sp = np.sort(np.concatenate([seg["score_pos"], ap_])) if len(ap_) else seg["score_pos"]
        is_act = np.isin(sp, ap_) if len(ap_) else np.zeros(len(sp), bool)
        bounds = sorted(seg["branches"].keys())
        cache = DynamicCache()
        pos = 0; last_h = None
        m1 = {k: [] for k in ["lp", "rank", "top1", "ent", "lpT"]}
        res = {}
        si = 0  # pointer into score positions

        def collect(H, a):
            """hidden H for main positions a..a+len(H)-1 predict tokens a+1..a+len(H)"""
            nonlocal si
            e = a + H.shape[0]
            lo = si
            while si < len(sp) and sp[si] <= e and sp[si] < N:
                si += 1
            if si > lo:
                p = torch.tensor(sp[lo:si] - 1 - a, device="cuda")
                tg = torch.tensor([ids[x] for x in sp[lo:si]], device="cuda")
                s = self.tok_stats(H[p], tg)
                for k in m1:
                    m1[k].append(s[k])

        for b in bounds + [N]:
            if b < pos:
                continue
            brs = seg["branches"].get(b, []) if b < N or b in seg["branches"] else []
            while b - pos > CH:
                H, _ = self.step(cache, ids[pos:pos + CH], pos, [])
                collect(H, pos); last_h = H[-1]; pos += CH
            if b == pos and not brs:
                continue
            H, bh = self.step(cache, ids[pos:b], pos, brs)
            if H.shape[0]:
                collect(H, pos); last_h = H[-1]
            for br, hs in zip(brs, bh):
                res[br["key"]] = self.eval_branch(br, hs, last_h)
            pos = b
        assert si == len(sp), (si, len(sp))
        m1 = {k: (np.concatenate(v) if v else np.zeros((0, len(TGRID)) if k == "lpT" else 0)) for k, v in m1.items()}
        if is_act.any():
            res["__act_lp"] = m1["lp"][is_act].astype(np.float32)
            m1 = {k: v[~is_act] for k, v in m1.items()}
        return m1, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model"); ap.add_argument("name")
    ap.add_argument("--ds", default="tp,swe"); ap.add_argument("--lora", default=None)
    ap.add_argument("--work", default=os.path.join(HERE, "work")); ap.add_argument("--out", default=os.path.join(HERE, "results", "raw"))
    ap.add_argument("--limit-segs", type=int, default=0)
    ap.add_argument("--subset", default=None, help="json {ds: [traj ids]}: only score segments of these trajectories")
    a = ap.parse_args()
    od = os.path.join(a.out, a.name); os.makedirs(od, exist_ok=True)
    t0 = time.time()
    R = Runner(a.model, a.lora)
    print(f"loaded {a.name} in {time.time()-t0:.0f}s", flush=True)
    for ds in a.ds.split(","):
        if os.path.exists(os.path.join(od, f"{ds}.done")) and not a.limit_segs:
            print("skip", ds); continue
        W = pickle.load(open(os.path.join(a.work, f"{ds}.pkl"), "rb"))
        sel = list(range(len(W["segs"])))
        if a.subset:
            keep = set(json.load(open(a.subset))[ds])
            sel = [i for i in sel if W["trajs"][W["segs"][i]["traj"]]["id"] in keep]
        sel = sel[: a.limit_segs or None]
        segs = [W["segs"][i] for i in sel]
        t1 = time.time(); n0 = R.ntok
        M1 = {k: [] for k in ["lp", "rank", "top1", "ent", "lpT"]}; BR = {}; ACT = []
        for i, seg in enumerate(segs):
            m1, res = R.run_segment(seg)
            for k in M1:
                M1[k].append(m1[k])
            ACT.append(res.pop("__act_lp", np.zeros(0, np.float32)))
            BR.update(res)
            if i % 20 == 0 or i == len(segs) - 1:
                el = time.time() - t1
                print(f"{ds} seg {i+1}/{len(segs)} {el:.0f}s tok={R.ntok-n0} {(R.ntok-n0)/max(el,1e-3):.0f} tok/s "
                      f"mem={torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
        np.savez(os.path.join(od, f"{ds}_m1.npz"), lp=np.concatenate(M1["lp"]).astype(np.float32),
                 rank=np.concatenate(M1["rank"]).astype(np.int32), top1=np.concatenate(M1["top1"]).astype(np.float16),
                 ent=np.concatenate(M1["ent"]).astype(np.float16), lpT=np.concatenate(M1["lpT"]).astype(np.float16),
                 tgrid=np.array(TGRID), seg_ids=np.array(sel), seg_ntok=np.array([len(s["score_pos"]) for s in segs]))
        pickle.dump(BR, open(os.path.join(od, f"{ds}_br.pkl"), "wb"), protocol=4)
        if any(len(x) for x in ACT):
            np.savez(os.path.join(od, f"{ds}_act.npz"), lp=np.concatenate(ACT), seg_ids=np.array(sel))
        json.dump(dict(seconds=time.time() - t1, tokens=R.ntok - n0, n_segs=len(segs), model=a.model, lora=a.lora,
                       gpu=torch.cuda.get_device_name(), max_mem_gb=torch.cuda.max_memory_allocated() / 1e9),
                  open(os.path.join(od, f"{ds}.done" if not a.limit_segs else f"{ds}.partial"), "w"))
        print(f"done {ds} {time.time()-t1:.0f}s", flush=True)


if __name__ == "__main__":
    main()
