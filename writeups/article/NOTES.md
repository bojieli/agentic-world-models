# Editorial notes

## Three alternative titles

- The world model comes from pretraining, not agent training
- The best tool predictor was already there before chat tuning
- Better agents. Same ceiling on predicting their tools.

## Number ledger

These entries cover the published copy, captions, thread and all seven figures. B denotes billions of parameters. Accuracy is a percentage of matched pairs. A change in that accuracy is in percentage points.

| Result used | Source and interpretation |
|---|---|
| November 22, 2026. Base-model log-perplexity around 0.99, 0.91 and 0.76. | FACTS.md lines 70–76. The three figures and the associated conversation, reasoning and math observations come from Pachocki’s post. The addendum summarizes reporting on Pachocki’s post. The article paraphrases his examples. [OpenAI primary source](https://openai.com/index/perplexity-and-intelligence/) |
| AgenticPPL +0.79 on held-out models. Terminal output −0.37. | FACTS.md line 8. Chai reports the first correlation on held-out models and trajectories. The second comes from the separate analysis by trajectory span. Signs follow Chai’s ranking convention. [AgenticPPL primary source](https://wenhaochai.com/blogs/agentic-ppl.html) |
| One family, Qwen3. Sizes 0.6B, 1.7B, 4B, 8B, 14B and 32B. No 32B base. | FACTS.md lines 3, 13–14 and 62. Same-size base comparisons end at 14B. |
| Base temperature 1.0, instruct 1.2–1.8. Recalibration closes about half the base–instruct terminal gap. | FACTS.md lines 79–80. The temperature minimizing held-out loss measures calibration in these terminal sessions. |
| About 35% content, 31% random strings and 21% harness boilerplate. | FACTS.md lines 44 and 81. Rounded neutral-format shares of output loss specifically for Qwen3-8B-Base. See the rows CONTENT(novel output,non-rand), rand(all 3) and boiler. [Token-class aggregates](../bundle/extra/token_classes/c_final_neutral.out) |
| Instruct raw 1.079, recalibrated 0.829. Nemotron raw 0.906, recalibrated 0.884 bits per content token. | FACTS.md line 82 gives the direction. For the figure, round the two model levels in the native / content / Nemo-8B vs Qwen3-8B rows, raw and T_obs_cal, to three decimal places. Each temperature was fitted on separate trajectories. [Native-format loss table, lines 367 and 379](../bundle/extra/pilot_size_equiv/tables.md) |
| 20 checkpoints, Spearman −0.77 with command-token entropy. At 8B, capped AgenticPPL −0.929 → −0.827, uncapped bits per selected span 1.81 → 3.22. | FACTS.md lines 50–54 and 83. Higher AgenticPPL and lower entropy indicate sharper command predictions. The uncapped unit is mean total loss per selected command range. See picks → obsgain-easy → mean_range_bits_uncapped in the two records. [Base](../bundle/p2/results/m5/Qwen3-8B-Base.json) · [Instruct](../bundle/p2/results/m5/Qwen3-8B.json) |
| Three prediction tests. Base terminal loss 0.170 → 0.108 bits/byte, 0.6B → 14B. Every base size step improves. | FACTS.md lines 79–80 and 86–89. Ordinary terminal transcripts use neutral rendering. The native-format filtered-content comparison above answers a separate question. [Cross-test comparison by size](../REVIEW.md) |
| 150 successful SWE-rebench runs from five models. Base 1.517 → 0.987 bits/content token, 0.6B → 14B. 32B instruct 1.016. | FACTS.md lines 33–35 and 88. The score recalibrates content prediction on task-disjoint data. [Run selection](../bundle/data-swe/README.md) · [SWE size results](../bundle/p2/results/size_equiv/size_equiv_swe.json) |
| 3,600 sandbox pairs, two executed variants per pair, two possible assignments, 50% chance. EVILO 5 / NEDRAG 6. | FACTS.md lines 11–12. For the example, read the last terminal reply from each executed branch of S2-0001, after “python calc.py olive” and “python calc.py garden” respectively. [Executed sandbox items](../bundle/sandbox/items.jsonl.gz) |
| Base plain sandbox curve 63.6, 68.6, 75.7, 77.1, 78.4%. Instruct curve 60.4, 64.6, 68.7, 71.7, 75.3, 79.3%. 4B base ≈ 14B instruct. | FACTS.md lines 13–14 and 89–90, in ascending size order. The individual 4B→8B and 8B→14B base steps both have paired intervals crossing zero. The scale chart includes both complete available ladders. |
| 8B training-stage chart, 77.1 → 71.7 → 75.3 → 74.9%. Nemotron-8B scores 74.8% in plain text. | Computed from the primary pairs in the plain sandbox item files using the calculation below. FACTS.md lines 16–18 give the corresponding differences. The connected stages in the cover chart follow the documented Qwen/TMax sequence. [Checkpoint lineage](../bundle/p2/CONTROLS.md) |
| Five of ten specialist checkpoints gain roughly one instruct-size doubling, five show no clear gain. Best available base comparison, Nemotron-14B +0.3 points. | FACTS.md lines 15–29. The doubling compares scores on the plain sandbox with size-matched instruct. At 32B the largest specialist runs beyond the measured instruct ladder. The 14B interval includes a tie with base. Nemotron comparisons use the size-matched instruct reference, as its exact starting release is undocumented. [Independent comparison](../REVIEW.md) |
| Chat tuning costs about 3–7 points of binding accuracy. | Subtract the instruct percentages from the base percentages at each shared size in FACTS.md lines 13–14. The smallest displayed gap is 3.1 points at 14B, the largest 7.0 at 4B. |
| Strongest result against base, Nemotron-14B. Gain over chat +3.4 points. Gain over base +0.3 points, 95% CI [−1.1, +1.9]. | FACTS.md lines 15 and 21 supply the point comparisons. The stratified paired bootstrap below reproduces the interval in the brief from the underlying items. The independent review’s environment bootstrap also spans zero. [Sandbox item scores](../bundle/sandbox/results/) · [Independent review, section 4](../REVIEW.md) |
| Gains figure, supervised agents vs same-size chat, in points. TMax-8B +3.6, Nemotron-14B +3.4, Nemotron-8B +3.1, Nemotron-32B +2.9, SERA-8B +1.4, FrogMini-14B +0.6, OpenThinkerAgent-32B −0.5. Agents after RL. TMax-8B +3.2, Arctic-AWM-8B −0.2, CodeScout-14B −0.2. | FACTS.md lines 15–25 and 29. Bars show point estimates. The shaded band of roughly 3–4 points reflects the instruct scale curve above 4B in line 13. The TMax RL bar includes the earlier supervised gain. |
| Gains figure, comparison models vs chat. Light-IF-14B +1.7, Light-IF-8B +1.5, WebWorld-8B −0.1, Klear-8B −3.5. Klear vs base −8.9. | FACTS.md lines 26–28. Klear’s documented parent is the pretrained 8B model. |
| Reported benchmark success rose roughly 2–8×. | FACTS.md lines 57–59. These are within-team comparisons. TMax’s TB-Lite ratio is 17.7/7.3 and Nemotron-32B’s Terminal-Bench ratio is 27.4/3.4. Each ratio uses its own benchmark and harness. |
| TMax on SWE, 1.31× after supervised training and 1.04× after RL. TB-Lite 11.5 → 17.7. Sandbox RL increment −0.4 points. | FACTS.md lines 18, 36–38 and 58. The two multipliers give the instruct-model size matching each TMax score, interpolated in log parameter count. The task scores are from the same team’s benchmark. The sandbox RL interval spans zero. |
| Chat check, three agent checkpoints. At 8B, instruct 71.7 → 69.8%, Nemotron 74.8 → 64.6%, TMax SFT 75.3 → 63.5%. At 32B, Nemotron is level with instruct within uncertainty. | FACTS.md lines 30 and 64–65, plus the plain-sandbox calculation below. The three specialists are two 8B models and one 32B model, in addition to the instruct references. |
| Nemotron-8B versus instruct, +0.77 on thoughts, +0.26 on commands, −0.36 on output. | FACTS.md line 45. These are changes in mean log probability in bits per token on the recorded histories. Positive means the recorded tokens became more likely. [Per-role measurements](../bundle/pilot/results/logratio.csv) |

Chart ticks are scale markings. The proposed paired-repository replication uses the same two-branch design as the sandbox, with plain and chat renderings and a hidden-edit control. [Replication design](../REVIEW.md)

### Reproduce the sandbox percentages

Run from the article directory. The recorded binding score gives half credit on ties. The primary strata and mask match the article and the plots.

```python
import json
from pathlib import Path
from statistics import mean

results = Path("../bundle/sandbox/results")
primary = {"S2", "S3", "S2h", "S3h"}

def accuracy(model, render="plain"):
    with (results / model / render / "per_item.jsonl").open() as f:
        scores = [r["T1/nocopy"]["bind"] for r in map(json.loads, f)
                  if r["stratum"] in primary]
    assert len(scores) == 3600
    return 100 * mean(scores)

for model in ("Qwen3-8B-Base", "Qwen3-8B", "tmax-sft-8b", "tmax-8b",
              "Nemotron-Terminal-8B"):
    print(model, round(accuracy(model), 1))
```

### Reproduce the 14B tie

This paired 95% basic bootstrap keeps the benchmark’s four strata equally represented. Within each stratum it resamples the same environments for both models. The original difference is +0.333 points. Reflecting the bootstrap quantiles around that difference yields [−1.139, +1.889] points. The bundle also reports a joint environment bootstrap with slightly different endpoints and the same verdict. [Plain binding results](../bundle/sandbox/results/size_equiv/size_equiv_plain_nocopy_T1.md)

```python
import json
from pathlib import Path

import numpy as np

strata = ("S2", "S3", "S2h", "S3h")
results = Path("../bundle/sandbox/results")

def scores(model):
    with (results / model / "plain/per_item.jsonl").open() as f:
        rows = [r for r in map(json.loads, f) if r["stratum"] in strata]
    assert len({r["env_id"] for r in rows}) == len(rows) == 3600
    return {(r["stratum"], r["id"]): r["T1/nocopy"]["bind"] for r in rows}

base = scores("Qwen3-14B-Base")
agent = scores("Nemotron-Terminal-14B")
assert base.keys() == agent.keys()
rng = np.random.default_rng(0)
draws = np.zeros(2000)
for stratum in strata:
    keys = sorted(key for key in base if key[0] == stratum)
    diffs = np.array([agent[key] - base[key] for key in keys])
    draws += rng.choice(diffs, (len(draws), len(keys))).sum(axis=1)

points = 100 / len(base)
observed = points * sum(agent[key] - base[key] for key in base)
interval = 2 * observed - np.percentile(points * draws, [97.5, 2.5])
print(observed, interval)
```

## Late additions (2026-11-28)

| Published quantity | Provenance |
|---|---|
| Margin shrank for all five agents that gained on binding; Nemotron-8B 0.540 → 0.407 bits/byte | Sandbox interaction, ratio of summed bits to summed bytes over the primary pool, plain rendering, copied words masked. FACTS.md, Addendum 2. |
| Five agents beat chat in plain text; in chat four fell behind and Nemotron-32B tied; Nemotron-14B +3.4 → −10.3 points | Paired binding deltas vs instruct start, environment-cluster bootstrap. FACTS.md, Addendum 2. |
| Light-IF-14B (non-agentic) flipped +1.7 → −4.3 points | Same source. |
| Role shift in Nemotron-8B/14B/32B and SERA-8B; not in RL agents or non-agentic controls | Per-token log-ratio vs instruct start by span type. FACTS.md, Addendum 2. |
| Qwen3.5-0.8B base 63.6% vs instruct 63.5% | Plain binding on the same 3,600 pairs. FACTS.md, Addendum 2. |
| Benchmark multipliers 1.6–8× in the dissociation figure | Within-paper ratios; figures/DISSOCIATION_NOTES.md. |

The SWE edit-acknowledgement information-gain figures (34% vs 18%) were removed from the article: that measure failed the size check set in advance.

