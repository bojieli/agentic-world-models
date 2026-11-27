# Observation perplexity as a world-model probe: Qwen3 base / instruct / Nemotron-Terminal pilot

## Setup
- **Data.** AgenticPPL held-out split. 200 eval trajectories, stratified by teacher (Opus-4.6 69, GLM-5 60, DeepSeek-V3.2 60, Gemini-3.1-Pro 9, GPT-5.4 2; seed 0), plus 50 calibration trajectories. All ≤32k tokens, none truncated.
- **Models.** 14, all with the same Qwen3 tokenizer. Token ids were verified identical per trajectory via a hash, for all models and both renderings.
  - Qwen3-{0.6,1.7,4,8,14}B-Base (no 32B base was released).
  - Qwen3-{0.6,1.7,4,8,14,32}B instruct.
  - Nemotron-Terminal-{8,14,32}B: SFT of Qwen3 on terminal trajectories. Terminal-Bench 2.0 from the model card: 13.0 / 20.2 / 27.4, against 2.47 / 4.04 / 3.37 for Qwen3.
- **Renderings.**
  - A = neutral plain text (`### Task` / `### Agent` / `### Terminal`).
  - B = native Qwen3 chat template: observations as user turns, assistant history without think blocks. Base models also get B.
- **Scoring.** One teacher-forced pass in HF transformers, bf16 with sdpa. A KV cache splits each pass at observation boundaries so measures 5–6 can branch off. Bits are attributed to UTF-8 bytes via offsets.
  - Cached/chunked vs plain full-forward log-probs: mean |Δ| 0.005–0.03 nats per token, max a few nats on isolated tokens (bf16 kernel differences).
- **Measures.**
  1. Span BPB.
  2. Observation split: first 16 tokens vs body; copyable (token completes an 8-gram seen earlier; 43% of observation tokens) vs novel.
  3. Special/role-token probability mass at observation positions.
  4. Temperature-scaled observation BPB (T fit on calibration observation tokens).
  5. Assistant-role prompted prediction of the next observation (≤512 tokens; 469 items).
  6. "Will this output contain an error? Yes/No" (469 items).
     - Regex labels: 44 positives on "new" lines, i.e. excluding lines already in context, prompt lines and heredoc echoes. A 20-item spot check gives about 2/3 precision; false positives come from cat'ed code and package.json containing "Error:".
- **GPU time.** About 5.5 GPU-hours on one RTX PRO 6000: 2.65 h main pass, 1.34 h teacher-forced backfill, 1.41 h copy test, plus checks.

## Headline table (eval set, 200 trajectories)
BPB = bits per byte. "neu/nat" = neutral/native rendering. T* = per-model temperature fit on calibration observation tokens. "pred" = measure 5, novel tokens only. AUROC is for the Yes/No error question (measure 6, "new" labels, neutral rendering).

| model | TB2.0 | obs BPB neu/nat | novel obs neu/nat | copy obs nat | obs@T* nat (T*) | thought nat | action nat | pred novel BPB neu/nat | AUROC(new) neu |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | – | 0.170/0.178 | 0.275/0.287 | 0.017 | 0.178 (1.0) | 0.504 | 0.226 | 0.200/0.226 | 0.647 |
| Qwen3-1.7B-Base | – | 0.142/0.147 | 0.231/0.238 | 0.012 | 0.147 (1.0) | 0.433 | 0.174 | 0.160/0.168 | 0.679 |
| Qwen3-4B-Base | – | 0.123/0.126 | 0.199/0.205 | 0.009 | 0.126 (1.0) | 0.378 | 0.139 | 0.132/0.146 | 0.571 |
| Qwen3-8B-Base | – | 0.115/0.115 | 0.187/0.188 | 0.008 | 0.115 (1.0) | 0.361 | 0.126 | 0.122/0.124 | 0.524 |
| Qwen3-14B-Base | – | 0.108/0.108 | 0.175/0.176 | 0.007 | 0.108 (1.0) | 0.335 | 0.115 | 0.111/0.116 | 0.618 |
| Qwen3-0.6B | – | 0.225/0.237 | 0.363/0.376 | 0.034 | 0.230 (1.2) | 0.543 | 0.283 | 0.295/0.334 | 0.512 |
| Qwen3-1.7B | – | 0.228/0.251 | 0.369/0.405 | 0.025 | 0.193 (1.8) | 0.642 | 0.299 | 0.306/0.395 | 0.546 |
| Qwen3-4B | – | 0.177/0.206 | 0.283/0.329 | 0.025 | 0.164 (1.7) | 0.545 | 0.221 | 0.210/0.306 | 0.599 |
| Qwen3-8B | 2.47 | 0.161/0.179 | 0.261/0.290 | 0.015 | 0.143 (1.7) | 0.458 | 0.191 | 0.188/0.243 | 0.542 |
| Qwen3-14B | 4.04 | 0.137/0.144 | 0.221/0.234 | 0.011 | 0.127 (1.5) | 0.392 | 0.152 | 0.150/0.223 | 0.594 |
| Qwen3-32B | 3.37 | 0.118/0.123 | 0.193/0.199 | 0.011 | 0.118 (1.2) | 0.335 | 0.120 | 0.130/0.136 | 0.672 |
| Nemotron-Terminal-8B | 13.0 | 0.275/0.234 | 0.321/0.294 | 0.147 | 0.220 (1.3) | 0.260 | 0.108 | 0.246/0.176 | 0.652 |
| Nemotron-Terminal-14B | 20.2 | 0.260/0.325 | 0.289/0.331 | 0.317 | 0.295 (1.4) | 0.238 | 0.100 | 0.206/0.185 | 0.667 |
| Nemotron-Terminal-32B | 27.4 | 0.144/0.153 | 0.212/0.223 | 0.050 | 0.147 (1.2) | 0.226 | 0.092 | 0.148/0.143 | 0.679 |

## Paired comparisons (Δ = second − first, 95% bootstrap CI over trajectories / items)

| comparison | fmt | Δ obs BPB | Δ novel obs BPB | Δ obs BPB @T* | Δ pred novel BPB | Δ AUROC(new) |
|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base → Qwen3-0.6B | neutral | +0.055 [+0.050,+0.061] | +0.088 [+0.080,+0.097] | +0.048 [+0.043,+0.053] | +0.095 [+0.085,+0.105] | -0.135 [-0.263,-0.001] |
| Qwen3-0.6B-Base → Qwen3-0.6B | native | +0.059 [+0.054,+0.065] | +0.089 [+0.080,+0.098] | +0.052 [+0.047,+0.057] | +0.108 [+0.098,+0.118] | +0.002 [-0.131,+0.121] |
| Qwen3-1.7B-Base → Qwen3-1.7B | neutral | +0.086 [+0.080,+0.093] | +0.138 [+0.128,+0.148] | +0.044 [+0.039,+0.049] | +0.146 [+0.134,+0.158] | -0.133 [-0.242,-0.021] |
| Qwen3-1.7B-Base → Qwen3-1.7B | native | +0.104 [+0.096,+0.111] | +0.166 [+0.155,+0.177] | +0.046 [+0.042,+0.052] | +0.228 [+0.208,+0.247] | +0.092 [-0.033,+0.220] |
| Qwen3-4B-Base → Qwen3-4B | neutral | +0.055 [+0.050,+0.059] | +0.084 [+0.077,+0.091] | +0.031 [+0.028,+0.035] | +0.078 [+0.071,+0.087] | +0.028 [-0.073,+0.130] |
| Qwen3-4B-Base → Qwen3-4B | native | +0.080 [+0.075,+0.086] | +0.124 [+0.115,+0.133] | +0.038 [+0.034,+0.042] | +0.160 [+0.145,+0.175] | +0.237 [+0.108,+0.363] |
| Qwen3-8B-Base → Qwen3-8B | neutral | +0.046 [+0.043,+0.050] | +0.073 [+0.068,+0.079] | +0.024 [+0.022,+0.028] | +0.066 [+0.060,+0.072] | +0.018 [-0.060,+0.096] |
| Qwen3-8B-Base → Qwen3-8B | native | +0.063 [+0.058,+0.068] | +0.101 [+0.094,+0.110] | +0.028 [+0.025,+0.031] | +0.119 [+0.109,+0.130] | +0.138 [+0.001,+0.271] |
| Qwen3-14B-Base → Qwen3-14B | neutral | +0.029 [+0.026,+0.032] | +0.046 [+0.042,+0.050] | +0.016 [+0.014,+0.019] | +0.039 [+0.034,+0.043] | -0.024 [-0.102,+0.058] |
| Qwen3-14B-Base → Qwen3-14B | native | +0.036 [+0.033,+0.039] | +0.058 [+0.054,+0.063] | +0.019 [+0.016,+0.022] | +0.107 [+0.098,+0.117] | +0.054 [-0.054,+0.154] |
| Qwen3-8B → Nemotron-Terminal-8B | neutral | +0.114 [+0.102,+0.128] | +0.060 [+0.046,+0.073] | +0.115 [+0.105,+0.126] | +0.058 [+0.047,+0.069] | +0.110 [+0.026,+0.186] |
| Qwen3-8B → Nemotron-Terminal-8B | native | +0.056 [+0.047,+0.065] | +0.004 [-0.006,+0.015] | +0.077 [+0.069,+0.084] | -0.067 [-0.074,-0.059] | -0.098 [-0.217,+0.018] |
| Qwen3-14B → Nemotron-Terminal-14B | neutral | +0.123 [+0.111,+0.133] | +0.068 [+0.059,+0.078] | +0.117 [+0.108,+0.127] | +0.057 [+0.049,+0.064] | +0.072 [-0.001,+0.141] |
| Qwen3-14B → Nemotron-Terminal-14B | native | +0.182 [+0.165,+0.198] | +0.097 [+0.085,+0.108] | +0.168 [+0.154,+0.181] | -0.037 [-0.045,-0.029] | -0.181 [-0.284,-0.075] |
| Qwen3-32B → Nemotron-Terminal-32B | neutral | +0.026 [+0.021,+0.031] | +0.019 [+0.012,+0.025] | +0.025 [+0.020,+0.029] | +0.019 [+0.015,+0.023] | +0.007 [-0.093,+0.113] |
| Qwen3-32B → Nemotron-Terminal-32B | native | +0.030 [+0.025,+0.036] | +0.024 [+0.017,+0.030] | +0.029 [+0.024,+0.034] | +0.007 [+0.003,+0.010] | -0.088 [-0.190,+0.021] |
| Qwen3-8B-Base → Nemotron-Terminal-8B | neutral | +0.160 [+0.148,+0.174] | +0.133 [+0.121,+0.147] | +0.139 [+0.128,+0.149] | +0.124 [+0.113,+0.133] | +0.128 [+0.030,+0.234] |
| Qwen3-8B-Base → Nemotron-Terminal-8B | native | +0.119 [+0.110,+0.128] | +0.105 [+0.097,+0.115] | +0.105 [+0.097,+0.113] | +0.052 [+0.046,+0.058] | +0.039 [-0.083,+0.158] |
| Qwen3-14B-Base → Nemotron-Terminal-14B | neutral | +0.152 [+0.140,+0.164] | +0.114 [+0.105,+0.123] | +0.133 [+0.123,+0.144] | +0.095 [+0.089,+0.102] | +0.049 [-0.019,+0.118] |
| Qwen3-14B-Base → Nemotron-Terminal-14B | native | +0.218 [+0.202,+0.235] | +0.155 [+0.143,+0.167] | +0.187 [+0.173,+0.203] | +0.070 [+0.065,+0.076] | -0.126 [-0.237,-0.012] |

## Findings
1. **Base beats instruct on raw observation perplexity at every size, in both renderings.**
   - Observation BPB gap: +0.03 to +0.10 (novel tokens: +0.05 to +0.17), all CIs exclude 0.
   - It shrinks with scale: neutral +0.055 at 0.6B, +0.029 at 14B. Qwen3-32B instruct (0.118 neutral) sits close to the 14B base (0.108).
   - The gap is the same under the neutral rendering, so it is not a chat-template artefact.
2. **Scale helps within each family.**
   - Base: 0.170 → 0.108 (0.6B → 14B).
   - Instruct: 0.225 → 0.118 (0.6B → 32B), with a dip at 1.7B.
   - Same pattern on novel tokens and in prompted prediction.
3. **Temperature scaling closes about half the base–instruct gap.**
   - Base models are calibrated (T* = 1.0). Instruct models are over-sharp (T* = 1.2–1.8).
   - After per-model T, the observation gap is +0.016 to +0.052.
   - So part is sharpening, part is real probability moved away from environment text (log-ratio section).
4. **Role-switch mass does not explain the gap.**
   - Special-token mass at observation positions averages ≤0.003 per token.
   - It is non-trivial only in the first 16 tokens under the native template: 0.01–0.06 for instruct and Nemotron, 0.000 for base.
   - The gap is mostly in the observation body and on novel tokens, and appears under the neutral rendering too. The article's "predicts its own next step" effect is real at observation onsets but small in mass.
5. **Nemotron (agentic SFT) is worse on raw observation perplexity, mostly through copying.** This reproduces the article's sign: the stronger terminal agent has higher observation perplexity.
   - Observation BPB versus Qwen3 instruct: +0.06 to +0.18 at 8B/14B, +0.03 at 32B.
   - Copyable-token BPB: about 0.01 → 0.15–0.32 at 8B/14B (0.05 at 32B).
   - Novel tokens: +0.004 [−0.006, +0.015] at 8B native (no change), +0.097 at 14B.
   - Nemotron is far better on its own role: thought 0.23–0.26 vs 0.34–0.46, action 0.09–0.11 vs 0.12–0.19.
6. **Prompted prediction (assistant role).**
   - Native rendering: Nemotron beats its Qwen3 instruct parent on novel tokens at 8B (−0.067 [−0.074, −0.059]) and 14B (−0.037), and is marginally worse at 32B (+0.007 [+0.003, +0.010]).
   - It still loses to the base models: 0.176 vs 0.124 at 8B, 0.185 vs 0.116 at 14B.
   - Neutral rendering: Nemotron is worse than instruct.
   - Agentic SFT helps when the model is asked in its trained role, but does not reach base-model world knowledge.
7. **The discrete error question is too weak to conclude from.**
   - AUROC 0.42–0.72 with 44 positives; CIs about ±0.1.
   - Under the native template, Nemotron puts ~0 probability on Yes/No (it answers in Terminus JSON), so its native numbers are meaningless.
   - Neutral rendering: Nemotron 0.65 / 0.67 / 0.68 vs instruct 0.54 / 0.59 / 0.67. That is +0.11 [+0.03, +0.19] at 8B; n.s. at 14B and 32B. Suggestive only.
8. **The Nemotron copy failure is real and specific to long agentic context.**
   - It is not a rendering bug (check below).
   - In the one-message terminal context, Nemotron copies random strings as well as Qwen3 (Δ ≤ 0.01 bits/char).
   - In the bare context the deltas are small and mixed in sign: pooled +0.00 / +0.08 / +0.01 at 8B / 14B / 32B.
   - Inside a real trajectory prefix it loses 0.36–1.6 bits/char, while Qwen3 base and instruct stay ≤0.03.

## Log-ratio  log p_post(x) − log p_base(x)  (bits/token)
Mean per span, with the share of total |log-ratio| mass in parentheses. Wrapper tokens are excluded from the denominator; observation sub-rows overlap the observation row. Both renderings, p10/p50/p90 and CIs are in `results/logratio.md`.


**native rendering, raw**

| pair | task | thought | action | observation | markup | obs:first16 | obs:body | obs:novel | obs:copy |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base → Qwen3-0.6B | -0.502 (0.37) | -0.178 (0.21) | -0.212 (0.15) | -0.186 (0.19) | -0.600 (0.08) | -0.745 (0.02) | -0.167 (0.17) | -0.292 (0.17) | -0.048 (0.02) |
| Qwen3-1.7B-Base → Qwen3-1.7B | -0.781 (0.33) | -0.936 (0.26) | -0.461 (0.16) | -0.325 (0.18) | -0.797 (0.07) | -0.755 (0.01) | -0.311 (0.17) | -0.546 (0.17) | -0.037 (0.01) |
| Qwen3-4B-Base → Qwen3-4B | -0.767 (0.38) | -0.749 (0.26) | -0.299 (0.13) | -0.251 (0.17) | -0.493 (0.05) | -1.117 (0.02) | -0.221 (0.15) | -0.407 (0.15) | -0.047 (0.01) |
| Qwen3-8B-Base → Qwen3-8B | -0.622 (0.40) | -0.432 (0.23) | -0.236 (0.13) | -0.198 (0.16) | -0.654 (0.08) | -0.566 (0.01) | -0.185 (0.15) | -0.334 (0.15) | -0.021 (0.01) |
| Qwen3-14B-Base → Qwen3-14B | -0.483 (0.45) | -0.255 (0.23) | -0.135 (0.11) | -0.113 (0.13) | -0.574 (0.09) | -0.374 (0.01) | -0.104 (0.12) | -0.191 (0.12) | -0.011 (0.01) |
| Qwen3-8B-Base → Nemotron-Terminal-8B | -0.237 (0.33) | +0.454 (0.24) | +0.066 (0.08) | -0.372 (0.29) | -0.446 (0.06) | -0.157 (0.01) | -0.379 (0.28) | -0.347 (0.19) | -0.404 (0.10) |
| Qwen3-14B-Base → Nemotron-Terminal-14B | -0.249 (0.30) | +0.433 (0.19) | +0.057 (0.07) | -0.681 (0.39) | -0.602 (0.06) | -2.320 (0.04) | -0.625 (0.34) | -0.509 (0.20) | -0.904 (0.18) |
| Qwen3-8B → Nemotron-Terminal-8B | +0.385 (0.32) | +0.886 (0.24) | +0.303 (0.11) | -0.174 (0.29) | +0.208 (0.03) | +0.409 (0.02) | -0.193 (0.28) | -0.013 (0.21) | -0.384 (0.08) |
| Qwen3-14B → Nemotron-Terminal-14B | +0.234 (0.29) | +0.687 (0.21) | +0.192 (0.09) | -0.568 (0.39) | -0.028 (0.02) | -1.946 (0.04) | -0.521 (0.35) | -0.318 (0.22) | -0.893 (0.18) |
| Qwen3-32B → Nemotron-Terminal-32B | +0.026 (0.36) | +0.489 (0.28) | +0.102 (0.10) | -0.094 (0.23) | +0.009 (0.02) | +0.218 (0.02) | -0.105 (0.22) | -0.077 (0.19) | -0.116 (0.04) |

**native rendering, after per-model temperature scaling**

| pair | task | thought | action | observation | markup | obs:first16 | obs:body | obs:novel | obs:copy |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base → Qwen3-0.6B | -0.381 (0.37) | -0.067 (0.21) | -0.164 (0.15) | -0.161 (0.20) | -0.489 (0.07) | -0.610 (0.02) | -0.146 (0.18) | -0.245 (0.18) | -0.052 (0.02) |
| Qwen3-1.7B-Base → Qwen3-1.7B | -0.459 (0.37) | -0.245 (0.24) | -0.165 (0.15) | -0.147 (0.18) | -0.433 (0.07) | -0.231 (0.01) | -0.144 (0.16) | -0.246 (0.16) | -0.018 (0.01) |
| Qwen3-4B-Base → Qwen3-4B | -0.358 (0.39) | -0.177 (0.26) | -0.110 (0.13) | -0.118 (0.17) | -0.270 (0.05) | -0.483 (0.02) | -0.106 (0.15) | -0.185 (0.15) | -0.031 (0.02) |
| Qwen3-8B-Base → Qwen3-8B | -0.259 (0.39) | -0.083 (0.24) | -0.090 (0.13) | -0.089 (0.16) | -0.395 (0.08) | -0.202 (0.01) | -0.085 (0.15) | -0.147 (0.15) | -0.013 (0.01) |
| Qwen3-14B-Base → Qwen3-14B | -0.202 (0.43) | -0.079 (0.24) | -0.066 (0.12) | -0.059 (0.13) | -0.374 (0.08) | -0.124 (0.01) | -0.057 (0.12) | -0.097 (0.12) | -0.011 (0.01) |
| Qwen3-8B-Base → Nemotron-Terminal-8B | -0.121 (0.32) | +0.506 (0.24) | +0.066 (0.09) | -0.327 (0.30) | -0.332 (0.05) | -0.086 (0.01) | -0.335 (0.28) | -0.296 (0.20) | -0.367 (0.10) |
| Qwen3-14B-Base → Nemotron-Terminal-14B | -0.109 (0.29) | +0.475 (0.20) | +0.059 (0.07) | -0.584 (0.39) | -0.454 (0.06) | -1.787 (0.04) | -0.544 (0.35) | -0.428 (0.21) | -0.788 (0.18) |
| Qwen3-8B → Nemotron-Terminal-8B | +0.138 (0.31) | +0.589 (0.24) | +0.156 (0.10) | -0.238 (0.32) | +0.063 (0.03) | +0.115 (0.02) | -0.250 (0.30) | -0.149 (0.22) | -0.354 (0.10) |
| Qwen3-14B → Nemotron-Terminal-14B | +0.092 (0.27) | +0.554 (0.21) | +0.125 (0.08) | -0.525 (0.42) | -0.081 (0.02) | -1.663 (0.04) | -0.487 (0.38) | -0.332 (0.22) | -0.777 (0.19) |
| Qwen3-32B → Nemotron-Terminal-32B | +0.062 (0.34) | +0.510 (0.29) | +0.095 (0.10) | -0.096 (0.25) | +0.042 (0.02) | +0.204 (0.02) | -0.106 (0.23) | -0.081 (0.20) | -0.116 (0.05) |

- **Instruct vs base.** Every span loses probability; medians are ≈0 and the mean comes from the low tail.
  - Task tokens (the Terminus system prompt) carry 33–45% of the |Δ| mass, against a token share of about 30%.
  - Observations carry 13–19% of the mass against 36% of tokens, so per token, post-training moved observation probability less than prompt and thought probability.
  - Temperature scaling halves the task/thought deltas but leaves observation deltas at −0.06 to −0.16. That residual is reallocation, not sharpening.
- **Nemotron vs Qwen3 instruct (the agentic-SFT stage alone).**
  - Gains on thought (+0.49 to +0.89 bits/token) and action (+0.10 to +0.30).
  - Losses on observations (−0.09 to −0.57), concentrated on copyable tokens (−0.12 to −0.89). Observations' share of |Δ| mass rises to 23–39%.
  - The loss survives temperature scaling (8B native −0.17 → −0.24, 14B −0.57 → −0.53): reallocation, not sharpening.
  - At 14B native, the first-16 observation tokens lose −1.9 bits/token: role-boundary predictions.
- **Nemotron-32B is much milder** (observations −0.09, copyable −0.12), consistent with its small copy-test loss.

## Synthetic copy test (`copytest.py`)
- **Strings.** 8/16/32/64 characters in four alphabets (hex, base64, concatenated common words, digits); 200 per cell, seed 0.
- **Contexts.**
  - (i) bare: `S\n<≈200-token filler>\nS`.
  - (ii) terminal: `root@S:/app# ls\nfile.txt\nroot@S:/app# `.
  - (iii) 50 real AgenticPPL prefixes (task, first agent turn, first observation; ≤3,072 tokens) with the container hostname replaced by S everywhere.
- **Score.** Bits per character over all repeated occurrences.

Δ bits/char, Nemotron − Qwen3 instruct (paired over strings, pooled over lengths):

| size | context | hex | base64 | words | digits | all |
|---|---|---|---|---|---|---|
| 8B | bare | +0.111 [+0.097,+0.124] | -0.123 [-0.164,-0.087] | -0.126 [-0.146,-0.108] | +0.139 [+0.131,+0.148] | +0.000 [-0.013,+0.012] |
| 8B | term/neutral | +0.018 [+0.010,+0.026] | +0.005 [+0.003,+0.007] | +0.003 [+0.002,+0.004] | +0.002 [+0.001,+0.003] | +0.007 [+0.005,+0.009] |
| 8B | term/native | +0.016 [+0.006,+0.027] | +0.005 [+0.002,+0.008] | +0.003 [+0.002,+0.005] | +0.003 [+0.002,+0.004] | +0.007 [+0.004,+0.010] |
| 8B | traj/neutral | +0.930 [+0.823,+1.048] | +1.037 [+0.898,+1.182] | +0.405 [+0.320,+0.501] | +0.581 [+0.523,+0.647] | +0.737 [+0.684,+0.790] |
| 8B | traj/native | +0.813 [+0.715,+0.914] | +0.915 [+0.797,+1.060] | +0.434 [+0.349,+0.524] | +0.539 [+0.487,+0.594] | +0.674 [+0.630,+0.722] |
| 14B | bare | +0.100 [+0.090,+0.110] | +0.068 [+0.055,+0.082] | +0.085 [+0.073,+0.097] | +0.052 [+0.044,+0.060] | +0.076 [+0.071,+0.082] |
| 14B | term/neutral | +0.023 [+0.013,+0.032] | -0.003 [-0.013,+0.003] | +0.001 [+0.001,+0.002] | +0.000 [-0.002,+0.002] | +0.005 [+0.002,+0.008] |
| 14B | term/native | +0.015 [+0.009,+0.022] | +0.000 [-0.002,+0.002] | +0.002 [+0.002,+0.003] | +0.001 [-0.000,+0.003] | +0.005 [+0.003,+0.006] |
| 14B | traj/neutral | +1.319 [+1.139,+1.500] | +1.628 [+1.412,+1.883] | +0.952 [+0.809,+1.101] | +1.141 [+1.003,+1.293] | +1.259 [+1.168,+1.358] |
| 14B | traj/native | +1.600 [+1.409,+1.798] | +2.152 [+1.880,+2.420] | +1.235 [+1.062,+1.424] | +1.403 [+1.256,+1.564] | +1.596 [+1.496,+1.708] |
| 32B | bare | +0.049 [+0.039,+0.061] | -0.024 [-0.043,-0.007] | -0.055 [-0.070,-0.041] | +0.051 [+0.045,+0.056] | +0.005 [-0.001,+0.011] |
| 32B | term/neutral | +0.002 [-0.001,+0.006] | -0.000 [-0.001,+0.001] | +0.000 [+0.000,+0.001] | +0.000 [-0.001,+0.001] | +0.001 [-0.000,+0.002] |
| 32B | term/native | +0.004 [+0.001,+0.007] | -0.002 [-0.005,+0.000] | -0.000 [-0.001,+0.001] | +0.000 [-0.002,+0.002] | +0.000 [-0.001,+0.002] |
| 32B | traj/neutral | +0.328 [+0.271,+0.397] | +0.445 [+0.358,+0.552] | +0.436 [+0.356,+0.514] | +0.242 [+0.201,+0.288] | +0.363 [+0.328,+0.405] |
| 32B | traj/native | +0.427 [+0.358,+0.508] | +0.579 [+0.471,+0.691] | +0.567 [+0.478,+0.668] | +0.330 [+0.275,+0.391] | +0.476 [+0.431,+0.522] |

- Only context (iii), a long agentic prefix, shows a large effect: about 0.7 / 1.3–1.6 / 0.4–0.5 bits/char for Nemotron 8B / 14B / 32B. Every Qwen3 base and instruct model stays ≤0.03. The terminal context gives Δ ≤ 0.01. The bare context gives small mixed-sign Δ (per alphabet −0.13 to +0.14, pooled ≤ +0.08).
- The excess is spread over later tokens (8B: 1.2 bits per later token). At 14B and 32B the first token after `root@` also costs 5–7 bits.
- It is present for all alphabets, including common words, so it is not a hex prior.
- Hypothesis, not tested: terminal SFT (loss on assistant turns only) degrades in-context copying inside long agentic transcripts, while short-context copying stays intact.
- In the bare context every model pays ~10 bits on the first token (S's recurrence is unexpected). This is the same for all models.

## Nemotron rendering / tokenisation check
- `tokenizer.json` is byte-identical to Qwen3-8B's (sha1 a1de58e2…).
- `config.json` is semantically identical: same rope, no scaling. Diffs are only the dtype key, `layer_types` (all full attention) and the transformers version.
- The chat template is identical (trailing newline only).
- `generation_config` is identical, and unused in teacher-forced scoring.
- A plain `model(input_ids).logits` pass, with no cache or chunking, on the same ids reproduces the pipeline log-probs (mean |Δ| 0.013–0.029 nats/token).
- Example: Nemotron-8B pays 5–12 bits on single hostname characters where Qwen3-8B pays ≈0.

## Caveats
- **One trajectory set.** One harness (Terminus-2), with teachers outside the scored family. Thought/action BPB partly measures style match to the teachers.
- **Few benchmark scores.** TB2.0 numbers exist only for the 8/14/32B instruct and Nemotron models, so only within-family deltas are reported, no cross-model correlation.
- **bf16 noise.** Per-token log-probs vary by up to a few nats on isolated tokens between kernel paths; means are stable, and segmentation is identical across models.
- **Measure 6 labels** are regex-based and only moderately precise.
- **No thinking mode.** Prompted prediction uses the non-thinking template (empty think block).
- **Base models under the native template** see special tokens they were never trained to produce. The neutral rendering is the fair base-vs-instruct comparison; the sign agrees across renderings.


---
# Appendix A: all pipeline tables (results/tables.md)

### Teacher-forced BPB by span type (eval, 200 traj)

| model | fmt | task | thought | action | obs | markup |
|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | neutral | 0.589 | 0.501 | 0.225 | 0.170 | 0.055 |
| Qwen3-0.6B-Base | native | 0.592 | 0.504 | 0.226 | 0.178 | 0.055 |
| Qwen3-1.7B-Base | neutral | 0.522 | 0.429 | 0.172 | 0.142 | 0.044 |
| Qwen3-1.7B-Base | native | 0.527 | 0.433 | 0.174 | 0.147 | 0.045 |
| Qwen3-4B-Base | neutral | 0.475 | 0.376 | 0.139 | 0.123 | 0.039 |
| Qwen3-4B-Base | native | 0.478 | 0.378 | 0.139 | 0.126 | 0.036 |
| Qwen3-8B-Base | neutral | 0.453 | 0.360 | 0.127 | 0.115 | 0.034 |
| Qwen3-8B-Base | native | 0.458 | 0.361 | 0.126 | 0.115 | 0.032 |
| Qwen3-14B-Base | neutral | 0.438 | 0.333 | 0.115 | 0.108 | 0.037 |
| Qwen3-14B-Base | native | 0.445 | 0.335 | 0.115 | 0.108 | 0.027 |
| Qwen3-0.6B | neutral | 0.701 | 0.527 | 0.282 | 0.225 | 0.090 |
| Qwen3-0.6B | native | 0.709 | 0.543 | 0.283 | 0.237 | 0.267 |
| Qwen3-1.7B | neutral | 0.701 | 0.544 | 0.283 | 0.228 | 0.114 |
| Qwen3-1.7B | native | 0.710 | 0.642 | 0.299 | 0.251 | 0.328 |
| Qwen3-4B | neutral | 0.631 | 0.458 | 0.202 | 0.177 | 0.107 |
| Qwen3-4B | native | 0.657 | 0.545 | 0.221 | 0.206 | 0.211 |
| Qwen3-8B | neutral | 0.570 | 0.420 | 0.180 | 0.161 | 0.070 |
| Qwen3-8B | native | 0.603 | 0.458 | 0.191 | 0.179 | 0.264 |
| Qwen3-14B | neutral | 0.549 | 0.373 | 0.144 | 0.137 | 0.107 |
| Qwen3-14B | native | 0.558 | 0.392 | 0.152 | 0.144 | 0.231 |
| Qwen3-32B | neutral | 0.464 | 0.332 | 0.118 | 0.118 | 0.082 |
| Qwen3-32B | native | 0.472 | 0.335 | 0.120 | 0.123 | 0.189 |
| Nemotron-Terminal-8B | neutral | 0.505 | 0.247 | 0.109 | 0.275 | 0.041 |
| Nemotron-Terminal-8B | native | 0.513 | 0.260 | 0.108 | 0.234 | 0.190 |
| Nemotron-Terminal-14B | neutral | 0.501 | 0.232 | 0.100 | 0.260 | 0.070 |
| Nemotron-Terminal-14B | native | 0.504 | 0.238 | 0.100 | 0.325 | 0.240 |
| Nemotron-Terminal-32B | neutral | 0.464 | 0.221 | 0.092 | 0.144 | 0.040 |
| Nemotron-Terminal-32B | native | 0.466 | 0.226 | 0.092 | 0.153 | 0.186 |

### Observation breakdown

| model | fmt | obs | first16 | body | novel | copy | capped bits/tok | mean p | copy frac |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | neutral | 0.170 | 0.295 | 0.166 | 0.275 | 0.015 | 0.228 | 0.889 | 0.434 |
| Qwen3-0.6B-Base | native | 0.178 | 0.313 | 0.173 | 0.287 | 0.017 | 0.230 | 0.889 | 0.434 |
| Qwen3-1.7B-Base | neutral | 0.142 | 0.303 | 0.137 | 0.231 | 0.011 | 0.190 | 0.908 | 0.434 |
| Qwen3-1.7B-Base | native | 0.147 | 0.323 | 0.141 | 0.238 | 0.012 | 0.194 | 0.906 | 0.434 |
| Qwen3-4B-Base | neutral | 0.123 | 0.265 | 0.118 | 0.199 | 0.010 | 0.169 | 0.919 | 0.434 |
| Qwen3-4B-Base | native | 0.126 | 0.281 | 0.121 | 0.205 | 0.009 | 0.170 | 0.918 | 0.434 |
| Qwen3-8B-Base | neutral | 0.115 | 0.250 | 0.110 | 0.187 | 0.009 | 0.160 | 0.923 | 0.434 |
| Qwen3-8B-Base | native | 0.115 | 0.260 | 0.111 | 0.188 | 0.008 | 0.162 | 0.922 | 0.434 |
| Qwen3-14B-Base | neutral | 0.108 | 0.265 | 0.103 | 0.175 | 0.009 | 0.152 | 0.927 | 0.434 |
| Qwen3-14B-Base | native | 0.108 | 0.242 | 0.103 | 0.176 | 0.007 | 0.151 | 0.928 | 0.434 |
| Qwen3-0.6B | neutral | 0.225 | 0.351 | 0.221 | 0.363 | 0.023 | 0.254 | 0.878 | 0.434 |
| Qwen3-0.6B | native | 0.237 | 0.557 | 0.227 | 0.376 | 0.034 | 0.262 | 0.874 | 0.434 |
| Qwen3-1.7B | neutral | 0.228 | 0.505 | 0.219 | 0.369 | 0.022 | 0.186 | 0.911 | 0.434 |
| Qwen3-1.7B | native | 0.251 | 0.570 | 0.240 | 0.405 | 0.025 | 0.187 | 0.910 | 0.434 |
| Qwen3-4B | neutral | 0.177 | 0.380 | 0.170 | 0.283 | 0.021 | 0.168 | 0.920 | 0.434 |
| Qwen3-4B | native | 0.206 | 0.646 | 0.192 | 0.329 | 0.025 | 0.165 | 0.921 | 0.434 |
| Qwen3-8B | neutral | 0.161 | 0.401 | 0.153 | 0.261 | 0.015 | 0.154 | 0.927 | 0.434 |
| Qwen3-8B | native | 0.179 | 0.446 | 0.170 | 0.290 | 0.015 | 0.148 | 0.929 | 0.434 |
| Qwen3-14B | neutral | 0.137 | 0.334 | 0.130 | 0.221 | 0.013 | 0.144 | 0.931 | 0.434 |
| Qwen3-14B | native | 0.144 | 0.365 | 0.137 | 0.234 | 0.011 | 0.142 | 0.932 | 0.434 |
| Qwen3-32B | neutral | 0.118 | 0.291 | 0.113 | 0.193 | 0.009 | 0.146 | 0.930 | 0.434 |
| Qwen3-32B | native | 0.123 | 0.347 | 0.115 | 0.199 | 0.011 | 0.146 | 0.930 | 0.434 |
| Nemotron-Terminal-8B | neutral | 0.275 | 0.320 | 0.274 | 0.321 | 0.209 | 0.303 | 0.854 | 0.434 |
| Nemotron-Terminal-8B | native | 0.234 | 0.312 | 0.232 | 0.294 | 0.147 | 0.271 | 0.870 | 0.434 |
| Nemotron-Terminal-14B | neutral | 0.260 | 0.345 | 0.257 | 0.289 | 0.216 | 0.283 | 0.864 | 0.434 |
| Nemotron-Terminal-14B | native | 0.325 | 1.002 | 0.303 | 0.331 | 0.317 | 0.313 | 0.849 | 0.434 |
| Nemotron-Terminal-32B | neutral | 0.144 | 0.182 | 0.143 | 0.212 | 0.044 | 0.183 | 0.912 | 0.434 |
| Nemotron-Terminal-32B | native | 0.153 | 0.275 | 0.149 | 0.223 | 0.050 | 0.186 | 0.910 | 0.434 |

### Role-switch mass at observation positions (mean prob per token)

| model | fmt | special all | special first16 | special body | <think> | <|im_end|> | '###' first16 | special @non-obs |
|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | neutral | 0.001 | 0.001 | 0.001 | 0.000 | 0.000 | 0.001 | 0.000 |
| Qwen3-0.6B-Base | native | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-1.7B-Base | neutral | 0.000 | 0.001 | 0.000 | 0.000 | 0.000 | 0.003 | 0.000 |
| Qwen3-1.7B-Base | native | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-4B-Base | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 |
| Qwen3-4B-Base | native | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-8B-Base | neutral | 0.001 | 0.000 | 0.001 | 0.000 | 0.000 | 0.001 | 0.000 |
| Qwen3-8B-Base | native | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-14B-Base | neutral | 0.001 | 0.000 | 0.001 | 0.000 | 0.000 | 0.002 | 0.000 |
| Qwen3-14B-Base | native | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-0.6B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-0.6B | native | 0.002 | 0.053 | 0.001 | 0.001 | 0.000 | 0.000 | 0.001 |
| Qwen3-1.7B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-1.7B | native | 0.001 | 0.020 | 0.001 | 0.000 | 0.000 | 0.000 | 0.001 |
| Qwen3-4B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 | 0.000 |
| Qwen3-4B | native | 0.002 | 0.041 | 0.001 | 0.001 | 0.000 | 0.000 | 0.001 |
| Qwen3-8B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Qwen3-8B | native | 0.001 | 0.015 | 0.001 | 0.000 | 0.000 | 0.000 | 0.002 |
| Qwen3-14B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 |
| Qwen3-14B | native | 0.001 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 |
| Qwen3-32B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.001 |
| Qwen3-32B | native | 0.002 | 0.041 | 0.001 | 0.000 | 0.000 | 0.000 | 0.002 |
| Nemotron-Terminal-8B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 |
| Nemotron-Terminal-8B | native | 0.000 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 |
| Nemotron-Terminal-14B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 | 0.000 |
| Nemotron-Terminal-14B | native | 0.003 | 0.062 | 0.001 | 0.003 | 0.000 | 0.000 | 0.001 |
| Nemotron-Terminal-32B | neutral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 | 0.000 |
| Nemotron-Terminal-32B | native | 0.002 | 0.036 | 0.001 | 0.002 | 0.000 | 0.000 | 0.001 |

### Temperature scaling (T fit on 50 cal traj, obs tokens)

| model | fmt | T* | obs T=1 | obs T* | novel T=1 | novel T* |
|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | neutral | 1.000 | 0.170 | 0.170 | 0.275 | 0.275 |
| Qwen3-0.6B-Base | native | 1.000 | 0.178 | 0.178 | 0.287 | 0.287 |
| Qwen3-1.7B-Base | neutral | 1.000 | 0.142 | 0.142 | 0.231 | 0.231 |
| Qwen3-1.7B-Base | native | 1.000 | 0.147 | 0.147 | 0.238 | 0.238 |
| Qwen3-4B-Base | neutral | 1.000 | 0.123 | 0.123 | 0.199 | 0.199 |
| Qwen3-4B-Base | native | 1.000 | 0.126 | 0.126 | 0.205 | 0.205 |
| Qwen3-8B-Base | neutral | 1.000 | 0.115 | 0.115 | 0.187 | 0.187 |
| Qwen3-8B-Base | native | 1.000 | 0.115 | 0.115 | 0.188 | 0.188 |
| Qwen3-14B-Base | neutral | 1.000 | 0.108 | 0.108 | 0.175 | 0.175 |
| Qwen3-14B-Base | native | 1.000 | 0.108 | 0.108 | 0.176 | 0.176 |
| Qwen3-0.6B | neutral | 1.200 | 0.225 | 0.219 | 0.363 | 0.350 |
| Qwen3-0.6B | native | 1.200 | 0.237 | 0.230 | 0.376 | 0.362 |
| Qwen3-1.7B | neutral | 1.700 | 0.228 | 0.186 | 0.369 | 0.301 |
| Qwen3-1.7B | native | 1.800 | 0.251 | 0.193 | 0.405 | 0.312 |
| Qwen3-4B | neutral | 1.500 | 0.177 | 0.154 | 0.283 | 0.246 |
| Qwen3-4B | native | 1.700 | 0.206 | 0.164 | 0.329 | 0.262 |
| Qwen3-8B | neutral | 1.600 | 0.161 | 0.139 | 0.261 | 0.225 |
| Qwen3-8B | native | 1.700 | 0.179 | 0.143 | 0.290 | 0.232 |
| Qwen3-14B | neutral | 1.400 | 0.137 | 0.124 | 0.221 | 0.200 |
| Qwen3-14B | native | 1.500 | 0.144 | 0.127 | 0.234 | 0.205 |
| Qwen3-32B | neutral | 1.200 | 0.118 | 0.115 | 0.193 | 0.186 |
| Qwen3-32B | native | 1.200 | 0.123 | 0.118 | 0.199 | 0.191 |
| Nemotron-Terminal-8B | neutral | 1.300 | 0.275 | 0.254 | 0.321 | 0.301 |
| Nemotron-Terminal-8B | native | 1.300 | 0.234 | 0.220 | 0.294 | 0.279 |
| Nemotron-Terminal-14B | neutral | 1.300 | 0.260 | 0.241 | 0.289 | 0.273 |
| Nemotron-Terminal-14B | native | 1.400 | 0.325 | 0.295 | 0.331 | 0.309 |
| Nemotron-Terminal-32B | neutral | 1.200 | 0.144 | 0.140 | 0.212 | 0.205 |
| Nemotron-Terminal-32B | native | 1.200 | 0.153 | 0.147 | 0.223 | 0.214 |

### Prompted prediction (assistant role) and Yes/No error question

| model | fmt | pred bpb | pred novel bpb | pred capped | AUROC new | Brier new | acc new | AUROC raw | P(yes) mean | Yes+No mass |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | neutral | 0.128 | 0.200 | 0.187 | 0.647 | 0.294 | 0.375 | 0.661 | 0.552 | 0.694 |
| Qwen3-0.6B-Base | native | 0.145 | 0.226 | 0.191 | 0.557 | 0.093 | 0.906 | 0.556 | 0.179 | 0.044 |
| Qwen3-1.7B-Base | neutral | 0.102 | 0.160 | 0.146 | 0.679 | 0.089 | 0.906 | 0.624 | 0.171 | 0.906 |
| Qwen3-1.7B-Base | native | 0.107 | 0.168 | 0.151 | 0.465 | 0.087 | 0.906 | 0.492 | 0.055 | 0.176 |
| Qwen3-4B-Base | neutral | 0.084 | 0.132 | 0.127 | 0.571 | 0.146 | 0.898 | 0.546 | 0.340 | 0.769 |
| Qwen3-4B-Base | native | 0.093 | 0.146 | 0.129 | 0.423 | 0.364 | 0.230 | 0.473 | 0.607 | 0.002 |
| Qwen3-8B-Base | neutral | 0.078 | 0.122 | 0.116 | 0.524 | 0.144 | 0.895 | 0.589 | 0.329 | 0.944 |
| Qwen3-8B-Base | native | 0.079 | 0.124 | 0.120 | 0.436 | 0.112 | 0.904 | 0.476 | 0.240 | 0.192 |
| Qwen3-14B-Base | neutral | 0.071 | 0.111 | 0.109 | 0.618 | 0.103 | 0.904 | 0.669 | 0.221 | 0.898 |
| Qwen3-14B-Base | native | 0.073 | 0.116 | 0.112 | 0.608 | 0.086 | 0.906 | 0.599 | 0.127 | 0.092 |
| Qwen3-0.6B | neutral | 0.188 | 0.295 | 0.215 | 0.512 | 0.520 | 0.096 | 0.577 | 0.749 | 0.252 |
| Qwen3-0.6B | native | 0.214 | 0.334 | 0.203 | 0.558 | 0.854 | 0.094 | 0.536 | 0.971 | 0.722 |
| Qwen3-1.7B | neutral | 0.197 | 0.306 | 0.147 | 0.546 | 0.858 | 0.094 | 0.570 | 0.973 | 0.989 |
| Qwen3-1.7B | native | 0.256 | 0.395 | 0.137 | 0.557 | 0.903 | 0.096 | 0.570 | 0.998 | 0.765 |
| Qwen3-4B | neutral | 0.136 | 0.210 | 0.125 | 0.599 | 0.337 | 0.390 | 0.629 | 0.571 | 0.936 |
| Qwen3-4B | native | 0.199 | 0.306 | 0.115 | 0.659 | 0.098 | 0.902 | 0.664 | 0.009 | 1.000 |
| Qwen3-8B | neutral | 0.121 | 0.188 | 0.109 | 0.542 | 0.120 | 0.857 | 0.578 | 0.155 | 0.988 |
| Qwen3-8B | native | 0.156 | 0.243 | 0.105 | 0.574 | 0.101 | 0.898 | 0.624 | 0.018 | 1.000 |
| Qwen3-14B | neutral | 0.096 | 0.150 | 0.104 | 0.594 | 0.274 | 0.627 | 0.592 | 0.379 | 0.728 |
| Qwen3-14B | native | 0.142 | 0.223 | 0.096 | 0.662 | 0.158 | 0.827 | 0.615 | 0.159 | 1.000 |
| Qwen3-32B | neutral | 0.083 | 0.130 | 0.108 | 0.672 | 0.086 | 0.898 | 0.663 | 0.133 | 0.231 |
| Qwen3-32B | native | 0.086 | 0.136 | 0.100 | 0.630 | 0.135 | 0.840 | 0.629 | 0.222 | 1.000 |
| Nemotron-Terminal-8B | neutral | 0.207 | 0.246 | 0.240 | 0.652 | 0.137 | 0.902 | 0.700 | 0.321 | 0.943 |
| Nemotron-Terminal-8B | native | 0.117 | 0.176 | 0.143 | 0.475 | 0.172 | 0.768 | 0.603 | 0.345 | 0.000 |
| Nemotron-Terminal-14B | neutral | 0.177 | 0.206 | 0.211 | 0.667 | 0.195 | 0.689 | 0.712 | 0.359 | 0.902 |
| Nemotron-Terminal-14B | native | 0.122 | 0.185 | 0.127 | 0.482 | 0.090 | 0.906 | 0.441 | 0.034 | 0.000 |
| Nemotron-Terminal-32B | neutral | 0.099 | 0.148 | 0.137 | 0.679 | 0.088 | 0.902 | 0.721 | 0.132 | 0.785 |
| Nemotron-Terminal-32B | native | 0.090 | 0.143 | 0.106 | 0.542 | 0.545 | 0.207 | 0.521 | 0.751 | 0.000 |

### Paired comparisons (Δ = second − first; 95% bootstrap CI over trajectories / items)

| comparison | fmt | Δ obs BPB | Δ novel obs BPB | Δ obs BPB @T* | Δ pred novel BPB | Δ AUROC(new) |
|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base → Qwen3-0.6B | neutral | +0.055 [+0.050,+0.061] | +0.088 [+0.080,+0.097] | +0.048 [+0.043,+0.053] | +0.095 [+0.085,+0.105] | -0.135 [-0.263,-0.001] |
| Qwen3-0.6B-Base → Qwen3-0.6B | native | +0.059 [+0.054,+0.065] | +0.089 [+0.080,+0.098] | +0.052 [+0.047,+0.057] | +0.108 [+0.098,+0.118] | +0.002 [-0.131,+0.121] |
| Qwen3-1.7B-Base → Qwen3-1.7B | neutral | +0.086 [+0.080,+0.093] | +0.138 [+0.128,+0.148] | +0.044 [+0.039,+0.049] | +0.146 [+0.134,+0.158] | -0.133 [-0.242,-0.021] |
| Qwen3-1.7B-Base → Qwen3-1.7B | native | +0.104 [+0.096,+0.111] | +0.166 [+0.155,+0.177] | +0.046 [+0.042,+0.052] | +0.228 [+0.208,+0.247] | +0.092 [-0.033,+0.220] |
| Qwen3-4B-Base → Qwen3-4B | neutral | +0.055 [+0.050,+0.059] | +0.084 [+0.077,+0.091] | +0.031 [+0.028,+0.035] | +0.078 [+0.071,+0.087] | +0.028 [-0.073,+0.130] |
| Qwen3-4B-Base → Qwen3-4B | native | +0.080 [+0.075,+0.086] | +0.124 [+0.115,+0.133] | +0.038 [+0.034,+0.042] | +0.160 [+0.145,+0.175] | +0.237 [+0.108,+0.363] |
| Qwen3-8B-Base → Qwen3-8B | neutral | +0.046 [+0.043,+0.050] | +0.073 [+0.068,+0.079] | +0.024 [+0.022,+0.028] | +0.066 [+0.060,+0.072] | +0.018 [-0.060,+0.096] |
| Qwen3-8B-Base → Qwen3-8B | native | +0.063 [+0.058,+0.068] | +0.101 [+0.094,+0.110] | +0.028 [+0.025,+0.031] | +0.119 [+0.109,+0.130] | +0.138 [+0.001,+0.271] |
| Qwen3-14B-Base → Qwen3-14B | neutral | +0.029 [+0.026,+0.032] | +0.046 [+0.042,+0.050] | +0.016 [+0.014,+0.019] | +0.039 [+0.034,+0.043] | -0.024 [-0.102,+0.058] |
| Qwen3-14B-Base → Qwen3-14B | native | +0.036 [+0.033,+0.039] | +0.058 [+0.054,+0.063] | +0.019 [+0.016,+0.022] | +0.107 [+0.098,+0.117] | +0.054 [-0.054,+0.154] |
| Qwen3-8B → Nemotron-Terminal-8B | neutral | +0.114 [+0.102,+0.128] | +0.060 [+0.046,+0.073] | +0.115 [+0.105,+0.126] | +0.058 [+0.047,+0.069] | +0.110 [+0.026,+0.186] |
| Qwen3-8B → Nemotron-Terminal-8B | native | +0.056 [+0.047,+0.065] | +0.004 [-0.006,+0.015] | +0.077 [+0.069,+0.084] | -0.067 [-0.074,-0.059] | -0.098 [-0.217,+0.018] |
| Qwen3-14B → Nemotron-Terminal-14B | neutral | +0.123 [+0.111,+0.133] | +0.068 [+0.059,+0.078] | +0.117 [+0.108,+0.127] | +0.057 [+0.049,+0.064] | +0.072 [-0.001,+0.141] |
| Qwen3-14B → Nemotron-Terminal-14B | native | +0.182 [+0.165,+0.198] | +0.097 [+0.085,+0.108] | +0.168 [+0.154,+0.181] | -0.037 [-0.045,-0.029] | -0.181 [-0.284,-0.075] |
| Qwen3-32B → Nemotron-Terminal-32B | neutral | +0.026 [+0.021,+0.031] | +0.019 [+0.012,+0.025] | +0.025 [+0.020,+0.029] | +0.019 [+0.015,+0.023] | +0.007 [-0.093,+0.113] |
| Qwen3-32B → Nemotron-Terminal-32B | native | +0.030 [+0.025,+0.036] | +0.024 [+0.017,+0.030] | +0.029 [+0.024,+0.034] | +0.007 [+0.003,+0.010] | -0.088 [-0.190,+0.021] |
| Qwen3-8B-Base → Nemotron-Terminal-8B | neutral | +0.160 [+0.148,+0.174] | +0.133 [+0.121,+0.147] | +0.139 [+0.128,+0.149] | +0.124 [+0.113,+0.133] | +0.128 [+0.030,+0.234] |
| Qwen3-8B-Base → Nemotron-Terminal-8B | native | +0.119 [+0.110,+0.128] | +0.105 [+0.097,+0.115] | +0.105 [+0.097,+0.113] | +0.052 [+0.046,+0.058] | +0.039 [-0.083,+0.158] |
| Qwen3-14B-Base → Nemotron-Terminal-14B | neutral | +0.152 [+0.140,+0.164] | +0.114 [+0.105,+0.123] | +0.133 [+0.123,+0.144] | +0.095 [+0.089,+0.102] | +0.049 [-0.019,+0.118] |
| Qwen3-14B-Base → Nemotron-Terminal-14B | native | +0.218 [+0.202,+0.235] | +0.155 [+0.143,+0.167] | +0.187 [+0.173,+0.203] | +0.070 [+0.065,+0.076] | -0.126 [-0.237,-0.012] |

GPU time (scoring only): 2.65 h over 14 models


# Appendix B: copy test tables (results/copytest.md)

#### Copy test, context = bare: bits per character on repeated occurrences (mean over strings)

| model | hex/8 | hex/16 | hex/32 | hex/64 | base64/8 | base64/16 | base64/32 | base64/64 | words/8 | words/16 | words/32 | words/64 | digits/8 | digits/16 | digits/32 | digits/64 | first-tok bits | later-tok bits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 2.318 | 1.079 | 0.537 | 0.277 | 2.130 | 1.156 | 0.585 | 0.295 | 2.453 | 1.281 | 0.677 | 0.337 | 2.430 | 1.094 | 0.486 | 0.247 | 15.60 | 0.277 |
| Qwen3-1.7B-Base | 1.677 | 0.832 | 0.422 | 0.217 | 1.632 | 0.922 | 0.456 | 0.228 | 1.710 | 0.954 | 0.517 | 0.253 | 1.598 | 0.819 | 0.442 | 0.209 | 11.55 | 0.245 |
| Qwen3-4B-Base | 1.026 | 0.594 | 0.317 | 0.162 | 0.997 | 0.705 | 0.408 | 0.217 | 0.881 | 0.498 | 0.336 | 0.195 | 1.048 | 0.561 | 0.295 | 0.150 | 7.64 | 0.224 |
| Qwen3-8B-Base | 0.932 | 0.505 | 0.275 | 0.153 | 1.038 | 0.629 | 0.326 | 0.169 | 0.879 | 0.493 | 0.295 | 0.165 | 1.159 | 0.640 | 0.335 | 0.161 | 7.21 | 0.199 |
| Qwen3-14B-Base | 1.058 | 0.551 | 0.269 | 0.129 | 1.060 | 0.559 | 0.267 | 0.118 | 0.658 | 0.370 | 0.233 | 0.147 | 1.033 | 0.518 | 0.258 | 0.124 | 6.13 | 0.175 |
| Qwen3-0.6B | 1.689 | 0.841 | 0.415 | 0.214 | 1.741 | 0.927 | 0.492 | 0.241 | 1.694 | 0.992 | 0.552 | 0.266 | 1.280 | 0.611 | 0.273 | 0.136 | 12.06 | 0.162 |
| Qwen3-1.7B | 1.820 | 0.881 | 0.454 | 0.231 | 1.973 | 1.022 | 0.519 | 0.263 | 2.577 | 1.355 | 0.679 | 0.347 | 1.430 | 0.658 | 0.317 | 0.164 | 14.13 | 0.180 |
| Qwen3-4B | 0.669 | 0.347 | 0.171 | 0.099 | 0.798 | 0.538 | 0.345 | 0.247 | 1.465 | 0.730 | 0.357 | 0.195 | 0.404 | 0.205 | 0.116 | 0.073 | 6.77 | 0.080 |
| Qwen3-8B | 0.955 | 0.522 | 0.277 | 0.144 | 1.856 | 0.754 | 0.321 | 0.204 | 2.363 | 1.180 | 0.491 | 0.171 | 0.637 | 0.393 | 0.227 | 0.130 | 9.83 | 0.142 |
| Qwen3-14B | 1.415 | 0.796 | 0.394 | 0.182 | 1.485 | 0.539 | 0.213 | 0.093 | 1.751 | 0.854 | 0.362 | 0.170 | 0.920 | 0.447 | 0.226 | 0.137 | 9.48 | 0.054 |
| Qwen3-32B | 1.301 | 0.489 | 0.213 | 0.100 | 1.967 | 0.623 | 0.224 | 0.108 | 2.759 | 1.452 | 0.702 | 0.299 | 0.408 | 0.251 | 0.123 | 0.062 | 10.06 | 0.080 |
| Nemotron-Terminal-8B | 1.162 | 0.639 | 0.342 | 0.197 | 1.446 | 0.679 | 0.324 | 0.194 | 2.002 | 1.027 | 0.481 | 0.190 | 0.959 | 0.526 | 0.298 | 0.161 | 9.93 | 0.121 |
| Nemotron-Terminal-14B | 1.644 | 0.872 | 0.452 | 0.219 | 1.513 | 0.667 | 0.287 | 0.136 | 1.933 | 0.966 | 0.403 | 0.174 | 1.104 | 0.470 | 0.241 | 0.122 | 10.18 | 0.098 |
| Nemotron-Terminal-32B | 1.301 | 0.591 | 0.272 | 0.137 | 1.740 | 0.664 | 0.278 | 0.142 | 2.632 | 1.382 | 0.675 | 0.302 | 0.553 | 0.279 | 0.143 | 0.071 | 10.59 | 0.070 |

#### Copy test, context = term/neutral: bits per character on repeated occurrences (mean over strings)

| model | hex/8 | hex/16 | hex/32 | hex/64 | base64/8 | base64/16 | base64/32 | base64/64 | words/8 | words/16 | words/32 | words/64 | digits/8 | digits/16 | digits/32 | digits/64 | first-tok bits | later-tok bits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 0.001 | 0.001 | 0.000 | 0.001 | 0.002 | 0.001 | 0.001 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.002 | 0.003 | 0.001 | 0.00 | 0.002 |
| Qwen3-1.7B-Base | 0.006 | 0.001 | 0.000 | 0.000 | 0.002 | 0.001 | 0.001 | 0.000 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.000 | 0.001 | 0.01 | 0.001 |
| Qwen3-4B-Base | 0.001 | 0.008 | 0.007 | 0.002 | 0.002 | 0.001 | 0.000 | 0.000 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.002 | 0.001 | 0.001 | 0.01 | 0.002 |
| Qwen3-8B-Base | 0.001 | 0.007 | 0.004 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.001 | 0.002 | 0.001 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.01 | 0.002 |
| Qwen3-14B-Base | 0.005 | 0.001 | 0.000 | 0.000 | 0.004 | 0.002 | 0.001 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.001 | 0.001 | 0.000 | 0.000 | 0.01 | 0.002 |
| Qwen3-0.6B | 0.193 | 0.131 | 0.050 | 0.025 | 0.064 | 0.067 | 0.033 | 0.013 | 0.075 | 0.018 | 0.009 | 0.008 | 0.000 | 0.001 | 0.002 | 0.000 | 0.72 | 0.002 |
| Qwen3-1.7B | 0.031 | 0.006 | 0.019 | 0.018 | 0.001 | 0.000 | 0.015 | 0.006 | 0.000 | 0.000 | 0.001 | 0.001 | 0.000 | 0.002 | 0.010 | 0.018 | 0.00 | 0.010 |
| Qwen3-4B | 0.002 | 0.126 | 0.075 | 0.061 | 0.000 | 0.002 | 0.002 | 0.000 | 0.001 | 0.000 | 0.001 | 0.000 | 0.007 | 0.021 | 0.022 | 0.008 | 0.00 | 0.025 |
| Qwen3-8B | 0.000 | 0.008 | 0.004 | 0.004 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 | 0.00 | 0.002 |
| Qwen3-14B | 0.000 | 0.010 | 0.010 | 0.002 | 0.017 | 0.001 | 0.001 | 0.005 | 0.000 | 0.000 | 0.000 | 0.000 | 0.002 | 0.002 | 0.002 | 0.001 | 0.00 | 0.004 |
| Qwen3-32B | 0.004 | 0.001 | 0.003 | 0.000 | 0.003 | 0.000 | 0.000 | 0.000 | 0.001 | 0.001 | 0.000 | 0.001 | 0.000 | 0.002 | 0.000 | 0.000 | 0.00 | 0.002 |
| Nemotron-Terminal-8B | 0.008 | 0.046 | 0.020 | 0.013 | 0.006 | 0.008 | 0.004 | 0.002 | 0.005 | 0.002 | 0.002 | 0.001 | 0.000 | 0.003 | 0.003 | 0.004 | 0.04 | 0.008 |
| Nemotron-Terminal-14B | 0.002 | 0.070 | 0.025 | 0.016 | 0.001 | 0.005 | 0.002 | 0.003 | 0.001 | 0.001 | 0.003 | 0.001 | 0.000 | 0.001 | 0.001 | 0.005 | 0.01 | 0.011 |
| Nemotron-Terminal-32B | 0.000 | 0.010 | 0.007 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.001 | 0.002 | 0.001 | 0.001 | 0.000 | 0.000 | 0.001 | 0.003 | 0.00 | 0.003 |

#### Copy test, context = term/native: bits per character on repeated occurrences (mean over strings)

| model | hex/8 | hex/16 | hex/32 | hex/64 | base64/8 | base64/16 | base64/32 | base64/64 | words/8 | words/16 | words/32 | words/64 | digits/8 | digits/16 | digits/32 | digits/64 | first-tok bits | later-tok bits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 0.002 | 0.001 | 0.001 | 0.001 | 0.003 | 0.002 | 0.001 | 0.003 | 0.001 | 0.001 | 0.001 | 0.002 | 0.002 | 0.002 | 0.003 | 0.001 | 0.01 | 0.002 |
| Qwen3-1.7B-Base | 0.001 | 0.001 | 0.000 | 0.000 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.002 | 0.001 | 0.000 | 0.000 | 0.01 | 0.001 |
| Qwen3-4B-Base | 0.003 | 0.010 | 0.008 | 0.002 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.002 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.000 | 0.01 | 0.003 |
| Qwen3-8B-Base | 0.002 | 0.007 | 0.004 | 0.002 | 0.003 | 0.002 | 0.001 | 0.001 | 0.002 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.000 | 0.01 | 0.002 |
| Qwen3-14B-Base | 0.008 | 0.002 | 0.001 | 0.000 | 0.006 | 0.002 | 0.002 | 0.001 | 0.002 | 0.002 | 0.001 | 0.001 | 0.001 | 0.001 | 0.002 | 0.000 | 0.01 | 0.003 |
| Qwen3-0.6B | 0.126 | 0.112 | 0.051 | 0.021 | 0.041 | 0.057 | 0.030 | 0.011 | 0.043 | 0.013 | 0.007 | 0.009 | 0.000 | 0.001 | 0.002 | 0.000 | 0.59 | 0.002 |
| Qwen3-1.7B | 0.022 | 0.009 | 0.020 | 0.013 | 0.001 | 0.004 | 0.014 | 0.005 | 0.000 | 0.006 | 0.001 | 0.000 | 0.000 | 0.002 | 0.007 | 0.013 | 0.00 | 0.010 |
| Qwen3-4B | 0.011 | 0.121 | 0.065 | 0.055 | 0.000 | 0.003 | 0.003 | 0.000 | 0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.015 | 0.007 | 0.006 | 0.00 | 0.022 |
| Qwen3-8B | 0.011 | 0.012 | 0.004 | 0.003 | 0.000 | 0.006 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 | 0.00 | 0.003 |
| Qwen3-14B | 0.003 | 0.005 | 0.007 | 0.002 | 0.007 | 0.000 | 0.000 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.003 | 0.000 | 0.00 | 0.002 |
| Qwen3-32B | 0.000 | 0.001 | 0.002 | 0.000 | 0.006 | 0.001 | 0.002 | 0.001 | 0.002 | 0.001 | 0.001 | 0.001 | 0.000 | 0.003 | 0.000 | 0.001 | 0.00 | 0.002 |
| Nemotron-Terminal-8B | 0.008 | 0.051 | 0.021 | 0.015 | 0.008 | 0.010 | 0.005 | 0.003 | 0.006 | 0.003 | 0.003 | 0.002 | 0.001 | 0.003 | 0.005 | 0.005 | 0.05 | 0.009 |
| Nemotron-Terminal-14B | 0.003 | 0.044 | 0.019 | 0.012 | 0.002 | 0.005 | 0.001 | 0.001 | 0.002 | 0.002 | 0.003 | 0.002 | 0.000 | 0.001 | 0.002 | 0.005 | 0.02 | 0.008 |
| Nemotron-Terminal-32B | 0.000 | 0.012 | 0.003 | 0.003 | 0.001 | 0.001 | 0.000 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.000 | 0.000 | 0.000 | 0.004 | 0.00 | 0.003 |

#### Copy test, context = traj/neutral: bits per character on repeated occurrences (mean over strings)

| model | hex/8 | hex/16 | hex/32 | hex/64 | base64/8 | base64/16 | base64/32 | base64/64 | words/8 | words/16 | words/32 | words/64 | digits/8 | digits/16 | digits/32 | digits/64 | first-tok bits | later-tok bits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 0.015 | 0.008 | 0.003 | 0.001 | 0.007 | 0.004 | 0.002 | 0.001 | 0.003 | 0.002 | 0.001 | 0.001 | 0.007 | 0.004 | 0.002 | 0.002 | 0.04 | 0.002 |
| Qwen3-1.7B-Base | 0.005 | 0.003 | 0.001 | 0.001 | 0.006 | 0.003 | 0.001 | 0.001 | 0.002 | 0.002 | 0.001 | 0.001 | 0.006 | 0.008 | 0.003 | 0.002 | 0.02 | 0.002 |
| Qwen3-4B-Base | 0.002 | 0.008 | 0.002 | 0.002 | 0.011 | 0.005 | 0.001 | 0.001 | 0.002 | 0.001 | 0.001 | 0.001 | 0.003 | 0.001 | 0.001 | 0.001 | 0.02 | 0.003 |
| Qwen3-8B-Base | 0.002 | 0.005 | 0.003 | 0.002 | 0.007 | 0.003 | 0.001 | 0.000 | 0.001 | 0.001 | 0.001 | 0.000 | 0.002 | 0.001 | 0.001 | 0.000 | 0.01 | 0.002 |
| Qwen3-14B-Base | 0.008 | 0.007 | 0.003 | 0.002 | 0.009 | 0.006 | 0.003 | 0.003 | 0.002 | 0.001 | 0.001 | 0.001 | 0.012 | 0.007 | 0.004 | 0.003 | 0.06 | 0.002 |
| Qwen3-0.6B | 0.017 | 0.009 | 0.005 | 0.000 | 0.002 | 0.001 | 0.000 | 0.000 | 0.002 | 0.023 | 0.003 | 0.001 | 0.000 | 0.013 | 0.003 | 0.001 | 0.03 | 0.009 |
| Qwen3-1.7B | 0.019 | 0.027 | 0.005 | 0.007 | 0.021 | 0.031 | 0.000 | 0.003 | 0.001 | 0.001 | 0.001 | 0.003 | 0.000 | 0.008 | 0.005 | 0.003 | 0.01 | 0.011 |
| Qwen3-4B | 0.015 | 0.088 | 0.029 | 0.015 | 0.002 | 0.011 | 0.019 | 0.008 | 0.001 | 0.008 | 0.002 | 0.000 | 0.028 | 0.028 | 0.012 | 0.010 | 0.00 | 0.022 |
| Qwen3-8B | 0.007 | 0.023 | 0.006 | 0.011 | 0.002 | 0.007 | 0.006 | 0.002 | 0.002 | 0.001 | 0.003 | 0.000 | 0.026 | 0.033 | 0.007 | 0.002 | 0.00 | 0.011 |
| Qwen3-14B | 0.004 | 0.013 | 0.020 | 0.010 | 0.000 | 0.000 | 0.003 | 0.008 | 0.000 | 0.000 | 0.001 | 0.000 | 0.016 | 0.018 | 0.003 | 0.006 | 0.00 | 0.008 |
| Qwen3-32B | 0.001 | 0.007 | 0.001 | 0.000 | 0.001 | 0.001 | 0.000 | 0.001 | 0.000 | 0.000 | 0.001 | 0.000 | 0.002 | 0.002 | 0.003 | 0.001 | 0.01 | 0.002 |
| Nemotron-Terminal-8B | 1.377 | 1.176 | 0.729 | 0.473 | 1.523 | 1.181 | 0.927 | 0.522 | 0.763 | 0.440 | 0.245 | 0.172 | 0.799 | 0.691 | 0.537 | 0.360 | 0.26 | 1.240 |
| Nemotron-Terminal-14B | 2.055 | 1.580 | 1.063 | 0.605 | 2.794 | 1.815 | 1.166 | 0.720 | 1.674 | 1.235 | 0.594 | 0.289 | 1.766 | 1.401 | 0.915 | 0.510 | 5.46 | 1.611 |
| Nemotron-Terminal-32B | 0.588 | 0.315 | 0.247 | 0.162 | 0.978 | 0.415 | 0.227 | 0.148 | 0.883 | 0.502 | 0.233 | 0.119 | 0.458 | 0.257 | 0.151 | 0.104 | 3.78 | 0.258 |

#### Copy test, context = traj/native: bits per character on repeated occurrences (mean over strings)

| model | hex/8 | hex/16 | hex/32 | hex/64 | base64/8 | base64/16 | base64/32 | base64/64 | words/8 | words/16 | words/32 | words/64 | digits/8 | digits/16 | digits/32 | digits/64 | first-tok bits | later-tok bits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Base | 0.012 | 0.006 | 0.002 | 0.001 | 0.005 | 0.002 | 0.001 | 0.001 | 0.003 | 0.002 | 0.001 | 0.001 | 0.004 | 0.002 | 0.001 | 0.001 | 0.03 | 0.002 |
| Qwen3-1.7B-Base | 0.007 | 0.004 | 0.002 | 0.001 | 0.008 | 0.004 | 0.002 | 0.001 | 0.002 | 0.002 | 0.001 | 0.001 | 0.008 | 0.008 | 0.002 | 0.002 | 0.03 | 0.003 |
| Qwen3-4B-Base | 0.003 | 0.007 | 0.002 | 0.002 | 0.007 | 0.004 | 0.001 | 0.001 | 0.002 | 0.001 | 0.002 | 0.001 | 0.006 | 0.001 | 0.001 | 0.001 | 0.02 | 0.003 |
| Qwen3-8B-Base | 0.003 | 0.006 | 0.003 | 0.002 | 0.008 | 0.003 | 0.002 | 0.001 | 0.002 | 0.002 | 0.002 | 0.001 | 0.005 | 0.002 | 0.002 | 0.001 | 0.02 | 0.003 |
| Qwen3-14B-Base | 0.012 | 0.009 | 0.003 | 0.003 | 0.013 | 0.008 | 0.004 | 0.002 | 0.003 | 0.002 | 0.002 | 0.001 | 0.017 | 0.008 | 0.005 | 0.004 | 0.08 | 0.003 |
| Qwen3-0.6B | 0.019 | 0.006 | 0.007 | 0.000 | 0.002 | 0.001 | 0.001 | 0.000 | 0.003 | 0.012 | 0.002 | 0.001 | 0.001 | 0.010 | 0.004 | 0.001 | 0.04 | 0.005 |
| Qwen3-1.7B | 0.010 | 0.022 | 0.010 | 0.011 | 0.009 | 0.027 | 0.000 | 0.001 | 0.000 | 0.002 | 0.000 | 0.001 | 0.000 | 0.009 | 0.002 | 0.005 | 0.01 | 0.009 |
| Qwen3-4B | 0.018 | 0.049 | 0.031 | 0.020 | 0.014 | 0.010 | 0.022 | 0.002 | 0.000 | 0.003 | 0.001 | 0.000 | 0.025 | 0.033 | 0.007 | 0.012 | 0.00 | 0.020 |
| Qwen3-8B | 0.009 | 0.027 | 0.007 | 0.008 | 0.001 | 0.004 | 0.003 | 0.002 | 0.004 | 0.000 | 0.000 | 0.001 | 0.007 | 0.017 | 0.003 | 0.000 | 0.00 | 0.008 |
| Qwen3-14B | 0.004 | 0.011 | 0.016 | 0.013 | 0.000 | 0.000 | 0.002 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 | 0.027 | 0.030 | 0.007 | 0.004 | 0.00 | 0.009 |
| Qwen3-32B | 0.001 | 0.006 | 0.001 | 0.001 | 0.003 | 0.003 | 0.002 | 0.001 | 0.001 | 0.001 | 0.002 | 0.001 | 0.002 | 0.002 | 0.007 | 0.002 | 0.01 | 0.003 |
| Nemotron-Terminal-8B | 1.222 | 1.041 | 0.636 | 0.392 | 1.468 | 0.974 | 0.728 | 0.483 | 0.858 | 0.444 | 0.253 | 0.180 | 0.736 | 0.628 | 0.492 | 0.323 | 0.33 | 1.185 |
| Nemotron-Terminal-14B | 2.458 | 2.023 | 1.237 | 0.704 | 3.621 | 2.464 | 1.573 | 0.920 | 2.174 | 1.545 | 0.801 | 0.396 | 2.176 | 1.765 | 1.102 | 0.617 | 7.10 | 2.084 |
| Nemotron-Terminal-32B | 0.769 | 0.444 | 0.294 | 0.201 | 1.191 | 0.604 | 0.330 | 0.183 | 1.165 | 0.627 | 0.308 | 0.160 | 0.660 | 0.353 | 0.193 | 0.119 | 5.29 | 0.314 |

#### Nemotron − Qwen3 instruct, Δ bits/char (paired over strings, 95% bootstrap CI), pooled over lengths per alphabet

| size | context | hex | base64 | words | digits | all |
|---|---|---|---|---|---|---|
| 8B | bare | +0.111 [+0.097,+0.124] | -0.123 [-0.164,-0.087] | -0.126 [-0.146,-0.108] | +0.139 [+0.131,+0.148] | +0.000 [-0.013,+0.012] |
| 8B | term/neutral | +0.018 [+0.010,+0.026] | +0.005 [+0.003,+0.007] | +0.003 [+0.002,+0.004] | +0.002 [+0.001,+0.003] | +0.007 [+0.005,+0.009] |
| 8B | term/native | +0.016 [+0.006,+0.027] | +0.005 [+0.002,+0.008] | +0.003 [+0.002,+0.005] | +0.003 [+0.002,+0.004] | +0.007 [+0.004,+0.010] |
| 8B | traj/neutral | +0.930 [+0.823,+1.048] | +1.037 [+0.898,+1.182] | +0.405 [+0.320,+0.501] | +0.581 [+0.523,+0.647] | +0.737 [+0.684,+0.790] |
| 8B | traj/native | +0.813 [+0.715,+0.914] | +0.915 [+0.797,+1.060] | +0.434 [+0.349,+0.524] | +0.539 [+0.487,+0.594] | +0.674 [+0.630,+0.722] |
| 14B | bare | +0.100 [+0.090,+0.110] | +0.068 [+0.055,+0.082] | +0.085 [+0.073,+0.097] | +0.052 [+0.044,+0.060] | +0.076 [+0.071,+0.082] |
| 14B | term/neutral | +0.023 [+0.013,+0.032] | -0.003 [-0.013,+0.003] | +0.001 [+0.001,+0.002] | +0.000 [-0.002,+0.002] | +0.005 [+0.002,+0.008] |
| 14B | term/native | +0.015 [+0.009,+0.022] | +0.000 [-0.002,+0.002] | +0.002 [+0.002,+0.003] | +0.001 [-0.000,+0.003] | +0.005 [+0.003,+0.006] |
| 14B | traj/neutral | +1.319 [+1.139,+1.500] | +1.628 [+1.412,+1.883] | +0.952 [+0.809,+1.101] | +1.141 [+1.003,+1.293] | +1.259 [+1.168,+1.358] |
| 14B | traj/native | +1.600 [+1.409,+1.798] | +2.152 [+1.880,+2.420] | +1.235 [+1.062,+1.424] | +1.403 [+1.256,+1.564] | +1.596 [+1.496,+1.708] |
| 32B | bare | +0.049 [+0.039,+0.061] | -0.024 [-0.043,-0.007] | -0.055 [-0.070,-0.041] | +0.051 [+0.045,+0.056] | +0.005 [-0.001,+0.011] |
| 32B | term/neutral | +0.002 [-0.001,+0.006] | -0.000 [-0.001,+0.001] | +0.000 [+0.000,+0.001] | +0.000 [-0.001,+0.001] | +0.001 [-0.000,+0.002] |
| 32B | term/native | +0.004 [+0.001,+0.007] | -0.002 [-0.005,+0.000] | -0.000 [-0.001,+0.001] | +0.000 [-0.002,+0.002] | +0.000 [-0.001,+0.002] |
| 32B | traj/neutral | +0.328 [+0.271,+0.397] | +0.445 [+0.358,+0.552] | +0.436 [+0.356,+0.514] | +0.242 [+0.201,+0.288] | +0.363 [+0.328,+0.405] |
| 32B | traj/native | +0.427 [+0.358,+0.508] | +0.579 [+0.471,+0.691] | +0.567 [+0.478,+0.668] | +0.330 [+0.275,+0.391] | +0.476 [+0.431,+0.522] |
