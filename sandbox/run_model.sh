#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
model=${1:?Usage: run_model.sh MODEL [plain,chat]}
python score2x2.py "$model" "${model##*/}" --render "${2:-plain}" --out runs
