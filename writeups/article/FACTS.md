# Measurements behind the article

All models are Qwen3-family, with aligned tokenization on the scored material. "Base" = pretrained only; "instruct" = Qwen's chat-tuned release; agentic checkpoints are public fine-tunes from other labs. Qwen never released a 32B base.

## The question
Agents call tools (shell, tests, files). Does training a model to be an agent make it better at predicting what its tools will say back, i.e. a better "world model" of its environment? Or does it just learn to act?

Inspiration: Wenhao Chai's "AgenticPPL" post (https://wenhaochai.com/blogs/agentic-ppl.html), which found that perplexity on *terminal output* anti-correlates with Terminal-Bench (rho −0.37), and built a perplexity metric on command tokens that predicts agent rank (rho +0.79 on held-out models).

## Experiment 1: a "physics test" for tool use (the sandbox) — the headline experiment
- 3,600 primary pairs in freshly generated mini-environments (random files, scripts, data). Commands were actually executed in an isolated container. Freshly sampled environments reduce exact-item memorization.
- Each item is a counterfactual pair: two commands (or two prior states) that differ minimally and produce different real outputs. Question for the model: which output goes with which command? ("binding accuracy"; coin flip = 50%.) Copied tokens excluded.
- Scale ladder (Qwen3 instruct, plain transcripts): 0.6B 60.4% → 1.7B 64.6% → 4B 68.7% → 8B 71.7% → 14B 75.3% → 32B 79.3%. Every step significant. Roughly +3–4 points per doubling of size above 4B.
- Base models (pretrained only): 0.6B 63.6, 1.7B 68.6, 4B 75.7, 8B 77.1, 14B 78.4. Base beats instruct at every matched size. 4B base (75.7) ≈ 14B instruct (75.3).
- Agentic and control fine-tunes (gain in points vs their instruct start [95% CI]; vs same-size base):
  - Nemotron-Terminal-8B (NVIDIA, agentic SFT): +3.1 [+1.5,+4.8]; vs base −2.4 (below)
  - tmax-sft-8b (AI2, agentic SFT): +3.6 [+2.0,+5.1]; vs base −1.8 (below)
  - tmax-8b (AI2, RL on top of tmax-sft): +3.2; RL step alone ≈ 0 (−0.4 [−1.5,+0.7]); vs base −2.2
  - SERA-8B (agentic SFT): +1.4 (n.s.); vs base −4.1
  - Arctic-AWM-8B (agentic RL): −0.2 (flat); vs base −5.7
  - Nemotron-Terminal-14B: +3.4 [+1.8,+4.8]; vs 14B base +0.3 (tie, n.s.)
  - CodeScout-14B (OpenHands, agentic RL; paper says tool outputs masked from loss): −0.2 (flat); vs base −3.3
  - FrogMini-14B (agentic SFT): +0.6 (n.s.); vs base −2.5
  - Nemotron-Terminal-32B: +2.9 [+1.6,+4.4] (≈ less than one 14→32B doubling); no 32B base exists
  - OpenThinkerAgent-32B (agentic SFT): −0.5 (flat)
  - Light-IF-8B / 14B (NON-agentic instruction-following fine-tune): +1.5 / +1.7
  - Klear-8B (non-agentic reasoning distillation, from base): −3.5 vs instruct, −8.9 vs base
  - WebWorld-8B (Qwen, trained to predict web-page states): −0.1
- Summary: 5 of 10 agentic models gain, and their gains are ≈ one doubling of model size (+2.9 to +3.6). The other 5 are flat. A non-agentic fine-tune gets about half the gain. RL adds nothing. No fine-tune clearly beats an available same-size pretrained base (best case: tie).
- In chat format (same items, wrapped in chat template): instruct 69.8%, Nemotron-8B 64.6%, tmax-sft 63.5% — the agentic models are 5–6 points WORSE than the chat model. Nemotron-32B is level (−0.8, n.s.). (These were the only specialists scored in chat.)
- Nemotron-8B's gain is mostly on easier items: +5.3 points on ordinary pairs vs +0.8 on the hardest ones.

## Experiment 2: real software-engineering trajectories (SWE-rebench, tasks from spring 2026, after the original Qwen3 release)
- 150 real agent runs from 5 frontier models; measure how well each model predicts the real tool outputs (recalibrated, content tokens only).
- Scale: every size step helps (instruct 1.82 → 1.02 bits/token from 0.6B to 32B). 14B base beats 32B instruct.
- Size-equivalent multiplier of agentic fine-tuning vs its instruct start ("how much bigger a plain model would need to be"):
  tmax-sft 1.31× (best on M1; the 1.52× upper bound is for M2), tmax (after RL) 1.04×, Arctic-AWM 1.01×, Nemotron-8B 0.99×, Nemotron-14B 0.82×, Nemotron-32B 0.81×, CodeScout 0.84×, OpenThinker-Agent-8B 0.56×, SERA-8B/14B below 0.5×, OpenThinkerAgent-32B below 0.5×.
- None reaches 2×. 7 of 11 are significantly WORSE than the model they started from. RL step alone: 0.79×.
- Non-agentic Light-IF-8B (1.08×) and the web world model WebWorld-8B (1.26×) land in the same range as the agents.
- Where agentic models gain, it is on reading-type outputs (file views, search); they get worse on execution outcomes (test runs, script output): e.g. Nemotron-32B 0.58× on test runs; Nemotron-8B saves 0.049 bits on file views but loses 0.055 on test runs.
- Swapping the command for a different one barely changes how well models predict the output — on real SWE logs, output is mostly determined by history, not the command.

## Experiment 3: terminal trajectories (the AgenticPPL dataset)
- Only ~35% of the "surprise" in terminal output is real content; the rest is random strings (31%: hashes, timestamps), harness boilerplate (21%), and copy/echo (11%).
- Nemotron-Terminal (trained with a closely related terminal format) shifts probability toward its own role: on identical histories it gives the teacher's thoughts +0.77 and commands +0.26 bits/token more probability, and the terminal output −0.36 bits/token less. It learned to write like the agent, not to anticipate the terminal.
- After calibration, Nemotron predicts terminal output worse than its starting model at 8B/14B/32B (≈0.6–0.8× size-equivalent).
- Weird side effect: Nemotron can't copy a random hostname inside long agent transcripts (8B: 1.18 bits/char vs 0.02 for its parent) but copies fine in short terminal snippets.
- The article's explanation ("strong agents predict their own next step at output positions") is small: ≤0.3% probability per token on role tokens.

## Experiment 4: what AgenticPPL actually tracks
- We reimplemented it (matches the authors' package within 0.001 on the 0.6B validation run).
- Across 20 checkpoints it correlates with how *confident* models are at command tokens (Spearman −0.77), not with tool-output prediction (≈0 at 8B).
- Base → instruct raises it by +0.10 while uncapped loss on the same command tokens gets *worse* (1.81 → 3.22 bits per selected span). RL (tmax-sft → tmax) lowers it while TB-Lite score rises 11.5 → 17.7.
- Nemotron is the one agentic model with a real (not just confidence) gain — and it was trained in the same Terminus-2 format the metric uses.
- AgenticPPL may still be a useful cheap rank predictor; our point is about *what* it measures.

## Benchmark context (from each model's own paper; harnesses differ, don't compare across papers)
- Nemotron-Terminal Terminal-Bench 2.0: 2.5→13.0 (8B), 4.0→20.2 (14B), 3.4→27.4 (32B) vs their Qwen3 starts. tmax TB-Lite 7.3 (Qwen3-8B) → 11.5 (SFT) → 17.7 (RL).
- So agentic training multiplies benchmark success 2–8×, while tool-output prediction moves ~0–1 doubling of size, and never past the pretrained base.

## Scope
- One model family (Qwen3), ~14 public fine-tunes; synthetic sandbox is shell/Python; SWE set is 150 runs.
- We don't know for most models whether tool outputs were excluded from the training loss (CodeScout states it was).
- The sandbox gain only shows in plain transcripts, and the chat-format test covered 3 models.
- An independent review (GPT-6.2-astra, given raw data only) reached the same overall picture and found the chat-format reversal.

See [the analysis notes](NOTES.md) and [recalibration and scale results](../REVIEW.md).

## Recalibration and pretraining scale
 (our data)
- Base models are calibrated (best temperature 1.0); Qwen3 instruct models are overconfident (best temperature 1.2–1.8 on terminal output). Temperature scaling closes only about half the base–instruct gap.
- Base beats instruct on terminal-output perplexity at every size; the gap shrinks with scale (+0.055 bits/byte at 0.6B, +0.029 at 14B).
- Only ~35% of terminal-output bits are real content (31% random strings, 21% harness boilerplate, 11% copying).
- The same model can look better or worse depending on calibration: Nemotron-Terminal looks 1.09–1.72× "bigger" than its start on raw terminal-output perplexity at 8B/14B, but 0.63–0.74× after per-model temperature recalibration (worse than its start).
- AgenticPPL: base→instruct at 8B raises the score (−0.929 → −0.827) while uncapped loss on the same command tokens worsens (1.81 → 3.22 bits); across 20 checkpoints it tracks command-token confidence (Spearman −0.77).
- Takeaway: perplexity is a proper score of prediction for a model trained on log-loss (a base model); after post-training it mostly reports calibration and role, so recalibration and a rank test help (like the sandbox binding test) interpret measured tool-output prediction.

### Base-model (pretraining) scale evidence
- Terminal output bits/byte, base: 0.170 (0.6B) → 0.142 → 0.123 → 0.115 → 0.108 (14B), every step significant.
- SWE recalibrated content bits/token, base: 1.517 (0.6B) → 1.284 → 1.116 → 1.056 → 0.987 (14B), every step passes; 14B base (0.987) beats 32B instruct (1.016).
- Sandbox binding, base: 63.6 → 68.6 → 75.7 → 77.1 → 78.4 (0.6B→14B); large gains to 4B, smaller and not individually significant above 4B (+1.4, +1.3 points). Instruct ladder rises every step to 32B (79.3).
- 4B base (75.7) ≈ 14B instruct (75.3) on the sandbox.
