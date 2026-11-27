# Size-equivalent multipliers (swe; inverse piecewise-linear interpolation in log2 non-embedding params; window 1/2x..4x of the start within the ladder; joint trajectory bootstrap, 1000 draws)


## M1 recal content bits/tok [content] (lower is better)

- inst ladder: 0.6B 1.8212, 1.7B 1.5555, 4B 1.3179, 8B 1.2029, 14B 1.0892, 32B 1.0164; monotone=True; GATE=PASS (0.6B->1.7B -0.2657 [-0.2848,-0.2472]; 1.7B->4B -0.2377 [-0.2536,-0.2228]; 4B->8B -0.1149 [-0.1248,-0.1061]; 8B->14B -0.1138 [-0.1207,-0.1065]; 14B->32B -0.0727 [-0.0791,-0.0671])
- base ladder: 0.6B 1.5172, 1.7B 1.2838, 4B 1.1164, 8B 1.0556, 14B 0.9872; monotone=True; GATE=PASS (0.6B->1.7B -0.2334 [-0.2480,-0.2203]; 1.7B->4B -0.1674 [-0.1786,-0.1565]; 4B->8B -0.0608 [-0.0665,-0.0549]; 8B->14B -0.0684 [-0.0735,-0.0631])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0024 [-0.0078,+0.0128] | 0.99x | -0.02 [-0.10,+0.06] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0481 [-0.0550,-0.0417] | 1.31x | +0.39 [+0.34,+0.44] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0062 [-0.0143,+0.0010] | 1.04x | +0.05 [-0.01,+0.11] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1430 [+0.1312,+0.1546] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.1034 [+0.0956,+0.1112] | 0.56x | -0.84 [-0.91,-0.78] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0024 [-0.0036,-0.0012] | 1.01x | +0.02 [+0.01,+0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0140 [-0.0175,-0.0103] | 1.08x | +0.11 [+0.08,+0.14] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0405 [-0.0448,-0.0359] | 1.26x | +0.33 [+0.29,+0.37] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.5017 [+0.4677,+0.5369] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0344 [+0.0254,+0.0433] | 0.82x | -0.28 [-0.35,-0.21] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0316 [+0.0296,+0.0335] | 0.84x | -0.26 [-0.28,-0.24] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1340 [+0.1245,+0.1435] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +1.3101 [+1.1364,+1.5111] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0357 [+0.0309,+0.0409] | 0.82x | -0.29 [-0.33,-0.25] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0175 [+0.0119,+0.0232] | 0.81x | -0.30 [-0.39,-0.21] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.7320 [+0.6576,+0.8075] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1497 [+0.1345,+0.1637] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1364 [+0.1222,+0.1491] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0420 [+0.0391,+0.0446] | 0.79x | -0.34 [-0.38,-0.31] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3040 [+0.2828,+0.3256] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2717 [+0.2566,+0.2863] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2015 [+0.1886,+0.2145] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1473 [+0.1388,+0.1557] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1020 [+0.0927,+0.1101] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [kind=edit_ack] (lower is better)

- inst ladder: 0.6B 0.5051, 1.7B 0.4890, 4B 0.3955, 8B 0.3686, 14B 0.3251, 32B 0.3030; monotone=True; GATE=FAIL (0.6B->1.7B -0.0161 [-0.0350,+0.0026]; 1.7B->4B -0.0935 [-0.1108,-0.0769]; 4B->8B -0.0269 [-0.0374,-0.0169]; 8B->14B -0.0434 [-0.0539,-0.0333]; 14B->32B -0.0222 [-0.0336,-0.0117])
- base ladder: 0.6B 0.4206, 1.7B 0.3566, 4B 0.3118, 8B 0.3066, 14B 0.2829; monotone=True; GATE=FAIL (0.6B->1.7B -0.0640 [-0.0787,-0.0518]; 1.7B->4B -0.0448 [-0.0591,-0.0306]; 4B->8B -0.0051 [-0.0137,+0.0033]; 8B->14B -0.0237 [-0.0329,-0.0143])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0184 [-0.0273,-0.0082] | 1.31x | +0.39 [+0.17,+0.60] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0221 [-0.0282,-0.0150] | 1.39x | +0.47 [+0.31,+0.68] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0496 [+0.0348,+0.0655] | <0.50x | -1.00 [-1.00,-0.98] | 0.97/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.2272 [+0.1809,+0.2835] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0438 [+0.0319,+0.0562] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0023 [-0.0051,-0.0003] | 1.03x | +0.05 [+0.01,+0.12] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0233 [-0.0291,-0.0185] | 1.41x | +0.50 [+0.34,+0.73] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0247 [-0.0315,-0.0183] | 1.44x | +0.53 [+0.37,+0.76] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.1098 [+0.0810,+0.1425] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0046 [-0.0156,+0.0074] | 1.19x | +0.26 [-0.17,+0.83] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0239 [+0.0206,+0.0272] | 0.70x | -0.51 [-0.65,-0.42] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1389 [+0.1087,+0.1689] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +1.8486 [+1.4520,+2.2353] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0266 [+0.0162,+0.0392] | 0.67x | -0.57 [-0.85,-0.34] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0008 [-0.0091,+0.0091] | >1.00x | +0.00 [-0.45,+0.00] | 0.00/0.60 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.6145 [+0.5078,+0.7166] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0435 [+0.0318,+0.0545] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0376 [+0.0237,+0.0530] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0717 [+0.0596,+0.0841] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0845 [+0.0587,+0.1065] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.1324 [+0.1139,+0.1516] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0837 [+0.0700,+0.0976] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0619 [+0.0496,+0.0740] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0422 [+0.0333,+0.0517] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [kind=file_view] (lower is better)

- inst ladder: 0.6B 1.6240, 1.7B 1.4389, 4B 1.2513, 8B 1.1453, 14B 1.0499, 32B 0.9829; monotone=True; GATE=PASS (0.6B->1.7B -0.1851 [-0.2159,-0.1560]; 1.7B->4B -0.1876 [-0.2077,-0.1699]; 4B->8B -0.1060 [-0.1207,-0.0899]; 8B->14B -0.0954 [-0.1051,-0.0864]; 14B->32B -0.0670 [-0.0797,-0.0551])
- base ladder: 0.6B 1.3917, 1.7B 1.2101, 4B 1.0564, 8B 1.0054, 14B 0.9463; monotone=True; GATE=PASS (0.6B->1.7B -0.1816 [-0.1995,-0.1629]; 1.7B->4B -0.1537 [-0.1732,-0.1383]; 4B->8B -0.0510 [-0.0610,-0.0405]; 8B->14B -0.0591 [-0.0689,-0.0506])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0487 [-0.0579,-0.0398] | 1.39x | +0.47 [+0.39,+0.57] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0528 [-0.0628,-0.0456] | 1.43x | +0.51 [+0.44,+0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0200 [-0.0317,-0.0116] | 1.14x | +0.19 [+0.12,+0.31] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1189 [+0.0933,+0.1445] | <0.50x | -1.00 [-1.00,-0.80] | 0.58/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0999 [+0.0825,+0.1203] | 0.54x | -0.88 [-1.00,-0.74] | 0.05/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0013 [-0.0029,+0.0003] | 1.01x | +0.01 [-0.00,+0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0106 [-0.0164,-0.0051] | 1.07x | +0.10 [+0.05,+0.16] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0474 [-0.0553,-0.0386] | 1.38x | +0.46 [+0.38,+0.53] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.4050 [+0.3542,+0.4532] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0106 [-0.0236,+0.0023] | 1.15x | +0.20 [-0.02,+0.43] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0276 [+0.0233,+0.0316] | 0.83x | -0.27 [-0.31,-0.22] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1068 [+0.0876,+0.1256] | <0.50x | -1.00 [-1.00,-0.83] | 0.59/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.7088 [+0.4430,+0.9721] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0387 [+0.0310,+0.0453] | 0.77x | -0.38 [-0.44,-0.31] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0115 [-0.0207,-0.0032] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.3496 [+0.2948,+0.4095] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0911 [+0.0721,+0.1072] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0930 [+0.0717,+0.1120] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0328 [+0.0290,+0.0363] | 0.82x | -0.29 [-0.35,-0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2323 [+0.2014,+0.2623] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2288 [+0.2080,+0.2474] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1949 [+0.1710,+0.2137] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1399 [+0.1226,+0.1557] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1036 [+0.0872,+0.1173] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [kind=python_exec] (lower is better)

- inst ladder: 0.6B 1.5361, 1.7B 1.2993, 4B 1.0669, 8B 0.9575, 14B 0.8608, 32B 0.8014; monotone=True; GATE=PASS (0.6B->1.7B -0.2368 [-0.2718,-0.2013]; 1.7B->4B -0.2324 [-0.2712,-0.1997]; 4B->8B -0.1094 [-0.1316,-0.0878]; 8B->14B -0.0967 [-0.1139,-0.0793]; 14B->32B -0.0594 [-0.0776,-0.0414])
- base ladder: 0.6B 1.2937, 1.7B 1.0346, 4B 0.8885, 8B 0.8357, 14B 0.7754; monotone=True; GATE=PASS (0.6B->1.7B -0.2590 [-0.2967,-0.2294]; 1.7B->4B -0.1461 [-0.1669,-0.1263]; 4B->8B -0.0528 [-0.0652,-0.0403]; 8B->14B -0.0603 [-0.0738,-0.0472])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0403 [+0.0098,+0.0734] | 0.79x | -0.34 [-0.60,-0.09] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0282 [-0.0454,-0.0110] | 1.21x | +0.27 [+0.11,+0.41] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0373 [+0.0202,+0.0556] | 0.80x | -0.32 [-0.50,-0.17] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1422 [+0.0984,+0.1837] | <0.50x | -1.00 [-1.00,-0.88] | 0.86/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.1064 [+0.0878,+0.1232] | 0.53x | -0.91 [-1.00,-0.75] | 0.10/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0057 [-0.0093,-0.0018] | 1.04x | +0.05 [+0.02,+0.08] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0304 [-0.0399,-0.0216] | 1.22x | +0.29 [+0.21,+0.39] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0364 [-0.0521,-0.0222] | 1.27x | +0.35 [+0.23,+0.48] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.3832 [+0.3254,+0.4471] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0672 [+0.0402,+0.0968] | 0.64x | -0.65 [-0.94,-0.38] | 0.01/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0392 [+0.0325,+0.0461] | 0.77x | -0.38 [-0.45,-0.32] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1314 [+0.0945,+0.1677] | <0.50x | -1.00 [-1.00,-0.90] | 0.91/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.4279 [+0.2585,+0.6761] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0174 [+0.0024,+0.0363] | 0.89x | -0.17 [-0.33,-0.02] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0364 [+0.0189,+0.0583] | 0.59x | -0.76 [-1.00,-0.44] | 0.12/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.4513 [+0.3572,+0.5715] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1621 [+0.1286,+0.1991] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1526 [+0.1189,+0.1879] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0655 [+0.0537,+0.0798] | 0.68x | -0.56 [-0.73,-0.44] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2424 [+0.2060,+0.2803] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2647 [+0.2290,+0.3080] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1784 [+0.1529,+0.2083] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1218 [+0.1025,+0.1420] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0854 [+0.0654,+0.1049] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [kind=search] (lower is better)

- inst ladder: 0.6B 2.5861, 1.7B 2.2788, 4B 2.0017, 8B 1.8563, 14B 1.7100, 32B 1.6247; monotone=True; GATE=PASS (0.6B->1.7B -0.3073 [-0.3666,-0.2568]; 1.7B->4B -0.2771 [-0.3278,-0.2392]; 4B->8B -0.1454 [-0.1744,-0.1221]; 8B->14B -0.1462 [-0.1745,-0.1246]; 14B->32B -0.0853 [-0.1126,-0.0581])
- base ladder: 0.6B 2.2714, 1.7B 1.9884, 4B 1.7682, 8B 1.6602, 14B 1.5594; monotone=True; GATE=PASS (0.6B->1.7B -0.2829 [-0.3529,-0.2384]; 1.7B->4B -0.2203 [-0.2548,-0.1933]; 4B->8B -0.1080 [-0.1374,-0.0865]; 8B->14B -0.1009 [-0.1314,-0.0775])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0330 [-0.0729,-0.0025] | 1.16x | +0.21 [+0.02,+0.43] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0852 [-0.1251,-0.0575] | 1.45x | +0.54 [+0.39,+0.73] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0461 [-0.0901,-0.0124] | 1.22x | +0.29 [+0.08,+0.51] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0966 [+0.0633,+0.1253] | 0.65x | -0.62 [-0.88,-0.39] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.1380 [+0.1103,+0.1663] | 0.54x | -0.89 [-1.00,-0.68] | 0.08/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0003 [-0.0054,+0.0055] | 1.00x | -0.00 [-0.03,+0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0139 [-0.0355,+0.0011] | 1.06x | +0.09 [-0.01,+0.22] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0720 [-0.0984,-0.0541] | 1.37x | +0.46 [+0.36,+0.58] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.6273 [+0.5509,+0.7161] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0151 [-0.0162,+0.0391] | 0.94x | -0.10 [-0.26,+0.20] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0460 [+0.0377,+0.0575] | 0.82x | -0.29 [-0.37,-0.23] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1169 [+0.0845,+0.1464] | 0.60x | -0.74 [-0.95,-0.51] | 0.01/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.5726 [+0.2330,+0.8148] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0631 [+0.0457,+0.0835] | 0.76x | -0.40 [-0.53,-0.27] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0135 [-0.0327,+0.0060] | >1.00x | +0.00 [-0.08,+0.00] | 0.00/0.93 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.5953 [+0.3626,+0.7604] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1631 [+0.1247,+0.1938] | <0.50x | -1.00 [-1.00,-0.96] | 0.96/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1658 [+0.1419,+0.1909] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0391 [+0.0260,+0.0507] | 0.84x | -0.25 [-0.36,-0.15] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3147 [+0.2647,+0.3606] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2904 [+0.2533,+0.3440] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2335 [+0.2040,+0.2683] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1960 [+0.1718,+0.2236] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1507 [+0.1282,+0.1759] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [kind=shell_other] (lower is better)

- inst ladder: 0.6B 1.4472, 1.7B 1.1178, 4B 0.8863, 8B 0.7936, 14B 0.7030, 32B 0.6386; monotone=True; GATE=PASS (0.6B->1.7B -0.3294 [-0.3747,-0.2868]; 1.7B->4B -0.2315 [-0.2650,-0.2029]; 4B->8B -0.0927 [-0.1123,-0.0757]; 8B->14B -0.0906 [-0.1063,-0.0768]; 14B->32B -0.0645 [-0.0760,-0.0543])
- base ladder: 0.6B 1.0906, 1.7B 0.8752, 4B 0.7258, 8B 0.6866, 14B 0.6369; monotone=True; GATE=PASS (0.6B->1.7B -0.2154 [-0.2417,-0.1906]; 1.7B->4B -0.1494 [-0.1704,-0.1297]; 4B->8B -0.0392 [-0.0482,-0.0296]; 8B->14B -0.0497 [-0.0603,-0.0402])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0190 [-0.0366,+0.0008] | 1.14x | +0.19 [-0.01,+0.36] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0722 [-0.0856,-0.0596] | 1.67x | +0.74 [+0.63,+0.86] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0454 [-0.0595,-0.0308] | 1.38x | +0.47 [+0.34,+0.59] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0839 [+0.0653,+0.1039] | 0.56x | -0.85 [-0.99,-0.68] | 0.01/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0847 [+0.0729,+0.0980] | 0.55x | -0.85 [-1.00,-0.71] | 0.02/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0035 [-0.0058,-0.0013] | 1.03x | +0.04 [+0.01,+0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0104 [-0.0170,-0.0031] | 1.08x | +0.11 [+0.03,+0.19] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0242 [-0.0343,-0.0128] | 1.19x | +0.25 [+0.13,+0.36] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.4632 [+0.3981,+0.5364] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0064 [-0.0187,+0.0075] | 1.09x | +0.12 [-0.07,+0.37] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0308 [+0.0269,+0.0348] | 0.80x | -0.32 [-0.38,-0.26] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.0798 [+0.0636,+0.0987] | 0.57x | -0.82 [-1.00,-0.63] | 0.05/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1853 [+0.1335,+0.2540] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0234 [+0.0147,+0.0332] | 0.85x | -0.24 [-0.31,-0.17] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0112 [-0.0209,-0.0020] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/0.99 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.4746 [+0.3951,+0.5600] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0881 [+0.0602,+0.1167] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0598 [+0.0300,+0.0880] | <0.50x | -1.00 [-1.00,-0.63] | 0.73/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0267 [+0.0229,+0.0309] | 0.83x | -0.27 [-0.33,-0.22] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3566 [+0.3045,+0.4160] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2427 [+0.2072,+0.2804] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1606 [+0.1303,+0.1894] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1070 [+0.0904,+0.1234] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0661 [+0.0409,+0.0886] | <0.50x | -1.00 [-1.00,-0.84] | 0.90/0.00 |

## M1 recal content bits/tok [kind=test_run] (lower is better)

- inst ladder: 0.6B 2.4603, 1.7B 2.1103, 4B 1.8013, 8B 1.6485, 14B 1.4908, 32B 1.3949; monotone=True; GATE=PASS (0.6B->1.7B -0.3500 [-0.3819,-0.3190]; 1.7B->4B -0.3089 [-0.3393,-0.2825]; 4B->8B -0.1528 [-0.1705,-0.1380]; 8B->14B -0.1577 [-0.1710,-0.1445]; 14B->32B -0.0959 [-0.1068,-0.0858])
- base ladder: 0.6B 2.0650, 1.7B 1.7560, 4B 1.5407, 8B 1.4520, 14B 1.3579; monotone=True; GATE=PASS (0.6B->1.7B -0.3090 [-0.3400,-0.2801]; 1.7B->4B -0.2153 [-0.2372,-0.1946]; 4B->8B -0.0887 [-0.1003,-0.0785]; 8B->14B -0.0940 [-0.1036,-0.0844])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0545 [+0.0365,+0.0757] | 0.79x | -0.33 [-0.44,-0.23] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0355 [-0.0486,-0.0238] | 1.16x | +0.21 [+0.14,+0.28] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0092 [-0.0037,+0.0210] | 0.96x | -0.06 [-0.13,+0.02] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1840 [+0.1643,+0.2068] | <0.50x | -1.00 [-1.00,-1.00] | 0.97/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.1249 [+0.1105,+0.1368] | 0.59x | -0.76 [-0.85,-0.68] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0022 [-0.0049,+0.0004] | 1.01x | +0.01 [-0.00,+0.03] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0118 [-0.0194,-0.0048] | 1.05x | +0.07 [+0.03,+0.11] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0446 [-0.0533,-0.0356] | 1.20x | +0.26 [+0.21,+0.30] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.7042 [+0.6475,+0.7601] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0967 [+0.0777,+0.1199] | 0.67x | -0.57 [-0.69,-0.47] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0322 [+0.0286,+0.0360] | 0.88x | -0.19 [-0.21,-0.17] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1893 [+0.1709,+0.2072] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +2.6697 [+2.2601,+3.0302] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0432 [+0.0345,+0.0516] | 0.84x | -0.25 [-0.31,-0.20] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0613 [+0.0494,+0.0742] | 0.58x | -0.79 [-0.93,-0.67] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +1.3011 [+1.1593,+1.4446] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.2511 [+0.2232,+0.2818] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.2296 [+0.2036,+0.2595] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0447 [+0.0388,+0.0509] | 0.83x | -0.27 [-0.31,-0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3953 [+0.3664,+0.4289] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3543 [+0.3261,+0.3858] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2606 [+0.2385,+0.2850] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1966 [+0.1801,+0.2133] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1329 [+0.1195,+0.1464] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M1 recal content bits/tok [outcome] (lower is better)

- inst ladder: 0.6B 1.6701, 1.7B 1.4821, 4B 1.2878, 8B 1.1975, 14B 1.0970, 32B 1.0399; monotone=True; GATE=PASS (0.6B->1.7B -0.1880 [-0.2114,-0.1654]; 1.7B->4B -0.1943 [-0.2117,-0.1766]; 4B->8B -0.0903 [-0.1013,-0.0801]; 8B->14B -0.1005 [-0.1119,-0.0889]; 14B->32B -0.0572 [-0.0662,-0.0483])
- base ladder: 0.6B 1.4149, 1.7B 1.2474, 4B 1.1249, 8B 1.0750, 14B 1.0145; monotone=True; GATE=PASS (0.6B->1.7B -0.1675 [-0.1816,-0.1527]; 1.7B->4B -0.1225 [-0.1365,-0.1084]; 4B->8B -0.0499 [-0.0584,-0.0423]; 8B->14B -0.0605 [-0.0685,-0.0532])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0185 [+0.0082,+0.0303] | 0.88x | -0.19 [-0.31,-0.09] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0319 [-0.0414,-0.0229] | 1.23x | +0.29 [+0.22,+0.38] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0035 [-0.0130,+0.0055] | 1.02x | +0.03 [-0.06,+0.12] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1907 [+0.1644,+0.2195] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0834 [+0.0736,+0.0931] | 0.55x | -0.86 [-0.97,-0.75] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0008 [-0.0026,+0.0009] | 1.01x | +0.01 [-0.01,+0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0219 [-0.0300,-0.0140] | 1.15x | +0.20 [+0.12,+0.28] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0334 [-0.0415,-0.0253] | 1.24x | +0.31 [+0.24,+0.37] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.3920 [+0.3507,+0.4326] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0389 [+0.0275,+0.0516] | 0.78x | -0.36 [-0.49,-0.26] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0343 [+0.0307,+0.0381] | 0.80x | -0.32 [-0.37,-0.27] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1261 [+0.1130,+0.1398] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +2.2595 [+1.9252,+2.5942] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0268 [+0.0186,+0.0347] | 0.84x | -0.25 [-0.31,-0.18] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0150 [+0.0080,+0.0230] | 0.80x | -0.32 [-0.47,-0.19] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.9533 [+0.8250,+1.0901] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1411 [+0.1279,+0.1556] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1214 [+0.1086,+0.1367] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0284 [+0.0246,+0.0324] | 0.82x | -0.29 [-0.35,-0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2552 [+0.2297,+0.2804] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2346 [+0.2160,+0.2524] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1629 [+0.1485,+0.1772] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1225 [+0.1107,+0.1336] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0825 [+0.0734,+0.0921] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M2 NLL given true action bits/tok @T* [content/all] (lower is better)

- inst ladder: 0.6B 1.8827, 1.7B 1.6734, 4B 1.3477, 8B 1.2152, 14B 1.0703, 32B 0.9748; monotone=True; GATE=PASS (0.6B->1.7B -0.2093 [-0.2365,-0.1821]; 1.7B->4B -0.3256 [-0.3572,-0.2978]; 4B->8B -0.1326 [-0.1506,-0.1149]; 8B->14B -0.1449 [-0.1587,-0.1319]; 14B->32B -0.0955 [-0.1065,-0.0856])
- base ladder: 0.6B 1.5492, 1.7B 1.2764, 4B 1.0958, 8B 1.0290, 14B 0.9456; monotone=True; GATE=PASS (0.6B->1.7B -0.2728 [-0.2958,-0.2503]; 1.7B->4B -0.1806 [-0.1977,-0.1657]; 4B->8B -0.0669 [-0.0774,-0.0565]; 8B->14B -0.0833 [-0.0931,-0.0737])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0123 [-0.0315,+0.0100] | 1.06x | +0.08 [-0.07,+0.20] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0819 [-0.0958,-0.0695] | 1.44x | +0.52 [+0.45,+0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0326 [-0.0462,-0.0191] | 1.16x | +0.21 [+0.12,+0.29] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1038 [+0.0826,+0.1257] | 0.60x | -0.73 [-0.90,-0.58] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0763 [+0.0633,+0.0898] | 0.69x | -0.54 [-0.61,-0.46] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0005 [-0.0014,+0.0025] | 1.00x | -0.00 [-0.02,+0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0560 [-0.0642,-0.0478] | 1.28x | +0.36 [+0.31,+0.41] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0747 [-0.0858,-0.0645] | 1.39x | +0.48 [+0.42,+0.54] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.5767 [+0.5266,+0.6328] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0396 [+0.0238,+0.0560] | 0.84x | -0.25 [-0.36,-0.16] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0728 [+0.0662,+0.0799] | 0.72x | -0.47 [-0.53,-0.42] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1291 [+0.1096,+0.1496] | 0.56x | -0.83 [-0.97,-0.69] | 0.01/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.7785 [+0.6432,+0.9233] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0178 [+0.0106,+0.0254] | 0.92x | -0.11 [-0.16,-0.07] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0312 [+0.0200,+0.0431] | 0.76x | -0.40 [-0.54,-0.26] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.5364 [+0.4650,+0.6150] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1740 [+0.1494,+0.2022] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1643 [+0.1418,+0.1878] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0493 [+0.0444,+0.0544] | 0.79x | -0.35 [-0.42,-0.29] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3335 [+0.3045,+0.3648] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3969 [+0.3645,+0.4312] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2519 [+0.2314,+0.2734] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1862 [+0.1719,+0.2020] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1247 [+0.1112,+0.1383] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=edit_ack] (lower is better)

- inst ladder: 0.6B 0.8273, 1.7B 0.8550, 4B 0.6356, 8B 0.6412, 14B 0.5419, 32B 0.4974; monotone=False; GATE=FAIL (0.6B->1.7B +0.0278 [-0.0400,+0.0985]; 1.7B->4B -0.2194 [-0.3346,-0.1205]; 4B->8B +0.0056 [-0.0502,+0.0720]; 8B->14B -0.0993 [-0.1765,-0.0358]; 14B->32B -0.0445 [-0.1110,-0.0004])
- base ladder: 0.6B 0.7256, 1.7B 0.5981, 4B 0.5256, 8B 0.5170, 14B 0.4606; monotone=True; GATE=FAIL (0.6B->1.7B -0.1275 [-0.1969,-0.0818]; 1.7B->4B -0.0725 [-0.1001,-0.0485]; 4B->8B -0.0086 [-0.0353,+0.0137]; 8B->14B -0.0565 [-0.1177,-0.0111])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0637 [-0.1416,-0.0105] | 1.55x | +0.63 [+0.15,+2.00] | 0.00/0.03 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0406 [-0.0688,-0.0105] | 1.32x | +0.40 [+0.08,+1.12] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0731 [+0.0341,+0.1312] | <0.50x | -1.00 [-1.00,-0.97] | 0.96/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.2616 [+0.1404,+0.4034] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0336 [-0.0036,+0.0671] | <0.50x | -1.00 [-1.00,+0.03] | 0.84/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0043 [-0.0135,+0.0047] | 1.03x | +0.04 [-0.28,+0.15] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0610 [-0.1054,-0.0243] | 1.52x | +0.60 [+0.27,+1.40] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0298 [-0.0752,+0.0004] | 1.23x | +0.29 [-0.05,+1.02] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.1566 [+0.0925,+0.2790] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0115 [-0.0645,+0.0261] | 1.25x | +0.32 [-0.31,+1.24] | 0.00/0.06 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0462 [+0.0294,+0.0717] | 0.73x | -0.46 [-1.00,-0.29] | 0.08/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1525 [+0.0660,+0.2269] | <0.50x | -1.00 [-1.00,-0.65] | 0.91/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.5737 [+0.2603,+0.9554] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.1159 [+0.0422,+0.2230] | <0.50x | -1.00 [-1.00,-0.77] | 0.87/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0076 [-0.0330,+0.0332] | 0.86x | -0.21 [-1.00,+0.00] | 0.07/0.30 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.2808 [+0.1452,+0.4017] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0605 [+0.0254,+0.0967] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0698 [+0.0462,+0.1016] | <0.50x | -1.00 [-1.00,-0.75] | 0.79/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.1137 [+0.0762,+0.1667] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.1016 [+0.0591,+0.1443] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2569 [+0.1474,+0.4030] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1100 [+0.0684,+0.1753] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1242 [+0.0684,+0.2048] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0813 [+0.0374,+0.1492] | <0.50x | -1.00 [-1.00,-0.75] | 0.85/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=file_view] (lower is better)

- inst ladder: 0.6B 1.8616, 1.7B 1.6974, 4B 1.4482, 8B 1.3322, 14B 1.1699, 32B 1.0910; monotone=True; GATE=PASS (0.6B->1.7B -0.1642 [-0.2251,-0.1001]; 1.7B->4B -0.2492 [-0.3091,-0.2003]; 4B->8B -0.1160 [-0.1498,-0.0849]; 8B->14B -0.1623 [-0.1972,-0.1299]; 14B->32B -0.0790 [-0.0973,-0.0590])
- base ladder: 0.6B 1.6055, 1.7B 1.3831, 4B 1.2057, 8B 1.1421, 14B 1.0516; monotone=True; GATE=PASS (0.6B->1.7B -0.2224 [-0.2671,-0.1812]; 1.7B->4B -0.1774 [-0.2227,-0.1397]; 4B->8B -0.0636 [-0.0819,-0.0467]; 8B->14B -0.0905 [-0.1146,-0.0652])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1022 [-0.1290,-0.0780] | 1.50x | +0.58 [+0.48,+0.71] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0974 [-0.1283,-0.0744] | 1.47x | +0.56 [+0.44,+0.70] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0689 [-0.0976,-0.0456] | 1.31x | +0.39 [+0.28,+0.54] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0457 [+0.0051,+0.0828] | 0.77x | -0.37 [-0.73,-0.04] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0625 [+0.0283,+0.0980] | 0.71x | -0.50 [-0.79,-0.23] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0030 [-0.0015,+0.0076] | 0.98x | -0.02 [-0.06,+0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0551 [-0.0760,-0.0367] | 1.24x | +0.31 [+0.23,+0.41] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0765 [-0.0974,-0.0537] | 1.35x | +0.44 [+0.32,+0.55] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.4877 [+0.3908,+0.5812] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0140 [-0.0306,+0.0030] | 1.16x | +0.22 [-0.02,+0.46] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0618 [+0.0482,+0.0775] | 0.78x | -0.35 [-0.47,-0.26] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.0893 [+0.0596,+0.1192] | 0.70x | -0.51 [-0.73,-0.33] | 0.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.3435 [+0.1657,+0.5947] | <0.50x | -1.00 [-1.00,-0.94] | 0.97/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0360 [+0.0250,+0.0472] | 0.87x | -0.21 [-0.28,-0.14] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0079 [-0.0260,+0.0084] | >1.00x | +0.00 [-0.13,+0.00] | 0.00/0.83 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.1879 [+0.1554,+0.2286] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0879 [+0.0658,+0.1085] | <0.50x | -1.00 [-1.00,-0.95] | 0.92/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1043 [+0.0799,+0.1298] | <0.50x | -1.00 [-1.00,-0.83] | 0.76/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0285 [+0.0229,+0.0348] | 0.85x | -0.23 [-0.34,-0.17] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2561 [+0.2034,+0.3050] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3143 [+0.2611,+0.3680] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2425 [+0.2016,+0.2797] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1901 [+0.1537,+0.2241] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1183 [+0.0955,+0.1404] | <0.50x | -1.00 [-1.00,-0.98] | 0.97/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=python_exec] (lower is better)

- inst ladder: 0.6B 1.4527, 1.7B 1.3687, 4B 1.0457, 8B 0.9431, 14B 0.8207, 32B 0.7476; monotone=True; GATE=PASS (0.6B->1.7B -0.0840 [-0.1264,-0.0406]; 1.7B->4B -0.3230 [-0.3880,-0.2675]; 4B->8B -0.1026 [-0.1385,-0.0688]; 8B->14B -0.1224 [-0.1531,-0.0943]; 14B->32B -0.0731 [-0.1002,-0.0451])
- base ladder: 0.6B 1.2186, 1.7B 0.9823, 4B 0.8355, 8B 0.7826, 14B 0.7172; monotone=True; GATE=PASS (0.6B->1.7B -0.2363 [-0.2773,-0.2030]; 1.7B->4B -0.1468 [-0.1808,-0.1166]; 4B->8B -0.0529 [-0.0735,-0.0350]; 8B->14B -0.0654 [-0.0878,-0.0450])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0028 [-0.0371,+0.0436] | 0.98x | -0.03 [-0.40,+0.26] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0565 [-0.0857,-0.0245] | 1.35x | +0.43 [+0.19,+0.60] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0102 [-0.0196,+0.0449] | 0.94x | -0.09 [-0.44,+0.14] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0979 [+0.0492,+0.1486] | 0.54x | -0.89 [-1.00,-0.48] | 0.22/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0763 [+0.0474,+0.1057] | 0.62x | -0.70 [-0.99,-0.41] | 0.02/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0030 [-0.0019,+0.0076] | 0.98x | -0.03 [-0.07,+0.01] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0715 [-0.0925,-0.0521] | 1.46x | +0.54 [+0.39,+0.72] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0709 [-0.1000,-0.0420] | 1.45x | +0.54 [+0.37,+0.73] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.3738 [+0.2918,+0.4696] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0517 [+0.0201,+0.0821] | 0.76x | -0.39 [-0.63,-0.15] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0934 [+0.0742,+0.1142] | 0.61x | -0.71 [-0.92,-0.56] | 0.01/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1182 [+0.0675,+0.1737] | 0.54x | -0.90 [-1.00,-0.50] | 0.32/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.2161 [+0.1519,+0.3019] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0088 [-0.0201,+0.0503] | 0.95x | -0.07 [-0.36,+0.40] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0418 [+0.0105,+0.0746] | 0.61x | -0.71 [-1.00,-0.20] | 0.16/0.01 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.3774 [+0.2949,+0.4711] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1633 [+0.1149,+0.2223] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1551 [+0.1081,+0.1993] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0667 [+0.0526,+0.0826] | 0.66x | -0.61 [-0.95,-0.41] | 0.01/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2341 [+0.1844,+0.2911] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3864 [+0.3258,+0.4604] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2102 [+0.1670,+0.2608] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1605 [+0.1234,+0.1990] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1035 [+0.0747,+0.1350] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=search] (lower is better)

- inst ladder: 0.6B 2.8866, 1.7B 2.7035, 4B 2.2616, 8B 2.0677, 14B 1.8477, 32B 1.7170; monotone=True; GATE=PASS (0.6B->1.7B -0.1830 [-0.2840,-0.0595]; 1.7B->4B -0.4419 [-0.5594,-0.3601]; 4B->8B -0.1940 [-0.2583,-0.1158]; 8B->14B -0.2200 [-0.3014,-0.1462]; 14B->32B -0.1307 [-0.1662,-0.0827])
- base ladder: 0.6B 2.4796, 1.7B 2.1568, 4B 1.9069, 8B 1.7783, 14B 1.6575; monotone=True; GATE=PASS (0.6B->1.7B -0.3228 [-0.4048,-0.2531]; 1.7B->4B -0.2500 [-0.3076,-0.2047]; 4B->8B -0.1286 [-0.1822,-0.0824]; 8B->14B -0.1207 [-0.1982,-0.0609])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1249 [-0.1843,-0.0621] | 1.44x | +0.53 [+0.29,+0.74] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1802 [-0.2477,-0.1141] | 1.69x | +0.76 [+0.54,+1.20] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.1329 [-0.2007,-0.0620] | 1.47x | +0.56 [+0.31,+0.82] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0050 [-0.0732,+0.0704] | 0.98x | -0.02 [-0.34,+0.28] | 0.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.1259 [+0.0629,+0.1743] | 0.66x | -0.61 [-0.93,-0.32] | 0.01/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0047 [-0.0043,+0.0145] | 0.98x | -0.02 [-0.08,+0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.1056 [-0.1585,-0.0678] | 1.36x | +0.45 [+0.30,+0.69] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.1507 [-0.2233,-0.1054] | 1.55x | +0.64 [+0.46,+0.98] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.7174 [+0.5585,+0.8695] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0099 [-0.0320,+0.0520] | 0.97x | -0.04 [-0.24,+0.29] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.1142 [+0.0895,+0.1476] | 0.72x | -0.48 [-0.79,-0.34] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1007 [+0.0372,+0.1550] | 0.75x | -0.42 [-0.74,-0.15] | 0.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.2475 [+0.0452,+0.4519] | <0.50x | -1.00 [-1.00,-0.16] | 0.51/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0514 [+0.0179,+0.0816] | 0.86x | -0.22 [-0.42,-0.07] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0130 [-0.0564,+0.0318] | >1.00x | +0.00 [-0.30,+0.00] | 0.00/0.75 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.3183 [+0.2039,+0.4288] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1645 [+0.1084,+0.2306] | <0.50x | -1.00 [-1.00,-0.84] | 0.79/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.2001 [+0.1520,+0.2556] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0472 [+0.0376,+0.0606] | 0.85x | -0.23 [-0.46,-0.15] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.4069 [+0.3026,+0.4895] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.5467 [+0.4568,+0.6603] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.3548 [+0.2812,+0.4145] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.2894 [+0.2326,+0.3521] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1902 [+0.1447,+0.2497] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=shell_other] (lower is better)

- inst ladder: 0.6B 1.4455, 1.7B 1.1419, 4B 0.8345, 8B 0.7272, 14B 0.6340, 32B 0.5543; monotone=True; GATE=PASS (0.6B->1.7B -0.3036 [-0.3599,-0.2476]; 1.7B->4B -0.3074 [-0.3677,-0.2519]; 4B->8B -0.1073 [-0.1384,-0.0773]; 8B->14B -0.0931 [-0.1175,-0.0707]; 14B->32B -0.0797 [-0.1023,-0.0590])
- base ladder: 0.6B 1.0457, 1.7B 0.7846, 4B 0.6310, 8B 0.6040, 14B 0.5547; monotone=True; GATE=PASS (0.6B->1.7B -0.2612 [-0.3028,-0.2243]; 1.7B->4B -0.1536 [-0.1827,-0.1293]; 4B->8B -0.0270 [-0.0442,-0.0107]; 8B->14B -0.0493 [-0.0640,-0.0372])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0013 [-0.0337,+0.0404] | 0.99x | -0.01 [-0.33,+0.29] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1006 [-0.1269,-0.0764] | 2.06x | +1.04 [+0.80,+1.33] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0666 [-0.0935,-0.0424] | 1.58x | +0.66 [+0.45,+0.88] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.0965 [+0.0627,+0.1337] | 0.56x | -0.84 [-1.00,-0.59] | 0.07/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0574 [+0.0390,+0.0759] | 0.71x | -0.50 [-0.64,-0.38] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0026 [-0.0057,+0.0007] | 1.02x | +0.03 [-0.01,+0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0358 [-0.0472,-0.0253] | 1.28x | +0.36 [+0.23,+0.49] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0458 [-0.0648,-0.0281] | 1.37x | +0.46 [+0.28,+0.66] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.5509 [+0.4498,+0.6595] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0144 [-0.0043,+0.0356] | 0.91x | -0.14 [-0.39,+0.07] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0689 [+0.0593,+0.0787] | 0.62x | -0.69 [-0.90,-0.53] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.0966 [+0.0654,+0.1306] | 0.51x | -0.96 [-1.00,-0.59] | 0.39/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1948 [+0.1472,+0.2429] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0067 [-0.0037,+0.0174] | 0.95x | -0.07 [-0.16,+0.06] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0073 [-0.0063,+0.0226] | 0.92x | -0.11 [-0.31,+0.00] | 0.00/0.15 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.4109 [+0.3356,+0.4854] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1245 [+0.0781,+0.1714] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0937 [+0.0528,+0.1329] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0340 [+0.0276,+0.0403] | 0.81x | -0.30 [-0.41,-0.22] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3998 [+0.3264,+0.4776] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3573 [+0.2929,+0.4338] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2035 [+0.1670,+0.2421] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1232 [+0.0955,+0.1494] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0793 [+0.0480,+0.1111] | <0.50x | -1.00 [-1.00,-0.89] | 0.96/0.00 |

## M2 NLL given true action bits/tok @T* [content/kind=test_run] (lower is better)

- inst ladder: 0.6B 2.3271, 1.7B 2.0752, 4B 1.7029, 8B 1.5258, 14B 1.3522, 32B 1.2271; monotone=True; GATE=PASS (0.6B->1.7B -0.2519 [-0.2994,-0.2080]; 1.7B->4B -0.3723 [-0.4259,-0.3267]; 4B->8B -0.1771 [-0.2127,-0.1457]; 8B->14B -0.1735 [-0.1971,-0.1492]; 14B->32B -0.1251 [-0.1461,-0.1050])
- base ladder: 0.6B 1.9439, 1.7B 1.6117, 4B 1.3960, 8B 1.2972, 14B 1.1893; monotone=True; GATE=PASS (0.6B->1.7B -0.3322 [-0.3814,-0.2869]; 1.7B->4B -0.2157 [-0.2499,-0.1865]; 4B->8B -0.0988 [-0.1218,-0.0777]; 8B->14B -0.1080 [-0.1270,-0.0900])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0497 [+0.0114,+0.0900] | 0.83x | -0.26 [-0.44,-0.07] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0557 [-0.0772,-0.0347] | 1.23x | +0.30 [+0.19,+0.41] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | +0.0021 [-0.0179,+0.0227] | 0.99x | -0.01 [-0.13,+0.09] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1460 [+0.1051,+0.1838] | 0.59x | -0.77 [-0.97,-0.57] | 0.01/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0929 [+0.0694,+0.1184] | 0.71x | -0.49 [-0.59,-0.39] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0001 [-0.0038,+0.0037] | 1.00x | -0.00 [-0.02,+0.02] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0542 [-0.0673,-0.0409] | 1.22x | +0.29 [+0.22,+0.37] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0867 [-0.1029,-0.0692] | 1.38x | +0.46 [+0.39,+0.55] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.7544 [+0.6600,+0.8634] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0947 [+0.0594,+0.1317] | 0.70x | -0.51 [-0.69,-0.32] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0676 [+0.0584,+0.0774] | 0.78x | -0.36 [-0.44,-0.30] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1833 [+0.1467,+0.2203] | 0.51x | -0.98 [-1.00,-0.76] | 0.40/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +1.8286 [+1.4784,+2.1840] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0018 [-0.0082,+0.0104] | 0.99x | -0.01 [-0.05,+0.08] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0775 [+0.0538,+0.1042] | 0.59x | -0.77 [-0.98,-0.54] | 0.01/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.9667 [+0.7856,+1.1666] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.2782 [+0.2198,+0.3363] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.2577 [+0.2110,+0.3067] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0578 [+0.0485,+0.0678] | 0.81x | -0.31 [-0.39,-0.24] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.3833 [+0.3342,+0.4337] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.4635 [+0.4042,+0.5254] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.3069 [+0.2615,+0.3543] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.2285 [+0.1974,+0.2587] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1630 [+0.1395,+0.1863] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M2 NLL given true action bits/tok @T* [outcome/all] (lower is better)

- inst ladder: 0.6B 1.7416, 1.7B 1.6460, 4B 1.3801, 8B 1.2491, 14B 1.1278, 32B 1.0360; monotone=True; GATE=PASS (0.6B->1.7B -0.0956 [-0.1316,-0.0582]; 1.7B->4B -0.2660 [-0.3013,-0.2353]; 4B->8B -0.1309 [-0.1567,-0.1056]; 8B->14B -0.1213 [-0.1400,-0.1030]; 14B->32B -0.0918 [-0.1090,-0.0727])
- base ladder: 0.6B 1.4945, 1.7B 1.2944, 4B 1.1638, 8B 1.0941, 14B 1.0209; monotone=True; GATE=PASS (0.6B->1.7B -0.2001 [-0.2265,-0.1747]; 1.7B->4B -0.1306 [-0.1515,-0.1111]; 4B->8B -0.0698 [-0.0862,-0.0561]; 8B->14B -0.0732 [-0.0869,-0.0602])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | +0.0058 [-0.0160,+0.0299] | 0.97x | -0.04 [-0.21,+0.12] | 0.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0578 [-0.0792,-0.0367] | 1.36x | +0.44 [+0.28,+0.61] | 0.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0207 [-0.0420,+0.0013] | 1.12x | +0.16 [-0.01,+0.32] | 0.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | +0.1315 [+0.0987,+0.1701] | 0.52x | -0.94 [-1.00,-0.66] | 0.31/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0606 [+0.0440,+0.0766] | 0.74x | -0.43 [-0.56,-0.32] | 0.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0044 [-0.0081,-0.0011] | 1.02x | +0.03 [+0.01,+0.06] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0706 [-0.0850,-0.0564] | 1.45x | +0.54 [+0.44,+0.66] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0644 [-0.0819,-0.0475] | 1.41x | +0.49 [+0.38,+0.61] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.4491 [+0.3934,+0.5092] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0354 [+0.0166,+0.0551] | 0.83x | -0.27 [-0.43,-0.13] | 0.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0755 [+0.0648,+0.0877] | 0.67x | -0.58 [-0.73,-0.47] | 0.00/0.00 |
| SERA-14B | Qwen3-14B (inst) | +0.1107 [+0.0861,+0.1365] | 0.56x | -0.85 [-1.00,-0.62] | 0.10/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +1.3887 [+1.0678,+1.7308] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0059 [-0.0043,+0.0157] | 0.97x | -0.04 [-0.12,+0.06] | 0.00/0.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0351 [+0.0202,+0.0488] | 0.72x | -0.47 [-0.67,-0.29] | 0.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.6823 [+0.5512,+0.8129] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.1608 [+0.1345,+0.1919] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.1423 [+0.1184,+0.1675] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0370 [+0.0305,+0.0442] | 0.83x | -0.26 [-0.35,-0.20] | 0.00/0.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.2471 [+0.2168,+0.2810] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.3516 [+0.3170,+0.3907] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2162 [+0.1865,+0.2461] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1550 [+0.1365,+0.1749] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1069 [+0.0901,+0.1246] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |

## M2 abs info gain bits/tok @T* [content/all] (higher is better)

- inst ladder: 0.6B 0.2242, 1.7B 0.2855, 4B 0.2645, 8B 0.2673, 14B 0.2532, 32B 0.2342; monotone=False; GATE=FAIL (0.6B->1.7B +0.0613 [+0.0486,+0.0742]; 1.7B->4B -0.0209 [-0.0334,-0.0078]; 4B->8B +0.0028 [-0.0053,+0.0109]; 8B->14B -0.0141 [-0.0218,-0.0065]; 14B->32B -0.0190 [-0.0272,-0.0114])
- base ladder: 0.6B 0.2117, 1.7B 0.2240, 4B 0.2301, 8B 0.2182, 14B 0.2192; monotone=False; GATE=FAIL (0.6B->1.7B +0.0123 [+0.0058,+0.0190]; 1.7B->4B +0.0061 [-0.0011,+0.0136]; 4B->8B -0.0118 [-0.0175,-0.0065]; 8B->14B +0.0009 [-0.0035,+0.0057])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0596 [-0.0725,-0.0480] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0380 [-0.0488,-0.0281] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0214 [-0.0310,-0.0120] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0470 [-0.0591,-0.0368] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0322 [-0.0411,-0.0238] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0012 [-0.0028,+0.0004] | <0.50x | -1.00 [-1.00,+2.00] | 0.93/0.07 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0226 [-0.0292,-0.0166] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0392 [-0.0486,-0.0305] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0210 [+0.0104,+0.0326] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0493 [-0.0595,-0.0399] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0280 [+0.0215,+0.0353] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0316 [-0.0412,-0.0227] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1005 [+0.0509,+0.1514] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0197 [+0.0137,+0.0264] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0188 [-0.0248,-0.0132] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0192 [-0.0435,+0.0051] | <0.50x | -1.00 [-1.00,+0.00] | 0.93/0.07 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0105 [-0.0172,-0.0043] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0152 [-0.0212,-0.0095] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0166 [+0.0123,+0.0217] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0125 [+0.0049,+0.0200] | 3.31x | +1.73 [+0.71,+2.00] | 0.00/0.38 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0615 [+0.0487,+0.0745] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0345 [+0.0251,+0.0442] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0491 [+0.0394,+0.0600] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0341 [+0.0269,+0.0418] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [content/kind=edit_ack] (higher is better)

- inst ladder: 0.6B 0.3610, 1.7B 0.3933, 4B 0.3710, 8B 0.3202, 14B 0.2617, 32B 0.2490; monotone=False; GATE=FAIL (0.6B->1.7B +0.0323 [-0.0412,+0.1372]; 1.7B->4B -0.0222 [-0.0962,+0.0319]; 4B->8B -0.0509 [-0.1016,+0.0030]; 8B->14B -0.0585 [-0.1045,-0.0180]; 14B->32B -0.0127 [-0.0410,+0.0209])
- base ladder: 0.6B 0.3270, 1.7B 0.2996, 4B 0.2730, 8B 0.2620, 14B 0.2382; monotone=False; GATE=FAIL (0.6B->1.7B -0.0275 [-0.0620,+0.0100]; 1.7B->4B -0.0266 [-0.0606,+0.0054]; 4B->8B -0.0110 [-0.0244,+0.0066]; 8B->14B -0.0238 [-0.0545,+0.0063])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0632 [-0.0995,-0.0277] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0296 [-0.0712,+0.0060] | <0.50x | -1.00 [-1.00,+2.00] | 0.95/0.05 |
| tmax-8b | Qwen3-8B (inst) | -0.0168 [-0.0828,+0.0423] | <0.50x | -1.00 [-1.00,+2.00] | 0.72/0.28 |
| SERA-8B | Qwen3-8B (inst) | -0.1712 [-0.2240,-0.1270] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0156 [-0.0751,+0.0238] | <0.50x | -1.00 [-1.00,+2.00] | 0.76/0.23 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0032 [-0.0127,+0.0046] | <0.50x | -1.00 [-1.00,+2.00] | 0.80/0.18 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0187 [-0.0655,+0.0142] | <0.50x | -1.00 [-1.00,+2.00] | 0.87/0.13 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0493 [-0.0874,-0.0240] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0685 [+0.0080,+0.1207] | >1.90x | +0.93 [+0.93,+0.93] | 0.02/0.98 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0390 [-0.0741,-0.0028] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.02 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0397 [+0.0261,+0.0584] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.1001 [-0.1448,-0.0534] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0090 [-0.2904,+0.2920] | <0.50x | -1.00 [-1.00,+1.24] | 0.54/0.46 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0026 [-0.0397,+0.0206] | <0.50x | -1.00 [-1.00,+1.24] | 0.57/0.43 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0504 [-0.0892,-0.0168] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0932 [-0.1698,-0.0057] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.02 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0050 [-0.0439,+0.0394] | <0.50x | -1.00 [-1.00,+0.93] | 0.64/0.36 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0155 [-0.0490,+0.0217] | <0.50x | -1.00 [-1.00,+0.00] | 0.78/0.22 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0128 [-0.0204,+0.0395] | >4.00x | +2.00 [-1.00,+2.00] | 0.20/0.79 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0340 [-0.0058,+0.0849] | >4.00x | +2.00 [+0.00,+2.00] | 0.05/0.94 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0937 [+0.0340,+0.1718] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0981 [+0.0604,+0.1502] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0582 [+0.0277,+0.0984] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0235 [+0.0062,+0.0501] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [content/kind=file_view] (higher is better)

- inst ladder: 0.6B 0.0175, 1.7B 0.0418, 4B 0.0346, 8B 0.0400, 14B 0.0508, 32B 0.0517; monotone=False; GATE=FAIL (0.6B->1.7B +0.0243 [+0.0058,+0.0442]; 1.7B->4B -0.0072 [-0.0239,+0.0087]; 4B->8B +0.0054 [-0.0061,+0.0181]; 8B->14B +0.0107 [-0.0009,+0.0223]; 14B->32B +0.0010 [-0.0118,+0.0120])
- base ladder: 0.6B 0.0162, 1.7B 0.0233, 4B 0.0292, 8B 0.0311, 14B 0.0377; monotone=True; GATE=FAIL (0.6B->1.7B +0.0071 [+0.0019,+0.0136]; 1.7B->4B +0.0059 [+0.0006,+0.0109]; 4B->8B +0.0019 [-0.0032,+0.0074]; 8B->14B +0.0066 [+0.0010,+0.0121])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0059 [-0.0200,+0.0057] | <0.50x | -1.00 [-1.00,+1.28] | 0.70/0.01 |
| tmax-sft-8b | Qwen3-8B (inst) | +0.0056 [-0.0063,+0.0164] | 1.49x | +0.58 [-1.00,+2.00] | 0.12/0.25 |
| tmax-8b | Qwen3-8B (inst) | +0.0128 [+0.0013,+0.0241] | >4.00x | +2.00 [+0.19,+2.00] | 0.01/0.66 |
| SERA-8B | Qwen3-8B (inst) | -0.0008 [-0.0136,+0.0126] | <0.50x | -1.00 [-1.00,+2.00] | 0.44/0.08 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | +0.0009 [-0.0137,+0.0132] | 1.07x | +0.10 [-1.00,+2.00] | 0.34/0.10 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0028 [-0.0059,-0.0004] | <0.50x | -1.00 [-1.00,-0.06] | 0.69/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0027 [-0.0115,+0.0057] | <0.50x | -1.00 [-1.00,+1.34] | 0.56/0.02 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0074 [-0.0196,+0.0032] | <0.50x | -1.00 [-1.00,+1.78] | 0.84/0.02 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0031 [-0.0058,+0.0133] | 1.35x | +0.43 [-1.00,+0.93] | 0.09/0.30 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0141 [-0.0256,-0.0033] | <0.50x | -1.00 [-1.00,-0.46] | 0.83/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0036 [-0.0022,+0.0106] | >2.36x | +1.24 [-1.00,+1.24] | 0.04/0.64 |
| SERA-14B | Qwen3-14B (inst) | -0.0065 [-0.0197,+0.0049] | 0.63x | -0.67 [-1.00,+1.24] | 0.48/0.05 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1010 [+0.0109,+0.1884] | >2.36x | +1.24 [+1.24,+1.24] | 0.01/0.98 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0081 [+0.0015,+0.0165] | >2.36x | +1.24 [+0.73,+1.24] | 0.00/0.89 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0104 [-0.0196,-0.0016] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.01 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0406 [+0.0064,+0.0889] | >1.00x | +0.00 [+0.00,+0.00] | 0.01/0.99 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0031 [-0.0025,+0.0088] | 1.35x | +0.43 [-1.00,+0.93] | 0.05/0.21 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0010 [-0.0104,+0.0083] | 0.91x | -0.14 [-1.00,+0.00] | 0.09/0.43 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0072 [+0.0030,+0.0132] | 1.68x | +0.75 [+0.22,+2.00] | 0.00/0.41 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0013 [-0.0062,+0.0083] | 1.23x | +0.30 [+0.00,+2.00] | 0.38/0.03 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0185 [-0.0001,+0.0377] | >4.00x | +2.00 [-0.02,+2.00] | 0.01/0.88 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0054 [-0.0048,+0.0168] | 2.69x | +1.43 [-1.00,+1.86] | 0.06/0.33 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0090 [-0.0014,+0.0215] | >1.90x | +0.93 [-0.83,+0.93] | 0.02/0.67 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0131 [+0.0030,+0.0257] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [content/kind=python_exec] (higher is better)

- inst ladder: 0.6B 0.8837, 1.7B 1.0750, 4B 0.9326, 8B 0.9224, 14B 0.8534, 32B 0.7766; monotone=False; GATE=FAIL (0.6B->1.7B +0.1913 [+0.1362,+0.2638]; 1.7B->4B -0.1424 [-0.2079,-0.0847]; 4B->8B -0.0102 [-0.0406,+0.0234]; 8B->14B -0.0690 [-0.1056,-0.0394]; 14B->32B -0.0768 [-0.1060,-0.0471])
- base ladder: 0.6B 0.8538, 1.7B 0.8465, 4B 0.8277, 8B 0.7662, 14B 0.7549; monotone=False; GATE=FAIL (0.6B->1.7B -0.0072 [-0.0329,+0.0207]; 1.7B->4B -0.0188 [-0.0549,+0.0165]; 4B->8B -0.0615 [-0.0809,-0.0412]; 8B->14B -0.0113 [-0.0329,+0.0062])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1760 [-0.2429,-0.1268] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1684 [-0.2315,-0.1225] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.1192 [-0.1764,-0.0778] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.1643 [-0.2221,-0.1146] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0885 [-0.1318,-0.0528] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0058 [-0.0125,+0.0006] | <0.50x | -1.00 [-1.00,+2.00] | 0.96/0.04 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0730 [-0.1059,-0.0490] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.1177 [-0.1579,-0.0867] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.1242 [+0.0872,+0.1666] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.1371 [-0.1744,-0.1040] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0866 [+0.0640,+0.1150] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.1056 [-0.1477,-0.0682] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0086 [-0.0854,+0.0683] | <0.50x | -1.00 [-1.00,+1.24] | 0.59/0.41 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0844 [+0.0583,+0.1100] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0520 [-0.0804,-0.0287] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.1461 [-0.2183,-0.0823] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0198 [-0.0535,+0.0057] | <0.50x | -1.00 [-1.00,+0.93] | 0.93/0.07 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0386 [-0.0609,-0.0141] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0492 [+0.0348,+0.0662] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0299 [-0.0047,+0.0661] | >4.00x | +2.00 [+0.00,+2.00] | 0.05/0.94 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2285 [+0.1710,+0.3011] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1049 [+0.0718,+0.1476] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1562 [+0.1197,+0.2020] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0985 [+0.0723,+0.1297] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [content/kind=search] (higher is better)

- inst ladder: 0.6B 0.1343, 1.7B 0.2124, 4B 0.2266, 8B 0.2386, 14B 0.2748, 32B 0.2401; monotone=False; GATE=FAIL (0.6B->1.7B +0.0781 [+0.0317,+0.1517]; 1.7B->4B +0.0142 [-0.0388,+0.0802]; 4B->8B +0.0120 [-0.0211,+0.0448]; 8B->14B +0.0362 [+0.0048,+0.0878]; 14B->32B -0.0347 [-0.0805,+0.0001])
- base ladder: 0.6B 0.1079, 1.7B 0.1396, 4B 0.1910, 8B 0.2050, 14B 0.2177; monotone=True; GATE=FAIL (0.6B->1.7B +0.0317 [+0.0033,+0.0742]; 1.7B->4B +0.0514 [+0.0213,+0.0985]; 4B->8B +0.0140 [-0.0034,+0.0377]; 8B->14B +0.0127 [-0.0085,+0.0407])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0822 [-0.1468,-0.0351] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0058 [-0.0522,+0.0319] | 0.73x | -0.46 [-1.00,+2.00] | 0.39/0.04 |
| tmax-8b | Qwen3-8B (inst) | +0.0242 [-0.0335,+0.0905] | 1.54x | +0.62 [-1.00,+2.00] | 0.10/0.36 |
| SERA-8B | Qwen3-8B (inst) | +0.0075 [-0.0293,+0.0472] | 1.14x | +0.19 [-1.00,+2.00] | 0.17/0.12 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0576 [-0.1084,-0.0174] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0013 [-0.0052,+0.0066] | 1.02x | +0.03 [-1.00,+2.00] | 0.07/0.04 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0075 [-0.0411,+0.0223] | 0.67x | -0.58 [-1.00,+2.00] | 0.42/0.03 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0266 [-0.0675,+0.0059] | <0.50x | -1.00 [-1.00,+0.16] | 0.83/0.01 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0099 [-0.0663,+0.0398] | 0.63x | -0.66 [-1.00,+0.93] | 0.36/0.17 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0901 [-0.1614,-0.0477] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0442 [+0.0202,+0.0845] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0433 [-0.0902,-0.0129] | <0.50x | -1.00 [-1.00,-0.34] | 0.67/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0924 [-0.0522,+0.2551] | >2.36x | +1.24 [-1.00,+1.24] | 0.08/0.73 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0099 [-0.0158,+0.0370] | >2.36x | +1.24 [-0.58,+1.24] | 0.01/0.77 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0227 [-0.0686,+0.0081] | <0.50x | -1.00 [-1.00,+0.00] | 0.91/0.09 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0327 [-0.0346,+0.1075] | >1.00x | +0.00 [-1.00,+0.00] | 0.19/0.81 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0486 [-0.0924,-0.0218] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0330 [-0.0766,-0.0039] | <0.50x | -1.00 [-1.00,-0.45] | 0.91/0.01 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0301 [+0.0054,+0.0747] | 1.71x | +0.77 [+0.14,+2.00] | 0.00/0.45 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0264 [+0.0051,+0.0584] | 2.63x | +1.39 [+0.25,+2.00] | 0.00/0.19 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0728 [+0.0129,+0.1642] | >4.00x | +2.00 [+0.39,+2.00] | 0.00/0.66 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0356 [+0.0014,+0.0924] | >3.64x | +1.86 [+0.15,+1.86] | 0.00/0.70 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0336 [+0.0017,+0.0747] | >1.90x | +0.93 [+0.08,+0.93] | 0.00/0.85 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0571 [+0.0226,+0.1161] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [content/kind=shell_other] (higher is better)

- inst ladder: 0.6B 0.0620, 1.7B 0.0857, 4B 0.0981, 8B 0.1209, 14B 0.1154, 32B 0.1154; monotone=False; GATE=FAIL (0.6B->1.7B +0.0237 [+0.0098,+0.0388]; 1.7B->4B +0.0124 [-0.0048,+0.0300]; 4B->8B +0.0227 [+0.0072,+0.0401]; 8B->14B -0.0055 [-0.0190,+0.0073]; 14B->32B +0.0000 [-0.0115,+0.0102])
- base ladder: 0.6B 0.0576, 1.7B 0.0894, 4B 0.1011, 8B 0.0983, 14B 0.1052; monotone=False; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0220,+0.0417]; 1.7B->4B +0.0118 [+0.0022,+0.0224]; 4B->8B -0.0029 [-0.0107,+0.0063]; 8B->14B +0.0069 [-0.0009,+0.0133])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0321 [-0.0491,-0.0169] | <0.50x | -1.00 [-1.00,-0.75] | 0.89/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0056 [-0.0188,+0.0065] | 0.85x | -0.23 [-0.92,+2.00] | 0.02/0.09 |
| tmax-8b | Qwen3-8B (inst) | +0.0025 [-0.0099,+0.0148] | >4.00x | +2.00 [-0.44,+2.00] | 0.00/0.55 |
| SERA-8B | Qwen3-8B (inst) | -0.0208 [-0.0374,-0.0052] | 0.55x | -0.86 [-1.00,-0.32] | 0.40/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0177 [-0.0315,-0.0066] | 0.60x | -0.73 [-1.00,-0.35] | 0.22/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0024 [-0.0005,+0.0054] | >4.00x | +2.00 [-0.03,+2.00] | 0.00/0.74 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0103 [-0.0188,-0.0028] | 0.75x | -0.42 [-1.00,-0.13] | 0.06/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0101 [-0.0229,+0.0023] | 0.75x | -0.41 [-1.00,+0.47] | 0.04/0.01 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0156 [-0.0377,+0.0030] | <0.50x | -1.00 [-1.00,+0.93] | 0.93/0.04 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0307 [-0.0428,-0.0208] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0035 [-0.0026,+0.0112] | >2.36x | +1.24 [-1.00,+1.24] | 0.04/0.78 |
| SERA-14B | Qwen3-14B (inst) | -0.0072 [-0.0191,+0.0029] | <0.50x | -1.00 [-1.00,+1.24] | 0.81/0.06 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0859 [+0.0421,+0.1247] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0093 [+0.0031,+0.0161] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/0.99 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0052 [-0.0151,+0.0043] | <0.50x | -1.00 [-1.00,+0.00] | 0.83/0.16 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0049 [-0.0297,+0.0238] | <0.50x | -1.00 [-1.00,+0.00] | 0.63/0.35 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0095 [-0.0192,-0.0017] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0205 [-0.0304,-0.0115] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0081 [+0.0036,+0.0139] | >4.00x | +2.00 [+0.71,+2.00] | 0.00/0.91 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0044 [-0.0107,+0.0171] | 1.17x | +0.23 [+0.00,+0.91] | 0.23/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | -0.0036 [-0.0192,+0.0108] | 0.88x | -0.19 [-0.99,+2.00] | 0.02/0.05 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0030 [-0.0158,+0.0084] | 0.79x | -0.35 [-1.00,+1.86] | 0.20/0.17 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0226 [+0.0082,+0.0372] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/0.99 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0102 [+0.0013,+0.0201] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/0.99 |

## M2 abs info gain bits/tok @T* [content/kind=test_run] (higher is better)

- inst ladder: 0.6B 0.1739, 1.7B 0.2267, 4B 0.2198, 8B 0.2162, 14B 0.2009, 32B 0.1842; monotone=False; GATE=FAIL (0.6B->1.7B +0.0529 [+0.0333,+0.0754]; 1.7B->4B -0.0069 [-0.0234,+0.0110]; 4B->8B -0.0036 [-0.0178,+0.0088]; 8B->14B -0.0153 [-0.0271,-0.0040]; 14B->32B -0.0167 [-0.0289,-0.0042])
- base ladder: 0.6B 0.1618, 1.7B 0.1718, 4B 0.1796, 8B 0.1699, 14B 0.1690; monotone=False; GATE=FAIL (0.6B->1.7B +0.0101 [+0.0021,+0.0200]; 1.7B->4B +0.0078 [-0.0018,+0.0171]; 4B->8B -0.0097 [-0.0226,-0.0003]; 8B->14B -0.0009 [-0.0084,+0.0070])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0542 [-0.0757,-0.0325] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0366 [-0.0544,-0.0214] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0249 [-0.0412,-0.0110] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0377 [-0.0564,-0.0201] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0338 [-0.0481,-0.0210] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0011 [-0.0037,+0.0016] | <0.50x | -1.00 [-1.00,+2.00] | 0.73/0.20 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0241 [-0.0357,-0.0144] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0457 [-0.0644,-0.0307] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0137 [-0.0029,+0.0327] | >1.90x | +0.93 [-1.00,+0.93] | 0.06/0.93 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0375 [-0.0538,-0.0216] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0297 [+0.0186,+0.0426] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0212 [-0.0362,-0.0060] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1728 [+0.0281,+0.3170] | >2.36x | +1.24 [+1.24,+1.24] | 0.01/0.99 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0100 [+0.0035,+0.0171] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0148 [-0.0241,-0.0066] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0098 [-0.0646,+0.0479] | <0.50x | -1.00 [-1.00,+0.00] | 0.64/0.36 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0080 [-0.0215,+0.0067] | <0.50x | -1.00 [-1.00,+0.93] | 0.85/0.14 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0056 [-0.0160,+0.0036] | <0.50x | -1.00 [-1.00,+0.00] | 0.86/0.14 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0118 [+0.0051,+0.0204] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0121 [+0.0006,+0.0235] | >4.00x | +2.00 [+0.09,+2.00] | 0.02/0.51 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0549 [+0.0316,+0.0820] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0402 [+0.0237,+0.0600] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0463 [+0.0301,+0.0668] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0319 [+0.0203,+0.0458] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok @T* [outcome/all] (higher is better)

- inst ladder: 0.6B 0.1754, 1.7B 0.2174, 4B 0.1929, 8B 0.2092, 14B 0.1968, 32B 0.1779; monotone=False; GATE=FAIL (0.6B->1.7B +0.0420 [+0.0235,+0.0625]; 1.7B->4B -0.0245 [-0.0447,-0.0055]; 4B->8B +0.0163 [+0.0038,+0.0288]; 8B->14B -0.0124 [-0.0251,+0.0001]; 14B->32B -0.0189 [-0.0304,-0.0071])
- base ladder: 0.6B 0.1713, 1.7B 0.1779, 4B 0.1826, 8B 0.1752, 14B 0.1726; monotone=False; GATE=FAIL (0.6B->1.7B +0.0066 [-0.0022,+0.0161]; 1.7B->4B +0.0047 [-0.0028,+0.0120]; 4B->8B -0.0074 [-0.0168,+0.0016]; 8B->14B -0.0027 [-0.0114,+0.0065])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0465 [-0.0669,-0.0287] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0326 [-0.0509,-0.0178] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0244 [-0.0423,-0.0097] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0380 [-0.0579,-0.0201] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0237 [-0.0370,-0.0111] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0010 [-0.0037,+0.0015] | <0.50x | -1.00 [-1.00,+2.00] | 0.63/0.23 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0109 [-0.0216,-0.0015] | <0.50x | -1.00 [-1.00,-0.62] | 0.95/0.01 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0289 [-0.0434,-0.0158] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0252 [+0.0099,+0.0403] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0343 [-0.0475,-0.0214] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0167 [+0.0093,+0.0255] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0213 [-0.0381,-0.0041] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1101 [-0.0210,+0.2540] | >2.36x | +1.24 [-1.00,+1.24] | 0.05/0.95 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0264 [+0.0169,+0.0365] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0129 [-0.0231,-0.0021] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0195 [-0.0744,+0.0346] | <0.50x | -1.00 [-1.00,+0.00] | 0.78/0.22 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0125 [-0.0239,-0.0015] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0101 [-0.0203,+0.0003] | <0.50x | -1.00 [-1.00,+0.00] | 0.97/0.03 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0082 [+0.0027,+0.0139] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/0.99 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0041 [-0.0057,+0.0138] | 2.06x | +1.05 [+0.00,+2.00] | 0.22/0.24 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0395 [+0.0207,+0.0581] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0103 [-0.0004,+0.0217] | >3.64x | +1.86 [-0.17,+1.86] | 0.01/0.96 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0340 [+0.0201,+0.0495] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0243 [+0.0140,+0.0350] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/all] (higher is better)

- inst ladder: 0.6B 0.2419, 1.7B 0.4246, 4B 0.3585, 8B 0.3686, 14B 0.2972, 32B 0.2479; monotone=False; GATE=FAIL (0.6B->1.7B +0.1827 [+0.1488,+0.2183]; 1.7B->4B -0.0661 [-0.0907,-0.0414]; 4B->8B +0.0101 [-0.0033,+0.0251]; 8B->14B -0.0714 [-0.0888,-0.0547]; 14B->32B -0.0493 [-0.0637,-0.0369])
- base ladder: 0.6B 0.2117, 1.7B 0.2240, 4B 0.2301, 8B 0.2182, 14B 0.2192; monotone=False; GATE=FAIL (0.6B->1.7B +0.0123 [+0.0058,+0.0190]; 1.7B->4B +0.0061 [-0.0011,+0.0136]; 4B->8B -0.0118 [-0.0175,-0.0065]; 8B->14B +0.0009 [-0.0036,+0.0057])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1555 [-0.1865,-0.1296] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1340 [-0.1619,-0.1100] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.1194 [-0.1457,-0.0958] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.1125 [-0.1370,-0.0917] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.1029 [-0.1225,-0.0855] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0205 [-0.0249,-0.0167] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.1024 [-0.1221,-0.0849] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.1232 [-0.1479,-0.1020] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0389 [+0.0255,+0.0537] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0874 [-0.1053,-0.0713] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0694 [+0.0555,+0.0856] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0585 [-0.0736,-0.0452] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0547 [-0.0010,+0.1127] | >2.36x | +1.24 [-1.00,+1.24] | 0.03/0.97 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0105 [+0.0025,+0.0188] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0260 [-0.0333,-0.0194] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0004 [-0.0292,+0.0300] | >1.00x | +0.00 [-1.00,+0.00] | 0.48/0.52 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0051 [-0.0123,+0.0014] | <0.50x | -1.00 [-1.00,+0.93] | 0.92/0.07 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0094 [-0.0154,-0.0036] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0146 [+0.0100,+0.0199] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0303 [+0.0204,+0.0403] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2006 [+0.1630,+0.2414] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1284 [+0.1025,+0.1570] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1503 [+0.1247,+0.1809] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0780 [+0.0630,+0.0950] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/kind=edit_ack] (higher is better)

- inst ladder: 0.6B 0.3835, 1.7B 0.5370, 4B 0.5134, 8B 0.4207, 14B 0.3007, 32B 0.2534; monotone=False; GATE=FAIL (0.6B->1.7B +0.1535 [+0.0341,+0.3123]; 1.7B->4B -0.0236 [-0.1523,+0.0776]; 4B->8B -0.0927 [-0.1833,+0.0070]; 8B->14B -0.1200 [-0.1992,-0.0506]; 14B->32B -0.0473 [-0.0836,-0.0066])
- base ladder: 0.6B 0.3270, 1.7B 0.2996, 4B 0.2730, 8B 0.2620, 14B 0.2382; monotone=False; GATE=FAIL (0.6B->1.7B -0.0274 [-0.0620,+0.0100]; 1.7B->4B -0.0266 [-0.0606,+0.0054]; 4B->8B -0.0110 [-0.0244,+0.0066]; 8B->14B -0.0238 [-0.0544,+0.0063])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1611 [-0.2254,-0.1019] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1240 [-0.1984,-0.0606] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.1130 [-0.2113,-0.0274] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| SERA-8B | Qwen3-8B (inst) | -0.2743 [-0.3439,-0.2164] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0836 [-0.1801,-0.0238] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0231 [-0.0428,-0.0101] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0987 [-0.1792,-0.0520] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.1339 [-0.1995,-0.0877] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0895 [+0.0226,+0.1485] | >1.90x | +0.93 [+0.93,+0.93] | 0.01/0.99 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0762 [-0.1229,-0.0332] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0955 [+0.0682,+0.1325] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.1438 [-0.2019,-0.0823] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0411 [-0.3239,+0.2546] | <0.50x | -1.00 [-1.00,+1.24] | 0.61/0.39 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0247 [-0.0768,+0.0118] | <0.50x | -1.00 [-1.00,+1.24] | 0.91/0.09 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0561 [-0.0993,-0.0187] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.1049 [-0.1990,-0.0004] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.02 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0023 [-0.0445,+0.0447] | <0.50x | -1.00 [-1.00,+0.93] | 0.57/0.43 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0137 [-0.0478,+0.0257] | <0.50x | -1.00 [-1.00,+0.00] | 0.74/0.26 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0110 [-0.0234,+0.0391] | >4.00x | +2.00 [-1.00,+2.00] | 0.23/0.75 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0564 [+0.0084,+0.1162] | >4.00x | +2.00 [+2.00,+2.00] | 0.01/0.99 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.2374 [+0.1116,+0.3932] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.2404 [+0.1656,+0.3431] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1588 [+0.0990,+0.2343] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0626 [+0.0337,+0.1002] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/kind=file_view] (higher is better)

- inst ladder: 0.6B 0.0150, 1.7B 0.0541, 4B 0.0398, 8B 0.0525, 14B 0.0542, 32B 0.0527; monotone=False; GATE=FAIL (0.6B->1.7B +0.0391 [+0.0059,+0.0765]; 1.7B->4B -0.0143 [-0.0427,+0.0120]; 4B->8B +0.0127 [-0.0064,+0.0338]; 8B->14B +0.0017 [-0.0186,+0.0223]; 14B->32B -0.0014 [-0.0191,+0.0135])
- base ladder: 0.6B 0.0162, 1.7B 0.0233, 4B 0.0292, 8B 0.0311, 14B 0.0377; monotone=True; GATE=FAIL (0.6B->1.7B +0.0070 [+0.0019,+0.0136]; 1.7B->4B +0.0059 [+0.0006,+0.0109]; 4B->8B +0.0019 [-0.0032,+0.0074]; 8B->14B +0.0066 [+0.0010,+0.0121])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0182 [-0.0476,+0.0074] | <0.50x | -1.00 [-1.00,+2.00] | 0.83/0.03 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0077 [-0.0338,+0.0159] | <0.50x | -1.00 [-1.00,+2.00] | 0.59/0.11 |
| tmax-8b | Qwen3-8B (inst) | -0.0022 [-0.0265,+0.0221] | <0.50x | -1.00 [-1.00,+2.00] | 0.42/0.24 |
| SERA-8B | Qwen3-8B (inst) | -0.0134 [-0.0382,+0.0120] | <0.50x | -1.00 [-1.00,+2.00] | 0.71/0.06 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0175 [-0.0445,+0.0069] | <0.50x | -1.00 [-1.00,+2.00] | 0.81/0.03 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0084 [-0.0137,-0.0040] | <0.50x | -1.00 [-1.00,-0.26] | 0.72/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0209 [-0.0430,-0.0007] | <0.50x | -1.00 [-1.00,-0.38] | 0.92/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0203 [-0.0458,+0.0033] | <0.50x | -1.00 [-1.00,+0.48] | 0.90/0.01 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0024 [-0.0078,+0.0140] | 1.27x | +0.34 [-1.00,+0.93] | 0.17/0.28 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0172 [-0.0338,-0.0017] | <0.50x | -1.00 [-1.00,-0.44] | 0.93/0.01 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0119 [+0.0013,+0.0246] | >2.36x | +1.24 [+0.31,+1.24] | 0.01/0.93 |
| SERA-14B | Qwen3-14B (inst) | -0.0094 [-0.0273,+0.0068] | <0.50x | -1.00 [-1.00,+1.24] | 0.78/0.08 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0779 [-0.0180,+0.1650] | >2.36x | +1.24 [-1.00,+1.24] | 0.05/0.94 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0084 [-0.0024,+0.0200] | >2.36x | +1.24 [-1.00,+1.24] | 0.05/0.89 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0105 [-0.0207,-0.0006] | <0.50x | -1.00 [-1.00,-0.89] | 0.97/0.02 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0423 [-0.0011,+0.1000] | >1.00x | +0.00 [-0.32,+0.00] | 0.02/0.97 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0032 [-0.0025,+0.0086] | 1.37x | +0.45 [-1.00,+0.93] | 0.04/0.23 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0007 [-0.0106,+0.0090] | 0.93x | -0.10 [-1.00,+0.00] | 0.09/0.45 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0056 [+0.0014,+0.0111] | >4.00x | +2.00 [+0.17,+2.00] | 0.00/0.72 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0012 [-0.0104,+0.0072] | <1.00x | +0.00 [+0.00,+1.82] | 0.62/0.02 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0308 [-0.0041,+0.0688] | >4.00x | +2.00 [-1.00,+2.00] | 0.03/0.89 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0106 [-0.0111,+0.0349] | >3.64x | +1.86 [-1.00,+1.86] | 0.11/0.58 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0214 [-0.0025,+0.0478] | >1.90x | +0.93 [-1.00,+0.93] | 0.03/0.88 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0165 [+0.0013,+0.0328] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/0.99 |

## M2 abs info gain bits/tok [content/kind=python_exec] (higher is better)

- inst ladder: 0.6B 0.9591, 1.7B 1.6275, 4B 1.2753, 8B 1.2586, 14B 1.0085, 32B 0.8275; monotone=False; GATE=FAIL (0.6B->1.7B +0.6684 [+0.5306,+0.8515]; 1.7B->4B -0.3522 [-0.4836,-0.2454]; 4B->8B -0.0167 [-0.0676,+0.0375]; 8B->14B -0.2501 [-0.3332,-0.1855]; 14B->32B -0.1810 [-0.2322,-0.1350])
- base ladder: 0.6B 0.8538, 1.7B 0.8465, 4B 0.8277, 8B 0.7662, 14B 0.7549; monotone=False; GATE=FAIL (0.6B->1.7B -0.0072 [-0.0330,+0.0207]; 1.7B->4B -0.0188 [-0.0549,+0.0165]; 4B->8B -0.0615 [-0.0808,-0.0412]; 8B->14B -0.0113 [-0.0329,+0.0063])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.4892 [-0.6385,-0.3751] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.4864 [-0.6312,-0.3820] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.4426 [-0.5816,-0.3412] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.3633 [-0.4860,-0.2674] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.2826 [-0.3811,-0.2035] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0694 [-0.0901,-0.0526] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.3242 [-0.4247,-0.2565] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.3832 [-0.4964,-0.2993] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.1960 [+0.1481,+0.2518] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.2707 [-0.3361,-0.2133] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.2224 [+0.1739,+0.2858] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.1970 [-0.2665,-0.1430] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.1193 [-0.2092,-0.0352] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0631 [+0.0292,+0.0924] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0783 [-0.1164,-0.0496] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0705 [-0.1513,+0.0089] | <0.50x | -1.00 [-1.00,+0.00] | 0.96/0.04 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0032 [-0.0298,+0.0287] | >1.90x | +0.93 [-1.00,+0.93] | 0.41/0.59 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0171 [-0.0409,+0.0104] | <0.50x | -1.00 [-1.00,+0.00] | 0.91/0.10 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0438 [+0.0284,+0.0615] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.1053 [+0.0637,+0.1508] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.7810 [+0.6214,+0.9962] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.4476 [+0.3511,+0.5735] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.4924 [+0.3869,+0.6227] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.2536 [+0.1949,+0.3253] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/kind=search] (higher is better)

- inst ladder: 0.6B 0.1448, 1.7B 0.3238, 4B 0.3035, 8B 0.3277, 14B 0.3308, 32B 0.2557; monotone=False; GATE=FAIL (0.6B->1.7B +0.1789 [+0.0849,+0.3400]; 1.7B->4B -0.0203 [-0.1099,+0.0709]; 4B->8B +0.0242 [-0.0374,+0.0822]; 8B->14B +0.0030 [-0.0522,+0.0745]; 14B->32B -0.0751 [-0.1522,-0.0204])
- base ladder: 0.6B 0.1079, 1.7B 0.1397, 4B 0.1910, 8B 0.2050, 14B 0.2177; monotone=True; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0034,+0.0742]; 1.7B->4B +0.0514 [+0.0213,+0.0985]; 4B->8B +0.0140 [-0.0034,+0.0377]; 8B->14B +0.0127 [-0.0086,+0.0407])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1703 [-0.2940,-0.0813] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0882 [-0.1873,-0.0145] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| tmax-8b | Qwen3-8B (inst) | -0.0607 [-0.1655,+0.0266] | <0.50x | -1.00 [-1.00,+2.00] | 0.88/0.05 |
| SERA-8B | Qwen3-8B (inst) | -0.0388 [-0.1099,+0.0228] | <0.50x | -1.00 [-1.00,+2.00] | 0.78/0.06 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.1360 [-0.2261,-0.0660] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0134 [-0.0300,-0.0013] | <0.50x | -1.00 [-1.00,-0.16] | 0.65/0.01 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0816 [-0.1585,-0.0223] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0985 [-0.1905,-0.0308] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0073 [-0.0521,+0.0682] | 1.45x | +0.54 [-1.00,+0.93] | 0.18/0.45 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.1431 [-0.2545,-0.0743] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.1004 [+0.0516,+0.1818] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0816 [-0.1551,-0.0333] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0301 [-0.1315,+0.1991] | >2.36x | +1.24 [-1.00,+1.24] | 0.39/0.59 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0025 [-0.0472,+0.0361] | 0.58x | -0.77 [-1.00,+1.24] | 0.39/0.48 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0324 [-0.0895,+0.0036] | <0.50x | -1.00 [-1.00,+0.00] | 0.95/0.05 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0656 [-0.0095,+0.1560] | >1.00x | +0.00 [-1.00,+0.00] | 0.04/0.96 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0476 [-0.0930,-0.0203] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0300 [-0.0723,+0.0002] | <0.50x | -1.00 [-1.00,+0.00] | 0.87/0.03 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0275 [+0.0008,+0.0757] | >4.00x | +2.00 [+0.07,+2.00] | 0.01/0.86 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0369 [+0.0082,+0.0760] | 3.52x | +1.82 [+0.40,+2.00] | 0.00/0.41 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.1841 [+0.0730,+0.3682] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/0.99 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1124 [+0.0424,+0.2341] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1227 [+0.0500,+0.2248] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.1131 [+0.0564,+0.2068] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/kind=shell_other] (higher is better)

- inst ladder: 0.6B 0.0687, 1.7B 0.1301, 4B 0.1320, 8B 0.1764, 14B 0.1360, 32B 0.1195; monotone=False; GATE=FAIL (0.6B->1.7B +0.0615 [+0.0393,+0.0899]; 1.7B->4B +0.0019 [-0.0251,+0.0285]; 4B->8B +0.0444 [+0.0204,+0.0712]; 8B->14B -0.0404 [-0.0662,-0.0160]; 14B->32B -0.0165 [-0.0344,-0.0015])
- base ladder: 0.6B 0.0576, 1.7B 0.0894, 4B 0.1011, 8B 0.0983, 14B 0.1052; monotone=False; GATE=FAIL (0.6B->1.7B +0.0318 [+0.0220,+0.0417]; 1.7B->4B +0.0118 [+0.0022,+0.0225]; 4B->8B -0.0029 [-0.0107,+0.0063]; 8B->14B +0.0069 [-0.0009,+0.0133])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0851 [-0.1208,-0.0537] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0584 [-0.0876,-0.0318] | <0.50x | -1.00 [-1.00,-0.69] | 0.88/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0514 [-0.0782,-0.0267] | <0.50x | -1.00 [-1.00,-0.59] | 0.80/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0633 [-0.0934,-0.0354] | <0.50x | -1.00 [-1.00,-0.87] | 0.95/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0670 [-0.0930,-0.0455] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0066 [-0.0123,-0.0019] | 0.91x | -0.14 [-0.38,-0.04] | 0.00/0.01 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0556 [-0.0753,-0.0394] | <0.50x | -1.00 [-1.00,-0.79] | 0.90/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0593 [-0.0864,-0.0354] | <0.50x | -1.00 [-1.00,-0.76] | 0.93/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0115 [-0.0364,+0.0114] | <0.50x | -1.00 [-1.00,+0.93] | 0.82/0.12 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0474 [-0.0678,-0.0310] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0185 [+0.0066,+0.0333] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0201 [-0.0368,-0.0061] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0572 [+0.0146,+0.0953] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/0.99 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0009 [-0.0085,+0.0105] | >2.36x | +1.24 [-1.00,+1.24] | 0.22/0.55 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0049 [-0.0157,+0.0053] | <0.50x | -1.00 [-1.00,+0.00] | 0.80/0.20 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0002 [-0.0313,+0.0368] | <0.50x | -1.00 [-1.00,+0.00] | 0.51/0.49 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0070 [-0.0161,+0.0012] | <0.50x | -1.00 [-1.00,+0.50] | 0.93/0.02 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0167 [-0.0269,-0.0069] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0070 [+0.0021,+0.0132] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0111 [-0.0081,+0.0266] | 1.50x | +0.59 [+0.00,+1.47] | 0.10/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0408 [+0.0097,+0.0707] | >4.00x | +2.00 [+0.91,+2.00] | 0.00/0.95 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0309 [+0.0009,+0.0602] | >3.64x | +1.86 [+0.96,+1.86] | 0.01/0.95 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0781 [+0.0482,+0.1116] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0308 [+0.0150,+0.0496] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [content/kind=test_run] (higher is better)

- inst ladder: 0.6B 0.1868, 1.7B 0.3311, 4B 0.2969, 8B 0.3009, 14B 0.2346, 32B 0.1966; monotone=False; GATE=FAIL (0.6B->1.7B +0.1444 [+0.0913,+0.2071]; 1.7B->4B -0.0342 [-0.0667,-0.0003]; 4B->8B +0.0040 [-0.0189,+0.0240]; 8B->14B -0.0663 [-0.0972,-0.0398]; 14B->32B -0.0380 [-0.0601,-0.0182])
- base ladder: 0.6B 0.1618, 1.7B 0.1718, 4B 0.1796, 8B 0.1699, 14B 0.1690; monotone=False; GATE=FAIL (0.6B->1.7B +0.0101 [+0.0021,+0.0200]; 1.7B->4B +0.0078 [-0.0018,+0.0171]; 4B->8B -0.0097 [-0.0226,-0.0003]; 8B->14B -0.0009 [-0.0084,+0.0070])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1350 [-0.1883,-0.0896] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1167 [-0.1649,-0.0779] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.1064 [-0.1504,-0.0698] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0910 [-0.1291,-0.0582] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0943 [-0.1280,-0.0657] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0174 [-0.0243,-0.0109] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0903 [-0.1274,-0.0615] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.1179 [-0.1631,-0.0809] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0284 [+0.0073,+0.0533] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0665 [-0.0947,-0.0416] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0633 [+0.0398,+0.0916] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0398 [-0.0638,-0.0173] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.1316 [-0.0359,+0.2969] | >2.36x | +1.24 [-1.00,+1.24] | 0.05/0.95 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0022 [-0.0068,+0.0106] | >2.36x | +1.24 [-1.00,+1.24] | 0.32/0.68 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0226 [-0.0349,-0.0125] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0075 [-0.0664,+0.0834] | >1.00x | +0.00 [-1.00,+0.00] | 0.44/0.56 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0040 [-0.0185,+0.0111] | <0.50x | -1.00 [-1.00,+0.93] | 0.68/0.31 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0010 [-0.0117,+0.0094] | <0.50x | -1.00 [-1.00,+0.00] | 0.57/0.43 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0103 [+0.0032,+0.0195] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0250 [+0.0103,+0.0405] | >4.00x | +2.00 [+1.36,+2.00] | 0.00/0.90 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.1593 [+0.0968,+0.2320] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.1173 [+0.0721,+0.1721] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1310 [+0.0903,+0.1826] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0655 [+0.0437,+0.0930] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 abs info gain bits/tok [outcome/all] (higher is better)

- inst ladder: 0.6B 0.1871, 1.7B 0.3128, 4B 0.2488, 8B 0.2802, 14B 0.2254, 32B 0.1866; monotone=False; GATE=FAIL (0.6B->1.7B +0.1257 [+0.0837,+0.1743]; 1.7B->4B -0.0641 [-0.1014,-0.0267]; 4B->8B +0.0315 [+0.0099,+0.0529]; 8B->14B -0.0548 [-0.0804,-0.0312]; 14B->32B -0.0388 [-0.0575,-0.0218])
- base ladder: 0.6B 0.1713, 1.7B 0.1779, 4B 0.1826, 8B 0.1752, 14B 0.1726; monotone=False; GATE=FAIL (0.6B->1.7B +0.0066 [-0.0021,+0.0161]; 1.7B->4B +0.0047 [-0.0029,+0.0120]; 4B->8B -0.0074 [-0.0168,+0.0016]; 8B->14B -0.0027 [-0.0114,+0.0065])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.1136 [-0.1536,-0.0782] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.1000 [-0.1388,-0.0675] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0942 [-0.1317,-0.0631] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0803 [-0.1149,-0.0499] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0760 [-0.1035,-0.0516] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0153 [-0.0211,-0.0105] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0655 [-0.0907,-0.0440] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0867 [-0.1181,-0.0594] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0415 [+0.0231,+0.0610] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0594 [-0.0803,-0.0408] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0431 [+0.0276,+0.0615] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0372 [-0.0606,-0.0148] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0545 [-0.1017,+0.2243] | >2.36x | +1.24 [-1.00,+1.24] | 0.27/0.73 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0252 [+0.0129,+0.0373] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0178 [-0.0291,-0.0059] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0073 [-0.0779,+0.0632] | <0.50x | -1.00 [-1.00,+0.00] | 0.61/0.39 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0086 [-0.0203,+0.0030] | <0.50x | -1.00 [-1.00,+0.93] | 0.92/0.07 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0065 [-0.0173,+0.0043] | <0.50x | -1.00 [-1.00,+0.00] | 0.88/0.11 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0058 [-0.0000,+0.0118] | >4.00x | +2.00 [-1.00,+2.00] | 0.03/0.97 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0159 [+0.0049,+0.0271] | >4.00x | +2.00 [+0.96,+2.00] | 0.00/0.87 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.1349 [+0.0894,+0.1878] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0661 [+0.0424,+0.0953] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.1050 [+0.0739,+0.1416] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0528 [+0.0353,+0.0734] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 relative gain [content/all] (higher is better)

- inst ladder: 0.6B 0.1090, 1.7B 0.1566, 4B 0.1715, 8B 0.1920, 14B 0.1974, 32B 0.1975; monotone=True; GATE=FAIL (0.6B->1.7B +0.0476 [+0.0395,+0.0562]; 1.7B->4B +0.0149 [+0.0072,+0.0241]; 4B->8B +0.0205 [+0.0132,+0.0282]; 8B->14B +0.0054 [-0.0002,+0.0110]; 14B->32B +0.0000 [-0.0060,+0.0063])
- base ladder: 0.6B 0.1202, 1.7B 0.1493, 4B 0.1735, 8B 0.1750, 14B 0.1882; monotone=True; GATE=FAIL (0.6B->1.7B +0.0291 [+0.0238,+0.0351]; 1.7B->4B +0.0243 [+0.0197,+0.0296]; 4B->8B +0.0015 [-0.0019,+0.0051]; 8B->14B +0.0132 [+0.0097,+0.0170])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0427 [-0.0518,-0.0342] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0231 [-0.0302,-0.0164] | <0.50x | -1.00 [-1.00,-0.76] | 0.68/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0202 [-0.0277,-0.0130] | 0.53x | -0.92 [-1.00,-0.63] | 0.37/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0439 [-0.0542,-0.0348] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0387 [-0.0460,-0.0320] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0039 [-0.0052,-0.0026] | 0.88x | -0.18 [-0.29,-0.11] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0150 [-0.0200,-0.0102] | 0.62x | -0.68 [-1.00,-0.46] | 0.03/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0225 [-0.0286,-0.0169] | <0.50x | -1.00 [-1.00,-0.75] | 0.64/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0432 [-0.0544,-0.0342] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0399 [-0.0480,-0.0326] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0093 [+0.0058,+0.0131] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/0.99 |
| SERA-14B | Qwen3-14B (inst) | -0.0383 [-0.0470,-0.0302] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0429 [-0.0731,-0.0133] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0080 [+0.0032,+0.0126] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/0.99 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0181 [-0.0235,-0.0132] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0722 [-0.0940,-0.0514] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0256 [-0.0332,-0.0192] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0306 [-0.0376,-0.0243] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0030 [+0.0005,+0.0055] | 1.42x | +0.51 [+0.07,+2.00] | 0.00/0.12 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0112 [-0.0167,-0.0063] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0073 [-0.0005,+0.0149] | 1.33x | +0.41 [-0.03,+0.88] | 0.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0020 [-0.0083,+0.0043] | 0.92x | -0.11 [-0.43,+1.14] | 0.00/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0171 [+0.0115,+0.0232] | >1.90x | +0.93 [+0.76,+0.93] | 0.00/0.88 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0093 [+0.0035,+0.0158] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 relative gain [content/kind=edit_ack] (higher is better)

- inst ladder: 0.6B 0.3045, 1.7B 0.2961, 4B 0.3795, 8B 0.3238, 14B 0.3245, 32B 0.3275; monotone=False; GATE=FAIL (0.6B->1.7B -0.0084 [-0.0728,+0.0812]; 1.7B->4B +0.0834 [+0.0081,+0.1476]; 4B->8B -0.0556 [-0.1192,+0.0115]; 8B->14B +0.0006 [-0.0617,+0.0639]; 14B->32B +0.0031 [-0.0517,+0.0561])
- base ladder: 0.6B 0.3107, 1.7B 0.3337, 4B 0.3418, 8B 0.3363, 14B 0.3408; monotone=False; GATE=FAIL (0.6B->1.7B +0.0230 [-0.0036,+0.0511]; 1.7B->4B +0.0081 [-0.0236,+0.0418]; 4B->8B -0.0055 [-0.0226,+0.0157]; 8B->14B +0.0046 [-0.0321,+0.0424])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0166 [-0.0663,+0.0254] | <0.50x | -1.00 [-1.00,+2.00] | 0.77/0.19 |
| tmax-sft-8b | Qwen3-8B (inst) | +0.0046 [-0.0426,+0.0417] | >4.00x | +2.00 [-1.00,+2.00] | 0.30/0.63 |
| tmax-8b | Qwen3-8B (inst) | -0.0212 [-0.0820,+0.0255] | <0.50x | -1.00 [-1.00,+2.00] | 0.77/0.18 |
| SERA-8B | Qwen3-8B (inst) | -0.1974 [-0.2963,-0.1259] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0084 [-0.0694,+0.0405] | <0.50x | -1.00 [-1.00,+2.00] | 0.58/0.37 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0012 [-0.0093,+0.0107] | >4.00x | +2.00 [-1.00,+2.00] | 0.20/0.53 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | +0.0196 [-0.0397,+0.0634] | >4.00x | +2.00 [-1.00,+2.00] | 0.20/0.76 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0161 [-0.0521,+0.0104] | <0.50x | -1.00 [-1.00,+2.00] | 0.82/0.12 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0039 [-0.0670,+0.0433] | <0.50x | -1.00 [-1.00,+0.93] | 0.52/0.38 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0317 [-0.0957,+0.0093] | <0.50x | -1.00 [-1.00,+1.24] | 0.91/0.09 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0223 [+0.0062,+0.0368] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/0.99 |
| SERA-14B | Qwen3-14B (inst) | -0.1490 [-0.2766,-0.0636] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.1334 [-0.3735,+0.0367] | <0.50x | -1.00 [-1.00,+1.24] | 0.94/0.07 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0509 [-0.1001,-0.0030] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.02 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0513 [-0.0837,-0.0094] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.1799 [-0.3181,-0.0539] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0290 [-0.0828,+0.0242] | <0.50x | -1.00 [-1.00,+0.93] | 0.85/0.11 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0480 [-0.1042,-0.0002] | <0.50x | -1.00 [-1.00,-0.55] | 0.97/0.03 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | -0.0258 [-0.0483,-0.0028] | <0.50x | -1.00 [-1.00,-0.97] | 0.96/0.01 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0062 [-0.0303,+0.0173] | <1.00x | +0.00 [+0.00,+0.90] | 0.70/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | -0.0377 [-0.1091,+0.0472] | <0.50x | -1.00 [-1.00,+2.00] | 0.75/0.10 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0377 [+0.0013,+0.0734] | >3.64x | +1.86 [+0.43,+1.86] | 0.00/0.95 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | -0.0124 [-0.0565,+0.0462] | <0.50x | -1.00 [-1.00,+0.93] | 0.64/0.29 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | -0.0164 [-0.0486,+0.0188] | <0.50x | -1.00 [-1.00,+0.00] | 0.74/0.16 |

## M2 relative gain [content/kind=file_view] (higher is better)

- inst ladder: 0.6B 0.0076, 1.7B 0.0228, 4B 0.0208, 8B 0.0300, 14B 0.0396, 32B 0.0447; monotone=False; GATE=FAIL (0.6B->1.7B +0.0152 [+0.0018,+0.0294]; 1.7B->4B -0.0020 [-0.0134,+0.0092]; 4B->8B +0.0092 [-0.0016,+0.0218]; 8B->14B +0.0096 [-0.0018,+0.0218]; 14B->32B +0.0052 [-0.0071,+0.0160])
- base ladder: 0.6B 0.0100, 1.7B 0.0166, 4B 0.0236, 8B 0.0265, 14B 0.0346; monotone=True; GATE=FAIL (0.6B->1.7B +0.0065 [+0.0031,+0.0113]; 1.7B->4B +0.0071 [+0.0030,+0.0115]; 4B->8B +0.0029 [-0.0015,+0.0078]; 8B->14B +0.0081 [+0.0027,+0.0130])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0030 [-0.0184,+0.0111] | 0.76x | -0.39 [-1.00,+1.08] | 0.28/0.01 |
| tmax-sft-8b | Qwen3-8B (inst) | +0.0044 [-0.0090,+0.0168] | 1.34x | +0.43 [-1.00,+2.00] | 0.03/0.04 |
| tmax-8b | Qwen3-8B (inst) | +0.0078 [-0.0049,+0.0210] | 1.69x | +0.76 [-0.40,+2.00] | 0.00/0.12 |
| SERA-8B | Qwen3-8B (inst) | -0.0051 [-0.0195,+0.0094] | 0.63x | -0.67 [-1.00,+0.84] | 0.41/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0087 [-0.0238,+0.0051] | <0.50x | -1.00 [-1.00,+0.39] | 0.58/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0040 [-0.0067,-0.0017] | 0.70x | -0.52 [-1.00,-0.15] | 0.33/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0074 [-0.0186,+0.0033] | <0.50x | -1.00 [-1.00,+0.27] | 0.53/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0064 [-0.0197,+0.0060] | 0.56x | -0.83 [-1.00,+0.69] | 0.46/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0075 [-0.0148,-0.0004] | <0.50x | -1.00 [-1.00,-0.35] | 0.91/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0089 [-0.0209,+0.0022] | 0.55x | -0.86 [-1.00,+0.25] | 0.47/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0024 [-0.0029,+0.0088] | 1.48x | +0.57 [-1.00,+1.24] | 0.03/0.34 |
| SERA-14B | Qwen3-14B (inst) | -0.0069 [-0.0200,+0.0048] | 0.63x | -0.66 [-1.00,+0.62] | 0.38/0.01 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0376 [-0.0207,+0.0859] | >2.36x | +1.24 [-1.00,+1.24] | 0.06/0.85 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0056 [-0.0026,+0.0140] | >2.36x | +1.24 [-0.35,+1.24] | 0.01/0.48 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0075 [-0.0158,+0.0009] | <0.50x | -1.00 [-1.00,+0.00] | 0.78/0.03 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0167 [-0.0099,+0.0565] | >1.00x | +0.00 [-1.00,+0.00] | 0.07/0.89 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0005 [-0.0041,+0.0049] | 1.04x | +0.05 [-1.00,+0.74] | 0.08/0.02 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0039 [-0.0120,+0.0043] | 0.73x | -0.45 [-1.00,+0.00] | 0.10/0.18 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0034 [+0.0004,+0.0077] | 1.26x | +0.33 [+0.03,+2.00] | 0.00/0.07 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0024 [-0.0068,+0.0016] | <1.00x | +0.00 [+0.00,+0.41] | 0.86/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0062 [-0.0084,+0.0199] | 2.31x | +1.21 [-1.00,+2.00] | 0.10/0.32 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0028 [-0.0135,+0.0074] | 0.68x | -0.55 [-1.00,+1.74] | 0.33/0.02 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0035 [-0.0094,+0.0176] | 1.32x | +0.40 [-1.00,+0.93] | 0.15/0.29 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0050 [-0.0051,+0.0167] | >1.00x | +0.00 [-0.62,+0.00] | 0.01/0.83 |

## M2 relative gain [content/kind=python_exec] (higher is better)

- inst ladder: 0.6B 0.3850, 1.7B 0.4579, 4B 0.4809, 8B 0.5048, 14B 0.5135, 32B 0.5134; monotone=False; GATE=FAIL (0.6B->1.7B +0.0729 [+0.0541,+0.0915]; 1.7B->4B +0.0231 [+0.0012,+0.0471]; 4B->8B +0.0239 [+0.0080,+0.0412]; 8B->14B +0.0086 [-0.0047,+0.0223]; 14B->32B -0.0000 [-0.0158,+0.0152])
- base ladder: 0.6B 0.4120, 1.7B 0.4629, 4B 0.4977, 8B 0.4947, 14B 0.5128; monotone=False; GATE=FAIL (0.6B->1.7B +0.0509 [+0.0387,+0.0661]; 1.7B->4B +0.0348 [+0.0207,+0.0503]; 4B->8B -0.0029 [-0.0118,+0.0071]; 8B->14B +0.0181 [+0.0094,+0.0264])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0586 [-0.0829,-0.0370] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0441 [-0.0656,-0.0257] | <0.50x | -1.00 [-1.00,-0.84] | 0.94/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0481 [-0.0709,-0.0290] | <0.50x | -1.00 [-1.00,-0.99] | 0.97/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0707 [-0.0946,-0.0476] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0498 [-0.0657,-0.0346] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0053 [-0.0087,-0.0021] | 0.87x | -0.21 [-0.72,-0.07] | 0.01/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0059 [-0.0181,+0.0076] | 0.85x | -0.23 [-0.96,+0.51] | 0.02/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0172 [-0.0320,-0.0016] | 0.63x | -0.67 [-1.00,-0.06] | 0.24/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0529 [-0.0748,-0.0353] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0584 [-0.0721,-0.0447] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | -0.0005 [-0.0078,+0.0072] | 0.97x | -0.05 [-1.00,+1.24] | 0.06/0.33 |
| SERA-14B | Qwen3-14B (inst) | -0.0633 [-0.0876,-0.0405] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0595 [-0.0860,-0.0334] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0261 [+0.0117,+0.0384] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0298 [-0.0469,-0.0151] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.1415 [-0.1873,-0.0958] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0485 [-0.0685,-0.0313] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0577 [-0.0738,-0.0415] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | -0.0040 [-0.0110,+0.0023] | 0.90x | -0.16 [-0.58,+1.16] | 0.01/0.02 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0270 [-0.0409,-0.0131] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | -0.0050 [-0.0285,+0.0161] | 0.89x | -0.17 [-0.82,+0.75] | 0.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0167 [-0.0357,-0.0009] | 0.63x | -0.66 [-1.00,-0.04] | 0.12/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0101 [-0.0043,+0.0249] | 1.54x | +0.62 [-1.00,+0.93] | 0.05/0.35 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0007 [-0.0103,+0.0132] | >1.00x | +0.00 [-0.74,+0.00] | 0.01/0.53 |

## M2 relative gain [content/kind=search] (higher is better)

- inst ladder: 0.6B 0.0453, 1.7B 0.0792, 4B 0.0937, 8B 0.1087, 14B 0.1359, 32B 0.1253; monotone=False; GATE=FAIL (0.6B->1.7B +0.0339 [+0.0141,+0.0627]; 1.7B->4B +0.0144 [-0.0060,+0.0423]; 4B->8B +0.0150 [-0.0046,+0.0342]; 8B->14B +0.0272 [+0.0086,+0.0570]; 14B->32B -0.0105 [-0.0338,+0.0130])
- base ladder: 0.6B 0.0417, 1.7B 0.0608, 4B 0.0911, 8B 0.1034, 14B 0.1161; monotone=True; GATE=PASS (0.6B->1.7B +0.0191 [+0.0082,+0.0357]; 1.7B->4B +0.0302 [+0.0164,+0.0526]; 4B->8B +0.0123 [+0.0041,+0.0256]; 8B->14B +0.0127 [+0.0006,+0.0291])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0342 [-0.0600,-0.0083] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | +0.0023 [-0.0216,+0.0275] | 1.06x | +0.08 [-1.00,+0.75] | 0.05/0.01 |
| tmax-8b | Qwen3-8B (inst) | +0.0113 [-0.0180,+0.0413] | 1.31x | +0.39 [-0.74,+2.00] | 0.02/0.10 |
| SERA-8B | Qwen3-8B (inst) | +0.0029 [-0.0169,+0.0274] | 1.07x | +0.10 [-1.00,+0.77] | 0.04/0.01 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0386 [-0.0615,-0.0184] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0008 [-0.0048,+0.0026] | 0.97x | -0.05 [-1.00,+0.10] | 0.03/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0040 [-0.0202,+0.0140] | 0.84x | -0.25 [-1.00,+0.40] | 0.07/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0071 [-0.0291,+0.0158] | 0.74x | -0.44 [-1.00,+0.39] | 0.22/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0287 [-0.0551,-0.0111] | <0.50x | -1.00 [-1.00,-0.85] | 0.95/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0452 [-0.0740,-0.0212] | <0.50x | -1.00 [-1.00,-0.69] | 0.91/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0147 [+0.0019,+0.0292] | >2.36x | +1.24 [+0.41,+1.24] | 0.00/0.94 |
| SERA-14B | Qwen3-14B (inst) | -0.0275 [-0.0498,-0.0099] | 0.52x | -0.95 [-1.00,-0.28] | 0.44/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0053 [-0.0435,+0.0560] | >2.36x | +1.24 [-1.00,+1.24] | 0.14/0.54 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0003 [-0.0171,+0.0169] | 0.99x | -0.01 [-0.83,+1.24] | 0.01/0.46 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0107 [-0.0342,+0.0066] | <0.50x | -1.00 [-1.00,+0.00] | 0.85/0.13 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0031 [-0.0366,+0.0277] | <0.50x | -1.00 [-1.00,+0.00] | 0.58/0.40 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0289 [-0.0499,-0.0154] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0254 [-0.0488,-0.0106] | <0.50x | -1.00 [-1.00,-0.84] | 0.95/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0090 [-0.0018,+0.0260] | 1.24x | +0.31 [-0.12,+2.00] | 0.00/0.06 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0036 [-0.0054,+0.0145] | 1.24x | +0.32 [+0.00,+1.73] | 0.20/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0184 [-0.0053,+0.0493] | 1.78x | +0.83 [-0.33,+2.00] | 0.00/0.06 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0026 [-0.0172,+0.0277] | 1.15x | +0.20 [-0.81,+1.61] | 0.01/0.02 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0053 [-0.0179,+0.0279] | 1.31x | +0.39 [-1.00,+0.93] | 0.05/0.26 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0198 [+0.0021,+0.0431] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/0.99 |

## M2 relative gain [content/kind=shell_other] (higher is better)

- inst ladder: 0.6B 0.0437, 1.7B 0.0782, 4B 0.1104, 8B 0.1592, 14B 0.1575, 32B 0.1732; monotone=False; GATE=FAIL (0.6B->1.7B +0.0345 [+0.0210,+0.0499]; 1.7B->4B +0.0323 [+0.0069,+0.0602]; 4B->8B +0.0488 [+0.0286,+0.0735]; 8B->14B -0.0017 [-0.0188,+0.0161]; 14B->32B +0.0157 [-0.0021,+0.0341])
- base ladder: 0.6B 0.0522, 1.7B 0.1023, 4B 0.1381, 8B 0.1399, 14B 0.1594; monotone=True; GATE=FAIL (0.6B->1.7B +0.0501 [+0.0357,+0.0678]; 1.7B->4B +0.0359 [+0.0205,+0.0570]; 4B->8B +0.0018 [-0.0096,+0.0145]; 8B->14B +0.0195 [+0.0089,+0.0306])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0486 [-0.0721,-0.0276] | 0.52x | -0.93 [-1.00,-0.63] | 0.40/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0023 [-0.0166,+0.0133] | 0.97x | -0.04 [-0.34,+1.86] | 0.00/0.02 |
| tmax-8b | Qwen3-8B (inst) | -0.0015 [-0.0167,+0.0147] | 0.98x | -0.03 [-0.33,+2.00] | 0.00/0.05 |
| SERA-8B | Qwen3-8B (inst) | -0.0499 [-0.0760,-0.0263] | 0.51x | -0.98 [-1.00,-0.63] | 0.48/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0501 [-0.0711,-0.0329] | 0.50x | -0.99 [-1.00,-0.68] | 0.47/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | +0.0000 [-0.0043,+0.0044] | 1.91x | +0.93 [-0.09,+2.00] | 0.00/0.07 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0198 [-0.0329,-0.0082] | 0.77x | -0.38 [-0.72,-0.15] | 0.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0188 [-0.0319,-0.0057] | 0.78x | -0.36 [-0.61,-0.13] | 0.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0733 [-0.1109,-0.0469] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0382 [-0.0564,-0.0236] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | -0.0096 [-0.0201,-0.0002] | <0.50x | -1.00 [-1.00,-0.04] | 0.72/0.01 |
| SERA-14B | Qwen3-14B (inst) | -0.0262 [-0.0465,-0.0080] | <0.50x | -1.00 [-1.00,-0.94] | 0.96/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0243 [-0.0143,+0.0562] | >2.36x | +1.24 [-1.00,+1.24] | 0.05/0.73 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0054 [-0.0051,+0.0175] | 1.39x | +0.48 [-0.99,+1.24] | 0.02/0.20 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0042 [-0.0187,+0.0097] | 0.77x | -0.37 [-1.00,+0.00] | 0.14/0.28 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0751 [-0.1179,-0.0361] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0292 [-0.0517,-0.0136] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0401 [-0.0620,-0.0224] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0008 [-0.0050,+0.0062] | 1.99x | +1.00 [-0.10,+2.00] | 0.00/0.12 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0085 [-0.0203,+0.0003] | <1.00x | +0.00 [+0.00,+0.01] | 0.97/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | -0.0241 [-0.0459,-0.0049] | 0.57x | -0.81 [-1.00,-0.21] | 0.24/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0277 [-0.0476,-0.0126] | <0.50x | -1.00 [-1.00,-0.48] | 0.59/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0193 [+0.0006,+0.0341] | 1.89x | +0.92 [+0.03,+0.93] | 0.01/0.54 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | -0.0019 [-0.0184,+0.0135] | 0.94x | -0.09 [-0.91,+0.00] | 0.02/0.40 |

## M2 relative gain [content/kind=test_run] (higher is better)

- inst ladder: 0.6B 0.0710, 1.7B 0.1055, 4B 0.1206, 8B 0.1358, 14B 0.1350, 32B 0.1347; monotone=False; GATE=FAIL (0.6B->1.7B +0.0346 [+0.0217,+0.0486]; 1.7B->4B +0.0151 [+0.0047,+0.0288]; 4B->8B +0.0151 [+0.0060,+0.0243]; 8B->14B -0.0008 [-0.0070,+0.0064]; 14B->32B -0.0003 [-0.0085,+0.0088])
- base ladder: 0.6B 0.0768, 1.7B 0.0963, 4B 0.1140, 8B 0.1158, 14B 0.1244; monotone=True; GATE=FAIL (0.6B->1.7B +0.0195 [+0.0122,+0.0291]; 1.7B->4B +0.0176 [+0.0115,+0.0264]; 4B->8B +0.0018 [-0.0044,+0.0075]; 8B->14B +0.0086 [+0.0043,+0.0141])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0415 [-0.0556,-0.0273] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0266 [-0.0373,-0.0165] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0247 [-0.0360,-0.0140] | <0.50x | -1.00 [-1.00,-0.93] | 0.97/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0347 [-0.0491,-0.0219] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0335 [-0.0440,-0.0232] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0036 [-0.0055,-0.0017] | 0.86x | -0.22 [-0.57,-0.09] | 0.01/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0166 [-0.0231,-0.0105] | <0.50x | -1.00 [-1.00,-0.63] | 0.55/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0279 [-0.0372,-0.0192] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0319 [-0.0486,-0.0196] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0319 [-0.0450,-0.0197] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0135 [+0.0073,+0.0196] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0273 [-0.0414,-0.0142] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0355 [-0.0885,+0.0143] | <0.50x | -1.00 [-1.00,+1.24] | 0.90/0.08 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0039 [-0.0007,+0.0091] | >2.36x | +1.24 [-0.93,+1.24] | 0.00/0.89 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0180 [-0.0275,-0.0107] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0606 [-0.0990,-0.0257] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0215 [-0.0335,-0.0108] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0214 [-0.0332,-0.0126] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0019 [-0.0018,+0.0056] | >4.00x | +2.00 [-0.13,+2.00] | 0.00/0.55 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0058 [-0.0138,-0.0003] | <1.00x | +0.00 [+0.00,+0.00] | 0.98/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0092 [-0.0027,+0.0200] | 1.64x | +0.71 [-0.19,+2.00] | 0.00/0.07 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0067 [-0.0011,+0.0151] | 2.74x | +1.45 [-0.08,+1.86] | 0.00/0.19 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0200 [+0.0110,+0.0288] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/0.99 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0105 [+0.0033,+0.0182] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## M2 relative gain [outcome/all] (higher is better)

- inst ladder: 0.6B 0.0927, 1.7B 0.1215, 4B 0.1236, 8B 0.1521, 14B 0.1526, 32B 0.1487; monotone=False; GATE=FAIL (0.6B->1.7B +0.0289 [+0.0163,+0.0426]; 1.7B->4B +0.0021 [-0.0085,+0.0136]; 4B->8B +0.0285 [+0.0162,+0.0413]; 8B->14B +0.0005 [-0.0090,+0.0107]; 14B->32B -0.0039 [-0.0129,+0.0064])
- base ladder: 0.6B 0.1028, 1.7B 0.1208, 4B 0.1356, 8B 0.1381, 14B 0.1446; monotone=True; GATE=FAIL (0.6B->1.7B +0.0180 [+0.0118,+0.0259]; 1.7B->4B +0.0148 [+0.0090,+0.0210]; 4B->8B +0.0024 [-0.0033,+0.0092]; 8B->14B +0.0065 [+0.0005,+0.0134])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0361 [-0.0517,-0.0214] | <0.50x | -1.00 [-1.00,-0.80] | 0.91/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0229 [-0.0369,-0.0100] | 0.59x | -0.75 [-1.00,-0.36] | 0.24/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0225 [-0.0372,-0.0094] | 0.60x | -0.74 [-1.00,-0.35] | 0.22/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0365 [-0.0539,-0.0219] | <0.50x | -1.00 [-1.00,-0.77] | 0.87/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0294 [-0.0405,-0.0191] | <0.50x | -1.00 [-1.00,-0.68] | 0.64/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0026 [-0.0050,-0.0002] | 0.94x | -0.09 [-0.21,-0.01] | 0.00/0.01 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0047 [-0.0135,+0.0035] | 0.90x | -0.15 [-0.44,+2.00] | 0.00/0.03 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0178 [-0.0282,-0.0076] | 0.67x | -0.58 [-1.00,-0.31] | 0.05/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0205 [-0.0331,-0.0102] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0289 [-0.0398,-0.0181] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0040 [-0.0019,+0.0094] | >2.36x | +1.24 [-0.95,+1.24] | 0.01/0.86 |
| SERA-14B | Qwen3-14B (inst) | -0.0258 [-0.0409,-0.0109] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0562 [-0.1142,+0.0061] | <0.50x | -1.00 [-1.00,+1.24] | 0.94/0.04 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0166 [+0.0092,+0.0249] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0140 [-0.0226,-0.0047] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | -0.0651 [-0.1046,-0.0284] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | -0.0221 [-0.0333,-0.0125] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | -0.0209 [-0.0313,-0.0118] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0004 [-0.0037,+0.0040] | 1.69x | +0.76 [-0.14,+2.00] | 0.00/0.32 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0102 [-0.0175,-0.0036] | <1.00x | +0.00 [+0.00,+0.00] | 1.00/0.00 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0007 [-0.0121,+0.0116] | 1.04x | +0.06 [-1.00,+1.20] | 0.04/0.01 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | -0.0120 [-0.0238,-0.0017] | <0.50x | -1.00 [-1.00,-0.17] | 0.57/0.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0140 [+0.0021,+0.0254] | >1.90x | +0.93 [+0.34,+0.93] | 0.00/0.88 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0080 [-0.0017,+0.0172] | >1.00x | +0.00 [-0.24,+0.00] | 0.01/0.96 |

## Reading: next-action bits/tok saved by seeing the obs [all] (higher is better)

- inst ladder: 0.6B 0.0249, 1.7B 0.0400, 4B 0.0502, 8B 0.0595, 14B 0.0306, 32B 0.0246; monotone=False; GATE=FAIL (0.6B->1.7B +0.0151 [+0.0070,+0.0234]; 1.7B->4B +0.0102 [+0.0022,+0.0184]; 4B->8B +0.0092 [+0.0024,+0.0168]; 8B->14B -0.0289 [-0.0365,-0.0220]; 14B->32B -0.0060 [-0.0093,-0.0028])
- base ladder: 0.6B 0.0187, 1.7B 0.0215, 4B 0.0228, 8B 0.0217, 14B 0.0205; monotone=False; GATE=FAIL (0.6B->1.7B +0.0028 [+0.0010,+0.0045]; 1.7B->4B +0.0013 [-0.0006,+0.0032]; 4B->8B -0.0011 [-0.0025,+0.0002]; 8B->14B -0.0012 [-0.0026,+0.0002])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0316 [-0.0397,-0.0248] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0283 [-0.0361,-0.0212] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0245 [-0.0326,-0.0171] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0233 [-0.0298,-0.0177] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0342 [-0.0411,-0.0278] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0042 [-0.0058,-0.0026] | 0.75x | -0.42 [-1.00,-0.23] | 0.04/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0332 [-0.0393,-0.0276] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0321 [-0.0393,-0.0252] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0075 [+0.0030,+0.0122] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0057 [-0.0088,-0.0028] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0119 [+0.0083,+0.0155] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0019 [-0.0050,+0.0010] | <0.50x | -1.00 [-1.00,+1.24] | 0.76/0.11 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0003 [-0.0034,+0.0027] | 0.51x | -0.96 [-1.00,+1.24] | 0.42/0.41 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0008 [-0.0016,+0.0030] | >2.36x | +1.24 [-1.00,+1.24] | 0.13/0.74 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0023 [+0.0003,+0.0045] | >1.00x | +0.00 [+0.00,+0.00] | 0.02/0.98 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0169 [+0.0124,+0.0219] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0062 [+0.0038,+0.0085] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0045 [+0.0022,+0.0066] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0038 [+0.0021,+0.0056] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0062 [+0.0021,+0.0102] | >4.00x | +2.00 [+1.11,+2.00] | 0.00/0.91 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0186 [+0.0089,+0.0289] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0274 [+0.0202,+0.0353] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0378 [+0.0300,+0.0467] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0101 [+0.0071,+0.0133] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## Reading: next-action bits/tok saved by seeing the obs [kind=edit_ack] (higher is better)

- inst ladder: 0.6B 0.0008, 1.7B 0.0392, 4B 0.0343, 8B 0.0320, 14B 0.0112, 32B 0.0135; monotone=False; GATE=FAIL (0.6B->1.7B +0.0385 [+0.0094,+0.0701]; 1.7B->4B -0.0050 [-0.0388,+0.0306]; 4B->8B -0.0023 [-0.0327,+0.0292]; 8B->14B -0.0208 [-0.0401,-0.0047]; 14B->32B +0.0023 [-0.0141,+0.0201])
- base ladder: 0.6B -0.0004, 1.7B 0.0033, 4B 0.0086, 8B 0.0053, 14B 0.0044; monotone=False; GATE=FAIL (0.6B->1.7B +0.0037 [-0.0045,+0.0118]; 1.7B->4B +0.0053 [-0.0009,+0.0119]; 4B->8B -0.0033 [-0.0122,+0.0048]; 8B->14B -0.0008 [-0.0069,+0.0088])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0262 [-0.0425,-0.0112] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0232 [-0.0405,-0.0054] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0291 [-0.0493,-0.0099] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0306 [-0.0480,-0.0139] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0357 [-0.0532,-0.0209] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0024 [-0.0091,+0.0041] | <0.50x | -1.00 [-1.00,+2.00] | 0.65/0.23 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0273 [-0.0404,-0.0125] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0183 [-0.0349,+0.0001] | <0.50x | -1.00 [-1.00,+2.00] | 0.97/0.03 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0030 [-0.0085,+0.0157] | >1.90x | +0.93 [-1.00,+0.93] | 0.25/0.70 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0060 [-0.0210,+0.0081] | <0.50x | -1.00 [-1.00,+1.24] | 0.81/0.19 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0071 [-0.0060,+0.0253] | >2.36x | +1.24 [-1.00,+1.24] | 0.13/0.87 |
| SERA-14B | Qwen3-14B (inst) | -0.0002 [-0.0157,+0.0171] | <0.50x | -1.00 [-1.00,+1.24] | 0.50/0.49 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0022 [-0.0157,+0.0128] | <0.50x | -1.00 [-1.00,+1.24] | 0.61/0.38 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0013 [-0.0055,+0.0100] | >2.36x | +1.24 [-1.00,+1.24] | 0.37/0.62 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | -0.0096 [-0.0251,+0.0008] | <0.50x | -1.00 [-1.00,+0.00] | 0.96/0.04 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0019 [-0.0123,+0.0133] | >1.00x | +0.00 [-1.00,+0.00] | 0.39/0.61 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0005 [-0.0052,+0.0074] | >1.90x | +0.93 [-1.00,+0.93] | 0.37/0.54 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0008 [-0.0088,+0.0095] | >1.00x | +0.00 [-1.00,+0.00] | 0.45/0.54 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | -0.0060 [-0.0143,+0.0007] | <0.50x | -1.00 [-1.00,+2.00] | 0.88/0.04 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0011 [-0.0097,+0.0168] | 1.42x | +0.51 [+0.00,+2.00] | 0.42/0.23 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0359 [+0.0109,+0.0695] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0257 [+0.0030,+0.0538] | >3.64x | +1.86 [+1.86,+1.86] | 0.01/0.99 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0267 [+0.0086,+0.0465] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0068 [-0.0043,+0.0193] | >1.00x | +0.00 [-1.00,+0.00] | 0.12/0.87 |

## Reading: next-action bits/tok saved by seeing the obs [kind=file_view] (higher is better)

- inst ladder: 0.6B 0.0497, 1.7B 0.0844, 4B 0.0884, 8B 0.0925, 14B 0.0519, 32B 0.0367; monotone=False; GATE=FAIL (0.6B->1.7B +0.0347 [+0.0073,+0.0685]; 1.7B->4B +0.0040 [-0.0152,+0.0265]; 4B->8B +0.0042 [-0.0086,+0.0167]; 8B->14B -0.0406 [-0.0656,-0.0207]; 14B->32B -0.0152 [-0.0256,-0.0072])
- base ladder: 0.6B 0.0294, 1.7B 0.0334, 4B 0.0356, 8B 0.0342, 14B 0.0313; monotone=False; GATE=FAIL (0.6B->1.7B +0.0040 [-0.0013,+0.0096]; 1.7B->4B +0.0022 [-0.0024,+0.0070]; 4B->8B -0.0014 [-0.0069,+0.0030]; 8B->14B -0.0030 [-0.0071,+0.0009])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0475 [-0.0793,-0.0232] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0479 [-0.0810,-0.0248] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0431 [-0.0757,-0.0200] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0442 [-0.0724,-0.0226] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0463 [-0.0722,-0.0255] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0057 [-0.0112,-0.0008] | <0.50x | -1.00 [-1.00,-0.13] | 0.66/0.01 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0508 [-0.0803,-0.0300] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0430 [-0.0759,-0.0208] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0147 [-0.0020,+0.0356] | >1.90x | +0.93 [-1.00,+0.93] | 0.03/0.95 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0143 [-0.0270,-0.0039] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0120 [+0.0050,+0.0210] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0116 [-0.0203,-0.0028] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0042 [-0.0134,+0.0054] | <0.50x | -1.00 [-1.00,+1.24] | 0.79/0.19 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0052 [-0.0103,-0.0002] | <0.50x | -1.00 [-1.00,-1.00] | 0.97/0.02 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0027 [-0.0044,+0.0094] | >1.00x | +0.00 [-1.00,+0.00] | 0.20/0.80 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0258 [+0.0133,+0.0428] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0108 [+0.0035,+0.0195] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0064 [+0.0003,+0.0137] | >1.00x | +0.00 [+0.00,+0.00] | 0.01/0.98 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0048 [+0.0014,+0.0089] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0202 [+0.0086,+0.0355] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/0.99 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0510 [+0.0197,+0.0965] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0528 [+0.0273,+0.0925] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0583 [+0.0318,+0.0938] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0206 [+0.0098,+0.0360] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## Reading: next-action bits/tok saved by seeing the obs [kind=python_exec] (higher is better)

- inst ladder: 0.6B -0.0018, 1.7B -0.0167, 4B 0.0127, 8B 0.0114, 14B 0.0014, 32B 0.0048; monotone=False; GATE=FAIL (0.6B->1.7B -0.0149 [-0.0270,-0.0032]; 1.7B->4B +0.0294 [+0.0182,+0.0425]; 4B->8B -0.0014 [-0.0106,+0.0078]; 8B->14B -0.0100 [-0.0177,-0.0029]; 14B->32B +0.0035 [-0.0006,+0.0077])
- base ladder: 0.6B -0.0005, 1.7B 0.0035, 4B 0.0031, 8B 0.0034, 14B 0.0027; monotone=False; GATE=FAIL (0.6B->1.7B +0.0040 [+0.0019,+0.0063]; 1.7B->4B -0.0004 [-0.0024,+0.0015]; 4B->8B +0.0003 [-0.0010,+0.0017]; 8B->14B -0.0007 [-0.0026,+0.0012])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0067 [-0.0134,-0.0000] | <0.50x | -1.00 [-1.00,-0.63] | 0.94/0.02 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0017 [-0.0081,+0.0045] | <0.50x | -1.00 [-1.00,+2.00] | 0.45/0.33 |
| tmax-8b | Qwen3-8B (inst) | +0.0052 [-0.0020,+0.0129] | >4.00x | +2.00 [-0.96,+2.00] | 0.02/0.93 |
| SERA-8B | Qwen3-8B (inst) | -0.0008 [-0.0088,+0.0066] | <0.50x | -1.00 [-1.00,+2.00] | 0.39/0.42 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0122 [-0.0205,-0.0040] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0009 [-0.0030,+0.0012] | <0.50x | -1.00 [-1.00,+2.00] | 0.36/0.20 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0096 [-0.0151,-0.0044] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0088 [-0.0151,-0.0031] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | -0.0017 [-0.0054,+0.0018] | <0.50x | -1.00 [-1.00,+0.93] | 0.78/0.18 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | +0.0020 [-0.0022,+0.0061] | >2.36x | +1.24 [-1.00,+1.24] | 0.15/0.84 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0037 [+0.0001,+0.0077] | >2.36x | +1.24 [+1.24,+1.24] | 0.02/0.98 |
| SERA-14B | Qwen3-14B (inst) | +0.0034 [-0.0001,+0.0072] | >2.36x | +1.24 [-1.00,+1.24] | 0.03/0.97 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0015 [-0.0020,+0.0050] | >2.36x | +1.24 [-1.00,+1.24] | 0.20/0.80 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0046 [+0.0017,+0.0077] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0002 [-0.0028,+0.0028] | >1.00x | +0.00 [-1.00,+0.00] | 0.43/0.56 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0069 [+0.0026,+0.0112] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0014 [-0.0014,+0.0040] | >1.90x | +0.93 [-1.00,+0.93] | 0.12/0.84 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0007 [-0.0023,+0.0033] | >1.00x | +0.00 [-1.00,+0.00] | 0.33/0.66 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0069 [+0.0041,+0.0102] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | -0.0013 [-0.0053,+0.0027] | <1.00x | +0.00 [+0.00,+1.14] | 0.74/0.01 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | -0.0202 [-0.0308,-0.0109] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0097 [+0.0030,+0.0172] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/0.99 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0080 [+0.0017,+0.0149] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | -0.0013 [-0.0044,+0.0014] | <0.50x | -1.00 [-1.00,+0.00] | 0.82/0.17 |

## Reading: next-action bits/tok saved by seeing the obs [kind=search] (higher is better)

- inst ladder: 0.6B 0.0612, 1.7B 0.0927, 4B 0.0847, 8B 0.1324, 14B 0.0753, 32B 0.0667; monotone=False; GATE=FAIL (0.6B->1.7B +0.0315 [+0.0007,+0.0748]; 1.7B->4B -0.0079 [-0.0422,+0.0209]; 4B->8B +0.0477 [+0.0178,+0.0945]; 8B->14B -0.0571 [-0.1097,-0.0272]; 14B->32B -0.0086 [-0.0283,+0.0065])
- base ladder: 0.6B 0.0475, 1.7B 0.0478, 4B 0.0464, 8B 0.0515, 14B 0.0449; monotone=False; GATE=FAIL (0.6B->1.7B +0.0003 [-0.0065,+0.0080]; 1.7B->4B -0.0014 [-0.0113,+0.0059]; 4B->8B +0.0051 [-0.0002,+0.0141]; 8B->14B -0.0066 [-0.0169,+0.0010])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0629 [-0.1199,-0.0295] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0562 [-0.1080,-0.0250] | <0.50x | -1.00 [-1.00,-0.84] | 0.93/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0363 [-0.0831,-0.0070] | 0.55x | -0.85 [-1.00,-0.29] | 0.43/0.01 |
| SERA-8B | Qwen3-8B (inst) | -0.0275 [-0.0579,-0.0057] | 0.64x | -0.65 [-1.00,-0.22] | 0.23/0.01 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0565 [-0.1073,-0.0232] | <0.50x | -1.00 [-1.00,-0.72] | 0.89/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0075 [-0.0156,-0.0005] | 0.88x | -0.18 [-1.00,-0.01] | 0.04/0.01 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0606 [-0.1087,-0.0327] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0676 [-0.1285,-0.0317] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0113 [-0.0023,+0.0299] | >1.90x | +0.93 [-0.35,+0.93] | 0.01/0.96 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0102 [-0.0268,+0.0042] | <0.50x | -1.00 [-1.00,+1.24] | 0.85/0.08 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0286 [+0.0118,+0.0532] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | +0.0007 [-0.0148,+0.0199] | >2.36x | +1.24 [-1.00,+1.24] | 0.35/0.53 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0139 [-0.0023,+0.0394] | >2.36x | +1.24 [-1.00,+1.24] | 0.03/0.95 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0056 [-0.0046,+0.0202] | >2.36x | +1.24 [-1.00,+1.24] | 0.07/0.84 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0086 [-0.0019,+0.0212] | >1.00x | +0.00 [-1.00,+0.00] | 0.04/0.96 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0520 [+0.0203,+0.1067] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0180 [+0.0085,+0.0351] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0202 [+0.0079,+0.0428] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | +0.0199 [+0.0119,+0.0360] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0137 [+0.0011,+0.0318] | >4.00x | +2.00 [+0.93,+2.00] | 0.01/0.95 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0448 [+0.0136,+0.1016] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/0.99 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0384 [+0.0157,+0.0757] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0809 [+0.0414,+0.1513] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0304 [+0.0115,+0.0613] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## Reading: next-action bits/tok saved by seeing the obs [kind=shell_other] (higher is better)

- inst ladder: 0.6B 0.0870, 1.7B 0.1376, 4B 0.1179, 8B 0.1240, 14B 0.0918, 32B 0.0727; monotone=False; GATE=FAIL (0.6B->1.7B +0.0506 [+0.0144,+0.0950]; 1.7B->4B -0.0197 [-0.0599,+0.0211]; 4B->8B +0.0061 [-0.0210,+0.0345]; 8B->14B -0.0322 [-0.0739,-0.0016]; 14B->32B -0.0191 [-0.0391,-0.0037])
- base ladder: 0.6B 0.0786, 1.7B 0.0733, 4B 0.0769, 8B 0.0698, 14B 0.0701; monotone=False; GATE=FAIL (0.6B->1.7B -0.0053 [-0.0185,+0.0061]; 1.7B->4B +0.0036 [-0.0067,+0.0137]; 4B->8B -0.0071 [-0.0139,-0.0011]; 8B->14B +0.0004 [-0.0060,+0.0067])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0371 [-0.0814,-0.0061] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0325 [-0.0749,-0.0018] | <0.50x | -1.00 [-1.00,-1.00] | 0.98/0.02 |
| tmax-8b | Qwen3-8B (inst) | -0.0344 [-0.0769,-0.0035] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| SERA-8B | Qwen3-8B (inst) | -0.0269 [-0.0649,+0.0015] | <0.50x | -1.00 [-1.00,+2.00] | 0.96/0.04 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0353 [-0.0738,-0.0062] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0061 [-0.0143,+0.0024] | <0.50x | -1.00 [-1.00,+2.00] | 0.84/0.08 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0430 [-0.0816,-0.0169] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0425 [-0.0842,-0.0130] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0166 [-0.0180,+0.0592] | >1.90x | +0.93 [-1.00,+0.93] | 0.20/0.80 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0161 [-0.0339,-0.0043] | <0.50x | -1.00 [-1.00,-1.00] | 0.99/0.01 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0213 [+0.0077,+0.0396] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | -0.0134 [-0.0317,+0.0012] | <0.50x | -1.00 [-1.00,+1.24] | 0.96/0.03 |
| FrogMini-14B | Qwen3-14B (inst) | -0.0119 [-0.0286,+0.0027] | <0.50x | -1.00 [-1.00,+1.24] | 0.94/0.06 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | +0.0025 [-0.0058,+0.0093] | >2.36x | +1.24 [-1.00,+1.24] | 0.26/0.73 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0056 [-0.0027,+0.0149] | >1.00x | +0.00 [-1.00,+0.00] | 0.09/0.92 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0365 [+0.0191,+0.0634] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0172 [+0.0063,+0.0311] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0056 [-0.0009,+0.0139] | >1.00x | +0.00 [-1.00,+0.00] | 0.05/0.95 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | -0.0019 [-0.0093,+0.0055] | <0.50x | -1.00 [-1.00,+2.00] | 0.60/0.30 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0084 [-0.0078,+0.0270] | >4.00x | +2.00 [+0.00,+2.00] | 0.17/0.77 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0643 [+0.0173,+0.1291] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/0.99 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0410 [+0.0062,+0.0862] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/0.99 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0542 [+0.0170,+0.1069] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0216 [+0.0077,+0.0432] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |

## Reading: next-action bits/tok saved by seeing the obs [kind=test_run] (higher is better)

- inst ladder: 0.6B 0.0169, 1.7B 0.0371, 4B 0.0443, 8B 0.0617, 14B 0.0250, 32B 0.0170; monotone=False; GATE=FAIL (0.6B->1.7B +0.0202 [+0.0093,+0.0329]; 1.7B->4B +0.0072 [-0.0039,+0.0198]; 4B->8B +0.0173 [+0.0067,+0.0298]; 8B->14B -0.0366 [-0.0515,-0.0253]; 14B->32B -0.0080 [-0.0135,-0.0033])
- base ladder: 0.6B 0.0122, 1.7B 0.0157, 4B 0.0181, 8B 0.0159, 14B 0.0160; monotone=False; GATE=FAIL (0.6B->1.7B +0.0035 [+0.0000,+0.0072]; 1.7B->4B +0.0024 [-0.0009,+0.0059]; 4B->8B -0.0022 [-0.0049,+0.0001]; 8B->14B +0.0000 [-0.0030,+0.0030])

| model | start (ladder) | Δ [95% CI] | n (size multiplier) | log2 n [95% CI] | censored draws low/high |
|---|---|---|---|---|---|
| Nemotron-Terminal-8B | Qwen3-8B (inst) | -0.0423 [-0.0575,-0.0313] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-sft-8b | Qwen3-8B (inst) | -0.0399 [-0.0542,-0.0289] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| tmax-8b | Qwen3-8B (inst) | -0.0412 [-0.0570,-0.0298] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| SERA-8B | Qwen3-8B (inst) | -0.0338 [-0.0469,-0.0235] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| OpenThinker-Agent-v1-SFT | Qwen3-8B (inst) | -0.0463 [-0.0598,-0.0363] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Arctic-AWM-8B | Qwen3-8B (inst) | -0.0059 [-0.0100,-0.0024] | 0.80x | -0.32 [-0.68,-0.16] | 0.00/0.00 |
| Light-IF-8B (non-agentic) | Qwen3-8B (inst) | -0.0412 [-0.0532,-0.0324] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| WebWorld-8B (web world model) | Qwen3-8B (inst) | -0.0424 [-0.0574,-0.0313] | <0.50x | -1.00 [-1.00,-1.00] | 1.00/0.00 |
| Klear-Reasoner-8B-SFT (non-agentic, base start) | Qwen3-8B-Base (base) | +0.0106 [+0.0052,+0.0171] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| Nemotron-Terminal-14B | Qwen3-14B (inst) | -0.0051 [-0.0100,-0.0011] | <0.50x | -1.00 [-1.00,-0.98] | 0.96/0.00 |
| CodeScout-14B | Qwen3-14B (inst) | +0.0149 [+0.0092,+0.0225] | >2.36x | +1.24 [+1.24,+1.24] | 0.00/1.00 |
| SERA-14B | Qwen3-14B (inst) | +0.0001 [-0.0049,+0.0049] | >2.36x | +1.24 [-1.00,+1.24] | 0.28/0.51 |
| FrogMini-14B | Qwen3-14B (inst) | +0.0002 [-0.0054,+0.0055] | >2.36x | +1.24 [-1.00,+1.24] | 0.30/0.52 |
| Light-IF-14B (non-agentic) | Qwen3-14B (inst) | -0.0018 [-0.0059,+0.0020] | <0.50x | -1.00 [-1.00,+1.24] | 0.62/0.14 |
| Nemotron-Terminal-32B | Qwen3-32B (inst) | +0.0036 [-0.0001,+0.0078] | >1.00x | +0.00 [-1.00,+0.00] | 0.03/0.97 |
| OpenThinkerAgent-32B | Qwen3-32B (inst) | +0.0107 [+0.0046,+0.0178] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: Nemotron-Terminal-8B vs 8B-Base | Qwen3-8B-Base (base) | +0.0035 [-0.0001,+0.0079] | >1.90x | +0.93 [-1.00,+0.93] | 0.03/0.97 |
| sensitivity: Nemotron-Terminal-14B vs 14B-Base | Qwen3-14B-Base (base) | +0.0040 [+0.0010,+0.0073] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
| sensitivity: tmax-8b vs tmax-sft-8b (RL step) | tmax-sft-8b (inst) | -0.0013 [-0.0055,+0.0021] | 0.95x | -0.07 [-0.35,+2.00] | 0.00/0.25 |
| reference: Qwen3-0.6B instruct vs base | Qwen3-0.6B-Base (base) | +0.0046 [-0.0018,+0.0120] | >4.00x | +2.00 [+0.00,+2.00] | 0.10/0.53 |
| reference: Qwen3-1.7B instruct vs base | Qwen3-1.7B-Base (base) | +0.0214 [+0.0081,+0.0368] | >4.00x | +2.00 [+2.00,+2.00] | 0.00/1.00 |
| reference: Qwen3-4B instruct vs base | Qwen3-4B-Base (base) | +0.0262 [+0.0163,+0.0381] | >3.64x | +1.86 [+1.86,+1.86] | 0.00/1.00 |
| reference: Qwen3-8B instruct vs base | Qwen3-8B-Base (base) | +0.0458 [+0.0337,+0.0615] | >1.90x | +0.93 [+0.93,+0.93] | 0.00/1.00 |
| reference: Qwen3-14B instruct vs base | Qwen3-14B-Base (base) | +0.0091 [+0.0049,+0.0146] | >1.00x | +0.00 [+0.00,+0.00] | 0.00/1.00 |
