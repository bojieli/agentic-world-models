# Predicting SWE tool outputs

## Headline (SWE-rebench 2026, M1/M2, instruct-ladder interpolation)

**Across 11 public agentic fine-tunes of Qwen3 at 8B, 14B and 32B (plus 4 non-agentic and world-model controls), none improved prediction of what a command will output by as much as one doubling of model size.** FrogMini-14B is excluded from the count; see the note under the table. This holds for both metrics that pass the ladder validity gate. Everything is reported per dataset: SWE is primary, Terminus is an exhibit only, and datasets are never pooled. Agentic SFT and RL checkpoints are not distinguishable from non-agentic fine-tunes, or from a web world model, on these metrics.

Size multiplier n vs the start checkpoint, with 95% joint-bootstrap CIs:

| model | type | start | M1 recalibrated content bits | M2 NLL of output given true action |
|---|---|---|---|---|
| Nemotron-Terminal-8B | agentic SFT | Qwen3-8B | **0.99×** [0.93, 1.05] | **1.06×** [0.96, 1.15] |
| tmax-sft-8b | agentic SFT | Qwen3-8B | **1.31×** [1.27, 1.36] | **1.44×** [1.37, 1.52] |
| tmax-8b | agentic RL | Qwen3-8B | **1.04×** [0.99, 1.08] | **1.16×** [1.09, 1.22] |
| Light-IF-8B | non-agentic SFT+RL | Qwen3-8B | 1.08× [1.06, 1.10] | 1.28× [1.24, 1.33] |
| WebWorld-8B | web world model | Qwen3-8B | 1.26× [1.22, 1.29] | 1.39× [1.34, 1.45] |
| Nemotron-Terminal-14B | agentic SFT | Qwen3-14B | **0.82×** [0.78, 0.87] | **0.84×** [0.78, 0.90] |
| CodeScout-14B | agentic RL | Qwen3-14B | **0.84×** [0.83, 0.85] | **0.72×** [0.69, 0.75] |
| Light-IF-14B | non-agentic SFT+RL | Qwen3-14B | 0.82× [0.79, 0.84] | 0.92× [0.89, 0.95] |
| SERA-8B | agentic SFT (SWE) | Qwen3-8B | **< 0.5×** (censored) | **0.60×** [0.54, 0.67] |
| OpenThinker-Agent-v1-SFT | agentic SFT (terminal + SWE) | Qwen3-8B | **0.56×** [0.53, 0.58] | **0.69×** [0.65, 0.73] |
| Arctic-AWM-8B | agentic RL (MCP tools) | Qwen3-8B | **1.01×** [1.01, 1.02] | **1.00×** [0.99, 1.01] |
| SERA-14B | agentic SFT (SWE) | Qwen3-14B | **< 0.5×** (censored) | **0.56×** [0.51, 0.62] |
| FrogMini-14B † | agentic SFT (SWE debugging) | Qwen3-14B | < 0.5× (censored; +1.31 bits/tok) | < 0.5× (censored) |
| Nemotron-Terminal-32B | agentic SFT | Qwen3-32B | **0.81×** [0.76, 0.86] | **0.76×** [0.69, 0.83] |
| OpenThinkerAgent-32B | agentic SFT (5 epochs, SWE + terminal) | Qwen3-32B | **< 0.5×** (censored; +0.73 bits/tok) | **< 0.5×** (censored; +0.54) |
| Klear-Reasoner-8B-SFT | non-agentic distillation | Qwen3-8B-Base | < 0.5× (censored) | < 0.5× (censored) |
| tmax-8b vs tmax-sft-8b | the RL step alone | tmax-sft-8b | 0.79× [0.77, 0.81] | 0.79× [0.75, 0.82] |

- † **FrogMini-14B: likely rendering mismatch.** It uses a custom chat template (R2E-Gym scaffold), and +1.31 bits/tok is larger than the whole 0.6B→32B instruct ladder span. It is reported, but excluded from the headline count. No check under its native template was run.
- Across the 11 counted agentic fine-tunes, the best aggregate multiplier is 1.31× on M1 and 1.44× on M2, both from tmax-sft-8b.
- On M1, 7 of the 11 are significantly **worse** than their own start: SERA-8B, OpenThinker-Agent-v1-SFT, Nemotron-14B, CodeScout-14B, SERA-14B, Nemotron-32B, OpenThinkerAgent-32B.
- Only tmax-sft (1.31×) and Arctic-AWM (1.01×) are significantly better. Nemotron-8B and tmax-8b include 1×.
- The SWE-trained agents degrade most: SERA-8B, SERA-14B and OpenThinker-Agent-v1-SFT fall to ≤0.56× on M1 (and FrogMini lower still, †). This is consistent with SFT that masks observation tokens, so the model's output model drifts. None of these cards states the masking.
- **32B.** Both agentic 32B models are worse than Qwen3-32B. For 32B starts the window can only show "worse than 32B" or "> 1× (censored)" because the ladder stops at 32B.
- **OpenThinkerAgent-32B** uses the identical Qwen3 template (CT=Q3 per SWE_CONTROLS.md), so its +0.73 bits/tok is **not** a rendering artefact of the FrogMini kind. It is the largest degradation among template-native models.
- **Per-obs_kind exceptions** to the aggregate result (size multiplier n, M2 / M1):
  - tmax-sft-8b, `shell_other`: M2 2.06× [1.74, 2.52], M1 1.67× [1.54, 1.82]. This is the only cell in the study whose point estimate exceeds 2×; its CI includes 2×.
  - tmax-sft-8b, `search`: M2 1.69× [1.45, 2.30], with the upper CI above 2×.
  - Nemotron-Terminal-32B, `shell_other` / `file_view` / `search` (M1): > 1× (censored at the top of the ladder), while test_run 0.58× and python_exec 0.59×.
  - Nemotron-8B, `file_view`: 1.39× (M1) / 1.50× (M2) against test_run 0.79× / 0.83×.
  - The same pattern holds at every size: agentic gains, where they exist, are in reading-type outputs (files, listings, shell); execution outcomes (tests, scripts) get worse.

- The largest upper CI bound on an aggregate metric is 1.52× (tmax-sft, M2).
- **Exception, by obs_kind:** tmax-sft-8b on `shell_other` outputs reaches 2.06× [1.74, 2.52] on M2, and its `search` upper bound is 2.30×. So "less than a doubling" holds for aggregate content tokens, not for every output kind of every model.
- **Where gains sit.** Nemotron-8B is worse than its start on execution outcomes (test_run 0.79×, python_exec 0.79×, outcome tokens 0.88×) and better only on file_view (1.39×) and search (1.16×). It reads files and listings slightly better; it predicts test or script results worse.
- **At 14B, every post-trained model is worse than Qwen3-14B** (0.72–0.92×). That includes CodeScout (agentic RL on SWE-type tasks) and Light-IF (non-agentic).
- **Instruct tuning itself costs more than any agentic gain.** Qwen3-8B-Base predicts SWE tool output better than Qwen3-8B by 0.147 bits/token on M1. That is larger than the whole 4B→8B instruct step (0.115) and censored at < 0.52× on the base ladder. Nemotron-8B measured against the base is < 0.52× too.
- **Verdict against the two predictions:** this matches "calibration/format only" (or worse), not "world model":
  - no recalibrated gain beyond a fraction of a doubling;
  - action-conditional measures are lower after post-training, not higher;
  - nothing concentrates in outcome tokens or execution kinds. Agentic gains, where they exist, sit in content kinds (file_view, search).

## Validity gate: the Qwen3 instruct ladder on SWE

A metric passes if the ladder (0.6, 1.7, 4, 8, 14, 32B) is monotone and every adjacent step's paired 95% CI excludes 0.

| metric | 0.6B | 1.7B | 4B | 8B | 14B | 32B | gate |
|---|---|---|---|---|---|---|---|
| **M1 recalibrated content bits/tok** (rank×confidence code; lower is better) | 1.821 | 1.556 | 1.318 | 1.203 | 1.089 | 1.016 | **PASS** |
| **M2 NLL of output | true action, @T*** (lower is better) | 1.883 | 1.673 | 1.348 | 1.215 | 1.070 | 0.975 | **PASS** |
| M2 absolute information gain, raw (bits/tok) | 0.242 | 0.425 | 0.359 | 0.369 | 0.297 | 0.248 | FAIL |
| M2 absolute information gain @T* | 0.224 | 0.286 | 0.265 | 0.267 | 0.253 | 0.234 | FAIL |
| M2 relative gain, 1 − true/swap | 0.109 | 0.157 | 0.172 | 0.192 | 0.197 | 0.198 | FAIL (flat above 8B) |
| Reading test: next-action bits/tok saved by seeing the output | 0.025 | 0.040 | 0.050 | 0.059 | 0.031 | 0.025 | FAIL |

- **Base ladder (0.6–14B-Base), M1:** 1.517 / 1.284 / 1.116 / 1.056 / 0.987. M2 NLL-given-action: 1.549 / 1.276 / 1.096 / 1.029 / 0.946. Both PASS.
- On the base ladder, information gain @T* is 0.212 / 0.224 / 0.230 / 0.218 / 0.219 and the reading benefit is 0.019–0.023. Both are flat and FAIL.
- **Answer for pretraining scale:** larger pretrained models predict tool output better, about 0.06–0.23 bits/tok per doubling on M1. They do not condition more on the command.
- Both gated metrics also pass per obs_kind (test_run, python_exec, shell_other, file_view, search) and on outcome tokens.
- `edit_ack` fails: its 0.6→1.7B step is not significant. Edit-ack outputs are excluded from n.
- **The non-monotone information gain is a finding in itself.** On SWE, larger models predict the output nearly as well when given a swapped same-kind command from the same trajectory. Most of what the output contains is therefore determined by history, not by the command. The gain peaks at 1.7B and then declines.
- Every post-trained 8B model lowers the gain relative to Qwen3-8B, by 0.021 to 0.060 bits/tok @T*. All CIs exclude 0, but the gate failed, so these are Δ without n.

## Data and method (SWE primary)
**Data.**
- SWE-rebench leaderboard 2026: 150 trajectories, 5 non-Qwen teachers, tasks from March–May 2026.
- Split by task: 30 calibration / 120 eval trajectories.
- Each trajectory is scored on one window of ≤16,384 tokens that ends at its last turn (task message + most recent turns). No truncated prefixes are used.
- Scored observations need ≥8k tokens of context, or the full history. Totals: 759k observation tokens; 426 M2 items (≤4 per trajectory); 1,233 reading items.
- Every model gets the identical Qwen3-native rendering, with `<tool_response>` wrapping as in the Qwen3 template. Each model's tokenizer is verified by a per-trajectory hash of the rendered ids (all 400 trajectories identical for every model).
- Template-native models: Qwen3 instruct, Nemotron-Terminal, OpenThinker(Agent), SERA-8B/14B. Base-template models: Light-IF, Klear, WebWorld. Custom templates: tmax, CodeScout, FrogMini, Arctic.

**Content tokens.**
- Classes follow the terminal token classes, plus SWE scaffold boilerplate and a `lineno` class.
- Content = novel (no 8-gram copy from the window) ∧ class ∈ {err_line, test_line, number, path, other, lineno}.
- Outcome tokens = novel ∧ {err_line, test_line, number}.

**M1.**
- Per-model recalibration, fitted on the calibration split.
- Code length = −log2 q(rank bucket | top-1-probability bucket) + log2(bucket width). The rank buckets are {0}, {1}, [2,4), …, [1024, V).
- This code uses only the model's ranking and confidence, so it is immune to the instruct models' probability miscalibration (instruct T* ≈ 1.6–1.9).

**M2.**
- At each M2 item, the current turn's thought is blanked, and the observation is echo-stripped and capped at 512 tokens.
- NLL of the same content tokens is taken under (i) the true action, and (ii, iii) two same-obs_kind actions from other turns of the trajectory (or other trajectories if fewer than 2).
- "NLL given true action" is (i), at the model's own T* (fitted on calibration content tokens). Absolute gain = mean(ii, iii) − (i). Relative gain = 1 − (i)/mean(ii, iii).
- Negative control: (ii − iii)/mean ≈ 0 for every model (e.g. Qwen3-8B on SWE −0.006 [−0.019, +0.005]; all CIs include 0).

**Reading test.** NLL of the next action's tokens with the observation shown (main pass), minus the NLL with the observation replaced by `[output omitted]`.

**Size multiplier.**
- Inverse piecewise-linear interpolation of the start-type ladder in log2(non-embedding params): 0.440 / 1.409 / 3.634 / 6.946 / 13.212 / 31.206 B.
- Anchored at the start's size, with the post-trained Δ added to the ladder value there.
- Window: ½×–4× of the start, intersected with the ladder range. Nothing is extrapolated, and values outside the window are censored ("<", ">").
- For 32B starts the upper window ends at 1×, so gains can only show as "> 1× (censored)".
- CIs: joint bootstrap over eval trajectories (1,000 draws); each draw re-estimates every ladder point and every model.

**Executor checks.**
- One left-to-right KV-cache pass per window. All branches at a boundary run in one forward with a tree attention mask.
- In fp32 this matches sequential forwards to ≤6e-4 nats (M1) and ≤1e-4 (branches).

## First-round measures: M1–M4 on both datasets (results/raw; models 0.6B pair, 8B pair, 32B instruct on the 53% subset)
These came before the plan revision. M3 and M4 were dropped as primary measures because they failed validity; the numbers are kept for the record.

**M1 (recalibrated content bits, eval split).** Base beats instruct at every size on both datasets once probability miscalibration is removed.
- Qwen3-8B vs 8B-Base, log2 ratio of rank×confidence code bits:
  - Terminus: +0.360 [+0.332, +0.395];
  - SWE: +0.190 [+0.183, +0.197].
- Raw content bits, same comparison: +0.80 / +0.52.
- Per-model T* ≈ 1.0 for base and 1.6–1.7 for instruct.

**M2 information gain (ratio form).**
- Terminus: 0.6B-Base 0.18, 8B-Base 0.29, Qwen3-8B 0.23.
- SWE (two-window set): 0.10 / 0.15 / 0.16.
- The negative control is ≈0 for every model: |(swapA − swapB)/swap| ≤ 0.0065, with all CIs including 0.

**M3 outcome forced choice: the leak check failed.**
- Setup: 4-way items (exception class, printed numbers, pytest counts) with foils drawn exchangeably from other items' true answers, of the same type and digit format, from the same task. Items whose true answer appears anywhere in the window were dropped.
- With the action and the preceding turn masked, accuracy stayed far above chance (0.25), and essentially equal to full-context accuracy:

| | Qwen3-8B-Base | Qwen3-8B | Qwen3-32B |
|---|---|---|---|
| SWE, full context | 0.714 | 0.682 | 0.714 |
| SWE, leak (masked) | 0.736 | 0.699 | 0.717 |
| Terminus, full context | 0.642 | – | – |
| Terminus, leak (masked) | 0.642 | – | – |

- The outcome is determined by the observation's own lead and prefix and by older history, not by the action. Examples: `HTTP/1.1` → `200`; `code ` → `404`; `ls -l` sizes.
- Fixes tried:
  - (a) exchangeable foils;
  - (b) same-task foils;
  - (c) an adversarially filtered subset (AF): items where Qwen3-0.6B-Base's leak-context posterior on the truth is ≤0.4.
- AF gives leak accuracy below chance by construction: SWE 0.15–0.32, against full 0.21–0.35.
- M3 filtering uses Qwen3-0.6B-Base alone. The Qwen3-1.7B-Base sensitivity check is unavailable.
- The binary items are as uninformative. Leak AUROC is close to full AUROC for:
  - first pytest status (8B-Base 0.825 full / 0.740 leak);
  - printed True/False (0.97 / 0.90);
  - grep hit/no-hit (0.69 / 0.57).
- Conclusion: we could not build leak-free outcome foils from this data; M3 does not measure action-conditional prediction.

**M4 outcome probe: no skill over the baseline.**
- Brier skill vs a logistic baseline (command type, previous error, obs_kind) is ≤0 for every model and variant. The best stacked BSS is +0.03 (Qwen3-8B, SWE native).
- Base models put < 5% of their mass on Yes/No in the native chat format, so they are gated out. Their plain few-shot coverage is 100%, with AUROC 0.55–0.69.
- Error-class accuracy is at or below the majority-class rate.

## M5: the article's AgenticPPL on matched checkpoints
**Setup.**
- Reference package bb189cc and release picks (sha-checked) are in `ext/`.
- Data: 960 held-out Terminus trajectories, each rendered with the model's own template, as the reference defines.
- Validated against `agenticppl score` (vLLM 0.31.0) on Qwen3-0.6B. Differences: plain PPL 4e-5; easy 8.8e-4; nothought 9e-5; taskgain 2.3e-4. Range counts are identical.
- Full table: `results/m5_tables.md`. Early 8B write-up: `M5_INTERIM.md`.

**Answers.**
1. **Agentic vs non-agentic on the same weights: only partly separated.**
   - 8B, paired: Nemotron-T − Light-IF +0.135; tmax-sft − Light-IF +0.031.
   - But the only post-trained model above its own start is Nemotron (+0.054 vs Qwen3-8B). tmax-sft is −0.050, tmax is −0.101.
   - 14B: Nemotron-14B +0.099, CodeScout +0.038, Light-IF −0.041 vs Qwen3-14B. At this size it does separate.
2. **SFT → RL: it goes down.** tmax − tmax-sft is −0.050 [−0.059, −0.042] (easy), significant on all three pick sets, although TB-Lite rises from 11.5 to 17.7.
3. **It tracks sharpness, not world modelling.**
   - Across 20 models, Spearman ρ(easy, entropy at command tokens) = −0.77. Within-size, r = −0.65.
   - ρ with the overconfidence gap is ≈ 0.
   - The 2-bit cap rewards confident wrong tokens. Qwen3-8B has the worst uncapped bits (3.22/range) yet ranks 2nd at 8B. CodeScout-14B has the lowest entropy (0.14) and worst uncapped bits (3.48), yet scores above Qwen3-14B.
   - Base → instruct alone gives +0.10 at 1.7B–8B and +0.08 at 14B.
4. **Ordering vs M1: unrelated.**
   - At 8B, the M1 (SWE) gains rank tmax-sft > WebWorld > Light-IF > tmax > Nemotron.
   - AgenticPPL ranks Nemotron > tmax-sft > WebWorld > Light-IF > tmax.
   - Spearman ρ = 0.0 over these five.
   - AgenticPPL's picks are command tokens the agent reads off the screen. They are not tool outputs, so the metric measures something different from world modelling.

## Scale (base ladder, SWE)
| model | M1 content bits | M2 NLL given action @T* | info gain @T* | reading |
|---|---|---|---|---|
| 0.6B-Base | 1.517 | 1.549 | 0.212 | 0.019 |
| 1.7B-Base | 1.284 | 1.276 | 0.224 | 0.022 |
| 4B-Base | 1.116 | 1.096 | 0.230 | 0.023 |
| 8B-Base | 1.056 | 1.029 | 0.218 | 0.022 |
| 14B-Base | 0.987 | 0.946 | 0.219 | 0.021 |

- At every size the base model beats its instruct sibling on M1, by +0.30 / +0.27 / +0.20 / +0.15 / +0.10 bits/tok from 0.6B to 14B. The gap shrinks with size.
- 4B-Base is better than 8B instruct, and 8B-Base is better than 14B instruct.
- The flat gain and reading columns are why both fail the gate on the base ladder too. They are the main negative result for the "larger pretrained models learn world models" hypothesis: better predictors, not more action-conditional ones.

## GPU, caveats, what did not work
The original runs took approximately 10.4 GPU-hours including validation.

**Caveats.**
- One SWE dataset (150 trajectories, 86 tasks). The sandbox benchmark is the primary dataset for the headline.
- One window per trajectory biases toward late turns.
- n is relative to the instruct ladder. Instruct tuning itself loses more than a doubling relative to base, so "n < 2×" is measured against a ladder that is already degraded.
- The obs-only context excludes images and the like (none present).
- Obs truncation: 4,096 tokens per observation in the main pass; 512 for M2.
- Thoughts are blanked in M2 for both conditions.
- Terminus is an exhibit only, because Nemotron-Terminal was trained on Terminus-2 format.

**What did not work.**
- M3 foils (leak check failed under every scheme tried).
- M4 (no skill).
- The M2 information gain and the reading test as yardsticks (they fail the gate).
- The first-round 32B and 1.7B/4B runs on the 53% subset were superseded by the full-SWE M1/M2 set.
- vLLM is installed only for the M5 reference check.

## Appendix A. Forest-plot data (SWE; every model x metric; n only for gated metrics)

### GATED (size multiplier reported)


**M1 recal content bits/tok [content]** (lower is better; instruct ladder 0.6B 1.821, 1.7B 1.556, 4B 1.318, 8B 1.203, 14B 1.089, 32B 1.016; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0024 [-0.0078, +0.0128] | 0.99x | -0.02 [-0.10, +0.06] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0481 [-0.0550, -0.0417] | 1.31x | +0.39 [+0.34, +0.44] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0062 [-0.0143, +0.0010] | 1.04x | +0.05 [-0.01, +0.11] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1430 [+0.1312, +0.1546] | <0.50x | -1.00 [-1.00, -1.00] | 0.99/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.1034 [+0.0956, +0.1112] | 0.56x | -0.84 [-0.91, -0.78] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0024 [-0.0036, -0.0012] | 1.01x | +0.02 [+0.01, +0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0140 [-0.0175, -0.0103] | 1.08x | +0.11 [+0.08, +0.14] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0405 [-0.0448, -0.0359] | 1.26x | +0.33 [+0.29, +0.37] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.5017 [+0.4677, +0.5369] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0344 [+0.0254, +0.0433] | 0.82x | -0.28 [-0.35, -0.21] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0316 [+0.0296, +0.0335] | 0.84x | -0.26 [-0.28, -0.24] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1340 [+0.1245, +0.1435] | <0.50x | -1.00 [-1.00, -1.00] | 0.99/0.00 |
| FrogMini-14B | Qwen3-14B | +1.3101 [+1.1364, +1.5111] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0357 [+0.0309, +0.0409] | 0.82x | -0.29 [-0.33, -0.25] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0175 [+0.0119, +0.0232] | 0.81x | -0.30 [-0.39, -0.21] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.7320 [+0.6576, +0.8075] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1497 [+0.1345, +0.1637] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1364 [+0.1222, +0.1491] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0420 [+0.0391, +0.0446] | 0.79x | -0.34 [-0.38, -0.31] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3040 [+0.2828, +0.3256] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2717 [+0.2566, +0.2863] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2015 [+0.1886, +0.2145] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1473 [+0.1388, +0.1557] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1020 [+0.0927, +0.1101] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M1 recal content bits/tok [outcome]** (lower is better; instruct ladder 0.6B 1.670, 1.7B 1.482, 4B 1.288, 8B 1.198, 14B 1.097, 32B 1.040; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0185 [+0.0082, +0.0303] | 0.88x | -0.19 [-0.31, -0.09] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0319 [-0.0414, -0.0229] | 1.23x | +0.29 [+0.22, +0.38] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0035 [-0.0130, +0.0055] | 1.02x | +0.03 [-0.06, +0.12] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1907 [+0.1644, +0.2195] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0834 [+0.0736, +0.0931] | 0.55x | -0.86 [-0.97, -0.75] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0008 [-0.0026, +0.0009] | 1.01x | +0.01 [-0.01, +0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0219 [-0.0300, -0.0140] | 1.15x | +0.20 [+0.12, +0.28] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0334 [-0.0415, -0.0253] | 1.24x | +0.31 [+0.24, +0.37] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.3920 [+0.3507, +0.4326] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0389 [+0.0275, +0.0516] | 0.78x | -0.36 [-0.49, -0.26] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0343 [+0.0307, +0.0381] | 0.80x | -0.32 [-0.37, -0.27] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1261 [+0.1130, +0.1398] | <0.50x | -1.00 [-1.00, -1.00] | 0.98/0.00 |
| FrogMini-14B | Qwen3-14B | +2.2595 [+1.9252, +2.5942] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0268 [+0.0186, +0.0347] | 0.84x | -0.25 [-0.31, -0.18] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0150 [+0.0080, +0.0230] | 0.80x | -0.32 [-0.47, -0.19] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.9533 [+0.8250, +1.0901] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1411 [+0.1279, +0.1556] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1214 [+0.1086, +0.1367] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0284 [+0.0246, +0.0324] | 0.82x | -0.29 [-0.35, -0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2552 [+0.2297, +0.2804] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2346 [+0.2160, +0.2524] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1629 [+0.1485, +0.1772] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1225 [+0.1107, +0.1336] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0825 [+0.0734, +0.0921] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M1 recal content bits/tok [kind=test_run]** (lower is better; instruct ladder 0.6B 2.460, 1.7B 2.110, 4B 1.801, 8B 1.649, 14B 1.491, 32B 1.395; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0545 [+0.0365, +0.0757] | 0.79x | -0.33 [-0.44, -0.23] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0355 [-0.0486, -0.0238] | 1.16x | +0.21 [+0.14, +0.28] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | +0.0092 [-0.0037, +0.0210] | 0.96x | -0.06 [-0.13, +0.02] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1840 [+0.1643, +0.2068] | <0.50x | -1.00 [-1.00, -1.00] | 0.97/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.1249 [+0.1105, +0.1368] | 0.59x | -0.76 [-0.85, -0.68] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0022 [-0.0049, +0.0004] | 1.01x | +0.01 [-0.00, +0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0118 [-0.0194, -0.0048] | 1.05x | +0.07 [+0.03, +0.11] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0446 [-0.0533, -0.0356] | 1.20x | +0.26 [+0.21, +0.30] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.7042 [+0.6475, +0.7601] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0967 [+0.0777, +0.1199] | 0.67x | -0.57 [-0.69, -0.47] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0322 [+0.0286, +0.0360] | 0.88x | -0.19 [-0.21, -0.17] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1893 [+0.1709, +0.2072] | <0.50x | -1.00 [-1.00, -1.00] | 0.99/0.00 |
| FrogMini-14B | Qwen3-14B | +2.6697 [+2.2601, +3.0302] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0432 [+0.0345, +0.0516] | 0.84x | -0.25 [-0.31, -0.20] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0613 [+0.0494, +0.0742] | 0.58x | -0.79 [-0.93, -0.67] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +1.3011 [+1.1593, +1.4446] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.2511 [+0.2232, +0.2818] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.2296 [+0.2036, +0.2595] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0447 [+0.0388, +0.0509] | 0.83x | -0.27 [-0.31, -0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3953 [+0.3664, +0.4289] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3543 [+0.3261, +0.3858] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2606 [+0.2385, +0.2850] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1966 [+0.1801, +0.2133] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1329 [+0.1195, +0.1464] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M1 recal content bits/tok [kind=python_exec]** (lower is better; instruct ladder 0.6B 1.536, 1.7B 1.299, 4B 1.067, 8B 0.957, 14B 0.861, 32B 0.801; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0403 [+0.0098, +0.0734] | 0.79x | -0.34 [-0.60, -0.09] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0282 [-0.0454, -0.0110] | 1.21x | +0.27 [+0.11, +0.41] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | +0.0373 [+0.0202, +0.0556] | 0.80x | -0.32 [-0.50, -0.17] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1422 [+0.0984, +0.1837] | <0.50x | -1.00 [-1.00, -0.88] | 0.86/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.1064 [+0.0878, +0.1232] | 0.53x | -0.91 [-1.00, -0.75] | 0.10/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0057 [-0.0093, -0.0018] | 1.04x | +0.05 [+0.02, +0.08] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0304 [-0.0399, -0.0216] | 1.22x | +0.29 [+0.21, +0.39] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0364 [-0.0521, -0.0222] | 1.27x | +0.35 [+0.23, +0.48] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.3832 [+0.3254, +0.4471] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0672 [+0.0402, +0.0968] | 0.64x | -0.65 [-0.94, -0.38] | 0.01/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0392 [+0.0325, +0.0461] | 0.77x | -0.38 [-0.45, -0.32] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1314 [+0.0945, +0.1677] | <0.50x | -1.00 [-1.00, -0.90] | 0.91/0.00 |
| FrogMini-14B | Qwen3-14B | +0.4279 [+0.2585, +0.6761] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0174 [+0.0024, +0.0363] | 0.89x | -0.17 [-0.33, -0.02] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0364 [+0.0189, +0.0583] | 0.59x | -0.76 [-1.00, -0.44] | 0.12/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.4513 [+0.3572, +0.5715] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1621 [+0.1286, +0.1991] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1526 [+0.1189, +0.1879] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0655 [+0.0537, +0.0798] | 0.68x | -0.56 [-0.73, -0.44] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2424 [+0.2060, +0.2803] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2647 [+0.2290, +0.3080] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1784 [+0.1529, +0.2083] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1218 [+0.1025, +0.1420] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0854 [+0.0654, +0.1049] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M1 recal content bits/tok [kind=shell_other]** (lower is better; instruct ladder 0.6B 1.447, 1.7B 1.118, 4B 0.886, 8B 0.794, 14B 0.703, 32B 0.639; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0190 [-0.0366, +0.0008] | 1.14x | +0.19 [-0.01, +0.36] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0722 [-0.0856, -0.0596] | 1.67x | +0.74 [+0.63, +0.86] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0454 [-0.0595, -0.0308] | 1.38x | +0.47 [+0.34, +0.59] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0839 [+0.0653, +0.1039] | 0.56x | -0.85 [-0.99, -0.68] | 0.01/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0847 [+0.0729, +0.0980] | 0.55x | -0.85 [-1.00, -0.71] | 0.02/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0035 [-0.0058, -0.0013] | 1.03x | +0.04 [+0.01, +0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0104 [-0.0170, -0.0031] | 1.08x | +0.11 [+0.03, +0.19] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0242 [-0.0343, -0.0128] | 1.19x | +0.25 [+0.13, +0.36] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.4632 [+0.3981, +0.5364] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0064 [-0.0187, +0.0075] | 1.09x | +0.12 [-0.07, +0.37] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0308 [+0.0269, +0.0348] | 0.80x | -0.32 [-0.38, -0.26] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.0798 [+0.0636, +0.0987] | 0.57x | -0.82 [-1.00, -0.63] | 0.05/0.00 |
| FrogMini-14B | Qwen3-14B | +0.1853 [+0.1335, +0.2540] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0234 [+0.0147, +0.0332] | 0.85x | -0.24 [-0.31, -0.17] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0112 [-0.0209, -0.0020] | >1.00x | +0.00 [+0.00, +0.00] | 0.00/0.99 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.4746 [+0.3951, +0.5600] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0881 [+0.0602, +0.1167] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0598 [+0.0300, +0.0880] | <0.50x | -1.00 [-1.00, -0.63] | 0.73/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0267 [+0.0229, +0.0309] | 0.83x | -0.27 [-0.33, -0.22] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3566 [+0.3045, +0.4160] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2427 [+0.2072, +0.2804] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1606 [+0.1303, +0.1894] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1070 [+0.0904, +0.1234] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0661 [+0.0409, +0.0886] | <0.50x | -1.00 [-1.00, -0.84] | 0.90/0.00 |

**M1 recal content bits/tok [kind=file_view]** (lower is better; instruct ladder 0.6B 1.624, 1.7B 1.439, 4B 1.251, 8B 1.145, 14B 1.050, 32B 0.983; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0487 [-0.0579, -0.0398] | 1.39x | +0.47 [+0.39, +0.57] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0528 [-0.0628, -0.0456] | 1.43x | +0.51 [+0.44, +0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0200 [-0.0317, -0.0116] | 1.14x | +0.19 [+0.12, +0.31] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1189 [+0.0933, +0.1445] | <0.50x | -1.00 [-1.00, -0.80] | 0.58/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0999 [+0.0825, +0.1203] | 0.54x | -0.88 [-1.00, -0.74] | 0.05/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0013 [-0.0029, +0.0003] | 1.01x | +0.01 [-0.00, +0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0106 [-0.0164, -0.0051] | 1.07x | +0.10 [+0.05, +0.16] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0474 [-0.0553, -0.0386] | 1.38x | +0.46 [+0.38, +0.53] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.4050 [+0.3542, +0.4532] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0106 [-0.0236, +0.0023] | 1.15x | +0.20 [-0.02, +0.43] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0276 [+0.0233, +0.0316] | 0.83x | -0.27 [-0.31, -0.22] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1068 [+0.0876, +0.1256] | <0.50x | -1.00 [-1.00, -0.83] | 0.59/0.00 |
| FrogMini-14B | Qwen3-14B | +0.7088 [+0.4430, +0.9721] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0387 [+0.0310, +0.0453] | 0.77x | -0.38 [-0.44, -0.31] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0115 [-0.0207, -0.0032] | >1.00x | +0.00 [+0.00, +0.00] | 0.00/1.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.3496 [+0.2948, +0.4095] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0911 [+0.0721, +0.1072] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0930 [+0.0717, +0.1120] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0328 [+0.0290, +0.0363] | 0.82x | -0.29 [-0.35, -0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2323 [+0.2014, +0.2623] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2288 [+0.2080, +0.2474] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1949 [+0.1710, +0.2137] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1399 [+0.1226, +0.1557] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1036 [+0.0872, +0.1173] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M1 recal content bits/tok [kind=search]** (lower is better; instruct ladder 0.6B 2.586, 1.7B 2.279, 4B 2.002, 8B 1.856, 14B 1.710, 32B 1.625; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0330 [-0.0729, -0.0025] | 1.16x | +0.21 [+0.02, +0.43] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0852 [-0.1251, -0.0575] | 1.45x | +0.54 [+0.39, +0.73] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0461 [-0.0901, -0.0124] | 1.22x | +0.29 [+0.08, +0.51] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0966 [+0.0633, +0.1253] | 0.65x | -0.62 [-0.88, -0.39] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.1380 [+0.1103, +0.1663] | 0.54x | -0.89 [-1.00, -0.68] | 0.08/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0003 [-0.0054, +0.0055] | 1.00x | -0.00 [-0.03, +0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0139 [-0.0355, +0.0011] | 1.06x | +0.09 [-0.01, +0.22] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0720 [-0.0984, -0.0541] | 1.37x | +0.46 [+0.36, +0.58] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.6273 [+0.5509, +0.7161] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0151 [-0.0162, +0.0391] | 0.94x | -0.10 [-0.26, +0.20] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0460 [+0.0377, +0.0575] | 0.82x | -0.29 [-0.37, -0.23] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1169 [+0.0845, +0.1464] | 0.60x | -0.74 [-0.95, -0.51] | 0.01/0.00 |
| FrogMini-14B | Qwen3-14B | +0.5726 [+0.2330, +0.8148] | <0.50x | -1.00 [-1.00, -1.00] | 0.99/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0631 [+0.0457, +0.0835] | 0.76x | -0.40 [-0.53, -0.27] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0135 [-0.0327, +0.0060] | >1.00x | +0.00 [-0.08, +0.00] | 0.00/0.93 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.5953 [+0.3626, +0.7604] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1631 [+0.1247, +0.1938] | <0.50x | -1.00 [-1.00, -0.96] | 0.96/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1658 [+0.1419, +0.1909] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0391 [+0.0260, +0.0507] | 0.84x | -0.25 [-0.36, -0.15] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3147 [+0.2647, +0.3606] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2904 [+0.2533, +0.3440] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2335 [+0.2040, +0.2683] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1960 [+0.1718, +0.2236] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1507 [+0.1282, +0.1759] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M2 NLL given true action bits/tok @T* [content/all]** (lower is better; instruct ladder 0.6B 1.883, 1.7B 1.673, 4B 1.348, 8B 1.215, 14B 1.070, 32B 0.975; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0123 [-0.0315, +0.0100] | 1.06x | +0.08 [-0.07, +0.20] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0819 [-0.0958, -0.0695] | 1.44x | +0.52 [+0.45, +0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0326 [-0.0462, -0.0191] | 1.16x | +0.21 [+0.12, +0.29] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1038 [+0.0826, +0.1257] | 0.60x | -0.73 [-0.90, -0.58] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0763 [+0.0633, +0.0898] | 0.69x | -0.54 [-0.61, -0.46] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0005 [-0.0014, +0.0025] | 1.00x | -0.00 [-0.02, +0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0560 [-0.0642, -0.0478] | 1.28x | +0.36 [+0.31, +0.41] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0747 [-0.0858, -0.0645] | 1.39x | +0.48 [+0.42, +0.54] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.5767 [+0.5266, +0.6328] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0396 [+0.0238, +0.0560] | 0.84x | -0.25 [-0.36, -0.16] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0728 [+0.0662, +0.0799] | 0.72x | -0.47 [-0.53, -0.42] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1291 [+0.1096, +0.1496] | 0.56x | -0.83 [-0.97, -0.69] | 0.01/0.00 |
| FrogMini-14B | Qwen3-14B | +0.7785 [+0.6432, +0.9233] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0178 [+0.0106, +0.0254] | 0.92x | -0.11 [-0.16, -0.07] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0312 [+0.0200, +0.0431] | 0.76x | -0.40 [-0.54, -0.26] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.5364 [+0.4650, +0.6150] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1740 [+0.1494, +0.2022] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1643 [+0.1418, +0.1878] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0493 [+0.0444, +0.0544] | 0.79x | -0.35 [-0.42, -0.29] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3335 [+0.3045, +0.3648] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3969 [+0.3645, +0.4312] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2519 [+0.2314, +0.2734] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1862 [+0.1719, +0.2020] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1247 [+0.1112, +0.1383] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M2 NLL given true action bits/tok @T* [outcome/all]** (lower is better; instruct ladder 0.6B 1.742, 1.7B 1.646, 4B 1.380, 8B 1.249, 14B 1.128, 32B 1.036; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0058 [-0.0160, +0.0299] | 0.97x | -0.04 [-0.21, +0.12] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0578 [-0.0792, -0.0367] | 1.36x | +0.44 [+0.28, +0.61] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0207 [-0.0420, +0.0013] | 1.12x | +0.16 [-0.01, +0.32] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1315 [+0.0987, +0.1701] | 0.52x | -0.94 [-1.00, -0.66] | 0.31/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0606 [+0.0440, +0.0766] | 0.74x | -0.43 [-0.56, -0.32] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0044 [-0.0081, -0.0011] | 1.02x | +0.03 [+0.01, +0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0706 [-0.0850, -0.0564] | 1.45x | +0.54 [+0.44, +0.66] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0644 [-0.0819, -0.0475] | 1.41x | +0.49 [+0.38, +0.61] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.4491 [+0.3934, +0.5092] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0354 [+0.0166, +0.0551] | 0.83x | -0.27 [-0.43, -0.13] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0755 [+0.0648, +0.0877] | 0.67x | -0.58 [-0.73, -0.47] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1107 [+0.0861, +0.1365] | 0.56x | -0.85 [-1.00, -0.62] | 0.10/0.00 |
| FrogMini-14B | Qwen3-14B | +1.3887 [+1.0678, +1.7308] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0059 [-0.0043, +0.0157] | 0.97x | -0.04 [-0.12, +0.06] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0351 [+0.0202, +0.0488] | 0.72x | -0.47 [-0.67, -0.29] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.6823 [+0.5512, +0.8129] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1608 [+0.1345, +0.1919] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1423 [+0.1184, +0.1675] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0370 [+0.0305, +0.0442] | 0.83x | -0.26 [-0.35, -0.20] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2471 [+0.2168, +0.2810] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3516 [+0.3170, +0.3907] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2162 [+0.1865, +0.2461] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1550 [+0.1365, +0.1749] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1069 [+0.0901, +0.1246] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M2 NLL given true action bits/tok @T* [content/kind=test_run]** (lower is better; instruct ladder 0.6B 2.327, 1.7B 2.075, 4B 1.703, 8B 1.526, 14B 1.352, 32B 1.227; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0497 [+0.0114, +0.0900] | 0.83x | -0.26 [-0.44, -0.07] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0557 [-0.0772, -0.0347] | 1.23x | +0.30 [+0.19, +0.41] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | +0.0021 [-0.0179, +0.0227] | 0.99x | -0.01 [-0.13, +0.09] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.1460 [+0.1051, +0.1838] | 0.59x | -0.77 [-0.97, -0.57] | 0.01/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0929 [+0.0694, +0.1184] | 0.71x | -0.49 [-0.59, -0.39] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0001 [-0.0038, +0.0037] | 1.00x | -0.00 [-0.02, +0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0542 [-0.0673, -0.0409] | 1.22x | +0.29 [+0.22, +0.37] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0867 [-0.1029, -0.0692] | 1.38x | +0.46 [+0.39, +0.55] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.7544 [+0.6600, +0.8634] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0947 [+0.0594, +0.1317] | 0.70x | -0.51 [-0.69, -0.32] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0676 [+0.0584, +0.0774] | 0.78x | -0.36 [-0.44, -0.30] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1833 [+0.1467, +0.2203] | 0.51x | -0.98 [-1.00, -0.76] | 0.40/0.00 |
| FrogMini-14B | Qwen3-14B | +1.8286 [+1.4784, +2.1840] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0018 [-0.0082, +0.0104] | 0.99x | -0.01 [-0.05, +0.08] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0775 [+0.0538, +0.1042] | 0.59x | -0.77 [-0.98, -0.54] | 0.01/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.9667 [+0.7856, +1.1666] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.2782 [+0.2198, +0.3363] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.2577 [+0.2110, +0.3067] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0578 [+0.0485, +0.0678] | 0.81x | -0.31 [-0.39, -0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3833 [+0.3342, +0.4337] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.4635 [+0.4042, +0.5254] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.3069 [+0.2615, +0.3543] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.2285 [+0.1974, +0.2587] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1630 [+0.1395, +0.1863] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M2 NLL given true action bits/tok @T* [content/kind=python_exec]** (lower is better; instruct ladder 0.6B 1.453, 1.7B 1.369, 4B 1.046, 8B 0.943, 14B 0.821, 32B 0.748; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0028 [-0.0371, +0.0436] | 0.98x | -0.03 [-0.40, +0.26] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0565 [-0.0857, -0.0245] | 1.35x | +0.43 [+0.19, +0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | +0.0102 [-0.0196, +0.0449] | 0.94x | -0.09 [-0.44, +0.14] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0979 [+0.0492, +0.1486] | 0.54x | -0.89 [-1.00, -0.48] | 0.22/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0763 [+0.0474, +0.1057] | 0.62x | -0.70 [-0.99, -0.41] | 0.02/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0030 [-0.0019, +0.0076] | 0.98x | -0.03 [-0.07, +0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0715 [-0.0925, -0.0521] | 1.46x | +0.54 [+0.39, +0.72] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0709 [-0.1000, -0.0420] | 1.45x | +0.54 [+0.37, +0.73] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.3738 [+0.2918, +0.4696] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0517 [+0.0201, +0.0821] | 0.76x | -0.39 [-0.63, -0.15] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0934 [+0.0742, +0.1142] | 0.61x | -0.71 [-0.92, -0.56] | 0.01/0.00 |
| SERA-14B | Qwen3-14B | +0.1182 [+0.0675, +0.1737] | 0.54x | -0.90 [-1.00, -0.50] | 0.32/0.00 |
| FrogMini-14B | Qwen3-14B | +0.2161 [+0.1519, +0.3019] | <0.50x | -1.00 [-1.00, -1.00] | 0.99/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0088 [-0.0201, +0.0503] | 0.95x | -0.07 [-0.36, +0.40] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0418 [+0.0105, +0.0746] | 0.61x | -0.71 [-1.00, -0.20] | 0.16/0.01 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.3774 [+0.2949, +0.4711] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1633 [+0.1149, +0.2223] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1551 [+0.1081, +0.1993] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0667 [+0.0526, +0.0826] | 0.66x | -0.61 [-0.95, -0.41] | 0.01/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2341 [+0.1844, +0.2911] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3864 [+0.3258, +0.4604] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2102 [+0.1670, +0.2608] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1605 [+0.1234, +0.1990] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1035 [+0.0747, +0.1350] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |

**M2 NLL given true action bits/tok @T* [content/kind=shell_other]** (lower is better; instruct ladder 0.6B 1.446, 1.7B 1.142, 4B 0.834, 8B 0.727, 14B 0.634, 32B 0.554; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | +0.0013 [-0.0337, +0.0404] | 0.99x | -0.01 [-0.33, +0.29] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.1006 [-0.1269, -0.0764] | 2.06x | +1.04 [+0.80, +1.33] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0666 [-0.0935, -0.0424] | 1.58x | +0.66 [+0.45, +0.88] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0965 [+0.0627, +0.1337] | 0.56x | -0.84 [-1.00, -0.59] | 0.07/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0574 [+0.0390, +0.0759] | 0.71x | -0.50 [-0.64, -0.38] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | -0.0026 [-0.0057, +0.0007] | 1.02x | +0.03 [-0.01, +0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0358 [-0.0472, -0.0253] | 1.28x | +0.36 [+0.23, +0.49] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0458 [-0.0648, -0.0281] | 1.37x | +0.46 [+0.28, +0.66] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.5509 [+0.4498, +0.6595] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0144 [-0.0043, +0.0356] | 0.91x | -0.14 [-0.39, +0.07] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0689 [+0.0593, +0.0787] | 0.62x | -0.69 [-0.90, -0.53] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.0966 [+0.0654, +0.1306] | 0.51x | -0.96 [-1.00, -0.59] | 0.39/0.00 |
| FrogMini-14B | Qwen3-14B | +0.1948 [+0.1472, +0.2429] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0067 [-0.0037, +0.0174] | 0.95x | -0.07 [-0.16, +0.06] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0073 [-0.0063, +0.0226] | 0.92x | -0.11 [-0.31, +0.00] | 0.00/0.15 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.4109 [+0.3356, +0.4854] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1245 [+0.0781, +0.1714] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0937 [+0.0528, +0.1329] | <0.50x | -1.00 [-1.00, -1.00] | 0.98/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0340 [+0.0276, +0.0403] | 0.81x | -0.30 [-0.41, -0.22] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.3998 [+0.3264, +0.4776] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3573 [+0.2929, +0.4338] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2035 [+0.1670, +0.2421] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1232 [+0.0955, +0.1494] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0793 [+0.0480, +0.1111] | <0.50x | -1.00 [-1.00, -0.89] | 0.96/0.00 |

**M2 NLL given true action bits/tok @T* [content/kind=file_view]** (lower is better; instruct ladder 0.6B 1.862, 1.7B 1.697, 4B 1.448, 8B 1.332, 14B 1.170, 32B 1.091; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.1022 [-0.1290, -0.0780] | 1.50x | +0.58 [+0.48, +0.71] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.0974 [-0.1283, -0.0744] | 1.47x | +0.56 [+0.44, +0.70] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.0689 [-0.0976, -0.0456] | 1.31x | +0.39 [+0.28, +0.54] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0457 [+0.0051, +0.0828] | 0.77x | -0.37 [-0.73, -0.04] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.0625 [+0.0283, +0.0980] | 0.71x | -0.50 [-0.79, -0.23] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0030 [-0.0015, +0.0076] | 0.98x | -0.02 [-0.06, +0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0551 [-0.0760, -0.0367] | 1.24x | +0.31 [+0.23, +0.41] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0765 [-0.0974, -0.0537] | 1.35x | +0.44 [+0.32, +0.55] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.4877 [+0.3908, +0.5812] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0140 [-0.0306, +0.0030] | 1.16x | +0.22 [-0.02, +0.46] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.0618 [+0.0482, +0.0775] | 0.78x | -0.35 [-0.47, -0.26] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.0893 [+0.0596, +0.1192] | 0.70x | -0.51 [-0.73, -0.33] | 0.00/0.00 |
| FrogMini-14B | Qwen3-14B | +0.3435 [+0.1657, +0.5947] | <0.50x | -1.00 [-1.00, -0.94] | 0.97/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0360 [+0.0250, +0.0472] | 0.87x | -0.21 [-0.28, -0.14] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0079 [-0.0260, +0.0084] | >1.00x | +0.00 [-0.13, +0.00] | 0.00/0.83 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.1879 [+0.1554, +0.2286] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0879 [+0.0658, +0.1085] | <0.50x | -1.00 [-1.00, -0.95] | 0.92/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.1043 [+0.0799, +0.1298] | <0.50x | -1.00 [-1.00, -0.83] | 0.76/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0285 [+0.0229, +0.0348] | 0.85x | -0.23 [-0.34, -0.17] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.2561 [+0.2034, +0.3050] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.3143 [+0.2611, +0.3680] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.2425 [+0.2016, +0.2797] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1901 [+0.1537, +0.2241] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1183 [+0.0955, +0.1404] | <0.50x | -1.00 [-1.00, -0.98] | 0.97/0.00 |

**M2 NLL given true action bits/tok @T* [content/kind=search]** (lower is better; instruct ladder 0.6B 2.887, 1.7B 2.704, 4B 2.262, 8B 2.068, 14B 1.848, 32B 1.717; gate PASS)

| model | start | Δ [95% CI] | n | log2 n [95% CI] | censored draws (low/high) |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.1249 [-0.1843, -0.0621] | 1.44x | +0.53 [+0.29, +0.74] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B | -0.1802 [-0.2477, -0.1141] | 1.69x | +0.76 [+0.54, +1.20] | 0.00/0.00 |
| tmax-8b | Qwen3-8B | -0.1329 [-0.2007, -0.0620] | 1.47x | +0.56 [+0.31, +0.82] | 0.00/0.00 |
| SERA-8B | Qwen3-8B | +0.0050 [-0.0732, +0.0704] | 0.98x | -0.02 [-0.34, +0.28] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | +0.1259 [+0.0629, +0.1743] | 0.66x | -0.61 [-0.93, -0.32] | 0.01/0.00 |
| Arctic-AWM-8B | Qwen3-8B | +0.0047 [-0.0043, +0.0145] | 0.98x | -0.02 [-0.08, +0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.1056 [-0.1585, -0.0678] | 1.36x | +0.45 [+0.30, +0.69] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B | -0.1507 [-0.2233, -0.1054] | 1.55x | +0.64 [+0.46, +0.98] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.7174 [+0.5585, +0.8695] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0099 [-0.0320, +0.0520] | 0.97x | -0.04 [-0.24, +0.29] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B | +0.1142 [+0.0895, +0.1476] | 0.72x | -0.48 [-0.79, -0.34] | 0.00/0.00 |
| SERA-14B | Qwen3-14B | +0.1007 [+0.0372, +0.1550] | 0.75x | -0.42 [-0.74, -0.15] | 0.00/0.00 |
| FrogMini-14B | Qwen3-14B | +0.2475 [+0.0452, +0.4519] | <0.50x | -1.00 [-1.00, -0.16] | 0.51/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0514 [+0.0179, +0.0816] | 0.86x | -0.22 [-0.42, -0.07] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0130 [-0.0564, +0.0318] | >1.00x | +0.00 [-0.30, +0.00] | 0.00/0.75 |
| OpenThinkerAgent-32B | Qwen3-32B | +0.3183 [+0.2039, +0.4288] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.1645 [+0.1084, +0.2306] | <0.50x | -1.00 [-1.00, -0.84] | 0.79/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.2001 [+0.1520, +0.2556] | <0.50x | -1.00 [-1.00, -1.00] | 0.98/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0472 [+0.0376, +0.0606] | 0.85x | -0.23 [-0.46, -0.15] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.4069 [+0.3026, +0.4895] | <1.00x | +0.00 [+0.00, +0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.5467 [+0.4568, +0.6603] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.3548 [+0.2812, +0.4145] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.2894 [+0.2326, +0.3521] | <0.50x | -1.00 [-1.00, -1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1902 [+0.1447, +0.2497] | <0.50x | -1.00 [-1.00, -1.00] | 0.98/0.00 |

### FAILS LADDER GATE (Δ only)


**M2 abs info gain bits/tok [content/all]** (higher is better; instruct ladder 0.6B 0.242, 1.7B 0.425, 4B 0.358, 8B 0.369, 14B 0.297, 32B 0.248; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.1555 [-0.1865, -0.1296] |
| tmax-sft-8b | Qwen3-8B | -0.1340 [-0.1619, -0.1100] |
| tmax-8b | Qwen3-8B | -0.1194 [-0.1457, -0.0958] |
| SERA-8B | Qwen3-8B | -0.1125 [-0.1370, -0.0917] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.1029 [-0.1225, -0.0855] |
| Arctic-AWM-8B | Qwen3-8B | -0.0205 [-0.0249, -0.0167] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.1024 [-0.1221, -0.0849] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.1232 [-0.1479, -0.1020] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0389 [+0.0255, +0.0537] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0874 [-0.1053, -0.0713] |
| CodeScout-14B | Qwen3-14B | +0.0694 [+0.0555, +0.0856] |
| SERA-14B | Qwen3-14B | -0.0585 [-0.0736, -0.0452] |
| FrogMini-14B | Qwen3-14B | +0.0547 [-0.0010, +0.1127] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0105 [+0.0025, +0.0188] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0260 [-0.0333, -0.0194] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0004 [-0.0292, +0.0300] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0051 [-0.0123, +0.0014] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0094 [-0.0154, -0.0036] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0146 [+0.0100, +0.0199] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0303 [+0.0204, +0.0403] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.2006 [+0.1630, +0.2414] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1284 [+0.1025, +0.1570] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1503 [+0.1247, +0.1809] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0780 [+0.0630, +0.0950] |

**M2 abs info gain bits/tok @T* [content/all]** (higher is better; instruct ladder 0.6B 0.224, 1.7B 0.285, 4B 0.265, 8B 0.267, 14B 0.253, 32B 0.234; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0596 [-0.0725, -0.0480] |
| tmax-sft-8b | Qwen3-8B | -0.0380 [-0.0488, -0.0281] |
| tmax-8b | Qwen3-8B | -0.0214 [-0.0310, -0.0120] |
| SERA-8B | Qwen3-8B | -0.0470 [-0.0591, -0.0368] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0322 [-0.0411, -0.0238] |
| Arctic-AWM-8B | Qwen3-8B | -0.0012 [-0.0028, +0.0004] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0226 [-0.0292, -0.0166] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0392 [-0.0486, -0.0305] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0210 [+0.0104, +0.0326] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0493 [-0.0595, -0.0399] |
| CodeScout-14B | Qwen3-14B | +0.0280 [+0.0215, +0.0353] |
| SERA-14B | Qwen3-14B | -0.0316 [-0.0412, -0.0227] |
| FrogMini-14B | Qwen3-14B | +0.1005 [+0.0509, +0.1514] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0197 [+0.0137, +0.0264] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0188 [-0.0248, -0.0132] |
| OpenThinkerAgent-32B | Qwen3-32B | -0.0192 [-0.0435, +0.0051] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0105 [-0.0172, -0.0043] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0152 [-0.0212, -0.0095] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0166 [+0.0123, +0.0217] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0125 [+0.0049, +0.0200] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0615 [+0.0487, +0.0745] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0345 [+0.0251, +0.0442] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0491 [+0.0394, +0.0600] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0341 [+0.0269, +0.0418] |

**M2 relative gain [content/all]** (higher is better; instruct ladder 0.6B 0.109, 1.7B 0.157, 4B 0.172, 8B 0.192, 14B 0.197, 32B 0.197; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0427 [-0.0518, -0.0342] |
| tmax-sft-8b | Qwen3-8B | -0.0231 [-0.0302, -0.0164] |
| tmax-8b | Qwen3-8B | -0.0202 [-0.0277, -0.0130] |
| SERA-8B | Qwen3-8B | -0.0439 [-0.0542, -0.0348] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0387 [-0.0460, -0.0320] |
| Arctic-AWM-8B | Qwen3-8B | -0.0039 [-0.0052, -0.0026] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0150 [-0.0200, -0.0102] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0225 [-0.0286, -0.0169] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | -0.0432 [-0.0544, -0.0342] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0399 [-0.0480, -0.0326] |
| CodeScout-14B | Qwen3-14B | +0.0093 [+0.0058, +0.0131] |
| SERA-14B | Qwen3-14B | -0.0383 [-0.0470, -0.0302] |
| FrogMini-14B | Qwen3-14B | -0.0429 [-0.0731, -0.0133] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0080 [+0.0032, +0.0126] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0181 [-0.0235, -0.0132] |
| OpenThinkerAgent-32B | Qwen3-32B | -0.0722 [-0.0940, -0.0514] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0256 [-0.0332, -0.0192] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0306 [-0.0376, -0.0243] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0030 [+0.0005, +0.0055] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | -0.0112 [-0.0167, -0.0063] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0073 [-0.0005, +0.0149] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | -0.0020 [-0.0083, +0.0043] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0171 [+0.0115, +0.0232] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0093 [+0.0035, +0.0158] |

**M2 abs info gain bits/tok [content/kind=test_run]** (higher is better; instruct ladder 0.6B 0.187, 1.7B 0.331, 4B 0.297, 8B 0.301, 14B 0.235, 32B 0.197; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.1350 [-0.1883, -0.0896] |
| tmax-sft-8b | Qwen3-8B | -0.1167 [-0.1649, -0.0779] |
| tmax-8b | Qwen3-8B | -0.1064 [-0.1504, -0.0698] |
| SERA-8B | Qwen3-8B | -0.0910 [-0.1291, -0.0582] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0943 [-0.1280, -0.0657] |
| Arctic-AWM-8B | Qwen3-8B | -0.0174 [-0.0243, -0.0109] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0903 [-0.1274, -0.0615] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.1179 [-0.1631, -0.0809] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0284 [+0.0073, +0.0533] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0665 [-0.0947, -0.0416] |
| CodeScout-14B | Qwen3-14B | +0.0633 [+0.0398, +0.0916] |
| SERA-14B | Qwen3-14B | -0.0398 [-0.0638, -0.0173] |
| FrogMini-14B | Qwen3-14B | +0.1316 [-0.0359, +0.2969] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0022 [-0.0068, +0.0106] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0226 [-0.0349, -0.0125] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0075 [-0.0664, +0.0834] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0040 [-0.0185, +0.0111] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0010 [-0.0117, +0.0094] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0103 [+0.0032, +0.0195] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0250 [+0.0103, +0.0405] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.1593 [+0.0968, +0.2320] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1173 [+0.0721, +0.1721] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1310 [+0.0903, +0.1826] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0655 [+0.0437, +0.0930] |

**M2 abs info gain bits/tok [content/kind=python_exec]** (higher is better; instruct ladder 0.6B 0.959, 1.7B 1.628, 4B 1.275, 8B 1.259, 14B 1.009, 32B 0.828; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.4892 [-0.6385, -0.3751] |
| tmax-sft-8b | Qwen3-8B | -0.4864 [-0.6312, -0.3820] |
| tmax-8b | Qwen3-8B | -0.4426 [-0.5816, -0.3412] |
| SERA-8B | Qwen3-8B | -0.3633 [-0.4860, -0.2674] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.2826 [-0.3811, -0.2035] |
| Arctic-AWM-8B | Qwen3-8B | -0.0694 [-0.0901, -0.0526] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.3242 [-0.4247, -0.2565] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.3832 [-0.4964, -0.2993] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.1960 [+0.1481, +0.2518] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.2707 [-0.3361, -0.2133] |
| CodeScout-14B | Qwen3-14B | +0.2224 [+0.1739, +0.2858] |
| SERA-14B | Qwen3-14B | -0.1970 [-0.2665, -0.1430] |
| FrogMini-14B | Qwen3-14B | -0.1193 [-0.2092, -0.0352] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0631 [+0.0292, +0.0924] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0783 [-0.1164, -0.0496] |
| OpenThinkerAgent-32B | Qwen3-32B | -0.0705 [-0.1513, +0.0089] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0032 [-0.0298, +0.0287] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0171 [-0.0409, +0.0104] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0438 [+0.0284, +0.0615] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.1053 [+0.0637, +0.1508] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.7810 [+0.6214, +0.9962] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.4476 [+0.3511, +0.5735] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.4924 [+0.3869, +0.6227] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.2536 [+0.1949, +0.3253] |

**M2 abs info gain bits/tok [content/kind=shell_other]** (higher is better; instruct ladder 0.6B 0.069, 1.7B 0.130, 4B 0.132, 8B 0.176, 14B 0.136, 32B 0.120; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0851 [-0.1208, -0.0537] |
| tmax-sft-8b | Qwen3-8B | -0.0584 [-0.0876, -0.0318] |
| tmax-8b | Qwen3-8B | -0.0514 [-0.0782, -0.0267] |
| SERA-8B | Qwen3-8B | -0.0633 [-0.0934, -0.0354] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0670 [-0.0930, -0.0455] |
| Arctic-AWM-8B | Qwen3-8B | -0.0066 [-0.0123, -0.0019] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0556 [-0.0753, -0.0394] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0593 [-0.0864, -0.0354] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | -0.0115 [-0.0364, +0.0114] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0474 [-0.0678, -0.0310] |
| CodeScout-14B | Qwen3-14B | +0.0185 [+0.0066, +0.0333] |
| SERA-14B | Qwen3-14B | -0.0201 [-0.0368, -0.0061] |
| FrogMini-14B | Qwen3-14B | +0.0572 [+0.0146, +0.0953] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0009 [-0.0085, +0.0105] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0049 [-0.0157, +0.0053] |
| OpenThinkerAgent-32B | Qwen3-32B | -0.0002 [-0.0313, +0.0368] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0070 [-0.0161, +0.0012] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0167 [-0.0269, -0.0069] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0070 [+0.0021, +0.0132] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0111 [-0.0081, +0.0266] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0408 [+0.0097, +0.0707] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0309 [+0.0009, +0.0602] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0781 [+0.0482, +0.1116] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0308 [+0.0150, +0.0496] |

**M2 abs info gain bits/tok [content/kind=file_view]** (higher is better; instruct ladder 0.6B 0.015, 1.7B 0.054, 4B 0.040, 8B 0.052, 14B 0.054, 32B 0.053; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0182 [-0.0476, +0.0074] |
| tmax-sft-8b | Qwen3-8B | -0.0077 [-0.0338, +0.0159] |
| tmax-8b | Qwen3-8B | -0.0022 [-0.0265, +0.0221] |
| SERA-8B | Qwen3-8B | -0.0134 [-0.0382, +0.0120] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0175 [-0.0445, +0.0069] |
| Arctic-AWM-8B | Qwen3-8B | -0.0084 [-0.0137, -0.0040] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0209 [-0.0430, -0.0007] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0203 [-0.0458, +0.0033] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0024 [-0.0078, +0.0140] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0172 [-0.0338, -0.0017] |
| CodeScout-14B | Qwen3-14B | +0.0119 [+0.0013, +0.0246] |
| SERA-14B | Qwen3-14B | -0.0094 [-0.0273, +0.0068] |
| FrogMini-14B | Qwen3-14B | +0.0779 [-0.0180, +0.1650] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0084 [-0.0024, +0.0200] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0105 [-0.0207, -0.0006] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0423 [-0.0011, +0.1000] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0032 [-0.0025, +0.0086] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0007 [-0.0106, +0.0090] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0056 [+0.0014, +0.0111] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | -0.0012 [-0.0104, +0.0072] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0308 [-0.0041, +0.0688] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0106 [-0.0111, +0.0349] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0214 [-0.0025, +0.0478] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0165 [+0.0013, +0.0328] |

**M2 abs info gain bits/tok [content/kind=search]** (higher is better; instruct ladder 0.6B 0.145, 1.7B 0.324, 4B 0.303, 8B 0.328, 14B 0.331, 32B 0.256; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.1703 [-0.2940, -0.0813] |
| tmax-sft-8b | Qwen3-8B | -0.0882 [-0.1873, -0.0145] |
| tmax-8b | Qwen3-8B | -0.0607 [-0.1655, +0.0266] |
| SERA-8B | Qwen3-8B | -0.0388 [-0.1099, +0.0228] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.1360 [-0.2261, -0.0660] |
| Arctic-AWM-8B | Qwen3-8B | -0.0134 [-0.0300, -0.0013] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0816 [-0.1585, -0.0223] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0985 [-0.1905, -0.0308] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0073 [-0.0521, +0.0682] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.1431 [-0.2545, -0.0743] |
| CodeScout-14B | Qwen3-14B | +0.1004 [+0.0516, +0.1818] |
| SERA-14B | Qwen3-14B | -0.0816 [-0.1551, -0.0333] |
| FrogMini-14B | Qwen3-14B | +0.0301 [-0.1315, +0.1991] |
| Light-IF-14B (non-agentic) | Qwen3-14B | -0.0025 [-0.0472, +0.0361] |
| Nemotron-Terminal-32B | Qwen3-32B | -0.0324 [-0.0895, +0.0036] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0656 [-0.0095, +0.1560] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | -0.0476 [-0.0930, -0.0203] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | -0.0300 [-0.0723, +0.0002] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0275 [+0.0008, +0.0757] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0369 [+0.0082, +0.0760] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.1841 [+0.0730, +0.3682] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.1124 [+0.0424, +0.2341] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.1227 [+0.0500, +0.2248] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.1131 [+0.0564, +0.2068] |

**Reading: next-action bits/tok saved by seeing the obs [all]** (higher is better; instruct ladder 0.6B 0.025, 1.7B 0.040, 4B 0.050, 8B 0.059, 14B 0.031, 32B 0.025; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0316 [-0.0397, -0.0248] |
| tmax-sft-8b | Qwen3-8B | -0.0283 [-0.0361, -0.0212] |
| tmax-8b | Qwen3-8B | -0.0245 [-0.0326, -0.0171] |
| SERA-8B | Qwen3-8B | -0.0233 [-0.0298, -0.0177] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0342 [-0.0411, -0.0278] |
| Arctic-AWM-8B | Qwen3-8B | -0.0042 [-0.0058, -0.0026] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0332 [-0.0393, -0.0276] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0321 [-0.0393, -0.0252] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0075 [+0.0030, +0.0122] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0057 [-0.0088, -0.0028] |
| CodeScout-14B | Qwen3-14B | +0.0119 [+0.0083, +0.0155] |
| SERA-14B | Qwen3-14B | -0.0019 [-0.0050, +0.0010] |
| FrogMini-14B | Qwen3-14B | -0.0003 [-0.0034, +0.0027] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0008 [-0.0016, +0.0030] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0023 [+0.0003, +0.0045] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0169 [+0.0124, +0.0219] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0062 [+0.0038, +0.0085] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0045 [+0.0022, +0.0066] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0038 [+0.0021, +0.0056] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0062 [+0.0021, +0.0102] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0186 [+0.0089, +0.0289] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0274 [+0.0202, +0.0353] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0378 [+0.0300, +0.0467] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0101 [+0.0071, +0.0133] |

**Reading: next-action bits/tok saved by seeing the obs [kind=test_run]** (higher is better; instruct ladder 0.6B 0.017, 1.7B 0.037, 4B 0.044, 8B 0.062, 14B 0.025, 32B 0.017; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0423 [-0.0575, -0.0313] |
| tmax-sft-8b | Qwen3-8B | -0.0399 [-0.0542, -0.0289] |
| tmax-8b | Qwen3-8B | -0.0412 [-0.0570, -0.0298] |
| SERA-8B | Qwen3-8B | -0.0338 [-0.0469, -0.0235] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0463 [-0.0598, -0.0363] |
| Arctic-AWM-8B | Qwen3-8B | -0.0059 [-0.0100, -0.0024] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0412 [-0.0532, -0.0324] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0424 [-0.0574, -0.0313] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0106 [+0.0052, +0.0171] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0051 [-0.0100, -0.0011] |
| CodeScout-14B | Qwen3-14B | +0.0149 [+0.0092, +0.0225] |
| SERA-14B | Qwen3-14B | +0.0001 [-0.0049, +0.0049] |
| FrogMini-14B | Qwen3-14B | +0.0002 [-0.0054, +0.0055] |
| Light-IF-14B (non-agentic) | Qwen3-14B | -0.0018 [-0.0059, +0.0020] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0036 [-0.0001, +0.0078] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0107 [+0.0046, +0.0178] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0035 [-0.0001, +0.0079] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0040 [+0.0010, +0.0073] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | -0.0013 [-0.0055, +0.0021] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0046 [-0.0018, +0.0120] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0214 [+0.0081, +0.0368] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0262 [+0.0163, +0.0381] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0458 [+0.0337, +0.0615] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0091 [+0.0049, +0.0146] |

**Reading: next-action bits/tok saved by seeing the obs [kind=python_exec]** (higher is better; instruct ladder 0.6B -0.002, 1.7B -0.017, 4B 0.013, 8B 0.011, 14B 0.001, 32B 0.005; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0067 [-0.0134, -0.0000] |
| tmax-sft-8b | Qwen3-8B | -0.0017 [-0.0081, +0.0045] |
| tmax-8b | Qwen3-8B | +0.0052 [-0.0020, +0.0129] |
| SERA-8B | Qwen3-8B | -0.0008 [-0.0088, +0.0066] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0122 [-0.0205, -0.0040] |
| Arctic-AWM-8B | Qwen3-8B | -0.0009 [-0.0030, +0.0012] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0096 [-0.0151, -0.0044] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0088 [-0.0151, -0.0031] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | -0.0017 [-0.0054, +0.0018] |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0020 [-0.0022, +0.0061] |
| CodeScout-14B | Qwen3-14B | +0.0037 [+0.0001, +0.0077] |
| SERA-14B | Qwen3-14B | +0.0034 [-0.0001, +0.0072] |
| FrogMini-14B | Qwen3-14B | +0.0015 [-0.0020, +0.0050] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0046 [+0.0017, +0.0077] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0002 [-0.0028, +0.0028] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0069 [+0.0026, +0.0112] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0014 [-0.0014, +0.0040] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0007 [-0.0023, +0.0033] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0069 [+0.0041, +0.0102] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | -0.0013 [-0.0053, +0.0027] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | -0.0202 [-0.0308, -0.0109] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0097 [+0.0030, +0.0172] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0080 [+0.0017, +0.0149] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | -0.0013 [-0.0044, +0.0014] |

**Reading: next-action bits/tok saved by seeing the obs [kind=shell_other]** (higher is better; instruct ladder 0.6B 0.087, 1.7B 0.138, 4B 0.118, 8B 0.124, 14B 0.092, 32B 0.073; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0371 [-0.0814, -0.0061] |
| tmax-sft-8b | Qwen3-8B | -0.0325 [-0.0749, -0.0018] |
| tmax-8b | Qwen3-8B | -0.0344 [-0.0769, -0.0035] |
| SERA-8B | Qwen3-8B | -0.0269 [-0.0649, +0.0015] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0353 [-0.0738, -0.0062] |
| Arctic-AWM-8B | Qwen3-8B | -0.0061 [-0.0143, +0.0024] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0430 [-0.0816, -0.0169] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0425 [-0.0842, -0.0130] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0166 [-0.0180, +0.0592] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0161 [-0.0339, -0.0043] |
| CodeScout-14B | Qwen3-14B | +0.0213 [+0.0077, +0.0396] |
| SERA-14B | Qwen3-14B | -0.0134 [-0.0317, +0.0012] |
| FrogMini-14B | Qwen3-14B | -0.0119 [-0.0286, +0.0027] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0025 [-0.0058, +0.0093] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0056 [-0.0027, +0.0149] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0365 [+0.0191, +0.0634] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0172 [+0.0063, +0.0311] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0056 [-0.0009, +0.0139] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | -0.0019 [-0.0093, +0.0055] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0084 [-0.0078, +0.0270] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0643 [+0.0173, +0.1291] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0410 [+0.0062, +0.0862] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0542 [+0.0170, +0.1069] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0216 [+0.0077, +0.0432] |

**Reading: next-action bits/tok saved by seeing the obs [kind=file_view]** (higher is better; instruct ladder 0.6B 0.050, 1.7B 0.084, 4B 0.088, 8B 0.093, 14B 0.052, 32B 0.037; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0475 [-0.0793, -0.0232] |
| tmax-sft-8b | Qwen3-8B | -0.0479 [-0.0810, -0.0248] |
| tmax-8b | Qwen3-8B | -0.0431 [-0.0757, -0.0200] |
| SERA-8B | Qwen3-8B | -0.0442 [-0.0724, -0.0226] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0463 [-0.0722, -0.0255] |
| Arctic-AWM-8B | Qwen3-8B | -0.0057 [-0.0112, -0.0008] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0508 [-0.0803, -0.0300] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0430 [-0.0759, -0.0208] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0147 [-0.0020, +0.0356] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0143 [-0.0270, -0.0039] |
| CodeScout-14B | Qwen3-14B | +0.0120 [+0.0050, +0.0210] |
| SERA-14B | Qwen3-14B | -0.0116 [-0.0203, -0.0028] |
| FrogMini-14B | Qwen3-14B | -0.0042 [-0.0134, +0.0054] |
| Light-IF-14B (non-agentic) | Qwen3-14B | -0.0052 [-0.0103, -0.0002] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0027 [-0.0044, +0.0094] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0258 [+0.0133, +0.0428] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0108 [+0.0035, +0.0195] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0064 [+0.0003, +0.0137] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0048 [+0.0014, +0.0089] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0202 [+0.0086, +0.0355] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0510 [+0.0197, +0.0965] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0528 [+0.0273, +0.0925] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0583 [+0.0318, +0.0938] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0206 [+0.0098, +0.0360] |

**Reading: next-action bits/tok saved by seeing the obs [kind=search]** (higher is better; instruct ladder 0.6B 0.061, 1.7B 0.093, 4B 0.085, 8B 0.132, 14B 0.075, 32B 0.067; gate FAIL)

| model | start | Δ [95% CI] |
|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B | -0.0629 [-0.1199, -0.0295] |
| tmax-sft-8b | Qwen3-8B | -0.0562 [-0.1080, -0.0250] |
| tmax-8b | Qwen3-8B | -0.0363 [-0.0831, -0.0070] |
| SERA-8B | Qwen3-8B | -0.0275 [-0.0579, -0.0057] |
| OpenThinker-Agent-v1-SFT | Qwen3-8B | -0.0565 [-0.1073, -0.0232] |
| Arctic-AWM-8B | Qwen3-8B | -0.0075 [-0.0156, -0.0005] |
| Light-IF-8B (non-agentic) | Qwen3-8B | -0.0606 [-0.1087, -0.0327] |
| WebWorld-8B (web world model) | Qwen3-8B | -0.0676 [-0.1285, -0.0317] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base | +0.0113 [-0.0023, +0.0299] |
| Nemotron-Terminal-14B | Qwen3-14B | -0.0102 [-0.0268, +0.0042] |
| CodeScout-14B | Qwen3-14B | +0.0286 [+0.0118, +0.0532] |
| SERA-14B | Qwen3-14B | +0.0007 [-0.0148, +0.0199] |
| FrogMini-14B | Qwen3-14B | +0.0139 [-0.0023, +0.0394] |
| Light-IF-14B (non-agentic) | Qwen3-14B | +0.0056 [-0.0046, +0.0202] |
| Nemotron-Terminal-32B | Qwen3-32B | +0.0086 [-0.0019, +0.0212] |
| OpenThinkerAgent-32B | Qwen3-32B | +0.0520 [+0.0203, +0.1067] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base | +0.0180 [+0.0085, +0.0351] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base | +0.0202 [+0.0079, +0.0428] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b | +0.0199 [+0.0119, +0.0360] |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base | +0.0137 [+0.0011, +0.0318] |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base | +0.0448 [+0.0136, +0.1016] |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base | +0.0384 [+0.0157, +0.0757] |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base | +0.0809 [+0.0414, +0.1513] |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base | +0.0304 [+0.0115, +0.0613] |

## Appendix B. Size multiplier by obs_kind (gated metrics)

**M1 recal content bits/tok: size multiplier n by obs_kind** (instruct-ladder gate PASS for every column)

| model | all content | outcome tokens | test_run | python_exec | shell_other | file_view | search |
|---|---|---|---|---|---|---|---|
| Nemotron-Terminal-8B | 0.99x [0.93,1.05] | 0.88x [0.81,0.94] | 0.79x [0.74,0.85] | 0.79x [0.66,0.94] | 1.14x [0.99,1.29] | 1.39x [1.31,1.48] | 1.16x [1.01,1.34] |
| tmax-sft-8b | 1.31x [1.27,1.36] | 1.23x [1.16,1.30] | 1.16x [1.10,1.21] | 1.21x [1.08,1.32] | 1.67x [1.54,1.82] | 1.43x [1.36,1.52] | 1.45x [1.31,1.65] |
| tmax-8b | 1.04x [0.99,1.08] | 1.02x [0.96,1.09] | 0.96x [0.91,1.01] | 0.80x [0.71,0.89] | 1.38x [1.26,1.50] | 1.14x [1.08,1.24] | 1.22x [1.06,1.42] |
| SERA-8B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.54] | 0.56x [0.50,0.62] | <0.50x [0.50,0.57] | 0.65x [0.55,0.76] |
| OpenThinker-Agent-v1-SFT | 0.56x [0.53,0.58] | 0.55x [0.51,0.59] | 0.59x [0.56,0.62] | 0.53x [0.50,0.60] | 0.55x [0.50,0.61] | 0.54x [0.50,0.60] | 0.54x [0.50,0.62] |
| Arctic-AWM-8B | 1.01x [1.01,1.02] | 1.01x [0.99,1.02] | 1.01x [1.00,1.02] | 1.04x [1.01,1.06] | 1.03x [1.01,1.04] | 1.01x [1.00,1.02] | 1.00x [0.98,1.02] |
| Light-IF-8B (non-agentic) | 1.08x [1.06,1.10] | 1.15x [1.09,1.22] | 1.05x [1.02,1.08] | 1.22x [1.16,1.31] | 1.08x [1.02,1.14] | 1.07x [1.03,1.12] | 1.06x [0.99,1.16] |
| WebWorld-8B (web world model) | 1.26x [1.22,1.29] | 1.24x [1.18,1.29] | 1.20x [1.16,1.23] | 1.27x [1.17,1.39] | 1.19x [1.09,1.28] | 1.38x [1.30,1.44] | 1.37x [1.29,1.49] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| Nemotron-Terminal-14B | 0.82x [0.78,0.87] | 0.78x [0.71,0.84] | 0.67x [0.62,0.72] | 0.64x [0.52,0.77] | 1.09x [0.95,1.29] | 1.15x [0.98,1.35] | 0.94x [0.83,1.15] |
| CodeScout-14B | 0.84x [0.83,0.85] | 0.80x [0.77,0.83] | 0.88x [0.86,0.89] | 0.77x [0.73,0.80] | 0.80x [0.77,0.84] | 0.83x [0.80,0.86] | 0.82x [0.78,0.85] |
| SERA-14B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.54] | 0.57x [0.50,0.65] | <0.50x [0.50,0.56] | 0.60x [0.52,0.70] |
| FrogMini-14B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| Light-IF-14B (non-agentic) | 0.82x [0.79,0.84] | 0.84x [0.81,0.88] | 0.84x [0.81,0.87] | 0.89x [0.79,0.98] | 0.85x [0.81,0.89] | 0.77x [0.74,0.81] | 0.76x [0.69,0.83] |
| Nemotron-Terminal-32B | 0.81x [0.76,0.86] | 0.80x [0.72,0.88] | 0.58x [0.53,0.63] | 0.59x [0.50,0.74] | >1.00x [1.00,1.00] | >1.00x [1.00,1.00] | >1.00x [0.94,1.00] |
| OpenThinkerAgent-32B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.51] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.65] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | 0.79x [0.77,0.81] | 0.82x [0.78,0.85] | 0.83x [0.81,0.85] | 0.68x [0.60,0.74] | 0.83x [0.79,0.86] | 0.82x [0.79,0.85] | 0.84x [0.78,0.90] |
| reference: Qwen3-0.6B instruct vs base | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] |
| reference: Qwen3-1.7B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-4B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-8B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-14B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.56] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |

**M2 NLL given true action bits/tok @T*: size multiplier n by obs_kind** (instruct-ladder gate PASS for every column)

| model | all content | outcome tokens | test_run | python_exec | shell_other | file_view | search |
|---|---|---|---|---|---|---|---|
| Nemotron-Terminal-8B | 1.06x [0.96,1.15] | 0.97x [0.87,1.08] | 0.83x [0.73,0.96] | 0.98x [0.76,1.20] | 0.99x [0.79,1.22] | 1.50x [1.40,1.64] | 1.44x [1.22,1.67] |
| tmax-sft-8b | 1.44x [1.37,1.52] | 1.36x [1.22,1.52] | 1.23x [1.14,1.32] | 1.35x [1.14,1.52] | 2.06x [1.74,2.52] | 1.47x [1.36,1.62] | 1.69x [1.45,2.30] |
| tmax-8b | 1.16x [1.09,1.22] | 1.12x [0.99,1.25] | 0.99x [0.92,1.07] | 0.94x [0.74,1.10] | 1.58x [1.36,1.85] | 1.31x [1.21,1.45] | 1.47x [1.24,1.77] |
| SERA-8B | 0.60x [0.54,0.67] | 0.52x [0.50,0.63] | 0.59x [0.51,0.67] | 0.54x [0.50,0.72] | 0.56x [0.50,0.67] | 0.77x [0.60,0.97] | 0.98x [0.79,1.22] |
| OpenThinker-Agent-v1-SFT | 0.69x [0.65,0.73] | 0.74x [0.68,0.80] | 0.71x [0.67,0.76] | 0.62x [0.50,0.75] | 0.71x [0.64,0.77] | 0.71x [0.58,0.85] | 0.66x [0.53,0.80] |
| Arctic-AWM-8B | 1.00x [0.99,1.01] | 1.02x [1.01,1.05] | 1.00x [0.99,1.01] | 0.98x [0.95,1.01] | 1.02x [1.00,1.04] | 0.98x [0.96,1.01] | 0.98x [0.95,1.01] |
| Light-IF-8B (non-agentic) | 1.28x [1.24,1.33] | 1.45x [1.36,1.58] | 1.22x [1.16,1.29] | 1.46x [1.31,1.65] | 1.28x [1.18,1.41] | 1.24x [1.17,1.33] | 1.36x [1.23,1.61] |
| WebWorld-8B (web world model) | 1.39x [1.34,1.45] | 1.41x [1.30,1.53] | 1.38x [1.31,1.46] | 1.45x [1.29,1.66] | 1.37x [1.21,1.58] | 1.35x [1.24,1.47] | 1.55x [1.37,1.97] |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| Nemotron-Terminal-14B | 0.84x [0.78,0.90] | 0.83x [0.74,0.91] | 0.70x [0.62,0.80] | 0.76x [0.64,0.90] | 0.91x [0.77,1.05] | 1.16x [0.99,1.38] | 0.97x [0.85,1.22] |
| CodeScout-14B | 0.72x [0.69,0.75] | 0.67x [0.60,0.72] | 0.78x [0.74,0.81] | 0.61x [0.53,0.68] | 0.62x [0.54,0.69] | 0.78x [0.72,0.83] | 0.72x [0.58,0.79] |
| SERA-14B | 0.56x [0.51,0.62] | 0.56x [0.50,0.65] | 0.51x [0.50,0.59] | 0.54x [0.50,0.71] | 0.51x [0.50,0.67] | 0.70x [0.60,0.80] | 0.75x [0.60,0.90] |
| FrogMini-14B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.52] | <0.50x [0.50,0.89] |
| Light-IF-14B (non-agentic) | 0.92x [0.89,0.95] | 0.97x [0.92,1.04] | 0.99x [0.96,1.06] | 0.95x [0.78,1.32] | 0.95x [0.89,1.04] | 0.87x [0.82,0.91] | 0.86x [0.75,0.95] |
| Nemotron-Terminal-32B | 0.76x [0.69,0.83] | 0.72x [0.63,0.82] | 0.59x [0.51,0.69] | 0.61x [0.50,0.87] | 0.92x [0.81,1.00] | >1.00x [0.91,1.00] | >1.00x [0.81,1.00] |
| OpenThinkerAgent-32B | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.52] | <0.50x [0.50,0.56] |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.56] | <0.50x [0.50,0.50] |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | 0.79x [0.75,0.82] | 0.83x [0.78,0.87] | 0.81x [0.76,0.84] | 0.66x [0.52,0.75] | 0.81x [0.75,0.86] | 0.85x [0.79,0.89] | 0.85x [0.73,0.90] |
| reference: Qwen3-0.6B instruct vs base | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] | <1.00x [1.00,1.00] |
| reference: Qwen3-1.7B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-4B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-8B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] |
| reference: Qwen3-14B instruct vs base | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.50] | <0.50x [0.50,0.54] | <0.50x [0.50,0.51] | <0.50x [0.50,0.50] |

## Appendix C. Ladders and gate details (all metrics)
## M1 recal content bits/tok [content] (lower is better)
- inst ladder: 0.6B 1.8212, 1.7B 1.5555, 4B 1.3179, 8B 1.2029, 14B 1.0892, 32B 1.0164; monotone=True; GATE=PASS (0.6B->1.7B -0.2657 [-0.2848,-0.2472]; 1.7B->4B -0.2377 [-0.2536,-0.2228]; 4B->8B -0.1149 [-0.1248,-0.1061]; 8B->14B -0.1138 [-0.1207,-0.1065]; 14B->32B -0.0727 [-0.0791,-0.0671])
- base ladder: 0.6B 1.5172, 1.7B 1.2838, 4B 1.1164, 8B 1.0556, 14B 0.9872; monotone=True; GATE=PASS (0.6B->1.7B -0.2334 [-0.2480,-0.2203]; 1.7B->4B -0.1674 [-0.1786,-0.1565]; 4B->8B -0.0608 [-0.0665,-0.0549]; 8B->14B -0.0684 [-0.0735,-0.0631])
## M1 recal content bits/tok [kind=edit_ack] (lower is better)
- inst ladder: 0.6B 0.5051, 1.7B 0.4890, 4B 0.3955, 8B 0.3686, 14B 0.3251, 32B 0.3030; monotone=True; GATE=FAIL (0.6B->1.7B -0.0161 [-0.0350,+0.0026]; 1.7B->4B -0.0935 [-0.1108,-0.0769]; 4B->8B -0.0269 [-0.0374,-0.0169]; 8B->14B -0.0434 [-0.0539,-0.0333]; 14B->32B -0.0222 [-0.0336,-0.0117])
- base ladder: 0.6B 0.4206, 1.7B 0.3566, 4B 0.3118, 8B 0.3066, 14B 0.2829; monotone=True; GATE=FAIL (0.6B->1.7B -0.0640 [-0.0787,-0.0518]; 1.7B->4B -0.0448 [-0.0591,-0.0306]; 4B->8B -0.0051 [-0.0137,+0.0033]; 8B->14B -0.0237 [-0.0329,-0.0143])
## M1 recal content bits/tok [kind=file_view] (lower is better)
- inst ladder: 0.6B 1.6240, 1.7B 1.4389, 4B 1.2513, 8B 1.1453, 14B 1.0499, 32B 0.9829; monotone=True; GATE=PASS (0.6B->1.7B -0.1851 [-0.2159,-0.1560]; 1.7B->4B -0.1876 [-0.2077,-0.1699]; 4B->8B -0.1060 [-0.1207,-0.0899]; 8B->14B -0.0954 [-0.1051,-0.0864]; 14B->32B -0.0670 [-0.0797,-0.0551])
- base ladder: 0.6B 1.3917, 1.7B 1.2101, 4B 1.0564, 8B 1.0054, 14B 0.9463; monotone=True; GATE=PASS (0.6B->1.7B -0.1816 [-0.1995,-0.1629]; 1.7B->4B -0.1537 [-0.1732,-0.1383]; 4B->8B -0.0510 [-0.0610,-0.0405]; 8B->14B -0.0591 [-0.0689,-0.0506])
## M1 recal content bits/tok [kind=python_exec] (lower is better)
- inst ladder: 0.6B 1.5361, 1.7B 1.2993, 4B 1.0669, 8B 0.9575, 14B 0.8608, 32B 0.8014; monotone=True; GATE=PASS (0.6B->1.7B -0.2368 [-0.2718,-0.2013]; 1.7B->4B -0.2324 [-0.2712,-0.1997]; 4B->8B -0.1094 [-0.1316,-0.0878]; 8B->14B -0.0967 [-0.1139,-0.0793]; 14B->32B -0.0594 [-0.0776,-0.0414])
- base ladder: 0.6B 1.2937, 1.7B 1.0346, 4B 0.8885, 8B 0.8357, 14B 0.7754; monotone=True; GATE=PASS (0.6B->1.7B -0.2590 [-0.2967,-0.2294]; 1.7B->4B -0.1461 [-0.1669,-0.1263]; 4B->8B -0.0528 [-0.0652,-0.0403]; 8B->14B -0.0603 [-0.0738,-0.0472])
## M1 recal content bits/tok [kind=search] (lower is better)
- inst ladder: 0.6B 2.5861, 1.7B 2.2788, 4B 2.0017, 8B 1.8563, 14B 1.7100, 32B 1.6247; monotone=True; GATE=PASS (0.6B->1.7B -0.3073 [-0.3666,-0.2568]; 1.7B->4B -0.2771 [-0.3278,-0.2392]; 4B->8B -0.1454 [-0.1744,-0.1221]; 8B->14B -0.1462 [-0.1745,-0.1246]; 14B->32B -0.0853 [-0.1126,-0.0581])
- base ladder: 0.6B 2.2714, 1.7B 1.9884, 4B 1.7682, 8B 1.6602, 14B 1.5594; monotone=True; GATE=PASS (0.6B->1.7B -0.2829 [-0.3529,-0.2384]; 1.7B->4B -0.2203 [-0.2548,-0.1933]; 4B->8B -0.1080 [-0.1374,-0.0865]; 8B->14B -0.1009 [-0.1314,-0.0775])
## M1 recal content bits/tok [kind=shell_other] (lower is better)
- inst ladder: 0.6B 1.4472, 1.7B 1.1178, 4B 0.8863, 8B 0.7936, 14B 0.7030, 32B 0.6386; monotone=True; GATE=PASS (0.6B->1.7B -0.3294 [-0.3747,-0.2868]; 1.7B->4B -0.2315 [-0.2650,-0.2029]; 4B->8B -0.0927 [-0.1123,-0.0757]; 8B->14B -0.0906 [-0.1063,-0.0768]; 14B->32B -0.0645 [-0.0760,-0.0543])
- base ladder: 0.6B 1.0906, 1.7B 0.8752, 4B 0.7258, 8B 0.6866, 14B 0.6369; monotone=True; GATE=PASS (0.6B->1.7B -0.2154 [-0.2417,-0.1906]; 1.7B->4B -0.1494 [-0.1704,-0.1297]; 4B->8B -0.0392 [-0.0482,-0.0296]; 8B->14B -0.0497 [-0.0603,-0.0402])
## M1 recal content bits/tok [kind=test_run] (lower is better)
- inst ladder: 0.6B 2.4603, 1.7B 2.1103, 4B 1.8013, 8B 1.6485, 14B 1.4908, 32B 1.3949; monotone=True; GATE=PASS (0.6B->1.7B -0.3500 [-0.3819,-0.3190]; 1.7B->4B -0.3089 [-0.3393,-0.2825]; 4B->8B -0.1528 [-0.1705,-0.1380]; 8B->14B -0.1577 [-0.1710,-0.1445]; 14B->32B -0.0959 [-0.1068,-0.0858])
- base ladder: 0.6B 2.0650, 1.7B 1.7560, 4B 1.5407, 8B 1.4520, 14B 1.3579; monotone=True; GATE=PASS (0.6B->1.7B -0.3090 [-0.3400,-0.2801]; 1.7B->4B -0.2153 [-0.2372,-0.1946]; 4B->8B -0.0887 [-0.1003,-0.0785]; 8B->14B -0.0940 [-0.1036,-0.0844])
## M1 recal content bits/tok [outcome] (lower is better)
- inst ladder: 0.6B 1.6701, 1.7B 1.4821, 4B 1.2878, 8B 1.1975, 14B 1.0970, 32B 1.0399; monotone=True; GATE=PASS (0.6B->1.7B -0.1880 [-0.2114,-0.1654]; 1.7B->4B -0.1943 [-0.2117,-0.1766]; 4B->8B -0.0903 [-0.1013,-0.0801]; 8B->14B -0.1005 [-0.1119,-0.0889]; 14B->32B -0.0572 [-0.0662,-0.0483])
- base ladder: 0.6B 1.4149, 1.7B 1.2474, 4B 1.1249, 8B 1.0750, 14B 1.0145; monotone=True; GATE=PASS (0.6B->1.7B -0.1675 [-0.1816,-0.1527]; 1.7B->4B -0.1225 [-0.1365,-0.1084]; 4B->8B -0.0499 [-0.0584,-0.0423]; 8B->14B -0.0605 [-0.0685,-0.0532])
## M2 NLL given true action bits/tok @T* [content/all] (lower is better)
- inst ladder: 0.6B 1.8827, 1.7B 1.6734, 4B 1.3477, 8B 1.2152, 14B 1.0703, 32B 0.9748; monotone=True; GATE=PASS (0.6B->1.7B -0.2093 [-0.2365,-0.1821]; 1.7B->4B -0.3256 [-0.3572,-0.2978]; 4B->8B -0.1326 [-0.1506,-0.1149]; 8B->14B -0.1449 [-0.1587,-0.1319]; 14B->32B -0.0955 [-0.1065,-0.0856])
- base ladder: 0.6B 1.5492, 1.7B 1.2764, 4B 1.0958, 8B 1.0290, 14B 0.9456; monotone=True; GATE=PASS (0.6B->1.7B -0.2728 [-0.2958,-0.2503]; 1.7B->4B -0.1806 [-0.1977,-0.1657]; 4B->8B -0.0669 [-0.0774,-0.0565]; 8B->14B -0.0833 [-0.0931,-0.0737])
## M2 NLL given true action bits/tok @T* [content/kind=edit_ack] (lower is better)
- inst ladder: 0.6B 0.8273, 1.7B 0.8550, 4B 0.6356, 8B 0.6412, 14B 0.5419, 32B 0.4974; monotone=False; GATE=FAIL (0.6B->1.7B +0.0278 [-0.0400,+0.0985]; 1.7B->4B -0.2194 [-0.3346,-0.1205]; 4B->8B +0.0056 [-0.0502,+0.0720]; 8B->14B -0.0993 [-0.1765,-0.0358]; 14B->32B -0.0445 [-0.1110,-0.0004])
- base ladder: 0.6B 0.7256, 1.7B 0.5981, 4B 0.5256, 8B 0.5170, 14B 0.4606; monotone=True; GATE=FAIL (0.6B->1.7B -0.1275 [-0.1969,-0.0818]; 1.7B->4B -0.0725 [-0.1001,-0.0485]; 4B->8B -0.0086 [-0.0353,+0.0137]; 8B->14B -0.0565 [-0.1177,-0.0111])
## M2 NLL given true action bits/tok @T* [content/kind=file_view] (lower is better)
- inst ladder: 0.6B 1.8616, 1.7B 1.6974, 4B 1.4482, 8B 1.3322, 14B 1.1699, 32B 1.0910; monotone=True; GATE=PASS (0.6B->1.7B -0.1642 [-0.2251,-0.1001]; 1.7B->4B -0.2492 [-0.3091,-0.2003]; 4B->8B -0.1160 [-0.1498,-0.0849]; 8B->14B -0.1623 [-0.1972,-0.1299]; 14B->32B -0.0790 [-0.0973,-0.0590])
- base ladder: 0.6B 1.6055, 1.7B 1.3831, 4B 1.2057, 8B 1.1421, 14B 1.0516; monotone=True; GATE=PASS (0.6B->1.7B -0.2224 [-0.2671,-0.1812]; 1.7B->4B -0.1774 [-0.2227,-0.1397]; 4B->8B -0.0636 [-0.0819,-0.0467]; 8B->14B -0.0905 [-0.1146,-0.0652])
## M2 NLL given true action bits/tok @T* [content/kind=python_exec] (lower is better)
- inst ladder: 0.6B 1.4527, 1.7B 1.3687, 4B 1.0457, 8B 0.9431, 14B 0.8207, 32B 0.7476; monotone=True; GATE=PASS (0.6B->1.7B -0.0840 [-0.1264,-0.0406]; 1.7B->4B -0.3230 [-0.3880,-0.2675]; 4B->8B -0.1026 [-0.1385,-0.0688]; 8B->14B -0.1224 [-0.1531,-0.0943]; 14B->32B -0.0731 [-0.1002,-0.0451])
- base ladder: 0.6B 1.2186, 1.7B 0.9823, 4B 0.8355, 8B 0.7826, 14B 0.7172; monotone=True; GATE=PASS (0.6B->1.7B -0.2363 [-0.2773,-0.2030]; 1.7B->4B -0.1468 [-0.1808,-0.1166]; 4B->8B -0.0529 [-0.0735,-0.0350]; 8B->14B -0.0654 [-0.0878,-0.0450])
## M2 NLL given true action bits/tok @T* [content/kind=search] (lower is better)
- inst ladder: 0.6B 2.8866, 1.7B 2.7035, 4B 2.2616, 8B 2.0677, 14B 1.8477, 32B 1.7170; monotone=True; GATE=PASS (0.6B->1.7B -0.1830 [-0.2840,-0.0595]; 1.7B->4B -0.4419 [-0.5594,-0.3601]; 4B->8B -0.1940 [-0.2583,-0.1158]; 8B->14B -0.2200 [-0.3014,-0.1462]; 14B->32B -0.1307 [-0.1662,-0.0827])
- base ladder: 0.6B 2.4796, 1.7B 2.1568, 4B 1.9069, 8B 1.7783, 14B 1.6575; monotone=True; GATE=PASS (0.6B->1.7B -0.3228 [-0.4048,-0.2531]; 1.7B->4B -0.2500 [-0.3076,-0.2047]; 4B->8B -0.1286 [-0.1822,-0.0824]; 8B->14B -0.1207 [-0.1982,-0.0609])
## M2 NLL given true action bits/tok @T* [content/kind=shell_other] (lower is better)
- inst ladder: 0.6B 1.4455, 1.7B 1.1419, 4B 0.8345, 8B 0.7272, 14B 0.6340, 32B 0.5543; monotone=True; GATE=PASS (0.6B->1.7B -0.3036 [-0.3599,-0.2476]; 1.7B->4B -0.3074 [-0.3677,-0.2519]; 4B->8B -0.1073 [-0.1384,-0.0773]; 8B->14B -0.0931 [-0.1175,-0.0707]; 14B->32B -0.0797 [-0.1023,-0.0590])
- base ladder: 0.6B 1.0457, 1.7B 0.7846, 4B 0.6310, 8B 0.6040, 14B 0.5547; monotone=True; GATE=PASS (0.6B->1.7B -0.2612 [-0.3028,-0.2243]; 1.7B->4B -0.1536 [-0.1827,-0.1293]; 4B->8B -0.0270 [-0.0442,-0.0107]; 8B->14B -0.0493 [-0.0640,-0.0372])
## M2 NLL given true action bits/tok @T* [content/kind=test_run] (lower is better)
- inst ladder: 0.6B 2.3271, 1.7B 2.0752, 4B 1.7029, 8B 1.5258, 14B 1.3522, 32B 1.2271; monotone=True; GATE=PASS (0.6B->1.7B -0.2519 [-0.2994,-0.2080]; 1.7B->4B -0.3723 [-0.4259,-0.3267]; 4B->8B -0.1771 [-0.2127,-0.1457]; 8B->14B -0.1735 [-0.1971,-0.1492]; 14B->32B -0.1251 [-0.1461,-0.1050])
- base ladder: 0.6B 1.9439, 1.7B 1.6117, 4B 1.3960, 8B 1.2972, 14B 1.1893; monotone=True; GATE=PASS (0.6B->1.7B -0.3322 [-0.3814,-0.2869]; 1.7B->4B -0.2157 [-0.2499,-0.1865]; 4B->8B -0.0988 [-0.1218,-0.0777]; 8B->14B -0.1080 [-0.1270,-0.0900])
## M2 NLL given true action bits/tok @T* [outcome/all] (lower is better)
- inst ladder: 0.6B 1.7416, 1.7B 1.6460, 4B 1.3801, 8B 1.2491, 14B 1.1278, 32B 1.0360; monotone=True; GATE=PASS (0.6B->1.7B -0.0956 [-0.1316,-0.0582]; 1.7B->4B -0.2660 [-0.3013,-0.2353]; 4B->8B -0.1309 [-0.1567,-0.1056]; 8B->14B -0.1213 [-0.1400,-0.1030]; 14B->32B -0.0918 [-0.1090,-0.0727])
- base ladder: 0.6B 1.4945, 1.7B 1.2944, 4B 1.1638, 8B 1.0941, 14B 1.0209; monotone=True; GATE=PASS (0.6B->1.7B -0.2001 [-0.2265,-0.1747]; 1.7B->4B -0.1306 [-0.1515,-0.1111]; 4B->8B -0.0698 [-0.0862,-0.0561]; 8B->14B -0.0732 [-0.0869,-0.0602])
## M2 abs info gain bits/tok @T* [content/all] (higher is better)
- inst ladder: 0.6B 0.2242, 1.7B 0.2855, 4B 0.2645, 8B 0.2673, 14B 0.2532, 32B 0.2342; monotone=False; GATE=FAIL (0.6B->1.7B +0.0613 [+0.0486,+0.0742]; 1.7B->4B -0.0209 [-0.0334,-0.0078]; 4B->8B +0.0028 [-0.0053,+0.0109]; 8B->14B -0.0141 [-0.0218,-0.0065]; 14B->32B -0.0190 [-0.0272,-0.0114])
- base ladder: 0.6B 0.2117, 1.7B 0.2240, 4B 0.2301, 8B 0.2182, 14B 0.2192; monotone=False; GATE=FAIL (0.6B->1.7B +0.0123 [+0.0058,+0.0190]; 1.7B->4B +0.0061 [-0.0011,+0.0136]; 4B->8B -0.0118 [-0.0175,-0.0065]; 8B->14B +0.0009 [-0.0035,+0.0057])
## M2 abs info gain bits/tok @T* [content/kind=edit_ack] (higher is better)
- inst ladder: 0.6B 0.3610, 1.7B 0.3933, 4B 0.3710, 8B 0.3202, 14B 0.2617, 32B 0.2490; monotone=False; GATE=FAIL (0.6B->1.7B +0.0323 [-0.0412,+0.1372]; 1.7B->4B -0.0222 [-0.0962,+0.0319]; 4B->8B -0.0509 [-0.1016,+0.0030]; 8B->14B -0.0585 [-0.1045,-0.0180]; 14B->32B -0.0127 [-0.0410,+0.0209])
- base ladder: 0.6B 0.3270, 1.7B 0.2996, 4B 0.2730, 8B 0.2620, 14B 0.2382; monotone=False; GATE=FAIL (0.6B->1.7B -0.0275 [-0.0620,+0.0100]; 1.7B->4B -0.0266 [-0.0606,+0.0054]; 4B->8B -0.0110 [-0.0244,+0.0066]; 8B->14B -0.0238 [-0.0545,+0.0063])
## M2 abs info gain bits/tok @T* [content/kind=file_view] (higher is better)
- inst ladder: 0.6B 0.0175, 1.7B 0.0418, 4B 0.0346, 8B 0.0400, 14B 0.0508, 32B 0.0517; monotone=False; GATE=FAIL (0.6B->1.7B +0.0243 [+0.0058,+0.0442]; 1.7B->4B -0.0072 [-0.0239,+0.0087]; 4B->8B +0.0054 [-0.0061,+0.0181]; 8B->14B +0.0107 [-0.0009,+0.0223]; 14B->32B +0.0010 [-0.0118,+0.0120])
- base ladder: 0.6B 0.0162, 1.7B 0.0233, 4B 0.0292, 8B 0.0311, 14B 0.0377; monotone=True; GATE=FAIL (0.6B->1.7B +0.0071 [+0.0019,+0.0136]; 1.7B->4B +0.0059 [+0.0006,+0.0109]; 4B->8B +0.0019 [-0.0032,+0.0074]; 8B->14B +0.0066 [+0.0010,+0.0121])
## M2 abs info gain bits/tok @T* [content/kind=python_exec] (higher is better)
- inst ladder: 0.6B 0.8837, 1.7B 1.0750, 4B 0.9326, 8B 0.9224, 14B 0.8534, 32B 0.7766; monotone=False; GATE=FAIL (0.6B->1.7B +0.1913 [+0.1362,+0.2638]; 1.7B->4B -0.1424 [-0.2079,-0.0847]; 4B->8B -0.0102 [-0.0406,+0.0234]; 8B->14B -0.0690 [-0.1056,-0.0394]; 14B->32B -0.0768 [-0.1060,-0.0471])
- base ladder: 0.6B 0.8538, 1.7B 0.8465, 4B 0.8277, 8B 0.7662, 14B 0.7549; monotone=False; GATE=FAIL (0.6B->1.7B -0.0072 [-0.0329,+0.0207]; 1.7B->4B -0.0188 [-0.0549,+0.0165]; 4B->8B -0.0615 [-0.0809,-0.0412]; 8B->14B -0.0113 [-0.0329,+0.0062])
## M2 abs info gain bits/tok @T* [content/kind=search] (higher is better)
- inst ladder: 0.6B 0.1343, 1.7B 0.2124, 4B 0.2266, 8B 0.2386, 14B 0.2748, 32B 0.2401; monotone=False; GATE=FAIL (0.6B->1.7B +0.0781 [+0.0317,+0.1517]; 1.7B->4B +0.0142 [-0.0388,+0.0802]; 4B->8B +0.0120 [-0.0211,+0.0448]; 8B->14B +0.0362 [+0.0048,+0.0878]; 14B->32B -0.0347 [-0.0805,+0.0001])
- base ladder: 0.6B 0.1079, 1.7B 0.1396, 4B 0.1910, 8B 0.2050, 14B 0.2177; monotone=True; GATE=FAIL (0.6B->1.7B +0.0317 [+0.0033,+0.0742]; 1.7B->4B +0.0514 [+0.0213,+0.0985]; 4B->8B +0.0140 [-0.0034,+0.0377]; 8B->14B +0.0127 [-0.0085,+0.0407])
## M2 abs info gain bits/tok @T* [content/kind=shell_other] (higher is better)
- inst ladder: 0.6B 0.0620, 1.7B 0.0857, 4B 0.0981, 8B 0.1209, 14B 0.1154, 32B 0.1154; monotone=False; GATE=FAIL (0.6B->1.7B +0.0237 [+0.0098,+0.0388]; 1.7B->4B +0.0124 [-0.0048,+0.0300]; 4B->8B +0.0227 [+0.0072,+0.0401]; 8B->14B -0.0055 [-0.0190,+0.0073]; 14B->32B +0.0000 [-0.0115,+0.0102])
- base ladder: 0.6B 0.0576, 1.7B 0.0894, 4B 0.1011, 8B 0.0983, 14B 0.1052; monotone=False; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0220,+0.0417]; 1.7B->4B +0.0118 [+0.0022,+0.0224]; 4B->8B -0.0029 [-0.0107,+0.0063]; 8B->14B +0.0069 [-0.0009,+0.0133])
## M2 abs info gain bits/tok @T* [content/kind=test_run] (higher is better)
- inst ladder: 0.6B 0.1739, 1.7B 0.2267, 4B 0.2198, 8B 0.2162, 14B 0.2009, 32B 0.1842; monotone=False; GATE=FAIL (0.6B->1.7B +0.0529 [+0.0333,+0.0754]; 1.7B->4B -0.0069 [-0.0234,+0.0110]; 4B->8B -0.0036 [-0.0178,+0.0088]; 8B->14B -0.0153 [-0.0271,-0.0040]; 14B->32B -0.0167 [-0.0289,-0.0042])
- base ladder: 0.6B 0.1618, 1.7B 0.1718, 4B 0.1796, 8B 0.1699, 14B 0.1690; monotone=False; GATE=FAIL (0.6B->1.7B +0.0101 [+0.0021,+0.0200]; 1.7B->4B +0.0078 [-0.0018,+0.0171]; 4B->8B -0.0097 [-0.0226,-0.0003]; 8B->14B -0.0009 [-0.0084,+0.0070])
## M2 abs info gain bits/tok @T* [outcome/all] (higher is better)
- inst ladder: 0.6B 0.1754, 1.7B 0.2174, 4B 0.1929, 8B 0.2092, 14B 0.1968, 32B 0.1779; monotone=False; GATE=FAIL (0.6B->1.7B +0.0420 [+0.0235,+0.0625]; 1.7B->4B -0.0245 [-0.0447,-0.0055]; 4B->8B +0.0163 [+0.0038,+0.0288]; 8B->14B -0.0124 [-0.0251,+0.0001]; 14B->32B -0.0189 [-0.0304,-0.0071])
- base ladder: 0.6B 0.1713, 1.7B 0.1779, 4B 0.1826, 8B 0.1752, 14B 0.1726; monotone=False; GATE=FAIL (0.6B->1.7B +0.0066 [-0.0022,+0.0161]; 1.7B->4B +0.0047 [-0.0028,+0.0120]; 4B->8B -0.0074 [-0.0168,+0.0016]; 8B->14B -0.0027 [-0.0114,+0.0065])
## M2 abs info gain bits/tok [content/all] (higher is better)
- inst ladder: 0.6B 0.2419, 1.7B 0.4246, 4B 0.3585, 8B 0.3686, 14B 0.2972, 32B 0.2479; monotone=False; GATE=FAIL (0.6B->1.7B +0.1827 [+0.1488,+0.2183]; 1.7B->4B -0.0661 [-0.0907,-0.0414]; 4B->8B +0.0101 [-0.0033,+0.0251]; 8B->14B -0.0714 [-0.0888,-0.0547]; 14B->32B -0.0493 [-0.0637,-0.0369])
- base ladder: 0.6B 0.2117, 1.7B 0.2240, 4B 0.2301, 8B 0.2182, 14B 0.2192; monotone=False; GATE=FAIL (0.6B->1.7B +0.0123 [+0.0058,+0.0190]; 1.7B->4B +0.0061 [-0.0011,+0.0136]; 4B->8B -0.0118 [-0.0175,-0.0065]; 8B->14B +0.0009 [-0.0036,+0.0057])
## M2 abs info gain bits/tok [content/kind=edit_ack] (higher is better)
- inst ladder: 0.6B 0.3835, 1.7B 0.5370, 4B 0.5134, 8B 0.4207, 14B 0.3007, 32B 0.2534; monotone=False; GATE=FAIL (0.6B->1.7B +0.1535 [+0.0341,+0.3123]; 1.7B->4B -0.0236 [-0.1523,+0.0776]; 4B->8B -0.0927 [-0.1833,+0.0070]; 8B->14B -0.1200 [-0.1992,-0.0506]; 14B->32B -0.0473 [-0.0836,-0.0066])
- base ladder: 0.6B 0.3270, 1.7B 0.2996, 4B 0.2730, 8B 0.2620, 14B 0.2382; monotone=False; GATE=FAIL (0.6B->1.7B -0.0274 [-0.0620,+0.0100]; 1.7B->4B -0.0266 [-0.0606,+0.0054]; 4B->8B -0.0110 [-0.0244,+0.0066]; 8B->14B -0.0238 [-0.0544,+0.0063])
## M2 abs info gain bits/tok [content/kind=file_view] (higher is better)
- inst ladder: 0.6B 0.0150, 1.7B 0.0541, 4B 0.0398, 8B 0.0525, 14B 0.0542, 32B 0.0527; monotone=False; GATE=FAIL (0.6B->1.7B +0.0391 [+0.0059,+0.0765]; 1.7B->4B -0.0143 [-0.0427,+0.0120]; 4B->8B +0.0127 [-0.0064,+0.0338]; 8B->14B +0.0017 [-0.0186,+0.0223]; 14B->32B -0.0014 [-0.0191,+0.0135])
- base ladder: 0.6B 0.0162, 1.7B 0.0233, 4B 0.0292, 8B 0.0311, 14B 0.0377; monotone=True; GATE=FAIL (0.6B->1.7B +0.0070 [+0.0019,+0.0136]; 1.7B->4B +0.0059 [+0.0006,+0.0109]; 4B->8B +0.0019 [-0.0032,+0.0074]; 8B->14B +0.0066 [+0.0010,+0.0121])
## M2 abs info gain bits/tok [content/kind=python_exec] (higher is better)
- inst ladder: 0.6B 0.9591, 1.7B 1.6275, 4B 1.2753, 8B 1.2586, 14B 1.0085, 32B 0.8275; monotone=False; GATE=FAIL (0.6B->1.7B +0.6684 [+0.5306,+0.8515]; 1.7B->4B -0.3522 [-0.4836,-0.2454]; 4B->8B -0.0167 [-0.0676,+0.0375]; 8B->14B -0.2501 [-0.3332,-0.1855]; 14B->32B -0.1810 [-0.2322,-0.1350])
- base ladder: 0.6B 0.8538, 1.7B 0.8465, 4B 0.8277, 8B 0.7662, 14B 0.7549; monotone=False; GATE=FAIL (0.6B->1.7B -0.0072 [-0.0330,+0.0207]; 1.7B->4B -0.0188 [-0.0549,+0.0165]; 4B->8B -0.0615 [-0.0808,-0.0412]; 8B->14B -0.0113 [-0.0329,+0.0063])
## M2 abs info gain bits/tok [content/kind=search] (higher is better)
- inst ladder: 0.6B 0.1448, 1.7B 0.3238, 4B 0.3035, 8B 0.3277, 14B 0.3308, 32B 0.2557; monotone=False; GATE=FAIL (0.6B->1.7B +0.1789 [+0.0849,+0.3400]; 1.7B->4B -0.0203 [-0.1099,+0.0709]; 4B->8B +0.0242 [-0.0374,+0.0822]; 8B->14B +0.0030 [-0.0522,+0.0745]; 14B->32B -0.0751 [-0.1522,-0.0204])
- base ladder: 0.6B 0.1079, 1.7B 0.1397, 4B 0.1910, 8B 0.2050, 14B 0.2177; monotone=True; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0034,+0.0742]; 1.7B->4B +0.0514 [+0.0213,+0.0985]; 4B->8B +0.0140 [-0.0034,+0.0377]; 8B->14B +0.0127 [-0.0086,+0.0407])
## M2 abs info gain bits/tok [content/kind=shell_other] (higher is better)
- inst ladder: 0.6B 0.0687, 1.7B 0.1301, 4B 0.1320, 8B 0.1764, 14B 0.1360, 32B 0.1195; monotone=False; GATE=FAIL (0.6B->1.7B +0.0615 [+0.0393,+0.0899]; 1.7B->4B +0.0019 [-0.0251,+0.0285]; 4B->8B +0.0444 [+0.0204,+0.0712]; 8B->14B -0.0404 [-0.0662,-0.0160]; 14B->32B -0.0165 [-0.0344,-0.0015])
- base ladder: 0.6B 0.0576, 1.7B 0.0894, 4B 0.1011, 8B 0.0983, 14B 0.1052; monotone=False; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0220,+0.0417]; 1.7B->4B +0.0118 [+0.0022,+0.0225]; 4B->8B -0.0029 [-0.0107,+0.0063]; 8B->14B +0.0069 [-0.0009,+0.0133])
## M2 abs info gain bits/tok [content/kind=test_run] (higher is better)
- inst ladder: 0.6B 0.1868, 1.7B 0.3311, 4B 0.2969, 8B 0.3009, 14B 0.2346, 32B 0.1966; monotone=False; GATE=FAIL (0.6B->1.7B +0.1444 [+0.0913,+0.2071]; 1.7B->4B -0.0342 [-0.0667,-0.0003]; 4B->8B +0.0040 [-0.0189,+0.0240]; 8B->14B -0.0663 [-0.0972,-0.0398]; 14B->32B -0.0380 [-0.0601,-0.0182])
- base ladder: 0.6B 0.1618, 1.7B 0.1718, 4B 0.1796, 8B 0.1699, 14B 0.1690; monotone=False; GATE=FAIL (0.6B->1.7B +0.0101 [+0.0021,+0.0200]; 1.7B->4B +0.0078 [-0.0018,+0.0171]; 4B->8B -0.0097 [-0.0226,-0.0003]; 8B->14B -0.0009 [-0.0084,+0.0070])
## M2 abs info gain bits/tok [outcome/all] (higher is better)
- inst ladder: 0.6B 0.1871, 1.7B 0.3128, 4B 0.2488, 8B 0.2802, 14B 0.2254, 32B 0.1866; monotone=False; GATE=FAIL (0.6B->1.7B +0.1257 [+0.0837,+0.1743]; 1.7B->4B -0.0641 [-0.1014,-0.0267]; 4B->8B +0.0315 [+0.0099,+0.0529]; 8B->14B -0.0548 [-0.0804,-0.0312]; 14B->32B -0.0388 [-0.0575,-0.0218])
- base ladder: 0.6B 0.1713, 1.7B 0.1779, 4B 0.1826, 8B 0.1752, 14B 0.1726; monotone=False; GATE=FAIL (0.6B->1.7B +0.0066 [-0.0021,+0.0161]; 1.7B->4B +0.0047 [-0.0029,+0.0120]; 4B->8B -0.0074 [-0.0168,+0.0016]; 8B->14B -0.0027 [-0.0114,+0.0065])
## M2 relative gain [content/all] (higher is better)
- inst ladder: 0.6B 0.1090, 1.7B 0.1566, 4B 0.1715, 8B 0.1920, 14B 0.1974, 32B 0.1975; monotone=True; GATE=FAIL (0.6B->1.7B +0.0476 [+0.0395,+0.0562]; 1.7B->4B +0.0149 [+0.0072,+0.0241]; 4B->8B +0.0205 [+0.0132,+0.0282]; 8B->14B +0.0054 [-0.0002,+0.0110]; 14B->32B +0.0000 [-0.0060,+0.0063])
- base ladder: 0.6B 0.1202, 1.7B 0.1493, 4B 0.1735, 8B 0.1750, 14B 0.1882; monotone=True; GATE=FAIL (0.6B->1.7B +0.0291 [+0.0238,+0.0351]; 1.7B->4B +0.0243 [+0.0197,+0.0296]; 4B->8B +0.0015 [-0.0019,+0.0051]; 8B->14B +0.0132 [+0.0097,+0.0170])
## M2 relative gain [content/kind=edit_ack] (higher is better)
- inst ladder: 0.6B 0.3045, 1.7B 0.2961, 4B 0.3795, 8B 0.3238, 14B 0.3245, 32B 0.3275; monotone=False; GATE=FAIL (0.6B->1.7B -0.0084 [-0.0728,+0.0812]; 1.7B->4B +0.0834 [+0.0081,+0.1476]; 4B->8B -0.0556 [-0.1192,+0.0115]; 8B->14B +0.0006 [-0.0617,+0.0639]; 14B->32B +0.0031 [-0.0517,+0.0561])
- base ladder: 0.6B 0.3107, 1.7B 0.3337, 4B 0.3418, 8B 0.3363, 14B 0.3408; monotone=False; GATE=FAIL (0.6B->1.7B +0.0230 [-0.0036,+0.0511]; 1.7B->4B +0.0081 [-0.0236,+0.0418]; 4B->8B -0.0055 [-0.0226,+0.0157]; 8B->14B +0.0046 [-0.0321,+0.0424])
## M2 relative gain [content/kind=file_view] (higher is better)
- inst ladder: 0.6B 0.0076, 1.7B 0.0228, 4B 0.0208, 8B 0.0300, 14B 0.0396, 32B 0.0447; monotone=False; GATE=FAIL (0.6B->1.7B +0.0152 [+0.0018,+0.0294]; 1.7B->4B -0.0020 [-0.0134,+0.0092]; 4B->8B +0.0092 [-0.0016,+0.0218]; 8B->14B +0.0096 [-0.0018,+0.0218]; 14B->32B +0.0052 [-0.0071,+0.0160])
- base ladder: 0.6B 0.0100, 1.7B 0.0166, 4B 0.0236, 8B 0.0265, 14B 0.0346; monotone=True; GATE=FAIL (0.6B->1.7B +0.0065 [+0.0031,+0.0113]; 1.7B->4B +0.0071 [+0.0030,+0.0115]; 4B->8B +0.0029 [-0.0015,+0.0078]; 8B->14B +0.0081 [+0.0027,+0.0130])
## M2 relative gain [content/kind=python_exec] (higher is better)
- inst ladder: 0.6B 0.3850, 1.7B 0.4579, 4B 0.4809, 8B 0.5048, 14B 0.5135, 32B 0.5134; monotone=False; GATE=FAIL (0.6B->1.7B +0.0729 [+0.0541,+0.0915]; 1.7B->4B +0.0231 [+0.0012,+0.0471]; 4B->8B +0.0239 [+0.0080,+0.0412]; 8B->14B +0.0086 [-0.0047,+0.0223]; 14B->32B -0.0000 [-0.0158,+0.0152])
- base ladder: 0.6B 0.4120, 1.7B 0.4629, 4B 0.4977, 8B 0.4947, 14B 0.5128; monotone=False; GATE=FAIL (0.6B->1.7B +0.0509 [+0.0387,+0.0661]; 1.7B->4B +0.0348 [+0.0207,+0.0503]; 4B->8B -0.0029 [-0.0118,+0.0071]; 8B->14B +0.0181 [+0.0094,+0.0264])
## M2 relative gain [content/kind=search] (higher is better)
- inst ladder: 0.6B 0.0453, 1.7B 0.0792, 4B 0.0937, 8B 0.1087, 14B 0.1359, 32B 0.1253; monotone=False; GATE=FAIL (0.6B->1.7B +0.0339 [+0.0141,+0.0627]; 1.7B->4B +0.0144 [-0.0060,+0.0423]; 4B->8B +0.0150 [-0.0046,+0.0342]; 8B->14B +0.0272 [+0.0086,+0.0570]; 14B->32B -0.0105 [-0.0338,+0.0130])
- base ladder: 0.6B 0.0417, 1.7B 0.0608, 4B 0.0911, 8B 0.1034, 14B 0.1161; monotone=True; GATE=PASS (0.6B->1.7B +0.0191 [+0.0082,+0.0357]; 1.7B->4B +0.0302 [+0.0164,+0.0526]; 4B->8B +0.0123 [+0.0041,+0.0256]; 8B->14B +0.0127 [+0.0006,+0.0291])
## M2 relative gain [content/kind=shell_other] (higher is better)
- inst ladder: 0.6B 0.0437, 1.7B 0.0782, 4B 0.1104, 8B 0.1592, 14B 0.1575, 32B 0.1732; monotone=False; GATE=FAIL (0.6B->1.7B +0.0345 [+0.0210,+0.0499]; 1.7B->4B +0.0323 [+0.0069,+0.0602]; 4B->8B +0.0488 [+0.0286,+0.0735]; 8B->14B -0.0017 [-0.0188,+0.0161]; 14B->32B +0.0157 [-0.0021,+0.0341])
- base ladder: 0.6B 0.0522, 1.7B 0.1023, 4B 0.1381, 8B 0.1399, 14B 0.1594; monotone=True; GATE=FAIL (0.6B->1.7B +0.0501 [+0.0357,+0.0678]; 1.7B->4B +0.0359 [+0.0205,+0.0570]; 4B->8B +0.0018 [-0.0096,+0.0145]; 8B->14B +0.0195 [+0.0089,+0.0306])
## M2 relative gain [content/kind=test_run] (higher is better)
- inst ladder: 0.6B 0.0710, 1.7B 0.1055, 4B 0.1206, 8B 0.1358, 14B 0.1350, 32B 0.1347; monotone=False; GATE=FAIL (0.6B->1.7B +0.0346 [+0.0217,+0.0486]; 1.7B->4B +0.0151 [+0.0047,+0.0288]; 4B->8B +0.0151 [+0.0060,+0.0243]; 8B->14B -0.0008 [-0.0070,+0.0064]; 14B->32B -0.0003 [-0.0085,+0.0088])
- base ladder: 0.6B 0.0768, 1.7B 0.0963, 4B 0.1140, 8B 0.1158, 14B 0.1244; monotone=True; GATE=FAIL (0.6B->1.7B +0.0195 [+0.0122,+0.0291]; 1.7B->4B +0.0176 [+0.0115,+0.0264]; 4B->8B +0.0018 [-0.0044,+0.0075]; 8B->14B +0.0086 [+0.0043,+0.0141])
## M2 relative gain [outcome/all] (higher is better)
- inst ladder: 0.6B 0.0927, 1.7B 0.1215, 4B 0.1236, 8B 0.1521, 14B 0.1526, 32B 0.1487; monotone=False; GATE=FAIL (0.6B->1.7B +0.0289 [+0.0163,+0.0426]; 1.7B->4B +0.0021 [-0.0085,+0.0136]; 4B->8B +0.0285 [+0.0162,+0.0413]; 8B->14B +0.0005 [-0.0090,+0.0107]; 14B->32B -0.0039 [-0.0129,+0.0064])
- base ladder: 0.6B 0.1028, 1.7B 0.1208, 4B 0.1356, 8B 0.1381, 14B 0.1446; monotone=True; GATE=FAIL (0.6B->1.7B +0.0180 [+0.0118,+0.0259]; 1.7B->4B +0.0148 [+0.0090,+0.0210]; 4B->8B +0.0024 [-0.0033,+0.0092]; 8B->14B +0.0065 [+0.0005,+0.0134])
## Reading: next-action bits/tok saved by seeing the obs [all] (higher is better)
- inst ladder: 0.6B 0.0249, 1.7B 0.0400, 4B 0.0502, 8B 0.0595, 14B 0.0306, 32B 0.0246; monotone=False; GATE=FAIL (0.6B->1.7B +0.0151 [+0.0070,+0.0234]; 1.7B->4B +0.0102 [+0.0022,+0.0184]; 4B->8B +0.0092 [+0.0024,+0.0168]; 8B->14B -0.0289 [-0.0365,-0.0220]; 14B->32B -0.0060 [-0.0093,-0.0028])
- base ladder: 0.6B 0.0187, 1.7B 0.0215, 4B 0.0228, 8B 0.0217, 14B 0.0205; monotone=False; GATE=FAIL (0.6B->1.7B +0.0028 [+0.0010,+0.0045]; 1.7B->4B +0.0013 [-0.0006,+0.0032]; 4B->8B -0.0011 [-0.0025,+0.0002]; 8B->14B -0.0012 [-0.0026,+0.0002])
## Reading: next-action bits/tok saved by seeing the obs [kind=edit_ack] (higher is better)
- inst ladder: 0.6B 0.0008, 1.7B 0.0392, 4B 0.0343, 8B 0.0320, 14B 0.0112, 32B 0.0135; monotone=False; GATE=FAIL (0.6B->1.7B +0.0385 [+0.0094,+0.0701]; 1.7B->4B -0.0050 [-0.0388,+0.0306]; 4B->8B -0.0023 [-0.0327,+0.0292]; 8B->14B -0.0208 [-0.0401,-0.0047]; 14B->32B +0.0023 [-0.0141,+0.0201])
- base ladder: 0.6B -0.0004, 1.7B 0.0033, 4B 0.0086, 8B 0.0053, 14B 0.0044; monotone=False; GATE=FAIL (0.6B->1.7B +0.0037 [-0.0045,+0.0118]; 1.7B->4B +0.0053 [-0.0009,+0.0119]; 4B->8B -0.0033 [-0.0122,+0.0048]; 8B->14B -0.0008 [-0.0069,+0.0088])
## Reading: next-action bits/tok saved by seeing the obs [kind=file_view] (higher is better)
- inst ladder: 0.6B 0.0497, 1.7B 0.0844, 4B 0.0884, 8B 0.0925, 14B 0.0519, 32B 0.0367; monotone=False; GATE=FAIL (0.6B->1.7B +0.0347 [+0.0073,+0.0685]; 1.7B->4B +0.0040 [-0.0152,+0.0265]; 4B->8B +0.0042 [-0.0086,+0.0167]; 8B->14B -0.0406 [-0.0656,-0.0207]; 14B->32B -0.0152 [-0.0256,-0.0072])
- base ladder: 0.6B 0.0294, 1.7B 0.0334, 4B 0.0356, 8B 0.0342, 14B 0.0313; monotone=False; GATE=FAIL (0.6B->1.7B +0.0040 [-0.0013,+0.0096]; 1.7B->4B +0.0022 [-0.0024,+0.0070]; 4B->8B -0.0014 [-0.0069,+0.0030]; 8B->14B -0.0030 [-0.0071,+0.0009])
## Reading: next-action bits/tok saved by seeing the obs [kind=python_exec] (higher is better)
- inst ladder: 0.6B -0.0018, 1.7B -0.0167, 4B 0.0127, 8B 0.0114, 14B 0.0014, 32B 0.0048; monotone=False; GATE=FAIL (0.6B->1.7B -0.0149 [-0.0270,-0.0032]; 1.7B->4B +0.0294 [+0.0182,+0.0425]; 4B->8B -0.0014 [-0.0106,+0.0078]; 8B->14B -0.0100 [-0.0177,-0.0029]; 14B->32B +0.0035 [-0.0006,+0.0077])
- base ladder: 0.6B -0.0005, 1.7B 0.0035, 4B 0.0031, 8B 0.0034, 14B 0.0027; monotone=False; GATE=FAIL (0.6B->1.7B +0.0040 [+0.0019,+0.0063]; 1.7B->4B -0.0004 [-0.0024,+0.0015]; 4B->8B +0.0003 [-0.0010,+0.0017]; 8B->14B -0.0007 [-0.0026,+0.0012])
## Reading: next-action bits/tok saved by seeing the obs [kind=search] (higher is better)
- inst ladder: 0.6B 0.0612, 1.7B 0.0927, 4B 0.0847, 8B 0.1324, 14B 0.0753, 32B 0.0667; monotone=False; GATE=FAIL (0.6B->1.7B +0.0315 [+0.0007,+0.0748]; 1.7B->4B -0.0079 [-0.0422,+0.0209]; 4B->8B +0.0477 [+0.0178,+0.0945]; 8B->14B -0.0571 [-0.1097,-0.0272]; 14B->32B -0.0086 [-0.0283,+0.0065])
- base ladder: 0.6B 0.0475, 1.7B 0.0478, 4B 0.0464, 8B 0.0515, 14B 0.0449; monotone=False; GATE=FAIL (0.6B->1.7B +0.0003 [-0.0065,+0.0080]; 1.7B->4B -0.0014 [-0.0113,+0.0059]; 4B->8B +0.0051 [-0.0002,+0.0141]; 8B->14B -0.0066 [-0.0169,+0.0010])
## Reading: next-action bits/tok saved by seeing the obs [kind=shell_other] (higher is better)
- inst ladder: 0.6B 0.0870, 1.7B 0.1376, 4B 0.1179, 8B 0.1240, 14B 0.0918, 32B 0.0727; monotone=False; GATE=FAIL (0.6B->1.7B +0.0506 [+0.0144,+0.0950]; 1.7B->4B -0.0197 [-0.0599,+0.0211]; 4B->8B +0.0061 [-0.0210,+0.0345]; 8B->14B -0.0322 [-0.0739,-0.0016]; 14B->32B -0.0191 [-0.0391,-0.0037])
- base ladder: 0.6B 0.0786, 1.7B 0.0733, 4B 0.0769, 8B 0.0698, 14B 0.0701; monotone=False; GATE=FAIL (0.6B->1.7B -0.0053 [-0.0185,+0.0061]; 1.7B->4B +0.0036 [-0.0067,+0.0137]; 4B->8B -0.0071 [-0.0139,-0.0011]; 8B->14B +0.0004 [-0.0060,+0.0067])
## Reading: next-action bits/tok saved by seeing the obs [kind=test_run] (higher is better)
- inst ladder: 0.6B 0.0169, 1.7B 0.0371, 4B 0.0443, 8B 0.0617, 14B 0.0250, 32B 0.0170; monotone=False; GATE=FAIL (0.6B->1.7B +0.0202 [+0.0093,+0.0329]; 1.7B->4B +0.0072 [-0.0039,+0.0198]; 4B->8B +0.0173 [+0.0067,+0.0298]; 8B->14B -0.0366 [-0.0515,-0.0253]; 14B->32B -0.0080 [-0.0135,-0.0033])
- base ladder: 0.6B 0.0122, 1.7B 0.0157, 4B 0.0181, 8B 0.0159, 14B 0.0160; monotone=False; GATE=FAIL (0.6B->1.7B +0.0035 [+0.0000,+0.0072]; 1.7B->4B +0.0024 [-0.0009,+0.0059]; 4B->8B -0.0022 [-0.0049,+0.0001]; 8B->14B +0.0000 [-0.0030,+0.0030])

## Appendix D. M5 AgenticPPL tables
| model | role | AgenticPPL obsgain-easy (capped_bits) | obsgain-nothought (prob_mean) | obsgain-taskgain (prob_mean) | plain mean bits/range (easy picks, uncapped) | bits/token on easy picks | entropy / loss−entropy on easy picks | entropy / loss−entropy at all command tokens | plain PPL (bits/byte) | published agentic score |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base |  | -1.1315 [-1.2293,-1.0328] | 0.3915 [0.3704,0.4137] | 0.3233 [0.2943,0.3565] | 2.827 [2.560,3.099] | 2.548 | 1.750 / +0.799 | 0.766 / +0.040 | 0.3582 | – |
| Qwen3-0.6B |  | -1.1146 [-1.2125,-1.0172] | 0.3864 [0.3652,0.4097] | 0.3238 [0.2944,0.3574] | 3.534 [3.195,3.885] | 3.186 | 1.286 / +1.900 | 0.577 / +0.429 | 0.4400 | – |
| Qwen3-1.7B-Base |  | -1.0524 [-1.1518,-0.9576] | 0.4327 [0.4122,0.4551] | 0.3576 [0.3286,0.3903] | 2.348 [2.126,2.577] | 2.117 | 1.483 / +0.634 | 0.603 / +0.020 | 0.3108 | – |
| Qwen3-1.7B |  | -0.9502 [-1.0424,-0.8649] | 0.4659 [0.4461,0.4873] | 0.3804 [0.3518,0.4127] | 4.854 [4.368,5.357] | 4.376 | 0.482 / +3.895 | 0.206 / +0.869 | 0.4775 | – |
| Qwen3-4B-Base |  | -0.9672 [-1.0606,-0.8774] | 0.4846 [0.4651,0.5067] | 0.3939 [0.3648,0.4255] | 1.977 [1.785,2.176] | 1.783 | 1.218 / +0.565 | 0.455 / +0.045 | 0.2733 | – |
| Qwen3-4B |  | -0.8664 [-0.9518,-0.7832] | 0.5135 [0.4938,0.5350] | 0.4182 [0.3895,0.4493] | 3.614 [3.246,3.993] | 3.258 | 0.466 / +2.793 | 0.181 / +0.619 | 0.4016 | – |
| Qwen3-8B-Base | base | -0.9288 [-1.0194,-0.8414] | 0.5051 [0.4858,0.5267] | 0.4122 [0.3840,0.4434] | 1.807 [1.631,1.991] | 1.630 | 1.150 / +0.480 | 0.415 / +0.039 | 0.2708 | – |
| Qwen3-8B | instruct | -0.8270 [-0.9096,-0.7466] | 0.5347 [0.5150,0.5558] | 0.4397 [0.4116,0.4705] | 3.224 [2.881,3.579] | 2.907 | 0.484 / +2.423 | 0.189 / +0.498 | 0.3455 | TB2.0 2.47 (NT paper); TB-Lite 7.3 / TB2.1 1.1 (Tmax paper) |
| Light-IF-8B | non-agentic SFT+RL | -0.9081 [-0.9970,-0.8195] | 0.5049 [0.4848,0.5269] | 0.4147 [0.3861,0.4463] | 2.417 [2.170,2.668] | 2.180 | 0.804 / +1.375 | 0.297 / +0.288 | 0.3055 | – |
| Klear-Reasoner-8B-SFT | non-agentic distill SFT (from Base) | -0.9836 [-1.0758,-0.8911] | 0.4701 [0.4504,0.4918] | 0.3852 [0.3566,0.4168] | 2.811 [2.536,3.101] | 2.535 | 0.927 / +1.608 | 0.349 / +0.381 | 0.3763 | – |
| Nemotron-Terminal-8B | agentic SFT | -0.7729 [-0.8462,-0.7000] | 0.5908 [0.5731,0.6093] | 0.4766 [0.4503,0.5052] | 1.441 [1.295,1.590] | 1.299 | 0.835 / +0.464 | 0.288 / +0.099 | 0.3086 | TB2.0 13.0 |
| tmax-sft-8b | agentic SFT | -0.8773 [-0.9642,-0.7956] | 0.5300 [0.5112,0.5498] | 0.4431 [0.4163,0.4732] | 1.760 [1.588,1.940] | 1.587 | 0.985 / +0.602 | 0.329 / +0.117 | 0.2844 | TB-Lite 11.5 / TB2.1 6.0 |
| tmax-8b | agentic RL (on tmax-sft) | -0.9276 [-1.0180,-0.8412] | 0.4990 [0.4798,0.5194] | 0.4252 [0.3983,0.4556] | 1.972 [1.775,2.172] | 1.778 | 1.021 / +0.756 | 0.352 / +0.141 | 0.3129 | TB-Lite 17.7 / TB2.1 5.2 |
| WebWorld-8B | world model (web) | -0.8755 [-0.9603,-0.7925] | 0.5252 [0.5060,0.5463] | 0.4264 [0.3984,0.4570] | 2.192 [1.965,2.422] | 1.976 | 0.817 / +1.159 | 0.314 / +0.225 | 0.3006 | – |
| Qwen3-14B-Base | base | -0.8912 [-0.9782,-0.8055] | 0.5234 [0.5042,0.5446] | 0.4285 [0.4007,0.4592] | 1.647 [1.487,1.817] | 1.485 | 1.100 / +0.385 | 0.392 / +0.021 | 0.2606 | – |
| Qwen3-14B | instruct | -0.8114 [-0.8920,-0.7337] | 0.5501 [0.5314,0.5706] | 0.4510 [0.4234,0.4813] | 2.431 [2.182,2.696] | 2.192 | 0.571 / +1.621 | 0.220 / +0.327 | 0.3067 | TB2.0 4.04 |
| Light-IF-14B | non-agentic SFT+RL | -0.8524 [-0.9370,-0.7712] | 0.5353 [0.5160,0.5557] | 0.4368 [0.4090,0.4674] | 2.204 [1.979,2.442] | 1.987 | 0.709 / +1.278 | 0.266 / +0.267 | 0.2934 | – |
| Nemotron-Terminal-14B | agentic SFT | -0.7119 [-0.7818,-0.6437] | 0.6155 [0.5979,0.6338] | 0.5007 [0.4742,0.5291] | 1.287 [1.156,1.421] | 1.160 | 0.749 / +0.411 | 0.256 / +0.098 | 0.3230 | TB2.0 20.2 |
| CodeScout-14B | agentic RL | -0.7732 [-0.8515,-0.6983] | 0.5642 [0.5455,0.5843] | 0.4644 [0.4372,0.4937] | 3.475 [3.105,3.858] | 3.133 | 0.364 / +2.769 | 0.140 / +0.620 | 0.3584 | SWE-V file-loc F1 68.6 (no TB) |
| Qwen3-32B | instruct | -0.8307 [-0.9119,-0.7498] | 0.5491 [0.5305,0.5695] | 0.4561 [0.4294,0.4859] | 1.673 [1.505,1.845] | 1.508 | 0.880 / +0.628 | 0.314 / +0.113 | 0.2601 | TB2.0 3.37 |

unmatched renderings / docs with special tokens in content: Qwen3-0.6B-Base: 0/0, Qwen3-0.6B: 0/0, Qwen3-1.7B-Base: 0/0, Qwen3-1.7B: 0/0, Qwen3-4B-Base: 0/0, Qwen3-4B: 0/0, Qwen3-8B-Base: 0/0, Qwen3-8B: 0/0, Light-IF-8B: 0/0, Klear-Reasoner-8B-SFT: 0/0, Nemotron-Terminal-8B: 0/0, tmax-sft-8b: 0/0, tmax-8b: 0/0, WebWorld-8B: 0/0, Qwen3-14B-Base: 0/0, Qwen3-14B: 0/0, Light-IF-14B: 0/0, Nemotron-Terminal-14B: 0/0, CodeScout-14B: 0/0, Qwen3-32B: 0/0

**Paired differences (A − B; higher AgenticPPL = predicted more agentic), 95% paired doc bootstrap**

| A | B | Δ obsgain-easy | Δ obsgain-nothought | Δ obsgain-taskgain |
|---|---|---|---|---|
| Qwen3-8B | Qwen3-8B-Base | +0.1018 [+0.0894,+0.1155] | +0.0296 [+0.0265,+0.0326] | +0.0275 [+0.0242,+0.0309] |
| Light-IF-8B | Qwen3-8B | -0.0811 [-0.0917,-0.0706] | -0.0298 [-0.0321,-0.0277] | -0.0250 [-0.0273,-0.0226] |
| Nemotron-Terminal-8B | Qwen3-8B | +0.0541 [+0.0367,+0.0743] | +0.0562 [+0.0497,+0.0634] | +0.0368 [+0.0311,+0.0432] |
| tmax-sft-8b | Qwen3-8B | -0.0504 [-0.0640,-0.0380] | -0.0047 [-0.0089,-0.0005] | +0.0033 [-0.0006,+0.0074] |
| tmax-8b | tmax-sft-8b | -0.0503 [-0.0589,-0.0423] | -0.0310 [-0.0334,-0.0287] | -0.0178 [-0.0199,-0.0158] |
| tmax-8b | Qwen3-8B | -0.1007 [-0.1176,-0.0852] | -0.0357 [-0.0410,-0.0306] | -0.0145 [-0.0191,-0.0099] |
| Klear-Reasoner-8B-SFT | Qwen3-8B-Base | -0.0548 [-0.0697,-0.0408] | -0.0350 [-0.0388,-0.0314] | -0.0270 [-0.0314,-0.0226] |
| WebWorld-8B | Qwen3-8B | -0.0485 [-0.0608,-0.0376] | -0.0094 [-0.0120,-0.0066] | -0.0133 [-0.0169,-0.0099] |
| Nemotron-Terminal-8B | Light-IF-8B | +0.1352 [+0.1141,+0.1594] | +0.0859 [+0.0791,+0.0935] | +0.0618 [+0.0556,+0.0686] |
| tmax-sft-8b | Light-IF-8B | +0.0307 [+0.0181,+0.0438] | +0.0251 [+0.0210,+0.0293] | +0.0283 [+0.0244,+0.0326] |
| Qwen3-14B | Qwen3-14B-Base | +0.0798 [+0.0687,+0.0922] | +0.0268 [+0.0240,+0.0294] | +0.0225 [+0.0193,+0.0259] |
| Nemotron-Terminal-14B | Qwen3-14B | +0.0994 [+0.0819,+0.1196] | +0.0654 [+0.0589,+0.0725] | +0.0497 [+0.0441,+0.0559] |
| CodeScout-14B | Qwen3-14B | +0.0381 [+0.0321,+0.0450] | +0.0141 [+0.0125,+0.0158] | +0.0134 [+0.0115,+0.0154] |
| Light-IF-14B | Qwen3-14B | -0.0410 [-0.0497,-0.0333] | -0.0148 [-0.0170,-0.0127] | -0.0141 [-0.0165,-0.0119] |
| Nemotron-Terminal-14B | Light-IF-14B | +0.1405 [+0.1206,+0.1630] | +0.0802 [+0.0739,+0.0872] | +0.0638 [+0.0579,+0.0704] |
| CodeScout-14B | Light-IF-14B | +0.0792 [+0.0679,+0.0919] | +0.0289 [+0.0261,+0.0318] | +0.0276 [+0.0244,+0.0308] |

**Spearman rho across the 20 scored models** (sign: positive = higher AgenticPPL goes with higher feature)

| feature | obsgain-easy | obsgain-nothought | obsgain-taskgain |
|---|---|---|---|
| entropy at command tokens | -0.77 | -0.66 | -0.62 |
| loss−entropy at command tokens | +0.20 | +0.06 | +0.05 |
| entropy on easy picks | -0.71 | -0.59 | -0.54 |
| loss−entropy on easy picks | -0.07 | -0.22 | -0.25 |
| −plain PPL | +0.17 | +0.32 | +0.32 |

**Within-size Pearson r (size-group means removed; 20 models)**

| feature | obsgain-easy | obsgain-nothought | obsgain-taskgain |
|---|---|---|---|
| entropy at command tokens | -0.65 | -0.42 | -0.44 |
| loss−entropy at command tokens | +0.36 | +0.10 | +0.10 |
| entropy on easy picks | -0.62 | -0.37 | -0.38 |
| loss−entropy on easy picks | +0.33 | +0.06 | +0.06 |
| −plain PPL | -0.42 | -0.21 | -0.22 |

**Scale trend (easy): base, instruct, instruct − base (paired)**

| size | base | instruct | Δ [95% CI] |
|---|---|---|---|
| 0.6B | -1.131 | -1.115 | +0.017 [+0.007,+0.027] |
| 1.7B | -1.052 | -0.950 | +0.102 [+0.088,+0.117] |
| 4B | -0.967 | -0.866 | +0.101 [+0.088,+0.115] |
| 8B | -0.929 | -0.827 | +0.102 [+0.089,+0.116] |
| 14B | -0.891 | -0.811 | +0.080 [+0.069,+0.092] |
| 32B | – | -0.831 | – |

## Status
Models with SWE M1/M2 results: Arctic-AWM-8B CodeScout-14B FrogMini-14B-2510 Klear-Reasoner-8B-SFT Light-IF-14B Light-IF-8B Nemotron-Terminal-14B Nemotron-Terminal-32B Nemotron-Terminal-8B OpenThinkerAgent-32B OpenThinker-Agent-v1-SFT Qwen3-0.6B Qwen3-0.6B-Base Qwen3-14B Qwen3-14B-Base Qwen3-1.7B Qwen3-1.7B-Base Qwen3-32B Qwen3-4B Qwen3-4B-Base Qwen3-8B Qwen3-8B-Base SERA-14B SERA-8B tmax-8b tmax-sft-8b WebWorld-8B

M1-M4 (results/raw)                                            1.53 GPU-h
M1/M2 SWE (results/raw_m12)                                    4.55 GPU-h
M5                                                             3.35 GPU-h
killed/partial runs, checks, vLLM reference (estimate)         1.00 GPU-h
TOTAL                                                         10.43 GPU-h
