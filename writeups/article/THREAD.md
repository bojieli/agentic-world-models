# Companion X thread

## Post 1 · Attach figures/training-stages.png

Pretraining builds the world model of tool outputs. Agentic post-training doesn't.

We tested 14 public agent and fine-tuned models built on Qwen3. None predicted what a command would print better than the pretrained Qwen3 model of the same size, where one exists. 🧵

## Post 2 · Attach figures/dissociation.png

The teams behind these agents report benchmark scores 1.6 to 8 times higher than their starting models.

Their ability to predict what a tool will print improved by at most about what doubling the model's size gives, and never beyond the pretrained model.

## Post 3 · Attach figures/pair.png

How we tested it: 3,600 pairs of commands, each actually run.

Same program, two inputs: "olive" prints EVILO 5, "garden" prints NEDRAG 6. Can the model match each output to the command that produced it? Random guessing scores 50%.

## Post 4 · Attach figures/scale.png

Model size is what improves it. The pretrained 4B Qwen3 model matched 75.7% of pairs, about the same as Qwen's 14B chat model (75.3%).

On real coding sessions, the pretrained 14B model predicted tool output better than the 32B chat model.

## Post 5 · Attach figures/margin.png

Agent training recovered part of what chat training lost: 5 of 10 agents gained about as much as doubling model size.

But all 5 preferred the correct answer by a smaller margin than before. They picked the right answer more often, with less certainty.

## Post 6 · Attach figures/chat.png

Then we changed only the format: same files, same commands, asked as a chat question.

5 agents beat Qwen's chat model on raw shell transcripts. In chat format, 4 scored below it and 1 tied. Nemotron-Terminal-14B went from +3.4 to −10.3 points.

## Post 7 · Attach figures/recalibration.png

Why raw perplexity misleads here: chat and agent models are overconfident.

On raw probabilities, Nemotron-Terminal-8B predicted terminal replies better than Qwen's chat model. After setting each model's temperature, the chat model did better.

## Post 8 · Attach figures/roles.png

What supervised agent training does teach: the agent's part of the session. Nemotron-Terminal gave more probability to the agent's reasoning and commands, less to the terminal's replies.

Agents trained mainly with reinforcement learning don't show this.

## Post 9 · Text only

Limits: one model family (Qwen3); in one Qwen3.5 pair, chat training cost nothing; we didn't finish testing a model trained to predict tool output.

Try it on your model. Does it beat its pretrained version in both formats?

Code + data: https://github.com/bojieli/agentic-world-models
