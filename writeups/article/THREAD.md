# Companion X thread

## Post 1 · Attach figures/training-stages.png

OpenAI found that base-model perplexity tracks capability. Wenhao Chai found that scoring terminal replies ranked agents backwards. So when does an agent learn to predict its tools? In our 8B tests, the best forecasts came before chat or agent training.

## Post 2 · Text only

Chai’s AgenticPPL scores commands that earlier output helps explain. It predicted held-out agent rank (ρ = +0.79). Across our 20 checkpoints it also tracked command confidence. Reading a filename and using it is a different skill from predicting which files a listing will show.

## Post 3 · Attach figures/recalibration.png

Only ~35% of the 8B base model’s surprise on terminal replies came from content. Even on content alone, raw perplexity favored Nemotron-8B over instruct in native format. Fit each model’s confidence on separate sessions and the verdict flips. Same models, same text.

## Post 4 · Attach figures/pair.png

We changed a command or an earlier file state and executed both versions. Could the model match each output to the history that produced it? On 3,600 pairs, the 4B pretrained model matched 75.7% in plain text, level with 14B instruct at 75.3%.

## Post 5 · Attach figures/scale.png

Base beat same-size instruct on terminal logs, software-engineering runs and the plain sandbox. The base sandbox curve flattened above 4B. On real repository replies, even 14B base beat 32B instruct after recalibration.

## Post 6 · Text only

Five of ten agent checkpoints gained about one size doubling over instruct on the plain sandbox. None clearly beat an available same-size base. TMax’s RL step lifted TB-Lite from 11.5 to 17.7. Its sandbox forecast changed by −0.4 points, within noise.

## Post 7 · Attach figures/chat.png

The 8B specialists led instruct in plain text. Ask for the same answers in chat and instruct wins at 69.8%, ahead of Nemotron at 64.6% and TMax SFT at 63.5%. We checked three agent checkpoints in chat. The third, 32B Nemotron, tied instruct.

## Post 8 · Attach figures/roles.png

On identical terminal histories, Nemotron-8B put more probability on the recorded thoughts and commands than instruct did. It put less on the shell’s replies. Pretraining built a predictor that agent training taught to act. That’s our read of one family, Qwen3.

## Post 9 · Text only

Try it on your agent. Fork a repo, change an earlier edit and run the same test in both copies. Can the agent match each result to its history better than its pretrained base? Try plain text and chat. Then hide the edit. Code and data at [LINK]
