"""Print the all-model results table (mask nocopy, T=1) used in VALIDATION.md."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
models = sys.argv[1:] or ["Qwen3-0.6B-Base", "Qwen3-1.7B-Base", "Qwen3-0.6B", "Qwen3-4B", "Qwen3-8B", "Qwen3-14B"]
print("| model | render | stratum | binding acc [95% CI] | interaction bits/byte [CI] | mean I (bits/pair) | info gain [CI] | null binding [CI] | null interaction bpb [CI] | binding at T* |")
print("|---|---|---|---|---|---|---|---|---|---|")
for m in models:
    for r in ["plain", "chat"]:
        p = os.path.join(HERE, "results", m, r, "summary.json")
        if not os.path.exists(p):
            continue
        S = json.load(open(p))
        s = S["summary"]["T=1"]["nocopy"]; Tk = [k for k in S["summary"] if k != "T=1"][0]
        for st in ["S2", "S3", "S2h", "S3h", "primary", "S1", "S4"]:
            x = s[st]
            f = lambda k: "%.3f [%.3f,%.3f]" % (x[k], *x[k + "_ci"])
            print("| %s | %s | %s | %s | %s | %.1f | %s | %s | %s | %.3f (%s) |" % (m, r, st, f("bind"), f("I_bpb"), x["I_bits"], f("IG"),
                  f("null_bind"), f("null_I_bpb"), S["summary"][Tk]["nocopy"][st]["bind"], Tk))
