"""Extract both T=1 masks from complete scorer runs, preserving float precision."""
import argparse
import csv
import gzip
import io
import json
from pathlib import Path

METRICS = ("bind", "I_bpb", "IG")
MASKS = ("nocopy", "all")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    files = sorted(args.results.glob("*/*/per_item.jsonl"))
    if not files:
        parser.error("No per_item.jsonl files under the input directory")
    columns = [(mask, metric) for mask in MASKS for metric in METRICS]
    with args.output.open("wb") as raw, gzip.GzipFile(
        fileobj=raw, filename="", mode="wb", compresslevel=8, mtime=0
    ) as compressed, io.TextIOWrapper(compressed, encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["model", "render", "item_id", "stratum", "family"] +
                        [f"T1/{mask}/{metric}" for mask, metric in columns])
        for path in files:
            model, render, _ = path.relative_to(args.results).parts
            with path.open() as stream:
                for item in map(json.loads, stream):
                    writer.writerow([model, render, item["id"], item["stratum"], item["family"]] +
                                    [item[f"T1/{mask}"][metric] for mask, metric in columns])


if __name__ == "__main__":
    main()
