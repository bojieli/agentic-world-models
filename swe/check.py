"""Correctness check of run.py's tree-mask branch evaluation against plain sequential forwards (tiny model)."""
import pickle, sys, os, random
import numpy as np, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from torch import inference_mode
from run import Runner

path, wk = sys.argv[1], sys.argv[2]
R = Runner(path)
W = pickle.load(open(wk, "rb"))
rng = random.Random(0)


@inference_mode()
def lp_seq(ids):
    x = torch.tensor([ids], device="cuda")
    z = R.model.model(input_ids=x).last_hidden_state[0].float() @ R.W.T
    ls = torch.log_softmax(z, -1)
    return ls[:-1].gather(1, x[0, 1:, None])[:, 0].cpu().numpy(), ls


worst = {}
for seg in [s for s in W["segs"] if len(s["ids"]) < 9000 and any(b["t"] == "fork" for bl in s["branches"].values() for b in bl)][:3]:
    m1, res = R.run_segment(seg)
    ids = seg["ids"].tolist()
    ref, _ = lp_seq(ids)
    d = np.abs(m1["lp"] - ref[seg["score_pos"] - 1])
    worst["m1"] = max(worst.get("m1", 0), d.max())
    print("m1 maxdiff", d.max(), "mean", d.mean(), "n", len(d))
    for b, brs in list(seg["branches"].items()):
        for br in [x for x in brs if x["t"] == "fork"][:4]:
            ctx = ids[:b]
            r = res[br["key"]]
            if br["t"] == "nll":
                suf = br["nodes"][0]
                ref, _ = lp_seq(ctx + suf)
                ref = ref[len(ctx) - 1:][br["pos"]]
                dd = np.abs(r["lp"] - ref).max()
            elif br["t"] == "next":
                _, ls = lp_seq(ctx + br["nodes"][0])
                dd = np.abs(r - ls[-1][br["cands"]].cpu().numpy()).max()
            else:
                P = br["nodes"][0]; dd = 0
                for c, rr in zip(br["nodes"][1:], r):
                    ref, _ = lp_seq(ctx + P + c)
                    dd = max(dd, np.abs(rr - ref[-len(c):]).max())
            worst[br["t"]] = max(worst.get(br["t"], 0), dd)
            print(br["key"], br["t"], "maxdiff", round(float(dd), 4))
print("WORST", worst)
