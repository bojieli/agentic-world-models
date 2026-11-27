# Data and model licenses

Bojie Li releases the study code, original writing and generated sandbox pairs under the [MIT License](LICENSE). Derived measurements retain the terms of the source data. We distribute scores and identifiers from recorded trajectories. Obtain the trajectories and model weights from their publishers.

## Datasets

| Source and credit | Revision used | Terms and use |
|---|---|---|
| [wchai/AgenticPPL](https://huggingface.co/datasets/wchai/AgenticPPL/tree/7768b574e0efdced30de307f540aa5d9c39c0ac1) | `7768b57` | Apache-2.0. Wenhao Chai’s released trajectories, command picks and span definitions. |
| [Lego-X/Terminal-Lego-Traj-8k](https://huggingface.co/datasets/Lego-X/Terminal-Lego-Traj-8k/tree/02279e0) | `02279e0` | Apache-2.0. LegoX Team, source within AgenticPPL. Third-party task material retains its terms. |
| [few-sh/terminal-wrench](https://huggingface.co/datasets/few-sh/terminal-wrench/tree/6ab64c4) | `6ab64c4` | Apache-2.0. Terminal Wrench authors, successful baseline runs within AgenticPPL. |
| [nebius/SWE-rebench-leaderboard-trajectories](https://huggingface.co/datasets/nebius/SWE-rebench-leaderboard-trajectories/tree/ed7fa38) | `ed7fa38` | CC-BY-4.0. Nebius, spring 2026 leaderboard subset used for scoring. |
| [nebius/SWE-rebench-openhands-trajectories](https://huggingface.co/datasets/nebius/SWE-rebench-openhands-trajectories/tree/3545538) | `3545538` | CC-BY-4.0. Nebius, secondary build. |
| [nebius/SWE-rebench](https://huggingface.co/datasets/nebius/SWE-rebench/tree/89cdfba) | `89cdfba` | CC-BY-4.0. Nebius, date and instance metadata for the secondary build. |
| [SWE-bench/SWE-smith-trajectories](https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories/tree/08e109b) | `08e109b` | MIT. SWE-smith authors, secondary build. |

For the SWE derivatives we selected runs, normalized messages, labeled tool outputs and computed likelihood summaries. The data card documents the sampling and transformations. [SWE build](swe/data/build.py) · [SWE data card](swe/data/README.md) · [terminal data card](terminal/data/README.md)

Wenhao Chai’s AgenticPPL reference implementation is Apache-2.0. The upstream pick sets were built with Recursive Intelligence’s Flint (Apache-2.0). The upstream terminal task scores are credited to Terminal-Bench and Artificial Analysis. [Reference implementation](https://github.com/wenhaochai/AgenticPPL/tree/bb189cc7a592da9f93bae61e5eb3a6e8d5ada1c0) · [Flint](https://huggingface.co/RecursiveSI/flint)

## Evaluated checkpoints

The links identify the publishers and their terms. The table covers the union of all study panels. The SWE trajectory teachers are credited in the data card. They supplied recorded actions through the dataset and their weights are outside this release.

| Publisher and checkpoint | Weight license |
|---|---|
| [Snowflake/Arctic-AWM-8B](https://huggingface.co/Snowflake/Arctic-AWM-8B) | Apache-2.0 |
| [OpenHands/CodeScout-14B](https://huggingface.co/OpenHands/CodeScout-14B) | Apache-2.0 |
| [microsoft/FrogMini-14B-2510](https://huggingface.co/microsoft/FrogMini-14B-2510) | MIT |
| [Kwai-Klear/Klear-Reasoner-8B-SFT](https://huggingface.co/Kwai-Klear/Klear-Reasoner-8B-SFT) | Apache-2.0 |
| [qihoo360/Light-IF-14B](https://huggingface.co/qihoo360/Light-IF-14B) | Apache-2.0 |
| [qihoo360/Light-IF-8B](https://huggingface.co/qihoo360/Light-IF-8B) | Apache-2.0 |
| [nvidia/Nemotron-Terminal-14B](https://huggingface.co/nvidia/Nemotron-Terminal-14B) | NVIDIA Open Model License |
| [nvidia/Nemotron-Terminal-32B](https://huggingface.co/nvidia/Nemotron-Terminal-32B) | NVIDIA Open Model License |
| [nvidia/Nemotron-Terminal-8B](https://huggingface.co/nvidia/Nemotron-Terminal-8B) | NVIDIA Open Model License |
| [open-thoughts/OpenThinker-Agent-v1-SFT](https://huggingface.co/open-thoughts/OpenThinker-Agent-v1-SFT) | Apache-2.0 |
| [open-thoughts/OpenThinkerAgent-32B](https://huggingface.co/open-thoughts/OpenThinkerAgent-32B) | Apache-2.0 |
| [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) | Apache-2.0 |
| [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | Apache-2.0 |
| [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B) | Apache-2.0 |
| [Qwen/Qwen3-1.7B-Base](https://huggingface.co/Qwen/Qwen3-1.7B-Base) | Apache-2.0 |
| [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | Apache-2.0 |
| [Qwen/Qwen3-14B-Base](https://huggingface.co/Qwen/Qwen3-14B-Base) | Apache-2.0 |
| [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) | Apache-2.0 |
| [Qwen/Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) | Apache-2.0 |
| [Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | Apache-2.0 |
| [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Apache-2.0 |
| [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | Apache-2.0 |
| [allenai/SERA-14B](https://huggingface.co/allenai/SERA-14B) | Apache-2.0 |
| [allenai/SERA-8B](https://huggingface.co/allenai/SERA-8B) | Apache-2.0 |
| [Qwen/WebWorld-8B](https://huggingface.co/Qwen/WebWorld-8B) | Apache-2.0 |
| [allenai/tmax-8b](https://huggingface.co/allenai/tmax-8b) | Apache-2.0 |
| [allenai/tmax-sft-8b](https://huggingface.co/allenai/tmax-sft-8b) | Apache-2.0 |
