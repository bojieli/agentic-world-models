"""Independent check of pipeline per-token logprobs: plain full forward (no cache/chunking), same token ids from tok/_shared."""
import sys, json, numpy as np, torch, gc
from transformers import AutoModelForCausalLM, AutoTokenizer
models = sys.argv[1:]  # pairs name=path
fmt = "native"
meta = np.load(f"tok/_shared/{fmt}.npz")
off = meta["offsets"]; ids_all = meta["ids"]; typ = meta["typ"]; cp = meta["copy"]
# pick 3 short trajectories
pick = [i for i in range(len(off) - 1) if off[i + 1] - off[i] < 7000][:3]
res = {}
for spec in models:
    name, path = spec.split("=")
    tok = AutoTokenizer.from_pretrained(path)
    m = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, device_map="cuda", attn_implementation="sdpa").eval()
    pipe = np.load(f"tok/{name}/{fmt}.npz")["lp"].astype(np.float64)
    lps = []
    for i in pick:
        a, b = off[i], off[i + 1]
        tgt = ids_all[a:b]
        # first token of the sequence is not stored; native rendering starts with <|im_start|>
        first = tok.convert_tokens_to_ids("<|im_start|>")
        seq = [first] + tgt.tolist()
        with torch.inference_mode():
            lg = m(input_ids=torch.tensor([seq], device="cuda")).logits[0, :-1].float()
            lp = torch.log_softmax(lg, -1).gather(1, torch.tensor(tgt, device="cuda")[:, None].long())[:, 0].cpu().numpy()
        d = np.abs(lp - pipe[a:b])
        print(f"{name} traj{i} N={b-a} maxdiff={d.max():.3f} meandiff={d.mean():.4f} mean_lp_pipe={pipe[a:b].mean():.4f} mean_lp_plain={lp.mean():.4f}", flush=True)
        lps.append(lp)
    res[name] = lps
    # template sanity: does the model's own chat template render a user/assistant turn identically to ours?
    msgs = [{"role": "user", "content": "TASK"}, {"role": "assistant", "content": "ACT"}, {"role": "user", "content": "OBS"}]
    print(name, "own template:", repr(tok.apply_chat_template(msgs, tokenize=False)), flush=True)
    del m; gc.collect(); torch.cuda.empty_cache()
# hostname-copy tokens: observation tokens with copy flag on prompt lines
names = list(res)
tokz = AutoTokenizer.from_pretrained(models[0].split("=")[1])
for k, i in enumerate(pick[:1]):
    a, b = off[i], off[i + 1]
    tgt = ids_all[a:b]; t = typ[a:b]
    txt = [tokz.decode([x]) for x in tgt]
    # find obs tokens that are part of 'root@<host>' strings
    shown = 0
    for j in range(len(tgt)):
        if t[j] == 3 and "@" in txt[j] and shown < 3:
            seg = range(j - 1, min(j + 8, len(tgt)))
            print("context:", repr("".join(txt[max(0, j - 6):j])))
            for q in seg:
                print(f"  {txt[q]!r:>14} copy={cp[a+q]} " + " ".join(f"{n}:{-res[n][k][q]/np.log(2):6.2f}b" for n in names))
            shown += 1
