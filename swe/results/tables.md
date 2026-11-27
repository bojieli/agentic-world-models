
## Terminus (AgenticPPL)

### M1 recalibrated content code length (bits/token, eval split; T and histogram fitted per model on the calibration split)

| size | role | model | n content | raw | T* | @T* | rank×conf hist | top-1 rate | entropy | loss−entropy | outcome raw | outcome @T* | outcome hist | exec-content hist |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 89962 | 1.137 | 1.0 | 1.137 | 1.226 | 0.821 | 1.044 | 0.093 | 1.132 | 1.132 | 1.229 | 1.323 |
| 0.6B | instruct | Qwen3-0.6B | 89962 | 1.658 | 1.2 | 1.583 | 1.703 | 0.767 | 0.975 | 0.682 | 1.459 | 1.412 | 1.538 | 1.836 |
| 8B | base | Qwen3-8B-Base | 89962 | 0.622 | 1.1 | 0.620 | 0.680 | 0.888 | 0.541 | 0.081 | 0.794 | 0.787 | 0.871 | 0.723 |
| 8B | instruct | Qwen3-8B | 89962 | 1.086 | 1.7 | 0.836 | 0.873 | 0.869 | 0.288 | 0.798 | 1.249 | 0.954 | 1.020 | 0.939 |
| 32B | instruct | Qwen3-32B | 38967 | 0.674 | 1.3 | 0.637 | 0.702 | 0.891 | 0.377 | 0.297 | 0.845 | 0.797 | 0.867 | 0.735 |

### M1 paired log2 ratio vs size-matched reference (negative = fewer bits than the reference; 95% trajectory bootstrap)

| comparison | content raw | content @T* | content hist | outcome @T* | outcome hist | exec-content hist |
|---|---|---|---|---|---|---|
| Qwen3-0.6B vs Qwen3-0.6B-Base | 0.543 [0.496,0.598] | 0.477 [0.429,0.531] | 0.474 [0.426,0.528] | 0.319 [0.288,0.351] | 0.323 [0.293,0.358] | 0.473 [0.409,0.540] |
| Qwen3-8B vs Qwen3-8B-Base | 0.804 [0.747,0.864] | 0.431 [0.402,0.467] | 0.360 [0.332,0.395] | 0.277 [0.248,0.309] | 0.228 [0.199,0.262] | 0.378 [0.339,0.422] |

### M2 action-conditional information gain = 1 − NLL(obs | true action) / NLL(obs | swapped action), content tokens

| size | role | model | n items | gain raw | gain @T* | gain outcome tokens | gain exec kinds | gain non-exec kinds | neg. control (swapA−swapB)/swap |
|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 527 | 0.182 [0.152,0.215] | 0.182 [0.152,0.215] | 0.096 [0.078,0.119] | 0.221 [0.178,0.271] | 0.106 [0.081,0.138] | -0.002 [-0.011,0.005] |
| 0.6B | instruct | Qwen3-0.6B | 527 | 0.138 [0.113,0.166] | 0.139 [0.114,0.168] | 0.068 [0.052,0.087] | 0.171 [0.133,0.212] | 0.074 [0.054,0.099] | -0.002 [-0.008,0.004] |
| 8B | base | Qwen3-8B-Base | 527 | 0.285 [0.252,0.322] | 0.284 [0.250,0.322] | 0.145 [0.121,0.174] | 0.309 [0.265,0.360] | 0.240 [0.202,0.290] | -0.002 [-0.012,0.006] |
| 8B | instruct | Qwen3-8B | 527 | 0.227 [0.198,0.262] | 0.225 [0.195,0.260] | 0.119 [0.091,0.149] | 0.245 [0.210,0.290] | 0.192 [0.154,0.233] | -0.001 [-0.013,0.009] |
| 32B | instruct | Qwen3-32B | 222 | 0.288 [0.242,0.336] | 0.291 [0.243,0.343] | 0.154 [0.109,0.198] | 0.299 [0.243,0.372] | 0.264 [0.214,0.326] | -0.005 [-0.024,0.012] |

### M3 outcome forced choice (true vs 3 foils differing only in the outcome span; LLR over the differing span)

| size | role | model | 4-way acc (n) | balanced | pairwise AUROC | LEAK acc (action+prev turn masked) | full−leak | AF subset acc full / leak (n) | err_class full/leak | number full/leak | first-pytest fail AUROC full / leak | bool False AUROC full / leak | grep no-hit AUROC full / leak |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 0.537 [0.347,0.662] (67) | 0.574 | 0.682 | 0.493 | 0.045 [-0.067,0.062] | 0.162 / 0.081 (37) | 0.667/0.600 | 0.500/0.462 | – / – | 1.000 / 1.000 | – / – |
| 0.6B | instruct | Qwen3-0.6B | 0.507 [0.322,0.588] (67) | 0.515 | 0.682 | 0.448 | 0.060 [0.000,0.130] | 0.189 / 0.081 (37) | 0.533/0.467 | 0.500/0.442 | – / – | 0.917 / 1.000 | – / – |
| 8B | base | Qwen3-8B-Base | 0.642 [0.536,0.758] (67) | 0.702 | 0.756 | 0.642 | 0.000 [-0.048,0.115] | 0.378 / 0.405 (37) | 0.867/0.867 | 0.577/0.577 | – / – | 1.000 / 0.917 | – / – |
| 8B | instruct | Qwen3-8B | 0.672 [0.469,0.760] (67) | 0.702 | 0.781 | 0.627 | 0.045 [0.000,0.131] | 0.432 / 0.378 (37) | 0.800/0.733 | 0.635/0.596 | – / – | 1.000 / 1.000 | – / – |
| 32B | instruct | Qwen3-32B | 0.721 [0.556,0.946] (43) | 0.812 | 0.814 | 0.651 | 0.070 [-0.106,0.512] | 0.520 / 0.440 (25) | 1.000/0.900 | 0.636/0.576 | – / – | – / – | – / – |

### M4 outcome probe (asked before the observation). n = native chat question, p = plain-text few-shot. Coverage = share with Yes+No mass ≥ 0.5; Platt fitted on cal; BSS vs logistic baseline (command type, previous error, kind); stacked = baseline features + model logit

| size | role | model | succ:n cov | succ:n AUROC | succ:n BSS | succ:n stacked BSS | succ:p cov | succ:p AUROC | succ:p BSS | succ:p stacked | tests:n AUROC/BSS | tests:p AUROC/BSS | err-class acc n / p (majority) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 0.00 | – | – | – | 1.00 | 0.56 | -0.02 [-0.03,-0.00] | -0.00 [-0.00,0.00] | –/– | –/– | – / 0.11 (0.62) |
| 0.6B | instruct | Qwen3-0.6B | 1.00 | 0.55 | -0.02 [-0.04,0.00] | -0.00 [-0.00,0.00] | 1.00 | 0.60 | -0.00 [-0.02,0.01] | 0.01 [0.00,0.01] | –/– | –/– | 0.14 / 0.39 (0.62) |
| 8B | base | Qwen3-8B-Base | 0.00 | – | – | – | 1.00 | 0.55 | -0.02 [-0.04,-0.00] | 0.00 [0.00,0.00] | –/– | –/– | – / 0.70 (0.62) |
| 8B | instruct | Qwen3-8B | 1.00 | 0.61 | -0.00 [-0.02,0.01] | 0.02 [0.01,0.03] | 0.99 | 0.53 | -0.01 [-0.03,0.00] | 0.01 [-0.01,0.02] | –/– | –/– | 0.66 / 0.70 (0.62) |
| 32B | instruct | Qwen3-32B | 1.00 | 0.68 | 0.00 [-0.06,0.05] | 0.07 [0.01,0.13] | 1.00 | 0.74 | 0.00 [-0.04,0.04] | 0.04 [0.02,0.07] | –/– | –/– | 0.55 / 0.83 (0.52) |

### Paired differences (M2 gain, M3 accuracy) vs size-matched reference

| comparison | M2 gain raw | M2 gain @T* | M2 gain outcome | M3 4-way acc | M3 full−leak | M3 AF acc | M3 AF full−leak |
|---|---|---|---|---|---|---|---|
| Qwen3-0.6B vs Qwen3-0.6B-Base | -0.044 [-0.053,-0.036] | -0.043 [-0.051,-0.035] | -0.029 [-0.040,-0.021] | -0.030 [-0.215,0.091] | 0.015 [-0.031,0.148] | 0.027 [-0.190,0.238] | 0.027 [-0.062,0.275] |
| Qwen3-8B vs Qwen3-8B-Base | -0.058 [-0.071,-0.045] | -0.059 [-0.068,-0.050] | -0.027 [-0.045,-0.011] | 0.030 [-0.133,0.078] | 0.045 [-0.054,0.147] | 0.054 [-0.240,0.136] | 0.081 [-0.096,0.302] |

## SWE-rebench 2026

### M1 recalibrated content code length (bits/token, eval split; T and histogram fitted per model on the calibration split)

| size | role | model | n content | raw | T* | @T* | rank×conf hist | top-1 rate | entropy | loss−entropy | outcome raw | outcome @T* | outcome hist | exec-content hist |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 558739 | 1.449 | 1.0 | 1.449 | 1.555 | 0.785 | 1.364 | 0.085 | 1.132 | 1.132 | 1.249 | 1.715 |
| 0.6B | instruct | Qwen3-0.6B | 558739 | 1.800 | 1.2 | 1.715 | 1.842 | 0.757 | 1.030 | 0.769 | 1.379 | 1.312 | 1.459 | 2.068 |
| 8B | base | Qwen3-8B-Base | 558739 | 1.021 | 1.0 | 1.021 | 1.098 | 0.833 | 0.969 | 0.052 | 0.860 | 0.859 | 0.950 | 1.174 |
| 8B | instruct | Qwen3-8B | 558739 | 1.462 | 1.6 | 1.190 | 1.253 | 0.822 | 0.445 | 1.017 | 1.177 | 0.975 | 1.063 | 1.341 |
| 32B | instruct | Qwen3-32B | 242536 | 1.015 | 1.2 | 0.987 | 1.067 | 0.839 | 0.698 | 0.317 | 0.853 | 0.833 | 0.927 | 1.168 |

### M1 paired log2 ratio vs size-matched reference (negative = fewer bits than the reference; 95% trajectory bootstrap)

| comparison | content raw | content @T* | content hist | outcome @T* | outcome hist | exec-content hist |
|---|---|---|---|---|---|---|
| Qwen3-0.6B vs Qwen3-0.6B-Base | 0.312 [0.304,0.322] | 0.243 [0.234,0.253] | 0.244 [0.235,0.253] | 0.213 [0.199,0.229] | 0.225 [0.212,0.240] | 0.270 [0.257,0.285] |
| Qwen3-8B vs Qwen3-8B-Base | 0.517 [0.501,0.536] | 0.221 [0.212,0.229] | 0.190 [0.183,0.197] | 0.183 [0.173,0.195] | 0.163 [0.151,0.176] | 0.192 [0.182,0.204] |

### M2 action-conditional information gain = 1 − NLL(obs | true action) / NLL(obs | swapped action), content tokens

| size | role | model | n items | gain raw | gain @T* | gain outcome tokens | gain exec kinds | gain non-exec kinds | neg. control (swapA−swapB)/swap |
|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 444 | 0.102 [0.080,0.129] | 0.102 [0.080,0.129] | 0.102 [0.071,0.134] | 0.139 [0.104,0.178] | 0.042 [0.031,0.055] | -0.006 [-0.018,0.003] |
| 0.6B | instruct | Qwen3-0.6B | 444 | 0.095 [0.075,0.120] | 0.093 [0.074,0.118] | 0.096 [0.070,0.126] | 0.126 [0.094,0.161] | 0.042 [0.031,0.055] | -0.007 [-0.018,0.002] |
| 8B | base | Qwen3-8B-Base | 444 | 0.151 [0.125,0.182] | 0.151 [0.125,0.182] | 0.143 [0.111,0.177] | 0.197 [0.153,0.244] | 0.081 [0.065,0.099] | -0.004 [-0.017,0.007] |
| 8B | instruct | Qwen3-8B | 444 | 0.164 [0.139,0.196] | 0.155 [0.131,0.187] | 0.159 [0.124,0.197] | 0.211 [0.169,0.259] | 0.089 [0.069,0.110] | -0.006 [-0.019,0.005] |
| 32B | instruct | Qwen3-32B | 185 | 0.142 [0.111,0.186] | 0.140 [0.109,0.183] | 0.138 [0.099,0.182] | 0.172 [0.125,0.234] | 0.088 [0.063,0.117] | -0.005 [-0.017,0.006] |

### M3 outcome forced choice (true vs 3 foils differing only in the outcome span; LLR over the differing span)

| size | role | model | 4-way acc (n) | balanced | pairwise AUROC | LEAK acc (action+prev turn masked) | full−leak | AF subset acc full / leak (n) | err_class full/leak | number full/leak | first-pytest fail AUROC full / leak | bool False AUROC full / leak | grep no-hit AUROC full / leak |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 0.694 [0.667,0.737] (598) | 0.679 | 0.814 | 0.701 | -0.007 [-0.024,0.018] | 0.207 / 0.148 (203) | 0.701/0.687 | 0.688/0.693 | 0.708 / 0.681 | 0.882 / 0.833 | 0.636 / 0.620 |
| 0.6B | instruct | Qwen3-0.6B | 0.647 [0.591,0.687] (598) | 0.588 | 0.785 | 0.629 | 0.018 [-0.013,0.049] | 0.232 / 0.182 (203) | 0.493/0.507 | 0.654/0.633 | 0.789 / 0.741 | 0.872 / 0.803 | 0.676 / 0.520 |
| 8B | base | Qwen3-8B-Base | 0.714 [0.684,0.767] (598) | 0.745 | 0.832 | 0.736 | -0.022 [-0.046,0.011] | 0.325 / 0.320 (203) | 0.836/0.851 | 0.689/0.713 | 0.825 / 0.740 | 0.971 / 0.902 | 0.686 / 0.569 |
| 8B | instruct | Qwen3-8B | 0.682 [0.638,0.730] (598) | 0.702 | 0.815 | 0.699 | -0.017 [-0.062,0.018] | 0.281 / 0.276 (203) | 0.776/0.866 | 0.660/0.670 | 0.798 / 0.730 | 0.940 / 0.924 | 0.739 / 0.614 |
| 32B | instruct | Qwen3-32B | 0.714 [0.683,0.776] (315) | 0.771 | 0.837 | 0.717 | -0.003 [-0.044,0.054] | 0.350 / 0.282 (103) | 0.917/0.889 | 0.678/0.693 | 0.896 / 0.796 | 0.968 / 0.927 | 0.787 / 0.581 |

### M4 outcome probe (asked before the observation). n = native chat question, p = plain-text few-shot. Coverage = share with Yes+No mass ≥ 0.5; Platt fitted on cal; BSS vs logistic baseline (command type, previous error, kind); stacked = baseline features + model logit

| size | role | model | succ:n cov | succ:n AUROC | succ:n BSS | succ:n stacked BSS | succ:p cov | succ:p AUROC | succ:p BSS | succ:p stacked | tests:n AUROC/BSS | tests:p AUROC/BSS | err-class acc n / p (majority) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B | base | Qwen3-0.6B-Base | 0.00 | – | – | – | 1.00 | 0.58 | -0.06 [-0.09,-0.04] | 0.00 [-0.00,0.01] | –/– | 0.66/-0.00 | – / 0.16 (0.32) |
| 0.6B | instruct | Qwen3-0.6B | 1.00 | 0.48 | -0.07 [-0.09,-0.04] | 0.00 [-0.00,0.01] | 1.00 | 0.57 | -0.07 [-0.09,-0.04] | -0.03 [-0.06,0.00] | 0.69/0.01 | 0.73/0.04 | 0.24 / 0.23 (0.32) |
| 8B | base | Qwen3-8B-Base | 0.04 | 0.64 | -0.13 [-0.39,-0.03] | -0.17 [-0.60,-0.01] | 1.00 | 0.69 | -0.03 [-0.05,-0.00] | 0.02 [0.01,0.04] | –/– | 0.71/0.07 | – / 0.53 (0.32) |
| 8B | instruct | Qwen3-8B | 1.00 | 0.58 | -0.06 [-0.08,-0.04] | 0.03 [0.02,0.05] | 0.98 | 0.70 | -0.01 [-0.04,0.02] | 0.03 [0.00,0.05] | 0.71/0.09 | 0.71/0.11 | 0.38 / 0.51 (0.32) |
| 32B | instruct | Qwen3-32B | 1.00 | 0.68 | -0.01 [-0.06,0.03] | 0.06 [0.03,0.09] | 0.99 | 0.67 | 0.01 [-0.04,0.06] | 0.07 [0.03,0.12] | 0.72/0.13 | 0.62/0.04 | 0.41 / 0.74 (0.30) |

### Paired differences (M2 gain, M3 accuracy) vs size-matched reference

| comparison | M2 gain raw | M2 gain @T* | M2 gain outcome | M3 4-way acc | M3 full−leak | M3 AF acc | M3 AF full−leak |
|---|---|---|---|---|---|---|---|
| Qwen3-0.6B vs Qwen3-0.6B-Base | -0.008 [-0.013,-0.003] | -0.010 [-0.015,-0.006] | -0.006 [-0.015,0.003] | -0.047 [-0.097,-0.033] | 0.025 [-0.009,0.051] | 0.025 [-0.081,0.056] | -0.010 [-0.104,0.037] |
| Qwen3-8B vs Qwen3-8B-Base | 0.013 [0.007,0.019] | 0.004 [-0.001,0.009] | 0.017 [0.005,0.028] | -0.032 [-0.074,-0.010] | 0.005 [-0.050,0.040] | -0.044 [-0.135,0.011] | 0.000 [-0.112,0.096] |
