#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
mkdir -p runs/items
python build.py --out runs/items/original.jsonl.gz
python build.py --strata S2h,S3h --out runs/items/hard.jsonl.gz
cat runs/items/original.jsonl.gz runs/items/hard.jsonl.gz > runs/items/v1.jsonl.gz
python build.py --strata S2,S3,S2h,S3h --per 600 --cand 1100 --seed 20261127 \
    --id-tag x --dedup-against runs/items/v1.jsonl.gz --out runs/items/extension.jsonl.gz
cat runs/items/v1.jsonl.gz runs/items/extension.jsonl.gz > runs/items/combined.jsonl.gz
