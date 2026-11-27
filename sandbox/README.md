# Counterfactual execution benchmark

Only one command or state change distinguishes the two branches of each generated environment. Both outputs were produced by execution. The primary pool contains 3,600 of the 4,200 pairs. [Run instructions](../README.md#reproduce-the-study) · [Validation](../writeups/SANDBOX_VALIDATION.md)

## Grammar (fixed, safe)

A command line is `PART` or `PART; echo $?`; a part is a head command optionally piped (`|`) into filters.
Paths are relative, never `..`, never absolute; literals are `[A-Za-z0-9_:=,. -]`; no `$(…)`, backticks,
redirections other than `< file` and `>> file`, no `&&`, no free-form shell.

* head commands: `ls [-1|-1A] [P…]`, `cat P…`, `wc -l|-w|-c [<] P…`, `grep [-c -n -i -v -l -q -w] LIT P…`,
  `head -n N P`, `tail -n N P`, `sort [-n|-r|-nr|-u|-t, -kK [-n|-nr|-r]] P`, `cut -d, -fK P`, `uniq [-c] P`,
  `find .[/P] [-name 'GLOB'] [-type f|d]`, `sed -n 'N[,M]p' P`, `sed -i 's/X/Y/[g]' P`, `python P [ARG…]`,
  `test -f|-d|-e P`, `echo $?`, `echo LIT >> P`, `mkdir [-p] P`, `mv P P`, `cp P P`, `chmod 000|400|444|600|644|755 P`
* pipe filters: `sort…`, `uniq [-c]`, `head -n N`, `tail -n N`, `wc -l|-w|-c`, `cut -d, -fK`, `grep [-c -n -i -v] LIT`
* python scripts are generated from templates (loops, argv, file parsing, string ops, CSV group-by, json, deliberate bugs).

## Sandbox

Every episode (= one variant of one item) runs in its own `podman run --rm` container (podman 3.4.4 rootless,
image `docker.io/library/python:3.12-slim`, GNU coreutils 9.7, Python 3.12.16):
`--network=none --read-only` rootfs, tmpfs `/home/user` (64 MB, the work dir `/home/user/project`) and `/tmp`,
uid/gid 65534 (so `chmod 000` really denies), `--cap-drop=ALL`, `no-new-privileges`, cgroup memory 512 MB and
pids 128, `RLIMIT_CPU` 30 s, `RLIMIT_FSIZE` 8 MB, per-command `timeout -s KILL 5`, 60 s per container.  The only
host path visible inside is `runner.py` (read-only bind).  Execution uses up to eight workers at reduced scheduling priority.  Environment: `LC_ALL=C.UTF-8`, `TZ=UTC`,
`PYTHONUNBUFFERED=1` (so stdout/stderr interleave as on a tty), `PYTHONHASHSEED=0`.
Each step runs as `bash -c '(exit $prev_rc); CMD'`, so `$?` carries across steps as in a live shell.
stdout and stderr are read through separate pipes with a selector and also concatenated in arrival order
(`terminal`), which is what the transcript shows.

## Items

`items.jsonl.gz`, one JSON object per pair:
`id, stratum, family, pair_type (action|state), diff, meta (gap, change_step, err, swapped), env_id,
variants[2] (files, dirs, modes, steps), executed[2] (per step: cmd, stdout, stderr, terminal, rc), final_tree[2],
prefix[2], output[2], output_streams[2] (stdout, stderr, rc of the scored step), text[2], span[2] (byte span of
output+terminator in text), copy_mask{nocopy,strict}[2] (byte ranges of copied words), n_tokens_qwen3[2],
null_partner`.

* **action pairs**: same state, different command (flag, path, pattern, argument); everything before the differing
  step is identical (checked on the executed outputs).
* **state pairs**: same final command; the state differs by one changed / inserted line, a loop bound, an earlier
  edit present vs absent, a different edit target or value, `mv` vs `cp`, `chmod` mode.
* Orientation (which variant is a) is a coin flip, so the null has mean 0 by construction.
* Every fact needed is visible in the transcript (`cat`, `ls -1`, `find`, or the edit commands themselves).
* Validity filters (counts in `stats.json`): container ok, no timeouts, outputs differ, action pairs share
  their executed prefix, no unexpected stderr in context (S1–S3), S4 has an error on at least one side, the pair's
  outputs differ in at least one NON-COPY word, <= 2000 Qwen3 tokens for every 2x2 combination, no duplicates.

Strata:

* **S1 single-step effects** (secondary): grep counts, `wc`, `test -f/-d` + `echo $?` (one- and two-step), `grep -q`.
* **S2 computed values** (primary): script results under a changed loop bound / argument / data line / literal,
  arithmetic, CSV group-by sums, `cut | sort | uniq -c`, `sort -t, -k` orders.
* **S3 multi-step state tracking** (primary): a state change at step k (`echo >>`, `sed -i`, `mv`/`cp`, `mkdir`),
  then 1–5 distractor steps on other files, then an inspection 2–6 steps after the change (`wc -l`, `grep -c`,
  `ls | wc -l`, `test -f; echo $?`, `python` on the edited file).  The counterfactual replaces the change by an
  edit of another file, a no-op inspection, a different value, or `cp` for `mv`.
* **S4 errors** (secondary): which exception / message and where — IndexError and its line, SyntaxError /
  IndentationError kind and line, ValueError vs ZeroDivisionError from data, KeyError, NameError, JSONDecodeError,
  missing files (coreutils and FileNotFoundError), `chmod`-induced permission errors, `mkdir` on existing dirs, exit codes.
* **S2h hard computed values** (primary, added after the v0 gate showed S2 at 0.90 already for Qwen3-1.7B-Base):
  outputs depend NON-MONOTONICALLY on a minimal change (+1 loop bound, ±1–3 literal, argument n vs n+1..3,
  one data value ±small): modular recurrences, `(a*b) % M`, digit sums / digital roots, xor/and/popcount, Collatz
  steps, nested-loop counts, filtered sums mod 10.  "Bigger input -> bigger number" heuristics cannot bind.
* **S3h hard state tracking** (primary): 3–5 edits (to the inspected file AND to other files: `echo >>`,
  `sed -i` in both directions, `mv`/`cp` chains between directories, several `sed -i` on config values) interleaved
  with distractors; exactly one edit differs (redirected to another file, other op, other destination, other value);
  inspection by a count or a modular computation over the final state.

### Stats (`stats.json`; rejection counts per family and reason are in it too)

| stratum | pairs | families | action / state | mean output bytes | non-copy byte frac | mean Qwen3 tokens (max) | mean steps | scored step rc!=0 |
|---|---|---|---|---|---|---|---|---|
| S1 | 300 | 8 | 227 / 73 | 6.0 | 0.56 | 86 (303) | 2.2 | 0.06 |
| S2 | 300 | 11 | 120 / 180 | 31.8 | 0.56 | 85 (189) | 2.2 | 0.00 |
| S3 | 300 | 10 | 0 / 300 | 4.5 | 0.82 | 115 (294) | 7.7 | 0.15 |
| S4 | 300 | 12 | 56 / 244 | 142.6 | 0.87 | 90 (335) | 2.7 | 0.56 |
| S2h | 300 | 6 | 78 / 222 | 5.1 | 1.00 | 71 (179) | 2.3 | 0.00 |
| S3h | 300 | 4 | 0 / 300 | 2.8 | 1.00 | 203 (436) | 13.2 | 0.01 |

S3 gap (steps from change to inspection): {'2': 59, '3': 59, '4': 62, '5': 63, '6': 57}

S3h gap (steps from change to inspection): {'2': 56, '3': 59, '4': 61, '5': 57, '6': 67}

* S1 families: s1_grep_count_pattern 39, s1_wc_path 38, s1_wc_flag 38, s1_count_state 38, s1_test_exists 38, s1_test_state 35, s1_grep_q_exit 38, s1_grep_flag 36
* S2 families: s2_loop_bound 32, s2_argv 31, s2_data_line 30, s2_sort_key 36, s2_uniq_count 34, s2_uniq_state 22, s2_py_string 24, s2_arith 36, s2_csv_group 36, s2_head_tail_sort 17, s2_sort_flag 2
* S3 families: s3_append_present 32, s3_sed_present 32, s3_mv_cp 29, s3_cp_alias 32, s3_multi_append 32, s3_mkdir_mv_find 27, s3_sed_count 30, s3_sed_number_python 31, s3_append_python 28, s3_append_value 27
* S4 families: s4_py_index 29, s4_py_where 28, s4_py_syntax 21, s4_py_exc_type 20, s4_py_keyerror 27, s4_py_nameerror 14, s4_json_decode 27, s4_missing_file 28, s4_py_missing_file 28, s4_permission 22, s4_mkdir_exists 28, s4_exit_code 28
* S2h families: h_mod_loop 61, h_mod_arith 62, h_argv 57, h_nested 40, h_list_key 59, h_csv_filter 21
* S3h families: h3_grep_net 49, h3_config_mod 98, h3_append_mod 112, h3_mv_chain 41

(S3h: the differing edit is at least `gap` steps before the inspection; non-copy byte fraction includes the terminator.)


## Rendering

Plain (all models): `$ cmd\n<output>$ cmd\n<output>…$ cmd\n<OUTPUT>$` — no header, no JSON, no chat markup.
The scored span is OUTPUT plus the `$` of the next prompt (so knowing where the output ends is scored too;
otherwise `head -n 2` vs `head -n 4` would be free).  Byte span: `render.compose(prefix, output)`.

Native chat (instruct / post-trained models, `--render chat`): user = a one-line instruction + the plain prefix;
assistant = OUTPUT; scored = OUTPUT + the template's end-of-turn marker (`<|im_end|>` for Qwen3).  Built with the
model's own `apply_chat_template(..., enable_thinking=False)` via a sentinel, so the empty think block of Qwen3
templates is included exactly as the template emits it.

## Scoring (`score2x2.py`)

Per item: 8 teacher-forced sequences, {c, c'} x {o, o', q, q'}, where (q, q') are the outputs of the item's null
partner (another item of the same family; derangement fixed in the dataset).  Scored tokens are those overlapping
the output byte span (offset mapping, so any fast tokenizer works); with masks `nocopy` (primary) and `strict` a
token is dropped if any of its bytes belongs to a copied word.  Copied word = an `[A-Za-z0-9_]+` run that occurs as
a whole word anywhere in either variant's prefix (commands and earlier outputs); `nocopy` exempts numbers of <= 2
digits (counts, exit codes, line numbers: their occurrence in context is coincidental), `strict` does not.
Denominators are the unmasked output bytes (+1 for the terminator), tokenizer independent.

Metrics per item, for 3 masks x 26 temperatures (0.5..3.0; 0.6B–8B instruct runs used 0.5..2.0):
`I_bits`, `I_bpb = I_bits / (B_o + B_o')`, `bind = 1[I > 0]` (0.5 on ties), `IG = mean over o,o' of
(NLL(o|c') - NLL(o|c)) / NLL(o|c')`, `gain_bpb`, and the same with the null partner (`null_*`).
**Primary metric: binding accuracy, mask nocopy, T = 1, on S2, S3, S2h, S3h (pools `S2+S3`, `S2h+S3h`, `primary`).**  T* (per model and rendering) minimises the NLL
of the true outputs in their own contexts and is reported as a secondary view.
Bootstrap: clusters = `env_id` (one generated environment per item, so env-clusters coincide with items here).

Outputs, per model and rendering, in `results/<NAME>/<render>/`:
`lp.npz` (full `lp[item, ctx, out, mask, T]` in nats, `den[item, out, mask]` bytes, token counts, ids),
`per_item.jsonl` (item-aligned metrics at T=1 and T* for each mask; this is the input to `gate.py` and
`size_equiv_cf.py`), `summary.json`, `summary.md`.

## Size-equivalent analysis

`size_equiv_cf.py` mirrors `../swe/size_equiv.py` (same ladders, same POST map, same non-embedding
params from `../swe/configs/params.json`, same `(kind, num, den)` spec format and value()).  Its loader
`per_item_specs(name, render, mask, temp, ids, results)` returns per-item numerator/denominator arrays for
`binding acc`, `interaction bits/byte`, `info gain` (kind `gain`: 1 - ΣNLL(o|c)/ΣNLL(o|c')) and `null binding`, per
stratum and pooled S2+S3, so it can also be plugged into the SWE analysis’s `per_traj` hook.  CIs: one joint env-cluster bootstrap.
