"""Per-obs_kind size-multiplier matrix (gated metrics) from size_equiv_<ds>.json -> markdown."""
import json, sys
r = json.load(open(sys.argv[1]))
KINDS = ["test_run", "python_exec", "shell_other", "file_view", "search"]
for base, fmt in [("M1 recal content bits/tok", "[kind={k}]"), ("M2 NLL given true action bits/tok @T*", "[content/kind={k}]")]:
    allk = f"{base} [content]" if base.startswith("M1") else f"{base} [content/all]"
    outk = f"{base} [outcome]" if base.startswith("M1") else f"{base} [outcome/all]"
    cols = [("all content", allk), ("outcome tokens", outk)] + [(k, f"{base} {fmt.format(k=k)}") for k in KINDS]
    labels = [x["label"] for x in r[allk]["rows"]]
    print(f"\n**{base}: size multiplier n by obs_kind** (instruct-ladder gate PASS for every column)\n")
    print("| model | " + " | ".join(c for c, _ in cols) + " |")
    print("|---|" + "---|" * len(cols))
    for lab in labels:
        cells = []
        for _, key in cols:
            row = next((x for x in r.get(key, {}).get("rows", []) if x["label"] == lab), None)
            cells.append("–" if row is None else f"{row['n']} [{2**row['log2n_ci'][0]:.2f},{2**row['log2n_ci'][1]:.2f}]")
        print(f"| {lab} | " + " | ".join(cells) + " |")
