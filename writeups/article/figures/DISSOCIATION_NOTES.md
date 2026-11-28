# DISSOCIATION_NOTES — `dissociation.png`

One picture of the dissociation: agentic post-training multiplies *solving* (published
agentic benchmark score) far more than *predicting what the tools return* (tool-output
prediction, size-equivalent multiplier vs the model's own Instruct start).

Reproduce: `cd article && ../.venv/bin/python figures/make_dissociation.py` —
reads only `figures/dissociation_data.json` (every number below, with provenance),
so no access to the study host is needed.

## Plotted points

x = published benchmark score ÷ **the same paper's** starting-checkpoint score (never
compared across papers/harnesses). y = size-equivalent multiplier vs the model's own
Instruct start ("how much bigger a plain Instruct model would have to be to match it"),
inverse-interpolated on the Qwen3 Instruct ladder in log2 non-embedding params
(`p2/configs/params.json`: 0.440 / 1.409 / 3.634 / 6.946 / 13.212 / 31.206 B).

| model | benchmark (paper / harness) | start score | tuned score | x multiplier | sandbox binding × [95% CI] | SWE M1 × [95% CI] | SWE M2 × [95% CI] |
|---|---|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Terminal-Bench 2.0 (arXiv 2602.21193 / Terminus-2) | 2.47 (Qwen3-8B) | 13.0 | **5.26×** | 1.73 [1.34, 2.37] | 0.99 [0.93, 1.05] | 1.06 [0.96, 1.15] |
| Nemotron-Terminal-14B | Terminal-Bench 2.0 (same) | 4.04 (Qwen3-14B) | 20.2 | **5.00×** | 2.08 [1.58, 2.36] | 0.82 [0.78, 0.87] | 0.84 [0.78, 0.90] |
| Nemotron-Terminal-32B | Terminal-Bench 2.0 (same) | 3.37 (Qwen3-32B) | 27.4 | **8.13×** | > 1.00 (censored; ladder stops at 32B) | 0.81 [0.76, 0.86] | 0.76 [0.69, 0.83] |
| tmax-sft-8b | Terminal-Bench Lite (arXiv 2606.23321 / Ai2 mini-swe-agent-like) | 7.3 (Qwen3-8B) | 11.5 | **1.58×** | 1.90 [1.46, 2.61] | 1.31 [1.27, 1.36] | 1.44 [1.37, 1.52] |
| tmax-8b | Terminal-Bench Lite (same) | 7.3 (Qwen3-8B) | 17.7 | **2.42×** | 1.77 [1.36, 2.42] | 1.04 [0.99, 1.08] | 1.16 [1.09, 1.22] |

Sources for the y columns:
- sandbox binding: `the study host: agentic-wm/sandbox/SIZE_EQUIV.md`, forest table
  `binding acc/primary` (primary pool S2+S3+S2h+S3h, plain, T1/nocopy; ladder
  interpolation n with a joint env-cluster bootstrap, 2000 draws).
- SWE M1/M2: `the study host: agentic-wm/p2/FINDINGS.md` headline table (SWE-rebench 2026,
  150 trajectories; M1 = recalibrated content bits/token, M2 = NLL of output given the
  true action; joint trajectory bootstrap, 1000 draws); same values in
  `~/agentic-wm/p2/results/size_equiv/size_equiv_swe.{md,json}`.
- benchmark scores: `the study host: agentic-wm/p2/CONTROLS.md` (paper, harness and score per
  model). `article/FACTS.md` rounds the Nemotron baselines to 2.5 / 4.0 / 3.4; the table
  uses CONTROLS.md's precise 2.47 / 4.04 / 3.37 (multipliers 5.26 / 5.00 / 8.13 instead
  of 5.2 / 5.05 / 8.06 — same picture).

The RL step, annotated in the figure: tmax-sft → tmax raises TB-Lite 11.5 → 17.7 but
forecasts are flat-to-worse — sandbox 1.90 → 1.77 (RL step alone n.s., +0.7 pts
[−0.3, +1.6]), SWE M1 1.31 → 1.04 (RL step alone 0.79× [0.77, 0.81]).

## Reference lines

- **y = 1**: no gain over the chat model (the model's own Instruct start).
- **y = 2**: one size doubling — what pretraining gets from 2× the parameters.
- **Base-model band (1.95–2.83×)**: the same-size Qwen3 **Base** model's tool-output
  prediction, expressed as the size of an Instruct model that matches it (inverse
  Instruct-ladder interpolation at the Base ladder value; computed in
  `make_dissociation.py::base_band()` from the ladders in the JSON):
  - sandbox binding: 8B-Base → 2.80× over Qwen3-8B, 14B-Base → 1.95× over Qwen3-14B
    (ladders: instruct 60.4/64.6/68.7/71.7/75.3/79.3%, base 63.6/68.6/75.7/77.1/78.4%);
  - SWE M1: 8B-Base → 2.83×, 14B-Base → > 2.36× (censored: 14B-Base 0.987 bits is
    better than the 32B top of the Instruct ladder, 1.016);
  - Qwen3-32B-Base does not exist, so the band says nothing about 32B starts.

## Excluded from the scatter, with reasons

| model | why excluded | its y values (for the record) |
|---|---|---|
| CodeScout-14B | no published agentic benchmark score at all (only SWE-V file-localisation F1 68.6) — no x value | sandbox 0.96 [0.80, 1.16]; M1 0.84 [0.83, 0.85]; M2 0.72 [0.69, 0.75] |
| OpenThinker-Agent-v1 | TB2.0 4.9 is published (blog only), but the vetted files give no starting-checkpoint TB2.0 score → no within-paper ratio; its SWE row is moreover for OpenThinker-Agent-v1-**SFT**, a different checkpoint | M1 0.56 [0.53, 0.58]; M2 0.69 [0.65, 0.73] (v1-SFT); no sandbox row |
| OpenThinkerAgent-32B | TB2.0 26.2 (blog only); the only Qwen3-32B TB2.0 score in the files (3.37) is a baseline run inside a *different* paper (Nemotron-Terminal) — cross-paper ratio prohibited by the rules | sandbox 0.89 [0.67, 1.00]; M1 < 0.5 (censored); M2 < 0.5 (censored) |
| SERA-8B / SERA-14B | only SWE-V scores (31.7 / 49.5), no start-checkpoint score in the same paper; not Terminal-Bench | sandbox 1.28 [0.96, 1.72] (8B); M1 < 0.5 (censored); M2 0.60 / 0.56 |
| FrogMini-14B-2510 | SWE-V 45.3 in the R2E-Gym scaffold with no same-harness start baseline in the files; and its SWE prediction row is flagged as a rendering mismatch (+1.31 bits/tok — larger than the whole ladder span) | sandbox 1.13 [0.86, 1.48]; M1/M2 < 0.5 (censored, suspect) |
| Arctic-AWM-8B | published numbers are tau-style MCP tool benchmarks, no Terminal-Bench, no within-paper start baseline | sandbox 0.95 [0.74, 1.14]; M1 1.01 [1.01, 1.02]; M2 1.00 [0.99, 1.01] |
| Light-IF-8B / 14B | non-agentic instruction-following control; no published agentic benchmark score | sandbox 1.30 / 1.43; M1 1.08 / 0.82; M2 1.28 / 0.92 |
| WebWorld-8B | web-page world-model positive control; no Terminal-Bench score | sandbox 0.99 [0.72, 1.30]; M1 1.26 [1.22, 1.29]; M2 1.39 [1.34, 1.45] |
| Klear-Reasoner-8B-SFT | non-agentic distillation from Qwen3-8B-**Base** (no Instruct start to ratio against); no agentic benchmark score | sandbox vs Instruct 0.46 [0.31, 0.67]; M1/M2 < 0.5 vs base ladder |

## Method / honesty notes

- **Within-paper ratios only.** Nemotron's x uses Terminal-Bench 2.0 as run in the
  Nemotron-Terminal paper (Terminus-2); tmax's x uses Terminal-Bench Lite as run in the
  Tmax paper (Ai2's own harness). The two are never divided into each other; each x is a
  ratio inside one paper. This is stated in the figure footer.
- **Censored values.** For 32B starts the ladder stops at 32B, so gains can only show as
  "> 1× (censored)" (Nemotron-Terminal-32B sandbox) or "< 0.5×" (OpenThinkerAgent-32B
  SWE). The figure draws the censored sandbox point as an open circle with an up-arrow.
- The sandbox and SWE measurements agree on the claim (nothing near the 5–8× benchmark
  multipliers; nothing past the Base) but not always in magnitude: on the sandbox, the
  Nemotron/tmax gains are ≈ one size doubling (1.7–2.1×); on SWE the same models sit at
  0.8–1.4×. Both are shown so the reader sees both.
- SWE per-kind exceptions exist (tmax-sft `shell_other` reaches 2.06× [1.74, 2.52] on M2)
  — the figure plots aggregate content tokens only.
- TB-2.1 (also in the Tmax paper: Qwen3-8B 1.1 → tmax-sft 6.0 → tmax 5.2) is not used:
  the prompt of record for tmax is TB-Lite, and TB-2.1's tiny denominator (1.1) makes the
  ratio unstable; the TB-Lite values are the ones FACTS.md uses.
- Terminal-trajectory observation bits/byte (`~/agentic-wm/results/summary.csv`) is
  context for the article, not a size-equivalent multiplier, and is not plotted here.
- Colour-blind safety: series pair `#ad450b` (sandbox) / `#1a6bb0` (SWE) — validated
  with the dataviz palette checker (lightness band, chroma floor, CVD ΔE ≥ 21.7 protan,
  normal-vision ΔE 27.0, contrast ≥ 3:1 all PASS). The article blue `#1c618c` failed the
  chroma floor ("reads gray") and was snapped to `#1a6bb0`; marker shape (circle /
  triangle / diamond) is a second, colour-independent encoding.
