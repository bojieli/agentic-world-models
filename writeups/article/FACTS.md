# Verified facts for the article (use only these numbers)

All models are Qwen3-family, same tokenizer. "Base" = pretrained only; "instruct" = Qwen's chat-tuned release; agentic checkpoints are public fine-tunes from other labs. Qwen never released a 32B base.

## The question
Agents call tools (shell, tests, files). Does training a model to be an agent make it better at predicting what its tools will say back, i.e. a better "world model" of its environment? Or does it just learn to act?

Inspiration: Wenhao Chai's "AgenticPPL" post (https://wenhaochai.com/blogs/agentic-ppl.html), which found that perplexity on *terminal output* anti-correlates with Terminal-Bench (rho −0.37), and built a perplexity metric on command tokens that predicts agent rank (rho +0.79 on held-out models).

## Experiment 1: a "physics test" for tool use (the sandbox) — the headline experiment
- 3,600 freshly generated mini-environments (random files, scripts, data). Commands were actually executed in an isolated container. Nothing could be memorized.
- Each item is a counterfactual pair: two commands (or two prior states) that differ minimally and produce different real outputs. Question for the model: which output goes with which command? ("binding accuracy"; coin flip = 50%.) Copied tokens excluded.
- Scale ladder (Qwen3 instruct, plain transcripts): 0.6B 60.4% → 1.7B 64.6% → 4B 68.7% → 8B 71.7% → 14B 75.3% → 32B 79.3%. Every step significant. Roughly +3–4 points per doubling of size above 4B.
- Base models (pretrained only): 0.6B 63.6, 1.7B 68.6, 4B 75.7, 8B 77.1, 14B 78.4. Base beats instruct at every size. 4B base (75.7) ≈ 14B instruct (75.3).
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
- Summary: 5 of 10 agentic models gain, and their gains are ≈ one doubling of model size (+2.9 to +3.6). The other 5 are flat. A non-agentic fine-tune gets about half the gain. RL adds nothing. No fine-tune beats its own pretrained base (best case: tie).
- In chat format (same items, wrapped in chat template): instruct 69.8%, Nemotron-8B 64.6%, tmax-sft 63.5% — the agentic models are 5–6 points WORSE than the chat model. Nemotron-32B is level (−0.8, n.s.). (Only these were scored in chat.)
- Nemotron-8B's gain is mostly on easier items: +5.3 points on ordinary pairs vs +0.8 on the hardest ones.

## Experiment 2: real software-engineering trajectories (SWE-rebench, tasks from spring 2026, after the models' training)
- 150 real agent runs from 5 frontier models; measure how well each model predicts the real tool outputs (recalibrated, content tokens only).
- Scale: every size step helps (instruct 1.82 → 1.02 bits/token from 0.6B to 32B). 14B base beats 32B instruct.
- Size-equivalent multiplier of agentic fine-tuning vs its instruct start ("how much bigger a plain model would need to be"):
  tmax-sft 1.31× (best; upper bound 1.52×), tmax (after RL) 1.04×, Arctic-AWM 1.01×, Nemotron-8B 0.99×, Nemotron-14B 0.82×, Nemotron-32B 0.81×, CodeScout 0.84×, OpenThinker-Agent-8B 0.56×, SERA-8B/14B below 0.5×, OpenThinkerAgent-32B below 0.5×.
- None reaches 2×. 7 of 11 are significantly WORSE than the model they started from. RL step alone: 0.79×.
- Non-agentic Light-IF-8B (1.08×) and the web world model WebWorld-8B (1.26×) land in the same range as the agents.
- Where agentic models gain, it is on reading-type outputs (file views, search); they get worse on execution outcomes (test runs, script output): e.g. Nemotron-32B 0.58× on test runs; Nemotron-8B saves 0.049 bits on file views but loses 0.055 on test runs.
- Swapping the command for a different one barely changes how well models predict the output — on real SWE logs, output is mostly determined by history, not the command.

## Experiment 3: terminal trajectories (the AgenticPPL dataset)
- Only ~35% of the "surprise" in terminal output is real content; the rest is random strings (31%: hashes, timestamps), harness boilerplate (21%), and copy/echo (11%).
- Nemotron-Terminal (trained in this exact format) shifts probability toward its own role: on identical histories it gives the teacher's thoughts +0.77 and commands +0.26 bits/token more probability, and the terminal output −0.36 bits/token less. It learned to write like the agent, not to anticipate the terminal.
- After calibration, Nemotron predicts terminal output worse than its starting model at 8B/14B/32B (≈0.6–0.8× size-equivalent).
- Weird side effect: Nemotron can't copy a random hostname inside long agent transcripts (8B: 1.18 bits/char vs 0.02 for its parent) but copies fine in short terminal snippets.
- The article's explanation ("strong agents predict their own next step at output positions") is small: ≤0.3% probability per token on role tokens.

## Experiment 4: what AgenticPPL actually tracks
- We reimplemented it (matches the authors' package within 0.001).
- Across 20 checkpoints it correlates with how *confident* models are at command tokens (Spearman −0.77), not with tool-output prediction (≈0 at 8B).
- Base → instruct raises it by +0.10 while uncapped loss on the same command tokens gets *worse* (1.81 → 3.22 bits). RL (tmax-sft → tmax) lowers it while TB-Lite score rises 11.5 → 17.7.
- Nemotron is the one agentic model with a real (not just confidence) gain — and it was trained in the same Terminus-2 format the metric uses.
- Fair framing: AgenticPPL may still be a useful cheap rank predictor; our point is about *what* it measures. Be respectful to the author.

## Benchmark context (from each model's own paper; harnesses differ, don't compare across papers)
- Nemotron-Terminal Terminal-Bench 2.0: 2.5→13.0 (8B), 4.0→20.2 (14B), 3.4→27.4 (32B) vs their Qwen3 starts. tmax TB-Lite 7.3 (Qwen3-8B) → 11.5 (SFT) → 17.7 (RL).
- So agentic training multiplies benchmark success 2–8×, while tool-output prediction moves ~0–1 doubling of size, and never past the pretrained base.

## Honest caveats (mention briefly, not a wall)
- One model family (Qwen3), ~14 public fine-tunes; synthetic sandbox is shell/Python; SWE set is 150 runs.
- We don't know for most models whether tool outputs were excluded from the training loss (CodeScout states it was).
- The sandbox gain only shows in plain transcripts, and the chat-format test covered 3 models.
- An independent review (GPT-6.2-astra, given raw data only) reached the same overall picture and found the chat-format reversal.
- Researchers: invite replication; code/data link placeholder: [LINK]

## ADDENDUM for revision (verified)

### OpenAI, "Perplexity and Intelligence" (Jakub Pachocki, OpenAI chief scientist, Nov 22, 2026)
Primary: https://openai.com/index/perplexity-and-intelligence/ (as cited by The Decoder) and Pachocki's X post https://x.com/merettm/status/2124549218995949967. Coverage: https://the-decoder.com/openai-warns-that-upcoming-ai-systems-could-outpace-safety-checks-and-urges-rivals-to-agree-on-shared-limits/ , https://cellcog.ai/blog/openai-perplexity-and-intelligence/
- Discloses BASE-MODEL log-perplexity on OpenAI's own held-out eval set (reported as drawn from its internal codebase) for every major GPT: GPT-3.5 0.986, GPT-4 0.913, GPT-6.2 Astra 0.761, internal model ~0.732 (lower is better).
- Claims capabilities map "surprisingly closely to specific perplexity scores": ~0.99 fluent conversation; ~0.91 productive chain-of-thought; ~0.76 breakthrough math results; expects further capabilities around 0.68–0.70.
- Stated limitation (per The Decoder): gains outside pretraining, such as chain-of-thought, "don't lower perplexity".
- Proposes perplexity as a shared cross-lab metric and "common limits" on development.
- Only secondary coverage was read; quote cautiously and link the primary URL.

### Why raw perplexity misreads post-trained models (our data)
- Base models are calibrated (best temperature 1.0); Qwen3 instruct models are overconfident (best temperature 1.2–1.8 on terminal output). Temperature scaling closes only about half the base–instruct gap.
- Base beats instruct on terminal-output perplexity at every size; the gap shrinks with scale (+0.055 bits/byte at 0.6B, +0.029 at 14B).
- Only ~35% of terminal-output bits are real content (31% random strings, 21% harness boilerplate, 11% copying).
- The same model can look better or worse depending on calibration: Nemotron-Terminal looks 1.09–1.72× "bigger" than its start on raw terminal-output perplexity at 8B/14B, but 0.63–0.74× after per-model temperature recalibration (worse than its start).
- AgenticPPL: base→instruct at 8B raises the score (−0.929 → −0.827) while uncapped loss on the same command tokens worsens (1.81 → 3.22 bits); across 20 checkpoints it tracks command-token confidence (Spearman −0.77).
- Takeaway: perplexity is a proper score of prediction for a model trained on log-loss (a base model); after post-training it mostly reports calibration and role, so you must recalibrate or use a rank test (like the sandbox binding test) to read world knowledge.

### Base-model (pretraining) scale evidence
- Terminal output bits/byte, base: 0.170 (0.6B) → 0.142 → 0.123 → 0.115 → 0.108 (14B), every step significant.
- SWE recalibrated content bits/token, base: 1.517 (0.6B) → 1.284 → 1.116 → 1.056 → 0.987 (14B), every step passes; 14B base (0.987) beats 32B instruct (1.016).
- Sandbox binding, base: 63.6 → 68.6 → 75.7 → 77.1 → 78.4 (0.6B→14B); large gains to 4B, smaller and not individually significant above 4B (+1.4, +1.3 points). Instruct ladder rises every step to 32B (79.3).
- 4B base (75.7) ≈ 14B instruct (75.3) on the sandbox.

## ADDENDUM 2 (2026-11-28) — late results folded into the article (verified from files on the study host)
Sources: sandbox/results/chat_delta.json; sandbox/results/<model>/plain/per_item.jsonl; p2/RESULTS_ROLES.md; sandbox/RESULTS_EXT.md.
- Margin (sandbox interaction, bits/byte, ratio of sums over primary pool S2+S3+S2h+S3h, plain, T1/nocopy): Qwen3-8B 0.540 → Nemotron-8B 0.407, tmax-sft-8b 0.409, tmax-8b 0.414; Qwen3-14B 0.693 → Nemotron-14B 0.544; Qwen3-32B 0.669 → Nemotron-32B 0.584. All five agents that gained on binding accuracy have a smaller margin than their instruct start. Only CodeScout-14B has a larger margin (+0.040, chat_delta.json).
- Chat-format sweep (paired Δ binding vs instruct start, 2000-draw env-cluster bootstrap): agents with a significant plain gain: Nemotron-8B +0.031→chat −0.052; tmax-sft +0.036→−0.064; tmax-8b +0.032→−0.063; Nemotron-14B +0.034→−0.103; Nemotron-32B +0.029→−0.008 (n.s., tie). Non-agentic Light-IF-14B +0.017→−0.043. Arctic-AWM and CodeScout flat in both formats.
- Role-shift (per-token log-ratio vs instruct start, neutral raw, bits/token): full signature (thought↑ action↑ observation↓) for Nemotron-8B (+0.77/+0.26/−0.36), Nemotron-14B (+0.63/+0.16/−0.38), Nemotron-32B (+0.50/+0.10/−0.08), SERA-8B (+0.11/+0.16/obs −0.09 copy, −0.12 novel). Not RL: tmax-8b thought −0.13; Arctic ≈0; CodeScout all down. OpenThinkerAgent-32B (SFT) thought −0.16 with observations collapsing (−2.22 copy). Non-agentic controls: none shift probability from observations toward thought/action (Light-IF-8B obs novel +0.10; WebWorld-8B +0.14; Klear vs base all down).
- Cross-family, one pair only: Qwen3.5-0.8B base 63.6% vs instruct 63.5% binding (plain) — no chat-tuning cost there.
- Not scored: positive control Qwen-AgentWorld-35B-A3B (anchor Qwen3.5-35B-A3B-Base scored 79.4%); OLMo-2 and Mistral pairs never ran.
- Dissociation figure: within-paper benchmark multipliers 1.58× (tmax-sft), 2.42× (tmax), 5.00× (Nemotron-14B), 5.26× (Nemotron-8B), 8.13× (Nemotron-32B); see figures/DISSOCIATION_NOTES.md.
- Removed from the article: the SWE edit-acknowledgement information-gain figures (34% vs 18%), because that measure failed the pre-registered ladder gate.
