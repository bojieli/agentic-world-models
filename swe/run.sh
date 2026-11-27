#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
model=${1:?Usage: run.sh MODEL}
if [[ ! -f work/swe.pkl ]]; then
    python prep2.py --datasets swe --max-segs-swe 1 --no-m3m4 --reading
fi
python prep2.py --datasets swe --hash-only work/reference.json
P2_TOK="$model" python prep2.py --datasets swe --hash-only work/candidate.json
cmp work/reference.json work/candidate.json
python run.py "$model" "${model##*/}" --ds swe --out runs
