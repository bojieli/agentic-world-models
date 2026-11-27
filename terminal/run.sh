#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
model=${1:?Usage: run.sh MODEL}
test -f prep.json || python prep.py
mkdir -p runs
python score.py "$model" "${model##*/}" --out runs
python copytest.py "$model" "${model##*/}" runs
