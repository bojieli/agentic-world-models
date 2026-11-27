"""Generate -> execute in sandbox -> validate -> render -> items.jsonl.gz (+ stats.json).

usage: nice -n 19 python build.py [--per 300] [--cand 420] [--seed 20261126] [--workers 8]
"""
import argparse, collections, gzip, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen, execute, render, copymask

TOK_PATH = os.environ.get("QWEN_TOKENIZER", "Qwen/Qwen3-0.6B-Base")      # Qwen3 tokenizer files (copied from Qwen3-0.6B-Base)
MAX_TOKENS = 2000
PER_DEFAULT = {"S1": 300, "S2": 300, "S3": 300, "S4": 300, "S2h": 300, "S3h": 300}
CAND_DEFAULT = {"S1": 450, "S2": 900, "S3": 900, "S4": 450, "S2h": 700, "S3h": 700}


def length_tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(TOK_PATH)


def first_diff_step(sa, sb):
    for i, (a, b) in enumerate(zip(sa, sb)):
        if a != b:
            return i
    return min(len(sa), len(sb))


def check(item, res, tok):
    """reason string if the executed pair is unusable, else None."""
    ra, rb = res
    if "error" in ra or "error" in rb:
        return "container error"
    A, B = ra["steps"], rb["steps"]
    oa, ob = A[-1]["terminal"], B[-1]["terminal"]
    if oa == ob:
        return "outputs equal"
    if any(s["rc"] in (124, 137) for s in A + B):
        return "timeout"
    if item["pair_type"] == "action":
        k = first_diff_step(item["variants"][0]["steps"], item["variants"][1]["steps"])
        if item["variants"][0]["files"] != item["variants"][1]["files"] or [s["terminal"] for s in A[:k]] != [s["terminal"] for s in B[:k]]:
            return "action pair with differing state"
    if item["stratum"] != "S4":
        for s in A[:-1] + B[:-1]:
            if s["stderr"] and not s["cmd"].startswith("test "):
                return "unexpected stderr in context"
    else:
        if not any(s["rc"] != 0 or s["stderr"] for s in (A[-1], B[-1])):
            return "S4 without error"
    pa, pb = render.prefix_of(A), render.prefix_of(B)
    words = copymask.context_words(pa, pb)
    if copymask.noncopy_words(oa, words) == copymask.noncopy_words(ob, words):
        return "outputs differ only in copied words"
    longest = max(len(tok(p + o + render.END)["input_ids"]) for p in (pa, pb) for o in (oa, ob))
    if longest > MAX_TOKENS:
        return "too long"
    return None


def null_partners(items, seed):
    """derangement within (stratum, family): item i's contexts are scored with partner j's outputs."""
    rng = random.Random(f"null/{seed}")
    groups = collections.defaultdict(list)
    for it in items:
        groups[(it["stratum"], it["family"])].append(it["id"])
    part = {}
    for k in sorted(groups):
        ids = list(groups[k]); rng.shuffle(ids)
        for i, x in enumerate(ids):
            part[x] = ids[(i + 1) % len(ids)] if len(ids) > 1 else None
    return part


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per", type=int, default=None, help="pairs per stratum (default 300)")
    ap.add_argument("--cand", type=int, default=None, help="candidates per stratum (default S2/S3 900, S1/S4 450)")
    ap.add_argument("--strata", default="S1,S2,S3,S4")
    ap.add_argument("--seed", default="20261126")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(HERE, "items.jsonl.gz"))
    ap.add_argument("--id-tag", default="", help="inserted into item ids (e.g. 'x' -> S2-x0000) for extra batches")
    ap.add_argument("--dedup-against", default=None, help="existing items file(s), comma-separated: pairs identical to any are rejected")
    a = ap.parse_args()
    tok = length_tokenizer()
    cache = os.path.join(HERE, "work", "exec_cache.jsonl")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    final, rejects, seen = [], collections.Counter(), set()
    for fpath in (a.dedup_against.split(",") if a.dedup_against else []):
        for l in gzip.open(fpath, "rt"):
            x = json.loads(l)
            seen.add(tuple(p + "\x00" + o for p, o in zip(x["prefix"], x["output"])))
    strata = a.strata.split(",")
    for st in strata:
        per = a.per or PER_DEFAULT[st]
        cands = gen.candidates(st, a.cand or CAND_DEFAULT[st], a.seed)
        eps = [v for c in cands for v in c["variants"]]
        res = execute.run_many(eps, a.workers, cache)
        kept = 0
        for i, c in enumerate(cands):
            r = (res[2 * i], res[2 * i + 1])
            why = check(c, r, tok)
            if why is None:
                key = tuple(render.prefix_of(x["steps"]) + "\x00" + x["steps"][-1]["terminal"] for x in r)
                if key in seen or key[::-1] in seen:
                    why = "duplicate"
                seen.add(key)
            if why:
                rejects[(st, c["family"], why)] += 1
                continue
            if kept >= per:
                continue
            A, B = r[0]["steps"], r[1]["steps"]
            pa, pb = render.prefix_of(A), render.prefix_of(B)
            oa, ob = A[-1]["terminal"], B[-1]["terminal"]
            ta, spa = render.compose(pa, oa)
            tb, spb = render.compose(pb, ob)
            c = dict(c, id=f"{st}-{a.id_tag}{kept:04d}", env_id=c["gen_seed"])
            words = copymask.context_words(pa, pb)
            c["copy_mask"] = {m: [copymask.copy_ranges(o, words, m) for o in (oa, ob)] for m in ("nocopy", "strict")}
            c["executed"] = [A, B]
            c["final_tree"] = [r[0]["final_tree"], r[1]["final_tree"]]
            c["prefix"] = [pa, pb]
            c["output"] = [oa, ob]
            c["output_streams"] = [{"stdout": A[-1]["stdout"], "stderr": A[-1]["stderr"], "rc": A[-1]["rc"]},
                                   {"stdout": B[-1]["stdout"], "stderr": B[-1]["stderr"], "rc": B[-1]["rc"]}]
            c["text"] = [ta, tb]
            c["span"] = [list(spa), list(spb)]
            c["n_tokens_qwen3"] = [len(tok(ta)["input_ids"]), len(tok(tb)["input_ids"])]
            final.append(c)
            kept += 1
        print(f"[build] {st}: kept {kept}/{len(cands)}", file=sys.stderr, flush=True)
    part = null_partners(final, a.seed)
    for it in final:
        it["null_partner"] = part[it["id"]]
    with gzip.open(a.out, "wt") as f:
        for it in final:
            f.write(json.dumps(it) + "\n")
    stats = {"n": len(final), "per_stratum": {}, "rejects": {"|".join(k): v for k, v in sorted(rejects.items())}}
    for st in strata:
        its = [x for x in final if x["stratum"] == st]
        ob = [render.norm_bytes(o) - 1 for x in its for o in x["output"]]
        nt = [n for x in its for n in x["n_tokens_qwen3"]]
        ncb = [render.norm_bytes(o) - copymask.masked_bytes(o, x["copy_mask"]["nocopy"][v]) for x in its for v, o in enumerate(x["output"])]
        stats["per_stratum"][st] = {
            "n": len(its), "families": dict(collections.Counter(x["family"] for x in its)),
            "pair_type": dict(collections.Counter(x["pair_type"] for x in its)),
            "output_bytes_mean": sum(ob) / max(len(ob), 1), "output_bytes_max": max(ob, default=0),
            "noncopy_bytes_mean (incl. terminator)": sum(ncb) / max(len(ncb), 1),
            "noncopy_byte_frac": sum(ncb) / max(sum(ob) + len(ob), 1),
            "tokens_mean": sum(nt) / max(len(nt), 1), "tokens_max": max(nt, default=0),
            "n_steps_mean": sum(len(x["executed"][0]) for x in its) / max(len(its), 1),
            "final_nonzero_rc_frac": sum(x["output_streams"][v]["rc"] != 0 for x in its for v in (0, 1)) / max(2 * len(its), 1),
            "gap_hist": dict(collections.Counter(x["meta"].get("gap") for x in its)) if st.startswith("S3") else None,
        }
    json.dump(stats, open(a.out.replace(".jsonl.gz", "") + ".stats.json" if "items.jsonl.gz" not in a.out else os.path.join(HERE, "stats.json"), "w"), indent=1)
    print(json.dumps(stats["per_stratum"], indent=1))


if __name__ == "__main__":
    main()
