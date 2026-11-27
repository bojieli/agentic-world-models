"""Forest-plot table from size_equiv_<ds>.json: model, delta, log2 n, CI, censoring; n only for gated metrics."""
import json, sys, os
p = sys.argv[1]
r = json.load(open(p))
GATED = ["M1 recal content bits/tok [content]", "M1 recal content bits/tok [outcome]"] + \
        [f"M1 recal content bits/tok [kind={k}]" for k in ["test_run", "python_exec", "shell_other", "file_view", "search"]] + \
        ["M2 NLL given true action bits/tok @T* [content/all]", "M2 NLL given true action bits/tok @T* [outcome/all]"] + \
        [f"M2 NLL given true action bits/tok @T* [content/kind={k}]" for k in ["test_run", "python_exec", "shell_other", "file_view", "search"]]
UNGATED = ["M2 abs info gain bits/tok [content/all]", "M2 abs info gain bits/tok @T* [content/all]", "M2 relative gain [content/all]"] + \
          [f"M2 abs info gain bits/tok [content/kind={k}]" for k in ["test_run", "python_exec", "shell_other", "file_view", "search"]] + \
          ["Reading: next-action bits/tok saved by seeing the obs [all]"] + \
          [f"Reading: next-action bits/tok saved by seeing the obs [kind={k}]" for k in ["test_run", "python_exec", "shell_other", "file_view", "search"]]
only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
for group, keys, show_n in [("GATED (size multiplier reported)", GATED, True), ("FAILS LADDER GATE (Δ only)", UNGATED, False)]:
    print(f"\n### {group}\n")
    for k in keys:
        if k not in r:
            continue
        g = r[k]["ladders"].get("inst", {})
        print(f"\n**{k}** ({'higher' if r[k]['higher_is_better'] else 'lower'} is better; instruct ladder "
              + ", ".join(f"{s} {v:.3f}" for s, v in g.get("points", {}).items()) + f"; gate {'PASS' if g.get('gate') else 'FAIL'})\n")
        print("| model | start | Δ [95% CI] |" + (" n | log2 n [95% CI] | censored draws (low/high) |" if show_n else ""))
        print("|---|---|---|" + ("---|---|---|" if show_n else ""))
        for x in r[k]["rows"]:
            if only and not any(o in x["label"] for o in only):
                continue
            row = f"| {x['label']} | {x['start']} | {x['delta']:+.4f} [{x['delta_ci'][0]:+.4f}, {x['delta_ci'][1]:+.4f}] |"
            if show_n:
                row += f" {x['n']} | {x['log2n']:+.2f} [{x['log2n_ci'][0]:+.2f}, {x['log2n_ci'][1]:+.2f}] | {x['frac_censored_low']:.2f}/{x['frac_censored_high']:.2f} |"
            print(row)
