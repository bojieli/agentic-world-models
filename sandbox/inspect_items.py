"""Print N random items (seeded) for hand inspection: both transcripts, the scored outputs and their copy masks.
usage: inspect_items.py [--n 20] [--seed 7] [--strata S2,S3]"""
import argparse, gzip, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render


def show_mask(o, ranges):
    b = o.encode()
    out, p = b"", 0
    for s, e in ranges:
        out += b[p:s] + b"[[" + b[s:e] + b"]]"; p = e
    return (out + b[p:]).decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20); ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--strata", default=None)
    a = ap.parse_args()
    items = [json.loads(l) for l in gzip.open(os.path.join(HERE, "items.jsonl.gz"), "rt")]
    if a.strata:
        items = [x for x in items if x["stratum"] in a.strata.split(",")]
    for it in random.Random(a.seed).sample(items, a.n):
        print("=" * 100)
        print(f"{it['id']}  {it['family']}  pair={it['pair_type']}  diff={it['diff']}  meta={it['meta']}")
        for v in range(2):
            t, sp = it["text"][v], it["span"][v]
            tb = t.encode()
            assert tb[sp[0]:sp[1]].decode() == it["output"][v] + render.END
            print(f"--- variant {'ab'[v]} ({it['n_tokens_qwen3'][v]} tok), rc={it['output_streams'][v]['rc']}")
            print(tb[:sp[0]].decode() + ">>>" + tb[sp[0]:sp[1]].decode() + "<<<")
            print("    nocopy mask ([[copied]]):", repr(show_mask(it["output"][v], it["copy_mask"]["nocopy"][v])))
        print("outputs differ:", it["output"][0] != it["output"][1])


if __name__ == "__main__":
    main()
