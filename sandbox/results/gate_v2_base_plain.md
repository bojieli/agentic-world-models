# Gate: Qwen3-0.6B-Base < Qwen3-1.7B-Base < Qwen3-4B-Base < Qwen3-8B-Base < Qwen3-14B-Base  (render=plain, mask=nocopy, T1, metric=bind, ids=^S(2|3|2h|3h)-)


## S2 (n=900)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.842 [0.819,0.867] |  |
| Qwen3-1.7B-Base | 0.902 [0.882,0.920] | +0.060 [+0.034,+0.084] |
| Qwen3-4B-Base | 0.930 [0.912,0.947] | +0.028 [+0.008,+0.049] |
| Qwen3-8B-Base | 0.928 [0.911,0.944] | -0.002 [-0.022,+0.017] |
| Qwen3-14B-Base | 0.920 [0.901,0.938] | -0.008 [-0.028,+0.010] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## S2h (n=900)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.550 [0.518,0.583] |  |
| Qwen3-1.7B-Base | 0.579 [0.548,0.610] | +0.029 [-0.011,+0.070] |
| Qwen3-4B-Base | 0.688 [0.657,0.719] | +0.109 [+0.068,+0.151] |
| Qwen3-8B-Base | 0.692 [0.663,0.723] | +0.004 [-0.032,+0.041] |
| Qwen3-14B-Base | 0.750 [0.721,0.778] | +0.058 [+0.022,+0.093] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## S3 (n=900)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.627 [0.594,0.659] |  |
| Qwen3-1.7B-Base | 0.732 [0.703,0.761] | +0.106 [+0.069,+0.142] |
| Qwen3-4B-Base | 0.876 [0.854,0.896] | +0.143 [+0.110,+0.176] |
| Qwen3-8B-Base | 0.878 [0.856,0.899] | +0.002 [-0.022,+0.027] |
| Qwen3-14B-Base | 0.901 [0.881,0.921] | +0.023 [-0.000,+0.048] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## S3h (n=900)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.527 [0.494,0.561] |  |
| Qwen3-1.7B-Base | 0.531 [0.499,0.561] | +0.004 [-0.039,+0.048] |
| Qwen3-4B-Base | 0.534 [0.502,0.567] | +0.003 [-0.040,+0.048] |
| Qwen3-8B-Base | 0.588 [0.553,0.619] | +0.053 [+0.012,+0.094] |
| Qwen3-14B-Base | 0.564 [0.533,0.597] | -0.023 [-0.067,+0.019] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## S2+S3 (n=1800)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.734 [0.713,0.754] |  |
| Qwen3-1.7B-Base | 0.817 [0.799,0.835] | +0.083 [+0.061,+0.106] |
| Qwen3-4B-Base | 0.903 [0.889,0.916] | +0.086 [+0.066,+0.105] |
| Qwen3-8B-Base | 0.903 [0.889,0.917] | +0.000 [-0.015,+0.015] |
| Qwen3-14B-Base | 0.911 [0.897,0.924] | +0.008 [-0.007,+0.024] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## S2h+S3h (n=1800)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.538 [0.515,0.561] |  |
| Qwen3-1.7B-Base | 0.555 [0.532,0.578] | +0.017 [-0.014,+0.046] |
| Qwen3-4B-Base | 0.611 [0.588,0.634] | +0.056 [+0.026,+0.087] |
| Qwen3-8B-Base | 0.640 [0.617,0.662] | +0.029 [-0.001,+0.057] |
| Qwen3-14B-Base | 0.657 [0.634,0.678] | +0.017 [-0.010,+0.045] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**

## primary (n=3600)

| model | bind [95% CI] | step Δ vs previous [paired 95% CI] |
|---|---|---|
| Qwen3-0.6B-Base | 0.636 [0.621,0.652] |  |
| Qwen3-1.7B-Base | 0.686 [0.671,0.701] | +0.050 [+0.031,+0.069] |
| Qwen3-4B-Base | 0.757 [0.744,0.771] | +0.071 [+0.053,+0.090] |
| Qwen3-8B-Base | 0.771 [0.758,0.785] | +0.014 [-0.003,+0.030] |
| Qwen3-14B-Base | 0.784 [0.771,0.797] | +0.012 [-0.003,+0.029] |

monotone with every step's paired CI > 0 and top < 0.95: **FAIL**
