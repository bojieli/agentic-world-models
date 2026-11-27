# Validation (2026-11-26, extended 2026-11-27)

Dataset: `items.jsonl.gz` v1 = v0 (S1–S4, 4×300) + hard strata (S2h, S3h, 2×300), seed `20261126`.
All numbers below: mask `nocopy`, T = 1, plain rendering unless noted; 95% CIs from env-cluster bootstrap
(2000 draws); "paired" CIs share one resample across models.  Raw: `results/<model>/<render>/`, gate tables in
`results/gate_*.md`, v0-only base runs in `results_v0/`.

## 1. Hand check (20 random items, `inspect_items.py --n 20 --seed 7`)

Mix: 8 S1, 3 S2, 5 S3, 4 S4 (s3_sed_number_python ×2, s2_csv_group, s1_test_exists ×3, s1_grep_q_exit, s4_py_syntax,
s1_count_state ×2, s3_mkdir_mv_find, s4_json_decode, s1_grep_flag, s4_missing_file, s2_uniq_state, s3_append_value,
s3_sed_count, s1_wc_path, s2_loop_bound, s4_py_index).

* **Outputs differ in all 20/20 pairs**, and for each one the difference is the intended one (count ±1, 0 vs 1 exit
  code, different sum, traceback vs value, different exception and line).
* **Rendering correct in 20/20**: the script asserts that the stored byte span decodes to exactly OUTPUT + `$`;
  by eye, every transcript is a plain `$ cmd` / output sequence, earlier outputs are the really executed ones,
  action pairs share their prefix and state pairs differ only where intended.
* Values recomputed by hand: e.g. S2-0008 group-by sums (ops 97+58 = 155; with peggy moved to ops 179, hr 26);
  S3-0063 hours 18×2 = 36, sum 30 vs 11×2 = 22, sum 23; S1-0118 `grep -c note` = 1 (case-sensitive) vs `grep -vc` = 5;
  S2-0192 Fibonacci range(8) = 21 vs range(6) = 8.  All correct.
* Extra checks: 10 S2/S3 items (seed 11) and 8 S2h/S3h items (seed 3) in compact form, all correct
  (e.g. S2h-0133 (97·3) mod 13 = 5, (97+9) mod 31 = 13, 291 // 31 = 9).
* Things seen that are true behaviour, not bugs: GNU coreutils in `C.UTF-8` uses curly quotes in some messages
  (`mkdir: cannot create directory ‘docs’: File exists`); `json.load` tracebacks include stdlib frames (long S4
  outputs); in some S3 counterfactuals the replaced edit is a no-op (e.g. `sed -i 's/INFO/ERROR/g'` when no INFO is
  present), which is the intended "edit absent / different edit" contrast.

## 2. Scorer checks

* Fast path (hidden states gathered at scored positions, padded bf16 batches) vs a per-sequence full-logits
  reference on 16 sequences: agreement within 0.04–0.34 nats per sequence (bf16 / padding numerics), no sign or
  token-selection differences.  Token selection inspected: scored tokens are exactly the output tokens plus `$`
  (`<|im_end|>` in chat); no sequence has a first scored token straddling the context boundary (`straddle_frac` = 0);
  no (item, ctx, output) ends up with zero scored nocopy tokens.
* Determinism: the v1 base runs reproduce the v0 base runs to 3 decimals on S1–S4.

## 3. v0 gate (S2, S3; base models)

| model | S2 binding | S3 binding | S2+S3 binding | S2+S3 interaction bpb | S2+S3 info gain | null binding | null bpb |
|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 0.830 [0.787,0.870] | 0.613 [0.560,0.667] | 0.722 [0.685,0.755] | 0.263 [0.223,0.302] | 0.130 | 0.512 | −0.006 [−0.019,0.007] |
| Qwen3-1.7B-Base | 0.900 [0.867,0.933] | 0.757 [0.707,0.807] | 0.828 [0.798,0.858] | 0.420 [0.369,0.472] | 0.235 | 0.475 | −0.010 [−0.025,0.005] |
| paired Δ | +0.070 [+0.027,+0.113] | +0.143 [+0.080,+0.207] | +0.107 [+0.068,+0.147] | | | | |

**v0 gate: PASS** — null ≈ 0 (binding ≈ 0.5, interaction ≈ 0 bits/byte), both strata above chance, and both rise
from 0.6B to 1.7B with paired CIs above 0.  S1 0.583 → 0.637 (step CI touches 0), S4 0.737 → 0.880.
Without the copy mask (`all`) S2 is 0.850/0.930, i.e. copying explains little of S2; the mask matters most in S4.
Because S2 was already at 0.90 for a 1.7B base model, the benchmark added the hard strata S2h and S3h (README) before the
ladder; base results on them: 0.6B-Base S2h 0.587, S3h 0.517; 1.7B-Base S2h 0.600, S3h 0.503 (primary pool
0.637 → 0.690, Δ +0.053 [+0.020,+0.086]).

## 4. Ladder gate (Qwen3 instruct)

The initial gate used the following instruct checkpoints.

Binding accuracy, plain rendering (`results/gate_ladder_plain.md`):

| stratum | 0.6B | 4B | 8B | 14B | steps (paired 95% CI) | gate |
|---|---|---|---|---|---|---|
| S2 | 0.780 | 0.920 | 0.873 | 0.897 | +.140 [+.087,+.193], −.047 [−.083,−.003], +.023 [−.017,+.063] | FAIL (≈ceiling, non-monotone) |
| S3 | 0.580 | 0.700 | 0.810 | 0.847 | +.120 [+.050,+.190], +.110 [+.053,+.167], +.037 [−.017,+.093] | FAIL at 8B→14B only |
| S2h | 0.530 | 0.610 | 0.600 | 0.700 | +.080 [+.010,+.153], −.010 [−.087,+.063], +.100 [+.030,+.167] | FAIL (4B→8B flat) |
| S3h | 0.500 | 0.503 | 0.603 | 0.560 | +.003, +.100 [+.023,+.177], −.043 | FAIL (near floor) |
| S2+S3 | 0.680 | 0.810 | 0.842 | 0.872 | +.130 [+.088,+.173], +.032 [−.005,+.068], +.030 [−.005,+.065] | FAIL |
| **primary (S2,S3,S2h,S3h)** | 0.598 | 0.683 | 0.722 | 0.751 | +.086 [+.049,+.121], +.038 [+.006,+.072], +.029 [−.001,+.061] | FAIL by a hair at 8B→14B |
| primary, at T* | 0.598 | 0.691 | 0.720 | 0.756 | +.092 [+.057,+.128], +.029 [−.003,+.063], +.036 [+.005,+.067] | FAIL at 4B→8B |

The 0.6B → 4B → 8B part of the initial ladder **passes on the primary pool** (both steps' CIs > 0), and nothing is
near a ceiling (14B: 0.751; top single stratum S3 at 0.847).  Native chat rendering (`gate_ladder_chat.md`):
primary 0.560 → 0.683 → 0.695 → 0.760 (4B→8B step +.012 [−.018,+.044], FAIL); S2+S3 0.608 → 0.778 → 0.853 → 0.865.

Secondary, interaction in bits/byte (`gate_ladder_plain_I_bpb.md`), primary: 0.115 → 0.441 → 0.495 → 0.733,
every step's paired CI > 0 (+.326, +.054 [+.025,+.085], +.238).  It keeps growing where binding flattens.
Information gain as ratio-of-sums (`size_equiv_cf.py`), S2+S3: 0.151 → 0.511 → 0.565 → 0.714.
Ladder slopes per doubling of non-embedding params (instruct, plain): binding primary b = +0.031
[+0.025,+0.038]; S3 +0.055; S2h +0.030; S2 +0.024; S3h +0.016.

Reading: binding accuracy is a sign statistic over 1200 pairs, so a 2× step (8B→14B) moves it by about 0.03, roughly
the size of its CI.  The pass/fail verdict on single steps hinges on power, not on a ceiling.  Instruct models also score
below base models of the same size (primary 0.598 vs 0.637 at 0.6B), and S2 dips at 8B: the instruct ladder is not a
clean scale series.

## 4b. Power extension (added AFTER the original gate narrowly failed at 8B→14B)

The pre-registered primary metric is unchanged: pooled binding accuracy (nocopy, T = 1) over S2, S3, S2h, S3h.
**The extension batch was generated after the original 1200-pair gate failed at 8B→14B** (lower CI −0.001).
Its purpose is power, not a different test.  It is a NEW independent batch from the same generator and the same
strata mix with a fresh seed (`20261127`): 600 pairs each of S2, S3, S2h, S3h = 2400 pairs.  Ids are `S2-x0000…`,
the batch is deduplicated against v1 (0 duplicates, 0 shared environments), and the files are
`items_ext.jsonl.gz` / `items_ext.stats.json`.
Dataset v2 = v1 + extension = 4200 pairs, 3600 of them primary.  All models were rescored on v2 (`results/`); the v1 results below provide the original gate for comparison.

Hand check of 10 extension items (seed 2027): 10/10 outputs differ, 10/10 renderings are
correct, and all values were recomputed by hand and correct.  The items were S2 data_line, uniq_count and arith;
S2h nested, list_key, argv and mod_arith; S3 sed_number_python and cp_alias; S3h append_mod.  Examples:
(82·17) mod 11 = 8, (82+51) mod 23 = 18, 1394 // 23 = 60; nested-loop count 3 → 4 when the bound goes 6 → 7;
appends to nums.txt n = 6, Σ mod 7 = 1 vs n = 5, Σ mod 7 = 5 when one append is redirected.

Primary binding accuracy, Qwen3 instruct, plain (paired steps, 95% CI, joint env-cluster bootstrap, 2000 draws):

| set | n | 0.6B | 4B | 8B | 14B | 0.6→4B | 4→8B | 8→14B | gate |
|---|---|---|---|---|---|---|---|---|---|
| (a) original 1200, v1 run (pre-registered) | 1200 | 0.598 | 0.683 | 0.722 | 0.751 | +.086 [+.049,+.121] | +.038 [+.006,+.072] | +.029 [−.001,+.061] | **FAIL** (8→14B) |
| (a′) original 1200, rescored in the v2 run | 1200 | 0.596 | 0.684 | 0.719 | 0.752 | +.088 [+.052,+.125] | +.035 [+.002,+.068] | +.033 [+.002,+.066] | pass (borderline) |
| extension only | 2400 | 0.609 | 0.689 | 0.716 | 0.753 | +.080 [+.056,+.103] | +.028 [+.006,+.050] | +.037 [+.016,+.057] | PASS |
| **(b) combined** | **3600** | **0.604** | **0.687** | **0.717** | **0.753** | **+.083 [+.063,+.103]** | **+.030 [+.012,+.048]** | **+.036 [+.019,+.054]** | **PASS** |

(a′) vs (a): the same items and models, only the batch composition differs.  bf16 numerics flip the sign of 0.7–0.8%
of items, which is enough to move the 8→14B lower bound from −0.001 to +0.002.  The original-set verdict is therefore
a coin toss at the margin.  The verdict of record for (a) is the pre-registered v1 run: FAIL.

Native chat rendering, combined 3600: 0.557 → 0.674 → 0.698 → 0.751; steps +.117 [+.096,+.139], +.025
[+.007,+.044], +.053 [+.035,+.071]: **PASS**.  On the original 1200 (v2 run) the 4→8B step is +.016 [−.017,+.047]: FAIL.

No ceiling: the top rung is 0.753 (requirement < 0.95).  Per stratum, combined, plain:
S2 0.790/0.907/0.856/0.872 (non-monotone, near ceiling); S3 0.592/0.744/0.828/0.860; S2h 0.532/0.587/0.610/0.718;
S3h 0.503/0.511/0.576/0.562.  The pooled primary metric passes, but no single stratum passes alone.

**32B rung.**
combined 3600, plain: 0.6B 0.604 → 4B 0.687 → 8B 0.717 → 14B 0.753 → **32B 0.793 [0.780,0.807]**; 14→32B step
+.040 [+.024,+.056].  **Ladder gate on the combined set with 32B: PASS** (every step's paired CI > 0, top < 0.95).
On the rungs 0.6/4/8/32B the 8→32B step is +.076.  On the original 1200 (v2 run): 32B 0.792, 14→32B
+.040 [+.012,+.068].  On the extension alone: 0.793, +.040 [+.020,+.060].
Chat, combined: 32B 0.766, 14→32B +.014 [−.003,+.031]: FAIL at the top step.  T* (32B) = 1.0 plain, 1.7 chat.
Interaction bits/byte at T*, primary: plain 32B 0.714, step +.065 [+.050,+.081]: PASS at every step;
chat 32B 0.616, step −.014: FAIL (chat is flat at 4→8B and at 14→32B).
32B per stratum, plain: S2 0.932, S3 0.901, S2h 0.754, S3h 0.584.  S2 and S3 approach the ceiling at 32B, while the
hard strata keep the pool well below it.

Secondary: interaction bits/byte at the per-model T* (grid 0.5–3.0), combined primary 3600
(`results/gate_v2_ladder_*_Ibpb_Tstar.md`):

| render | T* (0.6/4/8/14B) | 0.6B | 4B | 8B | 14B | steps (paired 95% CI) |
|---|---|---|---|---|---|---|
| plain | 1.1 / 1.3 / 1.2 / 1.1 | 0.099 | 0.343 | 0.413 | 0.649 | +.244 [+.227,+.261], +.070 [+.057,+.084], +.236 [+.217,+.255]: all > 0 |
| chat | 1.5 / 2.3 / 2.3 / 2.3 | 0.069 | 0.347 | 0.348 | 0.631 | +.279, +.001 [−.014,+.016], +.283: flat at 4→8B |

## 5. Nulls

Shuffled pairing (contexts of item i scored on outputs of a same-family partner j): binding 0.41–0.55 and interaction
−0.035…+0.040 bits/byte across all model × render × stratum cells, against real interactions of 0.003–1.7 bits/byte (≥ 0.04 everywhere except S3h).
12 of about 140 cells have a CI that excludes the null value, slightly more than the 7 expected at 95%.  S2h's null
interaction is slightly positive in 4 of 6 runs (+0.014…+0.040 bpb).  The null uses one fixed derangement, so its CI
does not include the pairing randomness.

## 6. Caveats

* Gate power: addressed by the extension batch (section 4b), which was added after the original gate failed.
* S2 (v0) is near ceiling from 4B on; S3h is near floor through 14B (its modular-arithmetic finals need exact multi-step
  arithmetic).  S3 and S2h give the most graded signal.
* The copy mask is word-level: whole-word matches against both prefixes, numbers of ≤ 2 digits exempt.  Under
  `strict` (no exemption), conclusions are unchanged on the base runs (S2+S3 0.730 vs 0.722 at 0.6B-Base).
* Per-item IG (mean of ratios) is heavy-tailed when NLL(o|c′) is tiny (S3h); use the ratio-of-sums form
  (`size_equiv_cf.py`, kind `gain`) for analysis.
* Chat T* hit the old grid edge (2.0) for 4B/8B/14B.  The grid is now 0.5–3.0 for all later runs.
* bf16 batched scoring differs from unbatched by ≤ 0.34 nats per sequence (numerics).
* Only Qwen3 models were run (single-family design).  The scorer is tokenizer-agnostic (offset
  mapping + byte spans) but was exercised only on the Qwen3 tokenizer.
