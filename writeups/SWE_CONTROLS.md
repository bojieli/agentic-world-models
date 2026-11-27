# Checkpoint controls and training lineage

The Qwen3 base and instruct ladders put checkpoint differences on a scale measured in the same evaluation. For each specialist, we use the closest documented start and retain a separate comparison with the same-size pretrained release. A missing or ambiguous parent limits causal attribution.

| Checkpoints | Training comparison and interpretation |
|---|---|
| Nemotron-Terminal 8B, 14B, 32B | NVIDIA used supervised training on terminal-agent trajectories. The publication identifies Qwen3 and the sizes. Context length and chat formatting suggest the hybrid instruct releases, but neither identifies the parent conclusively. Instruct is the reported reference. |
| TMax SFT and RL | Ai2 identifies Qwen3-8B as the supervised starting point and tmax-sft-8b as the immediate RL parent. The second contrast isolates the incremental RL step within this lineage. |
| SERA 8B and 14B, OpenThinker-Agent-v1-SFT, OpenThinkerAgent-32B | Supervised agents trained on software engineering or mixed terminal and software engineering traces. The 8B and 14B SERA models share the Qwen3 chat template. |
| CodeScout-14B | OpenHands used agentic reinforcement learning for code localization and explicitly masked environment observations from the loss. Its published localization scores use a different outcome from task resolution. |
| Arctic-AWM-8B | Snowflake trained tool use by reinforcement learning in synthetic MCP environments. The card text supports an 8B starting point, while its base-model metadata names 4B. |
| FrogMini-14B | Microsoft trained an agent on debugging trajectories with a custom template. The fixed SWE rendering produced exceptionally high loss. The measured row remains in the tables and the aggregate SWE specialist count excludes it. |
| Light-IF-8B and 14B | Non-agentic instruction-following SFT and RL from Qwen3 instruct provide a same-size control for post-training. |
| Klear-Reasoner-8B-SFT | Reasoning distillation starts from Qwen3-8B-Base. Its direct base comparison is the training-start comparison. |
| WebWorld-8B | Next-state prediction on web trajectories provides a cross-domain control. The model card identifies Qwen3-8B, while the paper describes a base checkpoint. Both references matter. |

All scored models use compatible tokenization on the material used for the fixed SWE rendering. Model-native chat templates, loss masks and evidence about dataset overlap vary. Published task scores use the original authors’ harnesses. [Checkpoint cards and licenses](../DATA_LICENSES.md) · [Nemotron-Terminal](https://arxiv.org/abs/2602.21193) · [TMax](https://arxiv.org/abs/2606.23321) · [CodeScout](https://arxiv.org/abs/2603.17829)
