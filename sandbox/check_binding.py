"""Verify released item scores against the original scorer summaries. CPU, standard library."""
import csv
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from compact_results import MASKS, METRICS

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
PRIMARY = {"S2", "S3", "S2h", "S3h"}


def main():
    with gzip.open(HERE / "items.jsonl.gz", "rt") as stream:
        items = {r["id"]: (r["stratum"], r["family"]) for r in map(json.loads, stream)}
    assert len(items) == 4200
    assert sum(s in PRIMARY for s, _ in items.values()) == 3600
    summaries = {(p.parent.parent.name, p.parent.name): p
                 for p in RESULTS.glob("*/*/summary.json")}
    scores = defaultdict(dict)
    with gzip.open(RESULTS / "binding.csv.gz", "rt", newline="") as stream:
        for row in csv.DictReader(stream):
            key = (row["model"], row["render"])
            item_id = row["item_id"]
            assert items[item_id] == (row["stratum"], row["family"]), (key, item_id)
            assert item_id not in scores[key], (key, item_id)
            scores[key][item_id] = [float(row[f"T1/{mask}/{metric}"])
                                    for mask in MASKS for metric in METRICS]
    assert scores.keys() == summaries.keys() and len(scores) == 33
    binding = {}
    for key, rows in sorted(scores.items()):
        assert rows.keys() == items.keys(), key
        with summaries[key].open() as stream:
            expected = json.load(stream)["summary"]["T=1"]
        for group in sorted({s for s, _ in items.values()} | {"primary"}):
            strata = PRIMARY if group == "primary" else {group}
            grouped = [v for i, v in rows.items() if items[i][0] in strata]
            for j, (mask, metric) in enumerate((m, k) for m in MASKS for k in METRICS):
                target = expected[mask][group]
                actual = fmean(v[j] for v in grouped)
                assert len(grouped) == target["n"]
                assert math.isclose(actual, target[metric], abs_tol=1e-10), (key, group, mask, metric)
                if (mask, metric, group) == ("nocopy", "bind", "primary"):
                    binding[key] = actual * 100
    print("Model / render                         Primary %    Δ instruct    Δ base")
    for (name, render), acc in sorted(binding.items()):
        size = next(s for s in ("0.6B", "1.7B", "32B", "14B", "4B", "8B")
                    if name.lower().endswith(s.lower()) or f"-{s.lower()}-" in name.lower())
        inst = binding[f"Qwen3-{size}", render]
        base = binding.get((f"Qwen3-{size}-Base", render))
        delta = "—" if base is None else f"{acc - base:+.1f}"
        print(f"{name + ' / ' + render:38} {acc:7.1f} {acc-inst:+13.1f} {delta:>9}")
    print(f"Verified {sum(map(len, scores.values())):,} rows across {len(scores)} model/render runs.")


if __name__ == "__main__":
    main()
