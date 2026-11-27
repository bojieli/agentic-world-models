# Companion X thread

## Post 1 · Attach figures/training-stages.png

Pretraining builds the world model. Agent training doesn't. On our tool-output test, no post-trained Qwen3 model beat its own pretrained base at any size where we had both. Chat tuning cost 3–7 points. The best agent recovered enough to tie.

## Post 2 · Attach figures/pair.png

Which command printed EVILO 5? We ran the same script with “olive” and “garden.” Both outputs looked plausible. Only one assignment was right. Across 3,600 such pairs, matching the outputs to their histories let us test what the model expected the shell to do.

## Post 3 · Attach figures/recalibration.png

OpenAI tracked capabilities with base-model perplexity. Wenhao Chai’s AgenticPPL predicted agent rank by scoring commands. Tool replies are a different test. Raw scores favored Nemotron-8B on terminal content. Adjust for confidence and the chat model won on the very same text.

## Post 4 · Attach figures/scale.png

A 4B pretrained model matched 75.7% of output pairs, about level with 14B chat at 75.3%. On real software-engineering runs, even the 14B base predicted tool replies better than 32B chat. The base sandbox gains got smaller above 4B.

## Post 5 · Attach figures/gains.png

Five of ten agent checkpoints gained about one size doubling over chat in plain text. The closest to beating base was Nemotron-14B. It beat 14B chat by 3.4 points, but tied 14B base (+0.3 points, 95% CI [−1.1, +1.9]). Qwen released no 32B base.

## Post 6 · Attach figures/chat.png

The 14B tie came from plain transcripts only. We tested three specialists in chat. At 8B, chat scored 69.8% on the same pairs, ahead of Nemotron at 64.6% and TMax at 63.5%. Nemotron-32B tied chat. Nemotron-14B wasn’t in that check.

## Post 7 · Text only

How much does the command tell the model? On real replies acknowledging file edits, showing the right command instead of a substitute cut loss by 34% for the 14B base and 18% for SERA-14B. The agent got about half as much help from the command on those replies.

## Post 8 · Attach figures/roles.png

Nemotron-8B put more probability on the recorded agent’s thoughts and commands and less on the terminal’s replies. TMax told a similar story in action. Reinforcement learning took TB-Lite from 11.5 to 17.7 while its sandbox accuracy moved by −0.4 points, within noise.

## Post 9 · Text only

In Qwen3, pretraining built the tool-output world model. Agent training taught the model to act on it. Task success rose 2–8×. The best agent tied its base on output matching. Try the paired test in another family. Code and data at https://github.com/bojieli/agentic-world-models
