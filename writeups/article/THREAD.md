# Companion X thread

## Post 1 · Attach figures/training-stages.png

Pretraining builds the world model of tool outputs. Agentic post-training doesn't.

No post-trained Qwen3 model we tested beat its own pretrained base at predicting what a command will output. The best agent tied. 🧵

## Post 2 · Attach figures/dissociation.png

Agent training multiplied benchmark scores 1.6–8× within each team's own harness.

Tool-output prediction? About one doubling of model size at most, and never past the base.

Agents got much better at doing. Not at predicting what comes back.

## Post 3 · Attach figures/pair.png

How we tested it: 3,600 command pairs, all actually executed.

Same script, two inputs: "olive" → EVILO 5, "garden" → NEDRAG 6. Both look plausible. Can the model match each output to the command that produced it? Coin flip = 50%.

## Post 4 · Attach figures/scale.png

Scale is what moves it. A 4B base matched 75.7% of pairs, level with 14B chat (75.3%).

On real SWE runs, the 14B base predicted tool replies better than 32B chat.

In Qwen3, chat tuning cost 3–7 points at every size.

## Post 5 · Attach figures/gains.png

Agent fine-tunes won some back: 5 of 10 gained about one size doubling over chat.

But on margin, how firmly the right pairing beats the wrong one, all 5 got worse. Nemotron-8B: 0.540 → 0.407 bits/byte.

More pairs right, by thinner margins.

## Post 6 · Attach figures/chat.png

Then we changed only the wrapper. Same files, same commands, same answers, asked in chat.

5 agents beat their chat model in plain text. In chat, 4 fell behind it and the 5th tied. Nemotron-14B: +3.4 → −10.3 points.

A non-agentic fine-tune flipped too.

## Post 7 · Attach figures/recalibration.png

Why perplexity misleads here: post-trained models are overconfident.

Raw scores favored Nemotron-8B on terminal output. Fit each model's temperature and the chat model won on the same text.

AgenticPPL mostly tracks command confidence (ρ −0.77).

## Post 8 · Attach figures/roles.png

What agent SFT does learn: the agent's side. Nemotron (8B/14B/32B) and SERA put more probability on the agent's thoughts and commands, less on the terminal's replies.

RL agents don't. RL took TMax's TB-Lite 11.5 → 17.7. Its forecasts didn't move.

## Post 9 · Text only

Caveats: one family (Qwen3); in one Qwen3.5 pair chat tuning cost nothing; we didn't score a model trained to predict tool output.

Test yours: can it beat its own base, in plain text and in chat?

Code + data: https://github.com/bojieli/agentic-world-models
