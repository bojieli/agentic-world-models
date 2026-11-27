#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
study=${1:?Usage: run_panel.sh sandbox|swe|terminal|agenticppl}
case "$study" in sandbox|swe|terminal|agenticppl) ;; *) exit 2 ;; esac
while IFS=$'\t' read -r model renders swe terminal ppl; do
    [[ "$model" == model ]] && continue
    case "$study" in
        sandbox)   if [[ "$renders" != - ]]; then sandbox/run_model.sh "$model" "$renders"; fi ;;
        swe)       if [[ "$swe" == yes ]]; then swe/run.sh "$model"; fi ;;
        terminal)  if [[ "$terminal" == yes ]]; then terminal/run.sh "$model"; fi ;;
        agenticppl) if [[ "$ppl" == yes ]]; then agenticppl/run_m5.sh "$model"; fi ;;
    esac
done < models.tsv
