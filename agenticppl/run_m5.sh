#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
model=${1:?Usage: run_m5.sh MODEL}
python m5.py "$model" "${model##*/}" --split heldout --out runs
