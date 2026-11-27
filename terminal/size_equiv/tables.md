models in tok/: Nemotron-Terminal-14B, Nemotron-Terminal-32B, Nemotron-Terminal-8B, Qwen3-0.6B, Qwen3-0.6B-Base, Qwen3-14B, Qwen3-14B-Base, Qwen3-32B, Qwen3-4B, Qwen3-4B-Base, Qwen3-8B, Qwen3-8B-Base

v3 (rank/top1/T-grid present): Nemotron-Terminal-14B, Nemotron-Terminal-32B, Qwen3-0.6B, Qwen3-0.6B-Base, Qwen3-14B, Qwen3-32B

bootstrap: 2000 joint trajectory resamples over 200 eval trajectories; cal trajectories in tok/: 0 -> T and q are 2-fold cross-fitted on eval halves (split seed 0)

token counts: neutral: content=89859, outcome=21810, random=21588, random_novel=12726, hash_novel=8045, boiler=14578, prompt_echo_ws=246718; native: content=89859, outcome=21810, random=21588, random_novel=12726, hash_novel=8045, boiler=14578, prompt_echo_ws=246718


## PRIMARY: size-equivalent by inverse piecewise-linear interpolation (x = log2 non-embedding params)

non-embedding params: 0.6B 0.440B, 1.7B 1.409B, 4B 3.634B, 8B 6.946B, 14B 13.212B, 32B 31.206B

Validity gate: each adjacent ladder step improves with paired 95% CI excluding 0. n is reported only when the gate passes.

| rendering | metric | mask | ladder | models | steps (improvement, 95% CI) | gate |
|---|---|---|---|---|---|---|
| neutral | rankrecal | content | inst | 2 | 14B→32B +0.0560 [+0.0452,+0.0675] | PASS |
| neutral | rankrecal | outcome | inst | 2 | 14B→32B +0.0401 [+0.0308,+0.0495] | PASS |
| neutral | T_cf_content | content | inst | 2 | 14B→32B +0.0787 [+0.0625,+0.0971] | PASS |
| neutral | T_cf_content | outcome | inst | 2 | 14B→32B +0.0511 [+0.0413,+0.0661] | PASS |
| neutral | T_obs_cal | content | base | 4 | 0.6B→4B +0.4310 [+0.3764,+0.4919]; 4B→8B +0.0715 [+0.0555,+0.0921]; 8B→14B +0.0708 [+0.0516,+0.1000] | PASS |
| neutral | T_obs_cal | content | inst | 4 | 4B→8B +0.1575 [+0.1351,+0.1814]; 8B→14B +0.1151 [+0.0931,+0.1424]; 14B→32B +0.0811 [+0.0648,+0.0987] | PASS |
| neutral | T_obs_cal | outcome | base | 4 | 0.6B→4B +0.2757 [+0.2407,+0.3198]; 4B→8B +0.0556 [+0.0428,+0.0695]; 8B→14B +0.0542 [+0.0433,+0.0655] | PASS |
| neutral | T_obs_cal | outcome | inst | 4 | 4B→8B +0.1219 [+0.1016,+0.1440]; 8B→14B +0.0782 [+0.0579,+0.1032]; 14B→32B +0.0571 [+0.0453,+0.0696] | PASS |
| neutral | raw | content | base | 4 | 0.6B→4B +0.4310 [+0.3764,+0.4919]; 4B→8B +0.0715 [+0.0555,+0.0921]; 8B→14B +0.0708 [+0.0516,+0.1000] | PASS |
| neutral | raw | content | inst | 4 | 4B→8B +0.1900 [+0.1642,+0.2168]; 8B→14B +0.1730 [+0.1454,+0.2076]; 14B→32B +0.1528 [+0.1305,+0.1778] | PASS |
| neutral | raw | outcome | base | 4 | 0.6B→4B +0.2757 [+0.2407,+0.3198]; 4B→8B +0.0556 [+0.0428,+0.0695]; 8B→14B +0.0542 [+0.0433,+0.0655] | PASS |
| neutral | raw | outcome | inst | 4 | 4B→8B +0.1411 [+0.1111,+0.1744]; 8B→14B +0.1427 [+0.1123,+0.1782]; 14B→32B +0.1324 [+0.1123,+0.1532] | PASS |
| neutral | capped2 | content | base | 4 | 0.6B→4B +0.1631 [+0.1478,+0.1799]; 4B→8B +0.0294 [+0.0242,+0.0358]; 8B→14B +0.0258 [+0.0182,+0.0365] | PASS |
| neutral | capped2 | content | inst | 4 | 4B→8B +0.0397 [+0.0338,+0.0460]; 8B→14B +0.0296 [+0.0239,+0.0369]; 14B→32B +0.0042 [-0.0003,+0.0090] ✗ | FAIL |
| neutral | capped2 | outcome | base | 4 | 0.6B→4B +0.1419 [+0.1223,+0.1703]; 4B→8B +0.0294 [+0.0252,+0.0339]; 8B→14B +0.0220 [+0.0168,+0.0275] | PASS |
| neutral | capped2 | outcome | inst | 4 | 4B→8B +0.0341 [+0.0284,+0.0402]; 8B→14B +0.0329 [+0.0261,+0.0406]; 14B→32B -0.0062 [-0.0112,-0.0017] ✗ | FAIL |
| neutral | prob | content | base | 4 | 0.6B→4B +0.0783 [+0.0710,+0.0860]; 4B→8B +0.0139 [+0.0114,+0.0170]; 8B→14B +0.0122 [+0.0088,+0.0171] | PASS |
| neutral | prob | content | inst | 4 | 4B→8B +0.0193 [+0.0165,+0.0222]; 8B→14B +0.0142 [+0.0114,+0.0177]; 14B→32B +0.0025 [+0.0003,+0.0047] | PASS |
| neutral | prob | outcome | base | 4 | 0.6B→4B +0.0664 [+0.0576,+0.0790]; 4B→8B +0.0131 [+0.0113,+0.0151]; 8B→14B +0.0104 [+0.0081,+0.0131] | PASS |
| neutral | prob | outcome | inst | 4 | 4B→8B +0.0163 [+0.0138,+0.0189]; 8B→14B +0.0157 [+0.0125,+0.0193]; 14B→32B -0.0018 [-0.0038,+0.0001] ✗ | FAIL |
| native | rankrecal | content | inst | 2 | 14B→32B +0.0611 [+0.0514,+0.0715] | PASS |
| native | rankrecal | outcome | inst | 2 | 14B→32B +0.0502 [+0.0405,+0.0600] | PASS |
| native | T_cf_content | content | inst | 2 | 14B→32B +0.0908 [+0.0733,+0.1079] | PASS |
| native | T_cf_content | outcome | inst | 2 | 14B→32B +0.0753 [+0.0594,+0.0890] | PASS |
| native | T_obs_cal | content | base | 4 | 0.6B→4B +0.4367 [+0.3819,+0.4972]; 4B→8B +0.0774 [+0.0621,+0.0982]; 8B→14B +0.0699 [+0.0503,+0.0986] | PASS |
| native | T_obs_cal | content | inst | 4 | 4B→8B +0.1659 [+0.1406,+0.1929]; 8B→14B +0.1306 [+0.1101,+0.1567]; 14B→32B +0.0886 [+0.0726,+0.1058] | PASS |
| native | T_obs_cal | outcome | base | 4 | 0.6B→4B +0.2805 [+0.2454,+0.3238]; 4B→8B +0.0583 [+0.0459,+0.0724]; 8B→14B +0.0532 [+0.0420,+0.0641] | PASS |
| native | T_obs_cal | outcome | inst | 4 | 4B→8B +0.1348 [+0.1116,+0.1612]; 8B→14B +0.0993 [+0.0785,+0.1227]; 14B→32B +0.0720 [+0.0584,+0.0862] | PASS |
| native | raw | content | base | 4 | 0.6B→4B +0.4367 [+0.3819,+0.4972]; 4B→8B +0.0774 [+0.0621,+0.0982]; 8B→14B +0.0699 [+0.0503,+0.0986] | PASS |
| native | raw | content | inst | 4 | 4B→8B +0.2036 [+0.1749,+0.2325]; 8B→14B +0.2410 [+0.2070,+0.2804]; 14B→32B +0.1934 [+0.1698,+0.2187] | PASS |
| native | raw | outcome | base | 4 | 0.6B→4B +0.2805 [+0.2454,+0.3238]; 4B→8B +0.0583 [+0.0459,+0.0724]; 8B→14B +0.0532 [+0.0420,+0.0641] | PASS |
| native | raw | outcome | inst | 4 | 4B→8B +0.1920 [+0.1535,+0.2355]; 8B→14B +0.2183 [+0.1856,+0.2552]; 14B→32B +0.1908 [+0.1647,+0.2176] | PASS |
| native | capped2 | content | base | 4 | 0.6B→4B +0.1609 [+0.1451,+0.1779]; 4B→8B +0.0275 [+0.0227,+0.0339]; 8B→14B +0.0290 [+0.0213,+0.0399] | PASS |
| native | capped2 | content | inst | 4 | 4B→8B +0.0393 [+0.0330,+0.0457]; 8B→14B +0.0276 [+0.0222,+0.0343]; 14B→32B +0.0010 [-0.0033,+0.0054] ✗ | FAIL |
| native | capped2 | outcome | base | 4 | 0.6B→4B +0.1369 [+0.1176,+0.1643]; 4B→8B +0.0275 [+0.0236,+0.0320]; 8B→14B +0.0257 [+0.0205,+0.0312] | PASS |
| native | capped2 | outcome | inst | 4 | 4B→8B +0.0326 [+0.0270,+0.0387]; 8B→14B +0.0300 [+0.0234,+0.0373]; 14B→32B -0.0084 [-0.0133,-0.0039] ✗ | FAIL |
| native | prob | content | base | 4 | 0.6B→4B +0.0771 [+0.0698,+0.0848]; 4B→8B +0.0131 [+0.0108,+0.0161]; 8B→14B +0.0136 [+0.0101,+0.0186] | PASS |
| native | prob | content | inst | 4 | 4B→8B +0.0192 [+0.0164,+0.0222]; 8B→14B +0.0135 [+0.0109,+0.0168]; 14B→32B +0.0011 [-0.0010,+0.0033] ✗ | FAIL |
| native | prob | outcome | base | 4 | 0.6B→4B +0.0644 [+0.0557,+0.0767]; 4B→8B +0.0124 [+0.0107,+0.0143]; 8B→14B +0.0119 [+0.0096,+0.0146] | PASS |
| native | prob | outcome | inst | 4 | 4B→8B +0.0159 [+0.0134,+0.0187]; 8B→14B +0.0148 [+0.0116,+0.0182]; 14B→32B -0.0025 [-0.0046,-0.0005] ✗ | FAIL |

| rendering | metric | mask | pair | Δ post−start [95% CI] | log2 n [95% CI] | n | P(gain) | P(cens. hi/lo) | ladder range (log2) |
|---|---|---|---|---|---|---|---|---|---|
| neutral | rankrecal | content | Nemo-14B vs Qwen3-14B | +0.0416 [+0.0282, +0.0546] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| neutral | rankrecal | content | Nemo-32B vs Qwen3-32B | +0.0342 [+0.0231, +0.0447] | -0.76 [-0.97, -0.54] | no gain (0.59x) | 0.00 | 0.00/0.00 | [-1.24, +0.00] (2 pts) |
| neutral | rankrecal | outcome | Nemo-14B vs Qwen3-14B | +0.0348 [+0.0203, +0.0481] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| neutral | rankrecal | outcome | Nemo-32B vs Qwen3-32B | +0.0474 [+0.0316, +0.0640] | <-1.24 [<-1.24, -0.99] | no gain (<0.42x) | 0.00 | 0.00/0.81 | [-1.24, +0.00] (2 pts) |
| neutral | T_cf_content | content | Nemo-14B vs Qwen3-14B | +0.0485 [+0.0298, +0.0670] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| neutral | T_cf_content | content | Nemo-32B vs Qwen3-32B | +0.0365 [+0.0221, +0.0505] | -0.57 [-0.76, -0.38] | no gain (0.67x) | 0.00 | 0.00/0.00 | [-1.24, +0.00] (2 pts) |
| neutral | T_cf_content | outcome | Nemo-14B vs Qwen3-14B | +0.0376 [+0.0177, +0.0545] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| neutral | T_cf_content | outcome | Nemo-32B vs Qwen3-32B | +0.0453 [+0.0284, +0.0642] | -1.10 [<-1.24, -0.66] | no gain (0.47x) | 0.00 | 0.00/0.23 | [-1.24, +0.00] (2 pts) |
| neutral | T_obs_cal | content | Nemo-8B vs Qwen3-8B | +0.1126 [+0.0895, +0.1354] | -0.67 [-0.83, -0.52] | no gain (0.63x) | 0.00 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| neutral | T_obs_cal | content | Nemo-14B vs Qwen3-14B | +0.0545 [+0.0361, +0.0732] | -0.44 [-0.57, -0.31] | no gain (0.74x) | 0.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| neutral | T_obs_cal | content | Nemo-32B vs Qwen3-32B | +0.0365 [+0.0218, +0.0507] | -0.56 [-0.73, -0.37] | no gain (0.68x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| neutral | T_obs_cal | content | Qwen3-4B vs Qwen3-4B-Base | +0.2640 [+0.2374, +0.2899] | -1.87 [-2.00, -1.74] | no gain (0.27x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | T_obs_cal | content | Qwen3-8B vs Qwen3-8B-Base | +0.1781 [+0.1582, +0.1983] | -1.69 [-1.82, -1.55] | no gain (0.31x) | 0.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | T_obs_cal | content | Qwen3-14B vs Qwen3-14B-Base | +0.1338 [+0.1148, +0.1550] | -1.75 [-1.96, -1.45] | no gain (0.30x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | T_obs_cal | outcome | Nemo-8B vs Qwen3-8B | +0.0988 [+0.0690, +0.1292] | -0.76 [<-0.93, -0.55] | no gain (0.59x) | 0.00 | 0.00/0.06 | [-0.93, +2.17] (4 pts) |
| neutral | T_obs_cal | outcome | Nemo-14B vs Qwen3-14B | +0.0253 [+0.0056, +0.0445] | -0.30 [-0.55, -0.07] | no gain (0.81x) | 0.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| neutral | T_obs_cal | outcome | Nemo-32B vs Qwen3-32B | +0.0410 [+0.0233, +0.0589] | -0.89 [-1.29, -0.50] | no gain (0.54x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| neutral | T_obs_cal | outcome | Qwen3-4B vs Qwen3-4B-Base | +0.1990 [+0.1767, +0.2220] | -2.20 [-2.48, -1.97] | no gain (0.22x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | T_obs_cal | outcome | Qwen3-8B vs Qwen3-8B-Base | +0.1328 [+0.1159, +0.1524] | -1.79 [-1.97, -1.60] | no gain (0.29x) | 0.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | T_obs_cal | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.1087 [+0.0934, +0.1252] | -1.84 [-2.03, -1.59] | no gain (0.28x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | rankrecal | content | Nemo-14B vs Qwen3-14B | +0.0386 [+0.0245, +0.0525] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| native | rankrecal | content | Nemo-32B vs Qwen3-32B | +0.0323 [+0.0210, +0.0430] | -0.66 [-0.85, -0.45] | no gain (0.63x) | 0.00 | 0.00/0.00 | [-1.24, +0.00] (2 pts) |
| native | rankrecal | outcome | Nemo-14B vs Qwen3-14B | +0.0300 [+0.0138, +0.0451] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| native | rankrecal | outcome | Nemo-32B vs Qwen3-32B | +0.0472 [+0.0300, +0.0636] | -1.16 [<-1.24, -0.78] | no gain (0.45x) | 0.00 | 0.00/0.34 | [-1.24, +0.00] (2 pts) |
| native | T_cf_content | content | Nemo-14B vs Qwen3-14B | +0.0389 [+0.0203, +0.0588] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.00 | 0.00/1.00 | [+0.00, +1.24] (2 pts) |
| native | T_cf_content | content | Nemo-32B vs Qwen3-32B | +0.0359 [+0.0209, +0.0503] | -0.49 [-0.66, -0.31] | no gain (0.71x) | 0.00 | 0.00/0.00 | [-1.24, +0.00] (2 pts) |
| native | T_cf_content | outcome | Nemo-14B vs Qwen3-14B | +0.0225 [+0.0026, +0.0447] | <+0.00 [<+0.00, <+0.00] | no gain (<1.00x) | 0.02 | 0.00/0.98 | [+0.00, +1.24] (2 pts) |
| native | T_cf_content | outcome | Nemo-32B vs Qwen3-32B | +0.0519 [+0.0337, +0.0702] | -0.85 [-1.23, -0.56] | no gain (0.55x) | 0.00 | 0.00/0.02 | [-1.24, +0.00] (2 pts) |
| native | T_obs_cal | content | Nemo-8B vs Qwen3-8B | +0.0547 [+0.0323, +0.0764] | -0.31 [-0.43, -0.19] | no gain (0.81x) | 0.00 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| native | T_obs_cal | content | Nemo-14B vs Qwen3-14B | +0.0746 [+0.0546, +0.0944] | -0.53 [-0.65, -0.41] | no gain (0.69x) | 0.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| native | T_obs_cal | content | Nemo-32B vs Qwen3-32B | +0.0339 [+0.0187, +0.0488] | -0.47 [-0.65, -0.28] | no gain (0.72x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| native | T_obs_cal | content | Qwen3-4B vs Qwen3-4B-Base | +0.3015 [+0.2714, +0.3310] | -2.10 [-2.26, -1.95] | no gain (0.23x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| native | T_obs_cal | content | Qwen3-8B vs Qwen3-8B-Base | +0.2130 [+0.1924, +0.2337] | -1.88 [-2.04, -1.72] | no gain (0.27x) | 0.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | T_obs_cal | content | Qwen3-14B vs Qwen3-14B-Base | +0.1523 [+0.1328, +0.1741] | -1.90 [-2.07, -1.60] | no gain (0.27x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | T_obs_cal | outcome | Nemo-8B vs Qwen3-8B | +0.0504 [+0.0200, +0.0812] | -0.35 [-0.54, -0.15] | no gain (0.78x) | 0.00 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| native | T_obs_cal | outcome | Nemo-14B vs Qwen3-14B | +0.0264 [+0.0044, +0.0481] | -0.25 [-0.46, -0.04] | no gain (0.84x) | 0.01 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| native | T_obs_cal | outcome | Nemo-32B vs Qwen3-32B | +0.0433 [+0.0253, +0.0618] | -0.75 [-1.10, -0.44] | no gain (0.60x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| native | T_obs_cal | outcome | Qwen3-4B vs Qwen3-4B-Base | +0.2527 [+0.2277, +0.2792] | -2.74 [<-3.05, -2.44] | no gain (0.15x) | 0.00 | 0.00/0.06 | [-3.05, +1.86] (4 pts) |
| native | T_obs_cal | outcome | Qwen3-8B vs Qwen3-8B-Base | +0.1762 [+0.1564, +0.1977] | -2.21 [-2.45, -1.99] | no gain (0.22x) | 0.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | T_obs_cal | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.1301 [+0.1132, +0.1489] | -2.06 [-2.27, -1.88] | no gain (0.24x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | raw | content | Nemo-8B vs Qwen3-8B | -0.0222 [-0.0553, +0.0100] | +0.12 [-0.05, +0.27] | 1.09x | 0.90 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| neutral | raw | content | Nemo-14B vs Qwen3-14B | -0.0299 [-0.0506, -0.0104] | +0.24 [+0.09, +0.41] | 1.18x | 1.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| neutral | raw | content | Nemo-32B vs Qwen3-32B | +0.0264 [+0.0112, +0.0402] | -0.21 [-0.32, -0.10] | no gain (0.86x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| neutral | raw | content | Qwen3-4B vs Qwen3-4B-Base | +0.4571 [+0.4170, +0.4975] | <-3.05 [<-3.05, -3.01] | no gain (<0.12x) | 0.00 | 0.00/0.95 | [-3.05, +1.86] (4 pts) |
| neutral | raw | content | Qwen3-8B vs Qwen3-8B-Base | +0.3386 [+0.3070, +0.3728] | -2.82 [-3.03, -2.62] | no gain (0.14x) | 0.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | raw | content | Qwen3-14B vs Qwen3-14B-Base | +0.2364 [+0.2105, +0.2656] | -2.53 [-2.74, -2.30] | no gain (0.17x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | raw | outcome | Nemo-8B vs Qwen3-8B | -0.0348 [-0.0746, +0.0017] | +0.23 [-0.01, +0.42] | 1.17x | 0.97 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| neutral | raw | outcome | Nemo-14B vs Qwen3-14B | -0.0514 [-0.0762, -0.0282] | +0.48 [+0.28, +0.68] | 1.40x | 1.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| neutral | raw | outcome | Nemo-32B vs Qwen3-32B | +0.0333 [+0.0137, +0.0533] | -0.31 [-0.51, -0.13] | no gain (0.81x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| neutral | raw | outcome | Qwen3-4B vs Qwen3-4B-Base | +0.3955 [+0.3584, +0.4352] | <-3.05 [<-3.05, <-3.05] | no gain (<0.12x) | 0.00 | 0.00/1.00 | [-3.05, +1.86] (4 pts) |
| neutral | raw | outcome | Qwen3-8B vs Qwen3-8B-Base | +0.3100 [+0.2759, +0.3450] | -3.75 [<-3.98, -3.36] | no gain (0.07x) | 0.00 | 0.00/0.13 | [-3.98, +0.93] (4 pts) |
| neutral | raw | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.2215 [+0.1945, +0.2513] | -3.10 [-3.46, -2.75] | no gain (0.12x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | capped2 | content | Nemo-8B vs Qwen3-8B | +0.0915 [+0.0838, +0.0993] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| neutral | capped2 | content | Nemo-14B vs Qwen3-14B | +0.0545 [+0.0469, +0.0622] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| neutral | capped2 | content | Nemo-32B vs Qwen3-32B | +0.0266 [+0.0200, +0.0329] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| neutral | capped2 | content | Qwen3-4B vs Qwen3-4B-Base | +0.0130 [+0.0070, +0.0194] | -0.24 [-0.35, -0.13] | no gain (0.84x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | capped2 | content | Qwen3-8B vs Qwen3-8B-Base | +0.0027 [-0.0014, +0.0068] | -0.09 [-0.21, +0.05] | no gain (0.94x) | 0.09 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | capped2 | content | Qwen3-14B vs Qwen3-14B-Base | -0.0011 [-0.0062, +0.0047] | >+0.00 [-0.12, >+0.00] | >1.00x | 0.66 | 0.66/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | capped2 | outcome | Nemo-8B vs Qwen3-8B | +0.0898 [+0.0787, +0.1011] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| neutral | capped2 | outcome | Nemo-14B vs Qwen3-14B | +0.0553 [+0.0455, +0.0653] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| neutral | capped2 | outcome | Nemo-32B vs Qwen3-32B | +0.0358 [+0.0279, +0.0447] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| neutral | capped2 | outcome | Qwen3-4B vs Qwen3-4B-Base | +0.0039 [-0.0026, +0.0099] | -0.08 [-0.20, +0.08] | no gain (0.94x) | 0.12 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | capped2 | outcome | Qwen3-8B vs Qwen3-8B-Base | -0.0008 [-0.0064, +0.0047] | +0.03 [-0.15, +0.29] | 1.02x | 0.63 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | capped2 | outcome | Qwen3-14B vs Qwen3-14B-Base | -0.0118 [-0.0159, -0.0080] | >+0.00 [>+0.00, >+0.00] | >1.00x | 1.00 | 1.00/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | prob | content | Nemo-8B vs Qwen3-8B | -0.0432 [-0.0468, -0.0396] | <-0.93 [<-0.93, <-0.93] | no gain (<0.52x) | 0.00 | 0.00/1.00 | [-0.93, +2.17] (4 pts) |
| neutral | prob | content | Nemo-14B vs Qwen3-14B | -0.0258 [-0.0294, -0.0224] | -1.49 [-1.68, -1.32] | no gain (0.36x) | 0.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| neutral | prob | content | Nemo-32B vs Qwen3-32B | -0.0128 [-0.0157, -0.0097] | -1.91 [-2.12, -1.72] | no gain (0.27x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| neutral | prob | content | Qwen3-4B vs Qwen3-4B-Base | -0.0070 [-0.0099, -0.0042] | -0.27 [-0.37, -0.17] | no gain (0.83x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | prob | content | Qwen3-8B vs Qwen3-8B-Base | -0.0015 [-0.0034, +0.0005] | -0.10 [-0.23, +0.04] | no gain (0.93x) | 0.06 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | prob | content | Qwen3-14B vs Qwen3-14B-Base | +0.0005 [-0.0023, +0.0030] | >+0.00 [-0.13, >+0.00] | >1.00x | 0.67 | 0.67/0.00 | [-4.91, +0.00] (4 pts) |
| neutral | prob | outcome | Nemo-8B vs Qwen3-8B | -0.0413 [-0.0464, -0.0361] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| neutral | prob | outcome | Nemo-14B vs Qwen3-14B | -0.0251 [-0.0295, -0.0208] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| neutral | prob | outcome | Nemo-32B vs Qwen3-32B | -0.0171 [-0.0214, -0.0134] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| neutral | prob | outcome | Qwen3-4B vs Qwen3-4B-Base | -0.0041 [-0.0067, -0.0013] | -0.19 [-0.29, -0.06] | no gain (0.88x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| neutral | prob | outcome | Qwen3-8B vs Qwen3-8B-Base | -0.0009 [-0.0034, +0.0015] | -0.07 [-0.23, +0.14] | no gain (0.96x) | 0.24 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| neutral | prob | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.0043 [+0.0027, +0.0061] | >+0.00 [>+0.00, >+0.00] | >1.00x | 1.00 | 1.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | raw | content | Nemo-8B vs Qwen3-8B | -0.1730 [-0.2121, -0.1371] | +0.67 [+0.56, +0.78] | 1.59x | 1.00 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| native | raw | content | Nemo-14B vs Qwen3-14B | -0.0734 [-0.0969, -0.0515] | +0.47 [+0.33, +0.62] | 1.39x | 1.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| native | raw | content | Nemo-32B vs Qwen3-32B | +0.0198 [+0.0042, +0.0347] | -0.13 [-0.22, -0.03] | no gain (0.92x) | 0.01 | 0.01/0.00 | [-3.10, +0.00] (4 pts) |
| native | raw | content | Qwen3-4B vs Qwen3-4B-Base | +0.5890 [+0.5410, +0.6363] | <-3.05 [<-3.05, <-3.05] | no gain (<0.12x) | 0.00 | 0.00/1.00 | [-3.05, +1.86] (4 pts) |
| native | raw | content | Qwen3-8B vs Qwen3-8B-Base | +0.4628 [+0.4218, +0.5058] | -3.62 [-3.95, -3.33] | no gain (0.08x) | 0.00 | 0.00/0.02 | [-3.98, +0.93] (4 pts) |
| native | raw | content | Qwen3-14B vs Qwen3-14B-Base | +0.2917 [+0.2630, +0.3230] | -2.87 [-3.13, -2.61] | no gain (0.14x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | raw | outcome | Nemo-8B vs Qwen3-8B | -0.1844 [-0.2268, -0.1447] | +0.78 [+0.65, +0.94] | 1.72x | 1.00 | 0.00/0.00 | [-0.93, +2.17] (4 pts) |
| native | raw | outcome | Nemo-14B vs Qwen3-14B | -0.1072 [-0.1371, -0.0785] | +0.70 [+0.55, +0.84] | 1.62x | 1.00 | 0.00/0.00 | [-1.86, +1.24] (4 pts) |
| native | raw | outcome | Nemo-32B vs Qwen3-32B | +0.0331 [+0.0131, +0.0531] | -0.22 [-0.35, -0.09] | no gain (0.86x) | 0.00 | 0.00/0.00 | [-3.10, +0.00] (4 pts) |
| native | raw | outcome | Qwen3-4B vs Qwen3-4B-Base | +0.5876 [+0.5356, +0.6427] | <-3.05 [<-3.05, <-3.05] | no gain (<0.12x) | 0.00 | 0.00/1.00 | [-3.05, +1.86] (4 pts) |
| native | raw | outcome | Qwen3-8B vs Qwen3-8B-Base | +0.4539 [+0.4081, +0.5001] | <-3.98 [<-3.98, <-3.98] | no gain (<0.06x) | 0.00 | 0.00/1.00 | [-3.98, +0.93] (4 pts) |
| native | raw | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.2888 [+0.2549, +0.3264] | -3.79 [-4.27, -3.33] | no gain (0.07x) | 0.00 | 0.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | capped2 | content | Nemo-8B vs Qwen3-8B | +0.0865 [+0.0787, +0.0938] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| native | capped2 | content | Nemo-14B vs Qwen3-14B | +0.0619 [+0.0545, +0.0697] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| native | capped2 | content | Nemo-32B vs Qwen3-32B | +0.0292 [+0.0227, +0.0356] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| native | capped2 | content | Qwen3-4B vs Qwen3-4B-Base | +0.0067 [+0.0001, +0.0134] | -0.13 [-0.24, -0.00] | no gain (0.92x) | 0.02 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| native | capped2 | content | Qwen3-8B vs Qwen3-8B-Base | -0.0051 [-0.0096, -0.0005] | +0.16 [+0.02, +0.35] | 1.12x | 0.98 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | capped2 | content | Qwen3-14B vs Qwen3-14B-Base | -0.0037 [-0.0090, +0.0022] | >+0.00 [-0.05, >+0.00] | >1.00x | 0.90 | 0.90/0.00 | [-4.91, +0.00] (4 pts) |
| native | capped2 | outcome | Nemo-8B vs Qwen3-8B | +0.0913 [+0.0804, +0.1024] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| native | capped2 | outcome | Nemo-14B vs Qwen3-14B | +0.0636 [+0.0528, +0.0744] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| native | capped2 | outcome | Nemo-32B vs Qwen3-32B | +0.0407 [+0.0328, +0.0496] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| native | capped2 | outcome | Qwen3-4B vs Qwen3-4B-Base | -0.0064 [-0.0133, +0.0001] | +0.22 [-0.00, +0.44] | 1.16x | 0.97 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| native | capped2 | outcome | Qwen3-8B vs Qwen3-8B-Base | -0.0115 [-0.0173, -0.0057] | +0.41 [+0.19, +0.69] | 1.33x | 1.00 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | capped2 | outcome | Qwen3-14B vs Qwen3-14B-Base | -0.0158 [-0.0201, -0.0117] | >+0.00 [>+0.00, >+0.00] | >1.00x | 1.00 | 1.00/0.00 | [-4.91, +0.00] (4 pts) |
| native | prob | content | Nemo-8B vs Qwen3-8B | -0.0404 [-0.0437, -0.0368] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| native | prob | content | Nemo-14B vs Qwen3-14B | -0.0291 [-0.0326, -0.0256] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| native | prob | content | Nemo-32B vs Qwen3-32B | -0.0140 [-0.0170, -0.0109] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| native | prob | content | Qwen3-4B vs Qwen3-4B-Base | -0.0045 [-0.0076, -0.0015] | -0.18 [-0.29, -0.06] | no gain (0.88x) | 0.00 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| native | prob | content | Qwen3-8B vs Qwen3-8B-Base | +0.0017 [-0.0005, +0.0038] | +0.12 [-0.03, +0.30] | 1.08x | 0.94 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | prob | content | Qwen3-14B vs Qwen3-14B-Base | +0.0016 [-0.0013, +0.0041] | >+0.00 [-0.07, >+0.00] | >1.00x | 0.87 | 0.87/0.00 | [-4.91, +0.00] (4 pts) |
| native | prob | outcome | Nemo-8B vs Qwen3-8B | -0.0410 [-0.0461, -0.0361] | gate FAIL – not reported | – | – | – | [-0.93, +2.17] (4 pts) |
| native | prob | outcome | Nemo-14B vs Qwen3-14B | -0.0281 [-0.0328, -0.0235] | gate FAIL – not reported | – | – | – | [-1.86, +1.24] (4 pts) |
| native | prob | outcome | Nemo-32B vs Qwen3-32B | -0.0191 [-0.0232, -0.0154] | gate FAIL – not reported | – | – | – | [-3.10, +0.00] (4 pts) |
| native | prob | outcome | Qwen3-4B vs Qwen3-4B-Base | -0.0008 [-0.0037, +0.0022] | -0.04 [-0.16, +0.17] | no gain (0.97x) | 0.29 | 0.00/0.00 | [-3.05, +1.86] (4 pts) |
| native | prob | outcome | Qwen3-8B vs Qwen3-8B-Base | +0.0027 [+0.0002, +0.0052] | +0.21 [+0.02, +0.45] | 1.16x | 0.98 | 0.00/0.00 | [-3.98, +0.93] (4 pts) |
| native | prob | outcome | Qwen3-14B vs Qwen3-14B-Base | +0.0055 [+0.0038, +0.0075] | >+0.00 [>+0.00, >+0.00] | >1.00x | 1.00 | 1.00/0.00 | [-4.91, +0.00] (4 pts) |

## SECONDARY (superseded): global OLS slopes b (metric per doubling of total params)

| rendering | metric | mask | ladder | pts | b | 95% CI | R² | residuals | monotone | P(monotone) |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | raw | content | base | 4 | -0.1263 | [-0.1489, -0.1080] | 0.973 | +0.0240, -0.0590, -0.0009, +0.0358 | yes | 1.00 |
| neutral | raw | content | inst | 4 | -0.1725 | [-0.2002, -0.1503] | 0.992 | +0.0115, -0.0015, -0.0278, +0.0177 | yes | 1.00 |
| neutral | raw | outcome | base | 4 | -0.0845 | [-0.0962, -0.0750] | 0.984 | +0.0124, -0.0307, +0.0003, +0.0180 | yes | 1.00 |
| neutral | raw | outcome | inst | 4 | -0.1396 | [-0.1547, -0.1259] | 0.995 | +0.0034, +0.0055, -0.0185, +0.0096 | yes | 1.00 |
| neutral | raw | random | base | 4 | -0.0307 | [-0.0471, -0.0172] | 0.996 | +0.0021, -0.0043, -0.0022, +0.0043 | yes | 1.00 |
| neutral | raw | random | inst | 4 | -0.0478 | [-0.0586, -0.0400] | 0.960 | +0.0028, +0.0063, -0.0184, +0.0093 | yes | 1.00 |
| neutral | raw | random_novel | base | 4 | -0.0447 | [-0.0697, -0.0220] | 0.997 | +0.0022, -0.0029, -0.0056, +0.0063 | yes | 1.00 |
| neutral | raw | random_novel | inst | 4 | -0.0736 | [-0.1026, -0.0580] | 0.962 | +0.0011, +0.0138, -0.0268, +0.0120 | yes | 1.00 |
| neutral | raw | hash_novel | base | 4 | -0.0633 | [-0.1077, -0.0325] | 0.991 | +0.0066, -0.0129, -0.0077, +0.0139 | yes | 1.00 |
| neutral | raw | hash_novel | inst | 4 | -0.0606 | [-0.0989, -0.0415] | 0.968 | +0.0134, -0.0164, -0.0069, +0.0099 | yes | 1.00 |
| neutral | raw | boiler | base | 4 | -0.1461 | [-0.1541, -0.1385] | 0.917 | +0.0498, -0.1091, -0.0308, +0.0900 | yes | 0.71 |
| neutral | raw | boiler | inst | 4 | -0.2709 | [-0.2829, -0.2598] | 0.806 | -0.1559, +0.2381, -0.0039, -0.0783 | NO | 0.00 |
| neutral | raw | prompt_echo_ws | base | 4 | -0.0170 | [-0.0182, -0.0158] | 0.970 | +0.0034, -0.0083, -0.0001, +0.0050 | yes | 1.00 |
| neutral | raw | prompt_echo_ws | inst | 4 | -0.0260 | [-0.0281, -0.0239] | 0.978 | -0.0009, +0.0052, -0.0066, +0.0023 | yes | 1.00 |
| neutral | T_obs_cal | content | base | 4 | -0.1263 | [-0.1489, -0.1080] | 0.973 | +0.0240, -0.0590, -0.0009, +0.0358 | yes | 1.00 |
| neutral | T_obs_cal | content | inst | 4 | -0.1176 | [-0.1394, -0.0998] | 0.969 | +0.0215, -0.0152, -0.0302, +0.0239 | yes | 1.00 |
| neutral | T_obs_cal | outcome | base | 4 | -0.0845 | [-0.0962, -0.0750] | 0.984 | +0.0124, -0.0307, +0.0003, +0.0180 | yes | 1.00 |
| neutral | T_obs_cal | outcome | inst | 4 | -0.0851 | [-0.0956, -0.0758] | 0.961 | +0.0187, -0.0158, -0.0218, +0.0189 | yes | 1.00 |
| neutral | T_obs_cal | random | base | 4 | -0.0307 | [-0.0471, -0.0172] | 0.996 | +0.0021, -0.0043, -0.0022, +0.0043 | yes | 1.00 |
| neutral | T_obs_cal | random | inst | 4 | -0.0413 | [-0.0592, -0.0269] | 0.914 | -0.0084, +0.0217, -0.0156, +0.0023 | yes | 0.88 |
| neutral | T_obs_cal | random_novel | base | 4 | -0.0447 | [-0.0697, -0.0220] | 0.997 | +0.0022, -0.0029, -0.0056, +0.0063 | yes | 1.00 |
| neutral | T_obs_cal | random_novel | inst | 4 | -0.0641 | [-0.0927, -0.0404] | 0.899 | -0.0166, +0.0384, -0.0231, +0.0013 | yes | 0.75 |
| neutral | T_obs_cal | hash_novel | base | 4 | -0.0633 | [-0.1077, -0.0325] | 0.991 | +0.0066, -0.0129, -0.0077, +0.0139 | yes | 1.00 |
| neutral | T_obs_cal | hash_novel | inst | 4 | -0.0751 | [-0.1200, -0.0401] | 0.878 | -0.0303, +0.0520, -0.0108, -0.0109 | NO | 0.42 |
| neutral | T_obs_cal | boiler | base | 4 | -0.1461 | [-0.1541, -0.1385] | 0.917 | +0.0498, -0.1091, -0.0308, +0.0900 | yes | 0.71 |
| neutral | T_obs_cal | boiler | inst | 4 | -0.1371 | [-0.1446, -0.1300] | 0.990 | -0.0056, +0.0204, -0.0206, +0.0059 | yes | 1.00 |
| neutral | T_obs_cal | prompt_echo_ws | base | 4 | -0.0170 | [-0.0182, -0.0158] | 0.970 | +0.0034, -0.0083, -0.0001, +0.0050 | yes | 1.00 |
| neutral | T_obs_cal | prompt_echo_ws | inst | 4 | -0.0166 | [-0.0180, -0.0151] | 0.963 | -0.0001, +0.0035, -0.0059, +0.0025 | yes | 1.00 |
| neutral | T_cf_content | content | inst | 2 | -0.0684 | [-0.0845, -0.0544] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| neutral | T_cf_content | outcome | inst | 2 | -0.0445 | [-0.0575, -0.0359] | 1.000 | +0.0000, -0.0000 | yes | 1.00 |
| neutral | T_cf_content | random | inst | 2 | -0.0372 | [-0.0613, -0.0084] | 1.000 | +0.0000, -0.0000 | yes | 1.00 |
| neutral | T_cf_content | random_novel | inst | 2 | -0.0609 | [-0.0958, -0.0164] | 1.000 | -0.0000, +0.0000 | yes | 1.00 |
| neutral | capped2 | content | base | 4 | -0.0482 | [-0.0547, -0.0428] | 0.975 | +0.0089, -0.0214, -0.0014, +0.0138 | yes | 1.00 |
| neutral | capped2 | content | inst | 4 | -0.0248 | [-0.0305, -0.0201] | 0.882 | +0.0088, -0.0054, -0.0139, +0.0104 | yes | 0.96 |
| neutral | capped2 | outcome | base | 4 | -0.0428 | [-0.0501, -0.0376] | 0.979 | +0.0073, -0.0169, -0.0024, +0.0120 | yes | 1.00 |
| neutral | capped2 | outcome | inst | 4 | -0.0212 | [-0.0246, -0.0181] | 0.794 | +0.0091, -0.0033, -0.0182, +0.0124 | NO | 0.00 |
| neutral | capped2 | random | base | 4 | -0.0141 | [-0.0191, -0.0100] | 0.991 | +0.0015, -0.0034, -0.0007, +0.0026 | yes | 1.00 |
| neutral | capped2 | random | inst | 4 | -0.0033 | [-0.0074, +0.0004] **crosses 0** | 0.370 | +0.0053, -0.0061, -0.0033, +0.0041 | NO | 0.02 |
| neutral | capped2 | random_novel | base | 4 | -0.0176 | [-0.0270, -0.0105] | 0.993 | +0.0015, -0.0025, -0.0025, +0.0036 | yes | 1.00 |
| neutral | capped2 | random_novel | inst | 4 | -0.0058 | [-0.0132, +0.0004] **crosses 0** | 0.657 | +0.0050, -0.0051, -0.0041, +0.0043 | NO | 0.27 |
| neutral | capped2 | hash_novel | base | 4 | -0.0188 | [-0.0364, -0.0089] | 0.995 | -0.0000, +0.0018, -0.0039, +0.0021 | yes | 1.00 |
| neutral | capped2 | hash_novel | inst | 4 | -0.0118 | [-0.0270, -0.0035] | 0.872 | +0.0055, -0.0064, -0.0033, +0.0043 | yes | 0.92 |
| neutral | capped2 | boiler | base | 4 | -0.0246 | [-0.0278, -0.0217] | 0.850 | +0.0114, -0.0309, +0.0059, +0.0136 | NO | 0.00 |
| neutral | capped2 | boiler | inst | 4 | -0.0091 | [-0.0116, -0.0067] | 0.262 | +0.0110, -0.0010, -0.0272, +0.0172 | NO | 0.00 |
| neutral | capped2 | prompt_echo_ws | base | 4 | -0.0082 | [-0.0088, -0.0077] | 0.957 | +0.0020, -0.0044, -0.0012, +0.0036 | yes | 1.00 |
| neutral | capped2 | prompt_echo_ws | inst | 4 | -0.0028 | [-0.0032, -0.0024] | 0.679 | +0.0020, -0.0016, -0.0026, +0.0022 | NO | 0.00 |
| neutral | prob | content | base | 4 | +0.0230 | [+0.0205, +0.0260] | 0.974 | -0.0044, +0.0104, +0.0007, -0.0068 | yes | 1.00 |
| neutral | prob | content | inst | 4 | +0.0121 | [+0.0099, +0.0149] | 0.888 | -0.0042, +0.0026, +0.0065, -0.0050 | yes | 0.99 |
| neutral | prob | outcome | base | 4 | +0.0199 | [+0.0176, +0.0232] | 0.977 | -0.0035, +0.0082, +0.0009, -0.0056 | yes | 1.00 |
| neutral | prob | outcome | inst | 4 | +0.0105 | [+0.0091, +0.0121] | 0.821 | -0.0041, +0.0015, +0.0082, -0.0056 | NO | 0.03 |
| neutral | prob | random | base | 4 | +0.0071 | [+0.0051, +0.0095] | 0.991 | -0.0008, +0.0019, +0.0001, -0.0012 | yes | 1.00 |
| neutral | prob | random | inst | 4 | +0.0016 | [-0.0003, +0.0037] **crosses 0** | 0.322 | -0.0027, +0.0029, +0.0022, -0.0023 | NO | 0.01 |
| neutral | prob | random_novel | base | 4 | +0.0085 | [+0.0051, +0.0131] | 0.993 | -0.0007, +0.0013, +0.0011, -0.0016 | yes | 1.00 |
| neutral | prob | random_novel | inst | 4 | +0.0030 | [-0.0001, +0.0070] **crosses 0** | 0.628 | -0.0026, +0.0023, +0.0029, -0.0026 | NO | 0.10 |
| neutral | prob | hash_novel | base | 4 | +0.0091 | [+0.0043, +0.0175] | 0.996 | -0.0001, -0.0005, +0.0017, -0.0011 | yes | 1.00 |
| neutral | prob | hash_novel | inst | 4 | +0.0051 | [+0.0009, +0.0125] | 0.855 | -0.0026, +0.0029, +0.0016, -0.0020 | yes | 0.83 |
| neutral | prob | boiler | base | 4 | +0.0138 | [+0.0125, +0.0152] | 0.902 | -0.0050, +0.0135, -0.0024, -0.0061 | NO | 0.00 |
| neutral | prob | boiler | inst | 4 | +0.0078 | [+0.0067, +0.0089] | 0.501 | -0.0065, +0.0023, +0.0131, -0.0089 | NO | 0.00 |
| neutral | prob | prompt_echo_ws | base | 4 | +0.0042 | [+0.0040, +0.0045] | 0.955 | -0.0010, +0.0024, +0.0005, -0.0018 | yes | 1.00 |
| neutral | prob | prompt_echo_ws | inst | 4 | +0.0013 | [+0.0011, +0.0014] | 0.621 | -0.0010, +0.0008, +0.0014, -0.0011 | NO | 0.00 |
| neutral | rankrecal | content | inst | 2 | -0.0487 | [-0.0587, -0.0393] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| neutral | rankrecal | outcome | inst | 2 | -0.0349 | [-0.0431, -0.0268] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| neutral | rankrecal | random | inst | 2 | -0.0002 | [-0.0397, +0.0484] **crosses 0** | 1.000 | +0.0000, +0.0000 | yes | 0.47 |
| neutral | rankrecal | random_novel | inst | 2 | +0.0077 | [-0.0599, +0.0896] **crosses 0** | 1.000 | +0.0000, +0.0000 | NO | 0.34 |
| native | raw | content | base | 4 | -0.1289 | [-0.1513, -0.1106] | 0.975 | +0.0239, -0.0577, -0.0030, +0.0368 | yes | 1.00 |
| native | raw | content | inst | 4 | -0.2159 | [-0.2452, -0.1916] | 0.991 | +0.0015, +0.0195, -0.0379, +0.0169 | yes | 1.00 |
| native | raw | outcome | base | 4 | -0.0860 | [-0.0980, -0.0763] | 0.984 | +0.0127, -0.0308, -0.0009, +0.0191 | yes | 1.00 |
| native | raw | outcome | inst | 4 | -0.2027 | [-0.2215, -0.1852] | 0.994 | +0.0004, +0.0164, -0.0295, +0.0128 | yes | 1.00 |
| native | raw | random | base | 4 | -0.0310 | [-0.0473, -0.0177] | 0.993 | +0.0029, -0.0063, -0.0017, +0.0051 | yes | 1.00 |
| native | raw | random | inst | 4 | -0.0723 | [-0.0900, -0.0607] | 0.928 | -0.0085, +0.0303, -0.0305, +0.0086 | yes | 0.99 |
| native | raw | random_novel | base | 4 | -0.0460 | [-0.0706, -0.0238] | 0.994 | +0.0036, -0.0064, -0.0054, +0.0082 | yes | 1.00 |
| native | raw | random_novel | inst | 4 | -0.1113 | [-0.1616, -0.0856] | 0.947 | -0.0091, +0.0377, -0.0417, +0.0131 | yes | 1.00 |
| native | raw | hash_novel | base | 4 | -0.0635 | [-0.1074, -0.0330] | 0.991 | +0.0068, -0.0142, -0.0058, +0.0132 | yes | 1.00 |
| native | raw | hash_novel | inst | 4 | -0.0677 | [-0.1088, -0.0482] | 0.984 | +0.0095, -0.0082, -0.0106, +0.0094 | yes | 1.00 |
| native | raw | boiler | base | 4 | -0.1663 | [-0.1742, -0.1584] | 0.985 | +0.0227, -0.0477, -0.0183, +0.0433 | yes | 1.00 |
| native | raw | boiler | inst | 4 | -0.6394 | [-0.6665, -0.6123] | 0.943 | +0.1602, -0.1127, -0.2257, +0.1782 | yes | 1.00 |
| native | raw | prompt_echo_ws | base | 4 | -0.0249 | [-0.0264, -0.0234] | 0.976 | +0.0045, -0.0097, -0.0029, +0.0081 | yes | 1.00 |
| native | raw | prompt_echo_ws | inst | 4 | -0.0318 | [-0.0345, -0.0293] | 0.944 | -0.0034, +0.0118, -0.0117, +0.0032 | yes | 1.00 |
| native | T_obs_cal | content | base | 4 | -0.1289 | [-0.1513, -0.1106] | 0.975 | +0.0239, -0.0577, -0.0030, +0.0368 | yes | 1.00 |
| native | T_obs_cal | content | inst | 4 | -0.1286 | [-0.1505, -0.1102] | 0.971 | +0.0213, -0.0127, -0.0339, +0.0253 | yes | 1.00 |
| native | T_obs_cal | outcome | base | 4 | -0.0860 | [-0.0980, -0.0763] | 0.984 | +0.0127, -0.0308, -0.0009, +0.0191 | yes | 1.00 |
| native | T_obs_cal | outcome | inst | 4 | -0.1018 | [-0.1127, -0.0923] | 0.971 | +0.0178, -0.0125, -0.0252, +0.0199 | yes | 1.00 |
| native | T_obs_cal | random | base | 4 | -0.0310 | [-0.0473, -0.0177] | 0.993 | +0.0029, -0.0063, -0.0017, +0.0051 | yes | 1.00 |
| native | T_obs_cal | random | inst | 4 | -0.0637 | [-0.0902, -0.0417] | 0.968 | -0.0077, +0.0198, -0.0143, +0.0021 | yes | 1.00 |
| native | T_obs_cal | random_novel | base | 4 | -0.0460 | [-0.0706, -0.0238] | 0.994 | +0.0036, -0.0064, -0.0054, +0.0082 | yes | 1.00 |
| native | T_obs_cal | random_novel | inst | 4 | -0.1035 | [-0.1437, -0.0701] | 0.972 | -0.0124, +0.0306, -0.0207, +0.0024 | yes | 1.00 |
| native | T_obs_cal | hash_novel | base | 4 | -0.0635 | [-0.1074, -0.0330] | 0.991 | +0.0068, -0.0142, -0.0058, +0.0132 | yes | 1.00 |
| native | T_obs_cal | hash_novel | inst | 4 | -0.1180 | [-0.1773, -0.0677] | 0.985 | -0.0171, +0.0255, +0.0006, -0.0090 | yes | 1.00 |
| native | T_obs_cal | boiler | base | 4 | -0.1663 | [-0.1742, -0.1584] | 0.985 | +0.0227, -0.0477, -0.0183, +0.0433 | yes | 1.00 |
| native | T_obs_cal | boiler | inst | 4 | -0.2305 | [-0.2411, -0.2194] | 0.707 | +0.1785, -0.1942, -0.1319, +0.1476 | NO | 0.09 |
| native | T_obs_cal | prompt_echo_ws | base | 4 | -0.0249 | [-0.0264, -0.0234] | 0.976 | +0.0045, -0.0097, -0.0029, +0.0081 | yes | 1.00 |
| native | T_obs_cal | prompt_echo_ws | inst | 4 | -0.0169 | [-0.0184, -0.0153] | 0.943 | -0.0006, +0.0050, -0.0072, +0.0028 | yes | 1.00 |
| native | T_cf_content | content | inst | 2 | -0.0790 | [-0.0939, -0.0638] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| native | T_cf_content | outcome | inst | 2 | -0.0655 | [-0.0774, -0.0516] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| native | T_cf_content | random | inst | 2 | -0.0492 | [-0.0882, -0.0170] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| native | T_cf_content | random_novel | inst | 2 | -0.0867 | [-0.1396, -0.0371] | 1.000 | -0.0000, +0.0000 | yes | 1.00 |
| native | capped2 | content | base | 4 | -0.0477 | [-0.0542, -0.0422] | 0.977 | +0.0084, -0.0210, +0.0005, +0.0121 | yes | 1.00 |
| native | capped2 | content | inst | 4 | -0.0229 | [-0.0284, -0.0183] | 0.850 | +0.0096, -0.0062, -0.0143, +0.0110 | yes | 0.66 |
| native | capped2 | outcome | base | 4 | -0.0417 | [-0.0490, -0.0366] | 0.983 | +0.0064, -0.0156, -0.0003, +0.0095 | yes | 1.00 |
| native | capped2 | outcome | inst | 4 | -0.0189 | [-0.0225, -0.0157] | 0.756 | +0.0093, -0.0039, -0.0178, +0.0123 | NO | 0.00 |
| native | capped2 | random | base | 4 | -0.0136 | [-0.0185, -0.0096] | 0.992 | +0.0014, -0.0033, -0.0002, +0.0021 | yes | 1.00 |
| native | capped2 | random | inst | 4 | -0.0008 | [-0.0049, +0.0031] **crosses 0** | 0.041 | +0.0050, -0.0064, -0.0022, +0.0035 | NO | 0.00 |
| native | capped2 | random_novel | base | 4 | -0.0174 | [-0.0266, -0.0104] | 0.994 | +0.0014, -0.0025, -0.0021, +0.0032 | yes | 1.00 |
| native | capped2 | random_novel | inst | 4 | -0.0038 | [-0.0108, +0.0028] **crosses 0** | 0.471 | +0.0049, -0.0058, -0.0029, +0.0038 | NO | 0.17 |
| native | capped2 | hash_novel | base | 4 | -0.0186 | [-0.0361, -0.0087] | 0.997 | +0.0000, +0.0013, -0.0030, +0.0017 | yes | 1.00 |
| native | capped2 | hash_novel | inst | 4 | -0.0112 | [-0.0262, -0.0028] | 0.856 | +0.0056, -0.0067, -0.0032, +0.0043 | yes | 0.89 |
| native | capped2 | boiler | base | 4 | -0.0232 | [-0.0265, -0.0202] | 0.824 | +0.0074, -0.0287, +0.0228, -0.0016 | NO | 0.00 |
| native | capped2 | boiler | inst | 4 | -0.0049 | [-0.0077, -0.0023] | 0.015 | +0.0481, -0.0657, -0.0124, +0.0299 | NO | 0.00 |
| native | capped2 | prompt_echo_ws | base | 4 | -0.0094 | [-0.0101, -0.0088] | 0.968 | +0.0019, -0.0050, +0.0004, +0.0026 | yes | 1.00 |
| native | capped2 | prompt_echo_ws | inst | 4 | -0.0019 | [-0.0023, -0.0016] | 0.398 | +0.0025, -0.0018, -0.0034, +0.0027 | NO | 0.00 |
| native | prob | content | base | 4 | +0.0228 | [+0.0203, +0.0258] | 0.976 | -0.0041, +0.0102, -0.0002, -0.0059 | yes | 1.00 |
| native | prob | content | inst | 4 | +0.0114 | [+0.0092, +0.0141] | 0.861 | -0.0046, +0.0030, +0.0068, -0.0052 | yes | 0.83 |
| native | prob | outcome | base | 4 | +0.0195 | [+0.0172, +0.0228] | 0.981 | -0.0031, +0.0076, +0.0001, -0.0046 | yes | 1.00 |
| native | prob | outcome | inst | 4 | +0.0098 | [+0.0083, +0.0115] | 0.800 | -0.0042, +0.0017, +0.0081, -0.0056 | NO | 0.01 |
| native | prob | random | base | 4 | +0.0068 | [+0.0049, +0.0092] | 0.991 | -0.0007, +0.0019, -0.0002, -0.0010 | yes | 1.00 |
| native | prob | random | inst | 4 | +0.0004 | [-0.0015, +0.0025] **crosses 0** | 0.040 | -0.0026, +0.0029, +0.0019, -0.0022 | NO | 0.00 |
| native | prob | random_novel | base | 4 | +0.0085 | [+0.0051, +0.0129] | 0.994 | -0.0007, +0.0014, +0.0009, -0.0015 | yes | 1.00 |
| native | prob | random_novel | inst | 4 | +0.0023 | [-0.0009, +0.0061] **crosses 0** | 0.517 | -0.0025, +0.0023, +0.0026, -0.0024 | NO | 0.08 |
| native | prob | hash_novel | base | 4 | +0.0091 | [+0.0042, +0.0173] | 0.998 | -0.0001, -0.0002, +0.0013, -0.0009 | yes | 1.00 |
| native | prob | hash_novel | inst | 4 | +0.0048 | [+0.0004, +0.0121] | 0.828 | -0.0027, +0.0031, +0.0016, -0.0021 | yes | 0.76 |
| native | prob | boiler | base | 4 | +0.0134 | [+0.0121, +0.0148] | 0.903 | -0.0030, +0.0117, -0.0094, +0.0007 | NO | 0.00 |
| native | prob | boiler | inst | 4 | +0.0071 | [+0.0059, +0.0083] | 0.113 | -0.0245, +0.0319, +0.0091, -0.0165 | NO | 0.00 |
| native | prob | prompt_echo_ws | base | 4 | +0.0047 | [+0.0044, +0.0050] | 0.966 | -0.0010, +0.0026, -0.0002, -0.0014 | yes | 1.00 |
| native | prob | prompt_echo_ws | inst | 4 | +0.0009 | [+0.0007, +0.0010] | 0.347 | -0.0012, +0.0009, +0.0017, -0.0014 | NO | 0.00 |
| native | rankrecal | content | inst | 2 | -0.0531 | [-0.0622, -0.0447] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| native | rankrecal | outcome | inst | 2 | -0.0437 | [-0.0522, -0.0353] | 1.000 | +0.0000, +0.0000 | yes | 1.00 |
| native | rankrecal | random | inst | 2 | -0.0050 | [-0.0428, +0.0688] **crosses 0** | 1.000 | -0.0000, +0.0000 | yes | 0.56 |
| native | rankrecal | random_novel | inst | 2 | +0.0007 | [-0.0660, +0.1226] **crosses 0** | 1.000 | -0.0000, +0.0000 | NO | 0.42 |

## SECONDARY (superseded): global-slope n = 2^(Δ/b) — fragile, ladder is concave

| rendering | metric | mask | pair | start | post | Δ [95% CI] | doublings [95% CI] | n [95% CI] | n, local slope [95% CI] | flags |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | raw | content | Nemo-8B vs Qwen3-8B | 0.9539 | 0.9317 | -0.0222 [-0.0553, +0.0100] | +0.13 [-0.06, +0.30] | 1.09 [0.96, 1.23] | 1.08 [0.96, 1.20] (4B/14B) |  |
| neutral | raw | content | Nemo-14B vs Qwen3-14B | 0.7809 | 0.7510 | -0.0299 [-0.0506, -0.0104] | +0.17 [+0.06, +0.30] | 1.13 [1.04, 1.23] | 1.14 [1.04, 1.25] (8B/32B) |  |
| neutral | raw | content | Nemo-32B vs Qwen3-32B | 0.6281 | 0.6545 | +0.0264 [+0.0112, +0.0402] | -0.15 [-0.23, -0.07] | 0.90 [0.86, 0.95] | 0.87 [0.82, 0.94] (14B/32B) |  |
| neutral | raw | content | Qwen3-4B vs Qwen3-4B-Base | 0.6869 | 1.1440 | +0.4571 [+0.4170, +0.4975] | -3.62 [-3.96, -3.29] | 0.08 [0.06, 0.10] | 0.09 [0.08, 0.11] (0.6B/8B) |  |
| neutral | raw | content | Qwen3-8B vs Qwen3-8B-Base | 0.6153 | 0.9539 | +0.3386 [+0.3070, +0.3728] | -2.68 [-2.93, -2.44] | 0.16 [0.13, 0.18] | 0.05 [0.02, 0.08] (4B/14B) |  |
| neutral | raw | content | Qwen3-14B vs Qwen3-14B-Base | 0.5445 | 0.7809 | +0.2364 [+0.2105, +0.2656] | -1.87 [-2.04, -1.73] | 0.27 [0.24, 0.30] | 0.14 [0.08, 0.21] (8B/14B) |  |
| neutral | raw | outcome | Nemo-8B vs Qwen3-8B | 1.1049 | 1.0701 | -0.0348 [-0.0746, +0.0017] | +0.25 [-0.01, +0.51] | 1.19 [0.99, 1.43] | 1.17 [0.99, 1.39] (4B/14B) |  |
| neutral | raw | outcome | Nemo-14B vs Qwen3-14B | 0.9622 | 0.9108 | -0.0514 [-0.0762, -0.0282] | +0.37 [+0.20, +0.55] | 1.29 [1.15, 1.47] | 1.30 [1.16, 1.48] (8B/32B) |  |
| neutral | raw | outcome | Nemo-32B vs Qwen3-32B | 0.8298 | 0.8630 | +0.0333 [+0.0137, +0.0533] | -0.24 [-0.38, -0.10] | 0.85 [0.77, 0.93] | 0.82 [0.72, 0.92] (14B/32B) |  |
| neutral | raw | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.8504 | 1.2460 | +0.3955 [+0.3584, +0.4352] | -4.68 [-5.22, -4.20] | 0.04 [0.03, 0.05] | 0.04 [0.03, 0.06] (0.6B/8B) |  |
| neutral | raw | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7948 | 1.1049 | +0.3100 [+0.2759, +0.3450] | -3.67 [-4.11, -3.28] | 0.08 [0.06, 0.10] | 0.03 [0.01, 0.04] (4B/14B) |  |
| neutral | raw | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.7406 | 0.9622 | +0.2215 [+0.1945, +0.2513] | -2.62 [-3.04, -2.22] | 0.16 [0.12, 0.22] | 0.09 [0.05, 0.14] (8B/14B) |  |
| neutral | T_obs_cal | content | Nemo-8B vs Qwen3-8B | 0.7934 | 0.9060 | +0.1126 [+0.0895, +0.1354] | -0.96 [-1.23, -0.73] | 0.52 [0.43, 0.60] | 0.58 [0.51, 0.66] (4B/14B) |  |
| neutral | T_obs_cal | content | Nemo-14B vs Qwen3-14B | 0.6783 | 0.7329 | +0.0545 [+0.0361, +0.0732] | -0.46 [-0.60, -0.33] | 0.73 [0.66, 0.80] | 0.68 [0.60, 0.76] (8B/32B) |  |
| neutral | T_obs_cal | content | Nemo-32B vs Qwen3-32B | 0.5972 | 0.6338 | +0.0365 [+0.0218, +0.0507] | -0.31 [-0.41, -0.20] | 0.81 [0.75, 0.87] | 0.70 [0.62, 0.79] (14B/32B) |  |
| neutral | T_obs_cal | content | Qwen3-4B vs Qwen3-4B-Base | 0.6869 | 0.9509 | +0.2640 [+0.2374, +0.2899] | -2.09 [-2.29, -1.88] | 0.23 [0.20, 0.27] | 0.25 [0.22, 0.28] (0.6B/8B) |  |
| neutral | T_obs_cal | content | Qwen3-8B vs Qwen3-8B-Base | 0.6153 | 0.7934 | +0.1781 [+0.1582, +0.1983] | -1.41 [-1.54, -1.28] | 0.38 [0.34, 0.41] | 0.20 [0.14, 0.27] (4B/14B) |  |
| neutral | T_obs_cal | content | Qwen3-14B vs Qwen3-14B-Base | 0.5445 | 0.6783 | +0.1338 [+0.1148, +0.1550] | -1.06 [-1.14, -0.98] | 0.48 [0.45, 0.51] | 0.33 [0.25, 0.41] (8B/14B) |  |
| neutral | T_obs_cal | outcome | Nemo-8B vs Qwen3-8B | 0.9276 | 1.0264 | +0.0988 [+0.0690, +0.1292] | -1.16 [-1.56, -0.78] | 0.45 [0.34, 0.58] | 0.53 [0.42, 0.65] (4B/14B) |  |
| neutral | T_obs_cal | outcome | Nemo-14B vs Qwen3-14B | 0.8493 | 0.8747 | +0.0253 [+0.0056, +0.0445] | -0.30 [-0.53, -0.06] | 0.81 [0.69, 0.96] | 0.77 [0.62, 0.95] (8B/32B) |  |
| neutral | T_obs_cal | outcome | Nemo-32B vs Qwen3-32B | 0.7922 | 0.8332 | +0.0410 [+0.0233, +0.0589] | -0.48 [-0.70, -0.28] | 0.72 [0.62, 0.83] | 0.56 [0.42, 0.73] (14B/32B) |  |
| neutral | T_obs_cal | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.8504 | 1.0494 | +0.1990 [+0.1767, +0.2220] | -2.36 [-2.62, -2.13] | 0.20 [0.16, 0.23] | 0.21 [0.18, 0.24] (0.6B/8B) |  |
| neutral | T_obs_cal | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7948 | 0.9276 | +0.1328 [+0.1159, +0.1524] | -1.57 [-1.75, -1.40] | 0.34 [0.30, 0.38] | 0.21 [0.16, 0.26] (4B/14B) |  |
| neutral | T_obs_cal | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.7406 | 0.8493 | +0.1087 [+0.0934, +0.1252] | -1.29 [-1.49, -1.09] | 0.41 [0.36, 0.47] | 0.31 [0.22, 0.38] (8B/14B) |  |
| neutral | T_cf_content | content | Nemo-14B vs Qwen3-14B | 0.6760 | 0.7245 | +0.0485 [+0.0298, +0.0670] | -0.71 [-1.02, -0.42] | 0.61 [0.49, 0.75] | 0.61 [0.49, 0.75] (14B/32B) | 2-pt slope |
| neutral | T_cf_content | content | Nemo-32B vs Qwen3-32B | 0.5973 | 0.6338 | +0.0365 [+0.0221, +0.0505] | -0.53 [-0.70, -0.35] | 0.69 [0.61, 0.79] | 0.69 [0.61, 0.79] (14B/32B) | 2-pt slope |
| neutral | T_cf_content | outcome | Nemo-14B vs Qwen3-14B | 0.8390 | 0.8767 | +0.0376 [+0.0177, +0.0545] | -0.85 [-1.34, -0.35] | 0.56 [0.39, 0.78] | 0.56 [0.39, 0.78] (14B/32B) | 2-pt slope |
| neutral | T_cf_content | outcome | Nemo-32B vs Qwen3-32B | 0.7879 | 0.8332 | +0.0453 [+0.0284, +0.0642] | -1.02 [-1.46, -0.61] | 0.49 [0.36, 0.65] | 0.49 [0.36, 0.65] (14B/32B) | 2-pt slope |
| neutral | capped2 | content | Nemo-8B vs Qwen3-8B | 0.2923 | 0.3837 | +0.0915 [+0.0838, +0.0993] | -3.68 [-4.46, -3.07] | 0.08 [0.05, 0.12] | 0.18 [0.14, 0.23] (4B/14B) |  |
| neutral | capped2 | content | Nemo-14B vs Qwen3-14B | 0.2627 | 0.3171 | +0.0545 [+0.0469, +0.0622] | -2.19 [-2.60, -1.86] | 0.22 [0.16, 0.28] | 0.11 [0.05, 0.17] (8B/32B) |  |
| neutral | capped2 | content | Nemo-32B vs Qwen3-32B | 0.2584 | 0.2850 | +0.0266 [+0.0200, +0.0329] | -1.07 [-1.28, -0.88] | 0.48 [0.41, 0.54] | 0.01 [0.00, 134898329.27] (14B/32B) |  |
| neutral | capped2 | content | Qwen3-4B vs Qwen3-4B-Base | 0.3189 | 0.3320 | +0.0130 [+0.0070, +0.0194] | -0.27 [-0.39, -0.15] | 0.83 [0.76, 0.90] | 0.84 [0.77, 0.91] (0.6B/8B) |  |
| neutral | capped2 | content | Qwen3-8B vs Qwen3-8B-Base | 0.2895 | 0.2923 | +0.0027 [-0.0014, +0.0068] | -0.06 [-0.14, +0.03] | 0.96 [0.91, 1.02] | 0.94 [0.85, 1.03] (4B/14B) |  |
| neutral | capped2 | content | Qwen3-14B vs Qwen3-14B-Base | 0.2637 | 0.2627 | -0.0011 [-0.0062, +0.0047] | +0.02 [-0.09, +0.14] | 1.02 [0.94, 1.10] | 1.02 [0.92, 1.21] (8B/14B) |  |
| neutral | capped2 | outcome | Nemo-8B vs Qwen3-8B | 0.4388 | 0.5285 | +0.0898 [+0.0787, +0.1011] | -4.24 [-5.16, -3.48] | 0.05 [0.03, 0.09] | 0.18 [0.13, 0.23] (4B/14B) |  |
| neutral | capped2 | outcome | Nemo-14B vs Qwen3-14B | 0.4059 | 0.4611 | +0.0553 [+0.0455, +0.0653] | -2.61 [-3.31, -2.06] | 0.16 [0.10, 0.24] | 0.06 [0.01, 0.13] (8B/32B) |  |
| neutral | capped2 | outcome | Nemo-32B vs Qwen3-32B | 0.4121 | 0.4479 | +0.0358 [+0.0279, +0.0447] | -1.69 [-2.20, -1.28] | 0.31 [0.22, 0.41] | 99.76 [9.90, 23983858.81] (14B/32B) |  |
| neutral | capped2 | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.4690 | 0.4729 | +0.0039 [-0.0026, +0.0099] | -0.09 [-0.22, +0.07] | 0.94 [0.86, 1.05] | 0.94 [0.87, 1.04] (0.6B/8B) |  |
| neutral | capped2 | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.4396 | 0.4388 | -0.0008 [-0.0064, +0.0047] | +0.02 [-0.10, +0.16] | 1.01 [0.93, 1.12] | 1.02 [0.89, 1.18] (4B/14B) |  |
| neutral | capped2 | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.4176 | 0.4059 | -0.0118 [-0.0159, -0.0080] | +0.27 [+0.17, +0.40] | 1.21 [1.13, 1.32] | 1.37 [1.20, 1.68] (8B/14B) |  |
| neutral | prob | content | Nemo-8B vs Qwen3-8B | 0.8609 | 0.8177 | -0.0432 [-0.0468, -0.0396] | -3.56 [-4.31, -2.96] | 0.08 [0.05, 0.13] | 0.19 [0.14, 0.24] (4B/14B) |  |
| neutral | prob | content | Nemo-14B vs Qwen3-14B | 0.8751 | 0.8493 | -0.0258 [-0.0294, -0.0224] | -2.13 [-2.52, -1.80] | 0.23 [0.17, 0.29] | 0.12 [0.06, 0.18] (8B/32B) |  |
| neutral | prob | content | Nemo-32B vs Qwen3-32B | 0.8776 | 0.8648 | -0.0128 [-0.0157, -0.0097] | -1.05 [-1.25, -0.87] | 0.48 [0.42, 0.55] | 0.02 [0.00, 0.11] (14B/32B) |  |
| neutral | prob | content | Qwen3-4B vs Qwen3-4B-Base | 0.8485 | 0.8416 | -0.0070 [-0.0099, -0.0042] | -0.30 [-0.42, -0.18] | 0.81 [0.75, 0.88] | 0.82 [0.76, 0.89] (0.6B/8B) |  |
| neutral | prob | content | Qwen3-8B vs Qwen3-8B-Base | 0.8624 | 0.8609 | -0.0015 [-0.0034, +0.0005] | -0.07 [-0.14, +0.02] | 0.96 [0.90, 1.02] | 0.93 [0.84, 1.03] (4B/14B) |  |
| neutral | prob | content | Qwen3-14B vs Qwen3-14B-Base | 0.8746 | 0.8751 | +0.0005 [-0.0023, +0.0030] | +0.02 [-0.09, +0.14] | 1.02 [0.94, 1.10] | 1.03 [0.92, 1.21] (8B/14B) |  |
| neutral | prob | outcome | Nemo-8B vs Qwen3-8B | 0.7960 | 0.7548 | -0.0413 [-0.0464, -0.0361] | -3.94 [-4.72, -3.28] | 0.07 [0.04, 0.10] | 0.19 [0.14, 0.24] (4B/14B) |  |
| neutral | prob | outcome | Nemo-14B vs Qwen3-14B | 0.8117 | 0.7866 | -0.0251 [-0.0295, -0.0208] | -2.40 [-2.97, -1.91] | 0.19 [0.13, 0.27] | 0.08 [0.03, 0.16] (8B/32B) |  |
| neutral | prob | outcome | Nemo-32B vs Qwen3-32B | 0.8099 | 0.7928 | -0.0171 [-0.0214, -0.0134] | -1.63 [-2.10, -1.25] | 0.32 [0.23, 0.42] | 1984.54 [0.00, 16868831662316174030749564928.00] (14B/32B) |  |
| neutral | prob | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.7838 | 0.7797 | -0.0041 [-0.0067, -0.0013] | -0.21 [-0.33, -0.07] | 0.87 [0.80, 0.95] | 0.87 [0.81, 0.96] (0.6B/8B) |  |
| neutral | prob | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7969 | 0.7960 | -0.0009 [-0.0034, +0.0015] | -0.05 [-0.16, +0.08] | 0.97 [0.90, 1.06] | 0.95 [0.84, 1.09] (4B/14B) |  |
| neutral | prob | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.8074 | 0.8117 | +0.0043 [+0.0027, +0.0061] | +0.22 [+0.13, +0.33] | 1.16 [1.09, 1.25] | 1.28 [1.14, 1.51] (8B/14B) |  |
| neutral | rankrecal | content | Nemo-14B vs Qwen3-14B | 0.5183 | 0.5599 | +0.0416 [+0.0282, +0.0546] | -0.85 [-1.18, -0.59] | 0.55 [0.44, 0.67] | 0.55 [0.44, 0.67] (14B/32B) | 2-pt slope |
| neutral | rankrecal | content | Nemo-32B vs Qwen3-32B | 0.4624 | 0.4965 | +0.0342 [+0.0231, +0.0447] | -0.70 [-0.90, -0.50] | 0.61 [0.54, 0.71] | 0.61 [0.54, 0.71] (14B/32B) | 2-pt slope |
| neutral | rankrecal | outcome | Nemo-14B vs Qwen3-14B | 0.6691 | 0.7039 | +0.0348 [+0.0203, +0.0481] | -1.00 [-1.55, -0.52] | 0.50 [0.34, 0.70] | 0.50 [0.34, 0.70] (14B/32B) | 2-pt slope |
| neutral | rankrecal | outcome | Nemo-32B vs Qwen3-32B | 0.6290 | 0.6764 | +0.0474 [+0.0316, +0.0640] | -1.36 [-1.87, -0.92] | 0.39 [0.27, 0.53] | 0.39 [0.27, 0.53] (14B/32B) | 2-pt slope |
| native | raw | content | Nemo-8B vs Qwen3-8B | 1.0790 | 0.9059 | -0.1730 [-0.2121, -0.1371] | +0.80 [+0.66, +0.95] | 1.74 [1.58, 1.93] | 1.66 [1.51, 1.84] (4B/14B) |  |
| native | raw | content | Nemo-14B vs Qwen3-14B | 0.8380 | 0.7645 | -0.0734 [-0.0969, -0.0515] | +0.34 [+0.24, +0.45] | 1.27 [1.18, 1.37] | 1.26 [1.18, 1.37] (8B/32B) |  |
| native | raw | content | Nemo-32B vs Qwen3-32B | 0.6446 | 0.6643 | +0.0198 [+0.0042, +0.0347] | -0.09 [-0.16, -0.02] | 0.94 [0.90, 0.99] | 0.92 [0.87, 0.98] (14B/32B) |  |
| native | raw | content | Qwen3-4B vs Qwen3-4B-Base | 0.6936 | 1.2826 | +0.5890 [+0.5410, +0.6363] | -4.57 [-5.05, -4.14] | 0.04 [0.03, 0.06] | 0.05 [0.04, 0.06] (0.6B/8B) |  |
| native | raw | content | Qwen3-8B vs Qwen3-8B-Base | 0.6161 | 1.0790 | +0.4628 [+0.4218, +0.5058] | -3.59 [-3.99, -3.23] | 0.08 [0.06, 0.11] | 0.02 [0.01, 0.04] (4B/14B) |  |
| native | raw | content | Qwen3-14B vs Qwen3-14B-Base | 0.5462 | 0.8380 | +0.2917 [+0.2630, +0.3230] | -2.26 [-2.49, -2.07] | 0.21 [0.18, 0.24] | 0.09 [0.04, 0.15] (8B/14B) |  |
| native | raw | outcome | Nemo-8B vs Qwen3-8B | 1.2478 | 1.0634 | -0.1844 [-0.2268, -0.1447] | +0.91 [+0.74, +1.10] | 1.88 [1.67, 2.14] | 1.79 [1.59, 2.04] (4B/14B) |  |
| native | raw | outcome | Nemo-14B vs Qwen3-14B | 1.0295 | 0.9223 | -0.1072 [-0.1371, -0.0785] | +0.53 [+0.39, +0.68] | 1.44 [1.31, 1.60] | 1.44 [1.31, 1.59] (8B/32B) |  |
| native | raw | outcome | Nemo-32B vs Qwen3-32B | 0.8387 | 0.8718 | +0.0331 [+0.0131, +0.0531] | -0.16 [-0.26, -0.06] | 0.89 [0.83, 0.96] | 0.87 [0.80, 0.95] (14B/32B) |  |
| native | raw | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.8522 | 1.4398 | +0.5876 [+0.5356, +0.6427] | -6.83 [-7.69, -6.07] | 0.01 [0.00, 0.01] | 0.01 [0.01, 0.02] (0.6B/8B) |  |
| native | raw | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7939 | 1.2478 | +0.4539 [+0.4081, +0.5001] | -5.28 [-5.96, -4.67] | 0.03 [0.02, 0.04] | 0.01 [0.00, 0.01] (4B/14B) |  |
| native | raw | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.7407 | 1.0295 | +0.2888 [+0.2549, +0.3264] | -3.36 [-3.88, -2.85] | 0.10 [0.07, 0.14] | 0.04 [0.02, 0.08] (8B/14B) |  |
| native | T_obs_cal | content | Nemo-8B vs Qwen3-8B | 0.8291 | 0.8838 | +0.0547 [+0.0323, +0.0764] | -0.43 [-0.60, -0.26] | 0.74 [0.66, 0.84] | 0.79 [0.71, 0.86] (4B/14B) |  |
| native | T_obs_cal | content | Nemo-14B vs Qwen3-14B | 0.6985 | 0.7731 | +0.0746 [+0.0546, +0.0944] | -0.58 [-0.71, -0.45] | 0.67 [0.61, 0.73] | 0.62 [0.56, 0.69] (8B/32B) |  |
| native | T_obs_cal | content | Nemo-32B vs Qwen3-32B | 0.6099 | 0.6438 | +0.0339 [+0.0187, +0.0488] | -0.26 [-0.36, -0.15] | 0.83 [0.78, 0.90] | 0.74 [0.66, 0.83] (14B/32B) |  |
| native | T_obs_cal | content | Qwen3-4B vs Qwen3-4B-Base | 0.6936 | 0.9950 | +0.3015 [+0.2714, +0.3310] | -2.34 [-2.56, -2.11] | 0.20 [0.17, 0.23] | 0.22 [0.19, 0.24] (0.6B/8B) |  |
| native | T_obs_cal | content | Qwen3-8B vs Qwen3-8B-Base | 0.6161 | 0.8291 | +0.2130 [+0.1924, +0.2337] | -1.65 [-1.83, -1.49] | 0.32 [0.28, 0.36] | 0.15 [0.10, 0.22] (4B/14B) |  |
| native | T_obs_cal | content | Qwen3-14B vs Qwen3-14B-Base | 0.5462 | 0.6985 | +0.1523 [+0.1328, +0.1741] | -1.18 [-1.29, -1.09] | 0.44 [0.41, 0.47] | 0.28 [0.20, 0.36] (8B/14B) |  |
| native | T_obs_cal | outcome | Nemo-8B vs Qwen3-8B | 0.9701 | 1.0205 | +0.0504 [+0.0200, +0.0812] | -0.50 [-0.81, -0.19] | 0.71 [0.57, 0.88] | 0.76 [0.64, 0.90] (4B/14B) |  |
| native | T_obs_cal | outcome | Nemo-14B vs Qwen3-14B | 0.8708 | 0.8972 | +0.0264 [+0.0044, +0.0481] | -0.26 [-0.48, -0.04] | 0.84 [0.72, 0.97] | 0.81 [0.67, 0.97] (8B/32B) |  |
| native | T_obs_cal | outcome | Nemo-32B vs Qwen3-32B | 0.7988 | 0.8422 | +0.0433 [+0.0253, +0.0618] | -0.43 [-0.60, -0.25] | 0.74 [0.66, 0.84] | 0.62 [0.49, 0.76] (14B/32B) |  |
| native | T_obs_cal | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.8522 | 1.1049 | +0.2527 [+0.2277, +0.2792] | -2.94 [-3.29, -2.64] | 0.13 [0.10, 0.16] | 0.14 [0.11, 0.17] (0.6B/8B) |  |
| native | T_obs_cal | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7939 | 0.9701 | +0.1762 [+0.1564, +0.1977] | -2.05 [-2.30, -1.82] | 0.24 [0.20, 0.28] | 0.13 [0.09, 0.17] (4B/14B) |  |
| native | T_obs_cal | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.7407 | 0.8708 | +0.1301 [+0.1132, +0.1489] | -1.51 [-1.75, -1.29] | 0.35 [0.30, 0.41] | 0.24 [0.15, 0.31] (8B/14B) |  |
| native | T_cf_content | content | Nemo-14B vs Qwen3-14B | 0.6988 | 0.7376 | +0.0389 [+0.0203, +0.0588] | -0.49 [-0.77, -0.26] | 0.71 [0.59, 0.83] | 0.71 [0.59, 0.83] (14B/32B) | 2-pt slope |
| native | T_cf_content | content | Nemo-32B vs Qwen3-32B | 0.6079 | 0.6438 | +0.0359 [+0.0209, +0.0503] | -0.45 [-0.61, -0.28] | 0.73 [0.65, 0.82] | 0.73 [0.65, 0.82] (14B/32B) | 2-pt slope |
| native | T_cf_content | outcome | Nemo-14B vs Qwen3-14B | 0.8656 | 0.8881 | +0.0225 [+0.0026, +0.0447] | -0.34 [-0.77, -0.04] | 0.79 [0.59, 0.97] | 0.79 [0.59, 0.97] (14B/32B) | 2-pt slope |
| native | T_cf_content | outcome | Nemo-32B vs Qwen3-32B | 0.7903 | 0.8422 | +0.0519 [+0.0337, +0.0702] | -0.79 [-1.14, -0.52] | 0.58 [0.45, 0.70] | 0.58 [0.45, 0.70] (14B/32B) | 2-pt slope |
| native | capped2 | content | Nemo-8B vs Qwen3-8B | 0.2882 | 0.3747 | +0.0865 [+0.0787, +0.0938] | -3.78 [-4.59, -3.16] | 0.07 [0.04, 0.11] | 0.19 [0.14, 0.23] (4B/14B) |  |
| native | capped2 | content | Nemo-14B vs Qwen3-14B | 0.2607 | 0.3226 | +0.0619 [+0.0545, +0.0697] | -2.70 [-3.26, -2.28] | 0.15 [0.10, 0.21] | 0.05 [0.02, 0.10] (8B/32B) |  |
| native | capped2 | content | Nemo-32B vs Qwen3-32B | 0.2597 | 0.2889 | +0.0292 [+0.0227, +0.0356] | -1.28 [-1.53, -1.06] | 0.41 [0.35, 0.48] | 0.00 [0.00, 22851441620219925033426396840468661535257747831724980568064.00] (14B/32B) |  |
| native | capped2 | content | Qwen3-4B vs Qwen3-4B-Base | 0.3208 | 0.3276 | +0.0067 [+0.0001, +0.0134] | -0.14 [-0.27, -0.00] | 0.91 [0.83, 1.00] | 0.91 [0.84, 1.00] (0.6B/8B) |  |
| native | capped2 | content | Qwen3-8B vs Qwen3-8B-Base | 0.2933 | 0.2882 | -0.0051 [-0.0096, -0.0005] | +0.11 [+0.01, +0.21] | 1.08 [1.01, 1.16] | 1.12 [1.01, 1.27] (4B/14B) |  |
| native | capped2 | content | Qwen3-14B vs Qwen3-14B-Base | 0.2643 | 0.2607 | -0.0037 [-0.0090, +0.0022] | +0.08 [-0.04, +0.20] | 1.05 [0.97, 1.15] | 1.08 [0.97, 1.27] (8B/14B) |  |
| native | capped2 | outcome | Nemo-8B vs Qwen3-8B | 0.4325 | 0.5238 | +0.0913 [+0.0804, +0.1024] | -4.82 [-5.98, -3.89] | 0.04 [0.02, 0.07] | 0.15 [0.11, 0.20] (4B/14B) |  |
| native | capped2 | outcome | Nemo-14B vs Qwen3-14B | 0.4025 | 0.4661 | +0.0636 [+0.0528, +0.0744] | -3.36 [-4.31, -2.61] | 0.10 [0.05, 0.16] | 0.02 [0.00, 0.07] (8B/32B) |  |
| native | capped2 | outcome | Nemo-32B vs Qwen3-32B | 0.4109 | 0.4515 | +0.0407 [+0.0328, +0.0496] | -2.15 [-2.79, -1.64] | 0.23 [0.14, 0.32] | 48.05 [9.64, 6918.26] (14B/32B) |  |
| native | capped2 | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.4715 | 0.4651 | -0.0064 [-0.0133, +0.0001] | +0.15 [-0.00, +0.34] | 1.11 [1.00, 1.27] | 1.11 [1.00, 1.26] (0.6B/8B) |  |
| native | capped2 | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.4439 | 0.4325 | -0.0115 [-0.0173, -0.0057] | +0.27 [+0.12, +0.44] | 1.21 [1.09, 1.36] | 1.32 [1.15, 1.54] (4B/14B) |  |
| native | capped2 | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.4183 | 0.4025 | -0.0158 [-0.0201, -0.0117] | +0.38 [+0.26, +0.52] | 1.30 [1.20, 1.43] | 1.44 [1.27, 1.72] (8B/14B) |  |
| native | prob | content | Nemo-8B vs Qwen3-8B | 0.8623 | 0.8219 | -0.0404 [-0.0437, -0.0368] | -3.54 [-4.27, -2.96] | 0.09 [0.05, 0.13] | 0.20 [0.16, 0.25] (4B/14B) |  |
| native | prob | content | Nemo-14B vs Qwen3-14B | 0.8758 | 0.8468 | -0.0291 [-0.0326, -0.0256] | -2.55 [-3.06, -2.15] | 0.17 [0.12, 0.23] | 0.06 [0.02, 0.12] (8B/32B) |  |
| native | prob | content | Nemo-32B vs Qwen3-32B | 0.8769 | 0.8629 | -0.0140 [-0.0170, -0.0109] | -1.23 [-1.47, -1.03] | 0.43 [0.36, 0.49] | 0.00 [0.00, 121095386273391939512202874785240186880.00] (14B/32B) |  |
| native | prob | content | Qwen3-4B vs Qwen3-4B-Base | 0.8476 | 0.8431 | -0.0045 [-0.0076, -0.0015] | -0.20 [-0.32, -0.07] | 0.87 [0.80, 0.96] | 0.88 [0.81, 0.96] (0.6B/8B) |  |
| native | prob | content | Qwen3-8B vs Qwen3-8B-Base | 0.8606 | 0.8623 | +0.0017 [-0.0005, +0.0038] | +0.07 [-0.02, +0.18] | 1.05 [0.99, 1.13] | 1.09 [0.98, 1.23] (4B/14B) |  |
| native | prob | content | Qwen3-14B vs Qwen3-14B-Base | 0.8743 | 0.8758 | +0.0016 [-0.0013, +0.0041] | +0.07 [-0.05, +0.20] | 1.05 [0.96, 1.15] | 1.07 [0.96, 1.26] (8B/14B) |  |
| native | prob | outcome | Nemo-8B vs Qwen3-8B | 0.7979 | 0.7568 | -0.0410 [-0.0461, -0.0361] | -4.19 [-5.09, -3.44] | 0.05 [0.03, 0.09] | 0.18 [0.13, 0.23] (4B/14B) |  |
| native | prob | outcome | Nemo-14B vs Qwen3-14B | 0.8127 | 0.7845 | -0.0281 [-0.0328, -0.0235] | -2.87 [-3.59, -2.28] | 0.14 [0.08, 0.21] | 0.04 [0.01, 0.11] (8B/32B) |  |
| native | prob | outcome | Nemo-32B vs Qwen3-32B | 0.8102 | 0.7910 | -0.0191 [-0.0232, -0.0154] | -1.95 [-2.49, -1.50] | 0.26 [0.18, 0.35] | 441.50 [18.99, 196780947864.92] (14B/32B) |  |
| native | prob | outcome | Qwen3-4B vs Qwen3-4B-Base | 0.7827 | 0.7819 | -0.0008 [-0.0037, +0.0022] | -0.04 [-0.18, +0.12] | 0.97 [0.89, 1.09] | 0.97 [0.89, 1.09] (0.6B/8B) |  |
| native | prob | outcome | Qwen3-8B vs Qwen3-8B-Base | 0.7952 | 0.7979 | +0.0027 [+0.0002, +0.0052] | +0.14 [+0.01, +0.29] | 1.10 [1.01, 1.22] | 1.15 [1.01, 1.34] (4B/14B) |  |
| native | prob | outcome | Qwen3-14B vs Qwen3-14B-Base | 0.8071 | 0.8127 | +0.0055 [+0.0038, +0.0075] | +0.28 [+0.18, +0.41] | 1.22 [1.13, 1.33] | 1.31 [1.18, 1.53] (8B/14B) |  |
| native | rankrecal | content | Nemo-14B vs Qwen3-14B | 0.5310 | 0.5696 | +0.0386 [+0.0245, +0.0525] | -0.73 [-1.02, -0.45] | 0.60 [0.49, 0.73] | 0.60 [0.49, 0.73] (14B/32B) | 2-pt slope |
| native | rankrecal | content | Nemo-32B vs Qwen3-32B | 0.4699 | 0.5022 | +0.0323 [+0.0210, +0.0430] | -0.61 [-0.79, -0.42] | 0.66 [0.58, 0.75] | 0.66 [0.58, 0.75] (14B/32B) | 2-pt slope |
| native | rankrecal | outcome | Nemo-14B vs Qwen3-14B | 0.6827 | 0.7127 | +0.0300 [+0.0138, +0.0451] | -0.69 [-1.13, -0.29] | 0.62 [0.46, 0.82] | 0.62 [0.46, 0.82] (14B/32B) | 2-pt slope |
| native | rankrecal | outcome | Nemo-32B vs Qwen3-32B | 0.6324 | 0.6796 | +0.0472 [+0.0300, +0.0636] | -1.08 [-1.47, -0.72] | 0.47 [0.36, 0.61] | 0.47 [0.36, 0.61] (14B/32B) | 2-pt slope |

## Ladder values (point [95% CI])

- neutral|raw|content|base: Qwen3-0.6B-Base 1.1179 [0.9828,1.2612]; Qwen3-4B-Base 0.6869 [0.5956,0.7817]; Qwen3-8B-Base 0.6153 [0.5361,0.6976]; Qwen3-14B-Base 0.5445 [0.4801,0.6093]
- neutral|raw|content|inst: Qwen3-4B 1.1440 [1.0194,1.2684]; Qwen3-8B 0.9539 [0.8499,1.0600]; Qwen3-14B 0.7809 [0.6954,0.8658]; Qwen3-32B 0.6281 [0.5595,0.6977]
- neutral|raw|outcome|base: Qwen3-0.6B-Base 1.1261 [1.0327,1.2261]; Qwen3-4B-Base 0.8504 [0.7690,0.9383]; Qwen3-8B-Base 0.7948 [0.7185,0.8768]; Qwen3-14B-Base 0.7406 [0.6644,0.8256]
- neutral|raw|outcome|inst: Qwen3-4B 1.2460 [1.1456,1.3537]; Qwen3-8B 1.1049 [1.0139,1.2024]; Qwen3-14B 0.9622 [0.8717,1.0625]; Qwen3-32B 0.8298 [0.7487,0.9186]
- neutral|raw|random|base: Qwen3-0.6B-Base 2.3524 [1.3381,3.2339]; Qwen3-4B-Base 2.2616 [1.2794,3.1022]; Qwen3-8B-Base 2.2322 [1.2505,3.0690]; Qwen3-14B-Base 2.2126 [1.2317,3.0462]
- neutral|raw|random|inst: Qwen3-4B 2.4061 [1.4080,3.2681]; Qwen3-8B 2.3605 [1.3735,3.2192]; Qwen3-14B 2.2950 [1.2891,3.1610]; Qwen3-32B 2.2677 [1.2592,3.1296]
- neutral|raw|random_novel|base: Qwen3-0.6B-Base 3.9142 [2.6875,4.8709]; Qwen3-4B-Base 3.7860 [2.6083,4.6676]; Qwen3-8B-Base 3.7374 [2.5611,4.6224]; Qwen3-14B-Base 3.7112 [2.5251,4.5849]
- neutral|raw|random_novel|inst: Qwen3-4B 4.0186 [2.8430,4.9289]; Qwen3-8B 3.9557 [2.7969,4.8527]; Qwen3-14B 3.8525 [2.6539,4.7651]; Qwen3-32B 3.8067 [2.5891,4.7191]
- neutral|raw|hash_novel|base: Qwen3-0.6B-Base 5.1737 [3.8324,6.2698]; Qwen3-4B-Base 4.9800 [3.6435,5.9977]; Qwen3-8B-Base 4.9203 [3.5524,5.9275]; Qwen3-14B-Base 4.8881 [3.5087,5.8843]
- neutral|raw|hash_novel|inst: Qwen3-4B 5.1905 [3.8399,6.2374]; Qwen3-8B 5.0985 [3.7211,6.1369]; Qwen3-14B 5.0563 [3.6496,6.1060]; Qwen3-32B 5.0034 [3.5850,6.0482]
- neutral|T_obs_cal|content|base: Qwen3-0.6B-Base 1.1179 [0.9828,1.2612]; Qwen3-4B-Base 0.6869 [0.5956,0.7817]; Qwen3-8B-Base 0.6153 [0.5361,0.6976]; Qwen3-14B-Base 0.5445 [0.4801,0.6093]
- neutral|T_obs_cal|content|inst: Qwen3-4B 0.9509 [0.8393,1.0644]; Qwen3-8B 0.7934 [0.6978,0.8919]; Qwen3-14B 0.6783 [0.5984,0.7576]; Qwen3-32B 0.5972 [0.5301,0.6659]
- neutral|T_obs_cal|outcome|base: Qwen3-0.6B-Base 1.1261 [1.0327,1.2261]; Qwen3-4B-Base 0.8504 [0.7690,0.9383]; Qwen3-8B-Base 0.7948 [0.7185,0.8768]; Qwen3-14B-Base 0.7406 [0.6644,0.8256]
- neutral|T_obs_cal|outcome|inst: Qwen3-4B 1.0494 [0.9635,1.1460]; Qwen3-8B 0.9276 [0.8471,1.0150]; Qwen3-14B 0.8493 [0.7666,0.9418]; Qwen3-32B 0.7922 [0.7138,0.8781]
- neutral|T_obs_cal|random|base: Qwen3-0.6B-Base 2.3524 [1.3381,3.2339]; Qwen3-4B-Base 2.2616 [1.2794,3.1022]; Qwen3-8B-Base 2.2322 [1.2505,3.0690]; Qwen3-14B-Base 2.2126 [1.2317,3.0462]
- neutral|T_obs_cal|random|inst: Qwen3-4B 2.3777 [1.3488,3.2683]; Qwen3-8B 2.3654 [1.3204,3.2696]; Qwen3-14B 2.2929 [1.2657,3.1729]; Qwen3-32B 2.2634 [1.2523,3.1248]
- neutral|T_obs_cal|random_novel|base: Qwen3-0.6B-Base 3.9142 [2.6875,4.8709]; Qwen3-4B-Base 3.7860 [2.6083,4.6676]; Qwen3-8B-Base 3.7374 [2.5611,4.6224]; Qwen3-14B-Base 3.7112 [2.5251,4.5849]
- neutral|T_obs_cal|random_novel|inst: Qwen3-4B 3.9669 [2.7272,4.9262]; Qwen3-8B 3.9562 [2.6959,4.9289]; Qwen3-14B 3.8401 [2.5934,4.7757]; Qwen3-32B 3.7909 [2.5640,4.7068]
- neutral|T_obs_cal|hash_novel|base: Qwen3-0.6B-Base 5.1737 [3.8324,6.2698]; Qwen3-4B-Base 4.9800 [3.6435,5.9977]; Qwen3-8B-Base 4.9203 [3.5524,5.9275]; Qwen3-14B-Base 4.8881 [3.5087,5.8843]
- neutral|T_obs_cal|hash_novel|inst: Qwen3-4B 5.2105 [3.7936,6.3360]; Qwen3-8B 5.2158 [3.7363,6.3655]; Qwen3-14B 5.0891 [3.6497,6.1703]; Qwen3-32B 5.0027 [3.5774,6.0421]
- neutral|T_cf_content|content|base: Qwen3-0.6B-Base 1.1179 [0.9832,1.2620]
- neutral|T_cf_content|content|inst: Qwen3-14B 0.6760 [0.5949,0.7582]; Qwen3-32B 0.5973 [0.5289,0.6664]
- neutral|T_cf_content|outcome|base: Qwen3-0.6B-Base 1.1261 [1.0327,1.2262]
- neutral|T_cf_content|outcome|inst: Qwen3-14B 0.8390 [0.7576,0.9334]; Qwen3-32B 0.7879 [0.7085,0.8739]
- neutral|T_cf_content|random|base: Qwen3-0.6B-Base 2.3524 [1.3381,3.2339]
- neutral|T_cf_content|random|inst: Qwen3-14B 2.3193 [1.2753,3.2059]; Qwen3-32B 2.2766 [1.2597,3.1509]
- neutral|T_cf_content|random_novel|base: Qwen3-0.6B-Base 3.9142 [2.6875,4.8709]
- neutral|T_cf_content|random_novel|inst: Qwen3-14B 3.8805 [2.6144,4.8245]; Qwen3-32B 3.8105 [2.5764,4.7335]
- neutral|capped2|content|base: Qwen3-0.6B-Base 0.4821 [0.4348,0.5294]; Qwen3-4B-Base 0.3189 [0.2803,0.3578]; Qwen3-8B-Base 0.2895 [0.2545,0.3239]; Qwen3-14B-Base 0.2637 [0.2335,0.2927]
- neutral|capped2|content|inst: Qwen3-4B 0.3320 [0.2941,0.3689]; Qwen3-8B 0.2923 [0.2578,0.3260]; Qwen3-14B 0.2627 [0.2312,0.2927]; Qwen3-32B 0.2584 [0.2294,0.2865]
- neutral|capped2|outcome|base: Qwen3-0.6B-Base 0.6110 [0.5627,0.6627]; Qwen3-4B-Base 0.4690 [0.4254,0.5172]; Qwen3-8B-Base 0.4396 [0.3971,0.4867]; Qwen3-14B-Base 0.4176 [0.3749,0.4646]
- neutral|capped2|outcome|inst: Qwen3-4B 0.4729 [0.4301,0.5199]; Qwen3-8B 0.4388 [0.3967,0.4838]; Qwen3-14B 0.4059 [0.3648,0.4521]; Qwen3-32B 0.4121 [0.3701,0.4590]
- neutral|capped2|random|base: Qwen3-0.6B-Base 0.9201 [0.6386,1.1367]; Qwen3-4B-Base 0.8762 [0.5930,1.0972]; Qwen3-8B-Base 0.8645 [0.5814,1.0858]; Qwen3-14B-Base 0.8558 [0.5707,1.0757]
- neutral|capped2|random|inst: Qwen3-4B 0.8612 [0.5765,1.0847]; Qwen3-8B 0.8464 [0.5600,1.0686]; Qwen3-14B 0.8464 [0.5621,1.0691]; Qwen3-32B 0.8500 [0.5646,1.0710]
- neutral|capped2|random_novel|base: Qwen3-0.6B-Base 1.4915 [1.2478,1.6344]; Qwen3-4B-Base 1.4391 [1.1867,1.5881]; Qwen3-8B-Base 1.4210 [1.1689,1.5706]; Qwen3-14B-Base 1.4121 [1.1586,1.5651]
- neutral|capped2|random_novel|inst: Qwen3-4B 1.4264 [1.1722,1.5810]; Qwen3-8B 1.4104 [1.1508,1.5677]; Qwen3-14B 1.4065 [1.1519,1.5622]; Qwen3-32B 1.4082 [1.1530,1.5646]
- neutral|capped2|hash_novel|base: Qwen3-0.6B-Base 1.7661 [1.5579,1.9090]; Qwen3-4B-Base 1.7161 [1.4993,1.8699]; Qwen3-8B-Base 1.6911 [1.4509,1.8497]; Qwen3-14B-Base 1.6811 [1.4340,1.8450]
- neutral|capped2|hash_novel|inst: Qwen3-4B 1.7109 [1.4832,1.8750]; Qwen3-8B 1.6868 [1.4408,1.8551]; Qwen3-14B 1.6799 [1.4334,1.8488]; Qwen3-32B 1.6739 [1.4196,1.8425]
- neutral|prob|content|base: Qwen3-0.6B-Base 0.7703 [0.7479,0.7925]; Qwen3-4B-Base 0.8485 [0.8302,0.8668]; Qwen3-8B-Base 0.8624 [0.8461,0.8791]; Qwen3-14B-Base 0.8746 [0.8609,0.8890]
- neutral|prob|content|inst: Qwen3-4B 0.8416 [0.8238,0.8596]; Qwen3-8B 0.8609 [0.8449,0.8772]; Qwen3-14B 0.8751 [0.8609,0.8902]; Qwen3-32B 0.8776 [0.8645,0.8914]
- neutral|prob|outcome|base: Qwen3-0.6B-Base 0.7174 [0.6938,0.7393]; Qwen3-4B-Base 0.7838 [0.7621,0.8035]; Qwen3-8B-Base 0.7969 [0.7756,0.8162]; Qwen3-14B-Base 0.8074 [0.7860,0.8267]
- neutral|prob|outcome|inst: Qwen3-4B 0.7797 [0.7585,0.7993]; Qwen3-8B 0.7960 [0.7752,0.8152]; Qwen3-14B 0.8117 [0.7909,0.8305]; Qwen3-32B 0.8099 [0.7885,0.8290]
- neutral|prob|random|base: Qwen3-0.6B-Base 0.5598 [0.4554,0.6957]; Qwen3-4B-Base 0.5820 [0.4749,0.7198]; Qwen3-8B-Base 0.5875 [0.4798,0.7255]; Qwen3-14B-Base 0.5922 [0.4836,0.7315]
- neutral|prob|random|inst: Qwen3-4B 0.5909 [0.4835,0.7296]; Qwen3-8B 0.5981 [0.4917,0.7375]; Qwen3-14B 0.5988 [0.4904,0.7382]; Qwen3-32B 0.5961 [0.4879,0.7350]
- neutral|prob|random_novel|base: Qwen3-0.6B-Base 0.2910 [0.2182,0.4151]; Qwen3-4B-Base 0.3166 [0.2430,0.4440]; Qwen3-8B-Base 0.3251 [0.2498,0.4557]; Qwen3-14B-Base 0.3297 [0.2531,0.4613]
- neutral|prob|random_novel|inst: Qwen3-4B 0.3232 [0.2460,0.4524]; Qwen3-8B 0.3312 [0.2549,0.4627]; Qwen3-14B 0.3344 [0.2570,0.4655]; Qwen3-32B 0.3324 [0.2549,0.4637]
- neutral|prob|hash_novel|base: Qwen3-0.6B-Base 0.1500 [0.0801,0.2526]; Qwen3-4B-Base 0.1748 [0.1010,0.2848]; Qwen3-8B-Base 0.1864 [0.1123,0.3078]; Qwen3-14B-Base 0.1914 [0.1152,0.3167]
- neutral|prob|hash_novel|inst: Qwen3-4B 0.1796 [0.1021,0.2948]; Qwen3-8B 0.1904 [0.1120,0.3152]; Qwen3-14B 0.1934 [0.1134,0.3199]; Qwen3-32B 0.1956 [0.1175,0.3236]
- neutral|rankrecal|content|base: Qwen3-0.6B-Base 0.7775 [0.7004,0.8581]
- neutral|rankrecal|content|inst: Qwen3-14B 0.5183 [0.4655,0.5743]; Qwen3-32B 0.4624 [0.4160,0.5119]
- neutral|rankrecal|outcome|base: Qwen3-0.6B-Base 0.8922 [0.8214,0.9673]
- neutral|rankrecal|outcome|inst: Qwen3-14B 0.6691 [0.6093,0.7396]; Qwen3-32B 0.6290 [0.5699,0.6979]
- neutral|rankrecal|random|base: Qwen3-0.6B-Base 1.3737 [0.9509,1.7298]
- neutral|rankrecal|random|inst: Qwen3-14B 1.3016 [0.8982,1.6792]; Qwen3-32B 1.3013 [0.8924,1.6890]
- neutral|rankrecal|random_novel|base: Qwen3-0.6B-Base 2.2398 [1.8705,2.5061]
- neutral|rankrecal|random_novel|inst: Qwen3-14B 2.1316 [1.7797,2.4597]; Qwen3-32B 2.1404 [1.7964,2.4503]
- native|raw|content|base: Qwen3-0.6B-Base 1.1302 [0.9944,1.2744]; Qwen3-4B-Base 0.6936 [0.6025,0.7885]; Qwen3-8B-Base 0.6161 [0.5360,0.6994]; Qwen3-14B-Base 0.5462 [0.4821,0.6114]
- native|raw|content|inst: Qwen3-4B 1.2826 [1.1532,1.4160]; Qwen3-8B 1.0790 [0.9668,1.1955]; Qwen3-14B 0.8380 [0.7494,0.9257]; Qwen3-32B 0.6446 [0.5749,0.7162]
- native|raw|outcome|base: Qwen3-0.6B-Base 1.1327 [1.0386,1.2343]; Qwen3-4B-Base 0.8522 [0.7709,0.9404]; Qwen3-8B-Base 0.7939 [0.7171,0.8759]; Qwen3-14B-Base 0.7407 [0.6647,0.8256]
- native|raw|outcome|inst: Qwen3-4B 1.4398 [1.3284,1.5634]; Qwen3-8B 1.2478 [1.1468,1.3543]; Qwen3-14B 1.0295 [0.9337,1.1351]; Qwen3-32B 0.8387 [0.7574,0.9286]
- native|raw|random|base: Qwen3-0.6B-Base 2.3533 [1.3387,3.2350]; Qwen3-4B-Base 2.2587 [1.2739,3.1000]; Qwen3-8B-Base 2.2316 [1.2478,3.0706]; Qwen3-14B-Base 2.2120 [1.2310,3.0452]
- native|raw|random|inst: Qwen3-4B 2.4722 [1.4963,3.3311]; Qwen3-8B 2.4368 [1.4687,3.2857]; Qwen3-14B 2.3144 [1.3149,3.1796]; Qwen3-32B 2.2704 [1.2621,3.1324]
- native|raw|random_novel|base: Qwen3-0.6B-Base 3.9166 [2.6901,4.8735]; Qwen3-4B-Base 3.7800 [2.6001,4.6630]; Qwen3-8B-Base 3.7338 [2.5526,4.6230]; Qwen3-14B-Base 3.7084 [2.5193,4.5820]
- native|raw|random_novel|inst: Qwen3-4B 4.1242 [3.0078,5.0255]; Qwen3-8B 4.0568 [2.9320,4.9412]; Qwen3-14B 3.8828 [2.6964,4.8011]; Qwen3-32B 3.8096 [2.5913,4.7218]
- native|raw|hash_novel|base: Qwen3-0.6B-Base 5.1754 [3.8341,6.2725]; Qwen3-4B-Base 4.9795 [3.6428,5.9974]; Qwen3-8B-Base 4.9227 [3.5445,5.9331]; Qwen3-14B-Base 4.8877 [3.5094,5.8839]
- native|raw|hash_novel|inst: Qwen3-4B 5.2106 [3.8660,6.2562]; Qwen3-8B 5.1234 [3.7513,6.1657]; Qwen3-14B 5.0634 [3.6591,6.1140]; Qwen3-32B 5.0056 [3.5849,6.0522]
- native|T_obs_cal|content|base: Qwen3-0.6B-Base 1.1302 [0.9944,1.2744]; Qwen3-4B-Base 0.6936 [0.6025,0.7885]; Qwen3-8B-Base 0.6161 [0.5360,0.6994]; Qwen3-14B-Base 0.5462 [0.4821,0.6114]
- native|T_obs_cal|content|inst: Qwen3-4B 0.9950 [0.8805,1.1117]; Qwen3-8B 0.8291 [0.7328,0.9271]; Qwen3-14B 0.6985 [0.6170,0.7798]; Qwen3-32B 0.6099 [0.5423,0.6797]
- native|T_obs_cal|outcome|base: Qwen3-0.6B-Base 1.1327 [1.0386,1.2343]; Qwen3-4B-Base 0.8522 [0.7709,0.9404]; Qwen3-8B-Base 0.7939 [0.7171,0.8759]; Qwen3-14B-Base 0.7407 [0.6647,0.8256]
- native|T_obs_cal|outcome|inst: Qwen3-4B 1.1049 [1.0158,1.2078]; Qwen3-8B 0.9701 [0.8862,1.0611]; Qwen3-14B 0.8708 [0.7868,0.9654]; Qwen3-32B 0.7988 [0.7197,0.8840]
- native|T_obs_cal|random|base: Qwen3-0.6B-Base 2.3533 [1.3387,3.2350]; Qwen3-4B-Base 2.2587 [1.2739,3.1000]; Qwen3-8B-Base 2.2316 [1.2478,3.0706]; Qwen3-14B-Base 2.2120 [1.2310,3.0452]
- native|T_obs_cal|random|inst: Qwen3-4B 2.4491 [1.3894,3.3682]; Qwen3-8B 2.4113 [1.3596,3.3248]; Qwen3-14B 2.3230 [1.2825,3.2142]; Qwen3-32B 2.2662 [1.2558,3.1280]
- native|T_obs_cal|random_novel|base: Qwen3-0.6B-Base 3.9166 [2.6901,4.8735]; Qwen3-4B-Base 3.7800 [2.6001,4.6630]; Qwen3-8B-Base 3.7338 [2.5526,4.6230]; Qwen3-14B-Base 3.7084 [2.5193,4.5820]
- native|T_obs_cal|random_novel|inst: Qwen3-4B 4.0923 [2.8147,5.0945]; Qwen3-8B 4.0291 [2.7687,5.0183]; Qwen3-14B 3.8898 [2.6291,4.8393]; Qwen3-32B 3.7940 [2.5662,4.7123]
- native|T_obs_cal|hash_novel|base: Qwen3-0.6B-Base 5.1754 [3.8341,6.2725]; Qwen3-4B-Base 4.9795 [3.6428,5.9974]; Qwen3-8B-Base 4.9227 [3.5445,5.9331]; Qwen3-14B-Base 4.8877 [3.5094,5.8839]
- native|T_obs_cal|hash_novel|inst: Qwen3-4B 5.3546 [3.8787,6.5335]; Qwen3-8B 5.2761 [3.7726,6.4431]; Qwen3-14B 5.1508 [3.6935,6.2555]; Qwen3-32B 5.0056 [3.5786,6.0460]
- native|T_cf_content|content|base: Qwen3-0.6B-Base 1.1302 [0.9948,1.2753]
- native|T_cf_content|content|inst: Qwen3-14B 0.6988 [0.6143,0.7808]; Qwen3-32B 0.6079 [0.5393,0.6788]
- native|T_cf_content|outcome|base: Qwen3-0.6B-Base 1.1327 [1.0386,1.2335]
- native|T_cf_content|outcome|inst: Qwen3-14B 0.8656 [0.7801,0.9602]; Qwen3-32B 0.7903 [0.7122,0.8763]
- native|T_cf_content|random|base: Qwen3-0.6B-Base 2.3533 [1.3387,3.2350]
- native|T_cf_content|random|inst: Qwen3-14B 2.3443 [1.2946,3.2445]; Qwen3-32B 2.2877 [1.2661,3.1586]
- native|T_cf_content|random_novel|base: Qwen3-0.6B-Base 3.9166 [2.6901,4.8735]
- native|T_cf_content|random_novel|inst: Qwen3-14B 3.9241 [2.6450,4.8911]; Qwen3-32B 3.8244 [2.5786,4.7504]
- native|capped2|content|base: Qwen3-0.6B-Base 0.4817 [0.4344,0.5290]; Qwen3-4B-Base 0.3208 [0.2824,0.3597]; Qwen3-8B-Base 0.2933 [0.2582,0.3277]; Qwen3-14B-Base 0.2643 [0.2340,0.2933]
- native|capped2|content|inst: Qwen3-4B 0.3276 [0.2903,0.3641]; Qwen3-8B 0.2882 [0.2549,0.3212]; Qwen3-14B 0.2607 [0.2293,0.2907]; Qwen3-32B 0.2597 [0.2307,0.2877]
- native|capped2|outcome|base: Qwen3-0.6B-Base 0.6084 [0.5604,0.6599]; Qwen3-4B-Base 0.4715 [0.4281,0.5195]; Qwen3-8B-Base 0.4439 [0.4011,0.4907]; Qwen3-14B-Base 0.4183 [0.3755,0.4654]
- native|capped2|outcome|inst: Qwen3-4B 0.4651 [0.4233,0.5119]; Qwen3-8B 0.4325 [0.3903,0.4778]; Qwen3-14B 0.4025 [0.3613,0.4486]; Qwen3-32B 0.4109 [0.3692,0.4578]
- native|capped2|random|base: Qwen3-0.6B-Base 0.9195 [0.6377,1.1360]; Qwen3-4B-Base 0.8773 [0.5941,1.0982]; Qwen3-8B-Base 0.8665 [0.5835,1.0880]; Qwen3-14B-Base 0.8572 [0.5723,1.0770]
- native|capped2|random|inst: Qwen3-4B 0.8547 [0.5688,1.0800]; Qwen3-8B 0.8424 [0.5551,1.0647]; Qwen3-14B 0.8458 [0.5613,1.0683]; Qwen3-32B 0.8506 [0.5648,1.0715]
- native|capped2|random_novel|base: Qwen3-0.6B-Base 1.4914 [1.2472,1.6342]; Qwen3-4B-Base 1.4396 [1.1879,1.5883]; Qwen3-8B-Base 1.4221 [1.1694,1.5709]; Qwen3-14B-Base 1.4126 [1.1588,1.5654]
- native|capped2|random_novel|inst: Qwen3-4B 1.4210 [1.1632,1.5757]; Qwen3-8B 1.4065 [1.1462,1.5640]; Qwen3-14B 1.4061 [1.1510,1.5617]; Qwen3-32B 1.4084 [1.1531,1.5651]
- native|capped2|hash_novel|base: Qwen3-0.6B-Base 1.7664 [1.5586,1.9089]; Qwen3-4B-Base 1.7162 [1.4995,1.8698]; Qwen3-8B-Base 1.6928 [1.4535,1.8509]; Qwen3-14B-Base 1.6817 [1.4365,1.8450]
- native|capped2|hash_novel|inst: Qwen3-4B 1.7094 [1.4804,1.8739]; Qwen3-8B 1.6856 [1.4399,1.8543]; Qwen3-14B 1.6795 [1.4331,1.8485]; Qwen3-32B 1.6740 [1.4205,1.8424]
- native|prob|content|base: Qwen3-0.6B-Base 0.7705 [0.7481,0.7928]; Qwen3-4B-Base 0.8476 [0.8292,0.8657]; Qwen3-8B-Base 0.8606 [0.8444,0.8774]; Qwen3-14B-Base 0.8743 [0.8605,0.8887]
- native|prob|content|inst: Qwen3-4B 0.8431 [0.8255,0.8610]; Qwen3-8B 0.8623 [0.8467,0.8783]; Qwen3-14B 0.8758 [0.8618,0.8909]; Qwen3-32B 0.8769 [0.8638,0.8907]
- native|prob|outcome|base: Qwen3-0.6B-Base 0.7183 [0.6948,0.7401]; Qwen3-4B-Base 0.7827 [0.7610,0.8023]; Qwen3-8B-Base 0.7952 [0.7739,0.8146]; Qwen3-14B-Base 0.8071 [0.7857,0.8265]
- native|prob|outcome|inst: Qwen3-4B 0.7819 [0.7608,0.8011]; Qwen3-8B 0.7979 [0.7769,0.8172]; Qwen3-14B 0.8127 [0.7916,0.8315]; Qwen3-32B 0.8102 [0.7888,0.8290]
- native|prob|random|base: Qwen3-0.6B-Base 0.5600 [0.4558,0.6961]; Qwen3-4B-Base 0.5815 [0.4744,0.7192]; Qwen3-8B-Base 0.5864 [0.4788,0.7246]; Qwen3-14B-Base 0.5914 [0.4829,0.7305]
- native|prob|random|inst: Qwen3-4B 0.5939 [0.4862,0.7331]; Qwen3-8B 0.5999 [0.4933,0.7393]; Qwen3-14B 0.5993 [0.4910,0.7386]; Qwen3-32B 0.5957 [0.4876,0.7348]
- native|prob|random_novel|base: Qwen3-0.6B-Base 0.2910 [0.2182,0.4151]; Qwen3-4B-Base 0.3164 [0.2429,0.4438]; Qwen3-8B-Base 0.3246 [0.2493,0.4553]; Qwen3-14B-Base 0.3294 [0.2529,0.4613]
- native|prob|random_novel|inst: Qwen3-4B 0.3253 [0.2479,0.4550]; Qwen3-8B 0.3324 [0.2559,0.4644]; Qwen3-14B 0.3347 [0.2572,0.4655]; Qwen3-32B 0.3323 [0.2548,0.4635]
- native|prob|hash_novel|base: Qwen3-0.6B-Base 0.1498 [0.0801,0.2520]; Qwen3-4B-Base 0.1747 [0.1009,0.2848]; Qwen3-8B-Base 0.1855 [0.1113,0.3076]; Qwen3-14B-Base 0.1911 [0.1152,0.3168]
- native|prob|hash_novel|inst: Qwen3-4B 0.1805 [0.1028,0.2960]; Qwen3-8B 0.1911 [0.1125,0.3160]; Qwen3-14B 0.1937 [0.1130,0.3205]; Qwen3-32B 0.1955 [0.1174,0.3235]
- native|rankrecal|content|base: Qwen3-0.6B-Base 0.7804 [0.7032,0.8617]
- native|rankrecal|content|inst: Qwen3-14B 0.5310 [0.4777,0.5876]; Qwen3-32B 0.4699 [0.4228,0.5204]
- native|rankrecal|outcome|base: Qwen3-0.6B-Base 0.8921 [0.8203,0.9671]
- native|rankrecal|outcome|inst: Qwen3-14B 0.6827 [0.6228,0.7541]; Qwen3-32B 0.6324 [0.5738,0.7002]
- native|rankrecal|random|base: Qwen3-0.6B-Base 1.3658 [0.9454,1.7074]
- native|rankrecal|random|inst: Qwen3-14B 1.3141 [0.8996,1.7107]; Qwen3-32B 1.3084 [0.9015,1.7152]
- native|rankrecal|random_novel|base: Qwen3-0.6B-Base 2.2262 [1.8617,2.4616]
- native|rankrecal|random_novel|inst: Qwen3-14B 2.1481 [1.7771,2.5017]; Qwen3-32B 2.1489 [1.8009,2.4953]

## Temperatures

- neutral: T_obs(cal, all obs tokens, 50 real cal trajs) = {'Nemotron-Terminal-14B': 1.3, 'Nemotron-Terminal-32B': 1.2, 'Nemotron-Terminal-8B': 1.3, 'Qwen3-0.6B': 1.2, 'Qwen3-0.6B-Base': 1.0, 'Qwen3-14B': 1.4, 'Qwen3-14B-Base': 1.0, 'Qwen3-32B': 1.2, 'Qwen3-4B': 1.5, 'Qwen3-4B-Base': 1.0, 'Qwen3-8B': 1.6, 'Qwen3-8B-Base': 1.0}
- neutral: T_cf(content; fold A / fold B / full-data) = {'Nemotron-Terminal-14B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Nemotron-Terminal-32B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Qwen3-0.6B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Qwen3-0.6B-Base': {'A': 1.0, 'B': 1.0, 'full': 1.0}, 'Qwen3-14B': {'A': 1.5, 'B': 1.5, 'full': 1.5}, 'Qwen3-32B': {'A': 1.2, 'B': 1.3, 'full': 1.3}}
- neutral: split-seed SD of cross-fit point estimates: T_cf {'Nemotron-Terminal-14B': 4.965068306494546e-17, 'Nemotron-Terminal-32B': 4.965068306494546e-17, 'Qwen3-0.6B': 2.1065000811460205e-16, 'Qwen3-0.6B-Base': 1.5700924586837752e-16, 'Qwen3-14B': 0.0007550587399053751, 'Qwen3-32B': 0.0002568813926799268}; rankrecal {'Nemotron-Terminal-14B': 0.0005543339564901698, 'Nemotron-Terminal-32B': 0.0004862708976569002, 'Qwen3-0.6B': 0.0007222754531464614, 'Qwen3-0.6B-Base': 0.0010083125450017034, 'Qwen3-14B': 0.00044945290805851145, 'Qwen3-32B': 0.0006040371189989502}
- native: T_obs(cal, all obs tokens, 50 real cal trajs) = {'Nemotron-Terminal-14B': 1.4, 'Nemotron-Terminal-32B': 1.2, 'Nemotron-Terminal-8B': 1.3, 'Qwen3-0.6B': 1.2, 'Qwen3-0.6B-Base': 1.0, 'Qwen3-14B': 1.5, 'Qwen3-14B-Base': 1.0, 'Qwen3-32B': 1.2, 'Qwen3-4B': 1.7, 'Qwen3-4B-Base': 1.0, 'Qwen3-8B': 1.7, 'Qwen3-8B-Base': 1.0}
- native: T_cf(content; fold A / fold B / full-data) = {'Nemotron-Terminal-14B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Nemotron-Terminal-32B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Qwen3-0.6B': {'A': 1.2, 'B': 1.2, 'full': 1.2}, 'Qwen3-0.6B-Base': {'A': 1.0, 'B': 1.0, 'full': 1.0}, 'Qwen3-14B': {'A': 1.5, 'B': 1.6, 'full': 1.6}, 'Qwen3-32B': {'A': 1.3, 'B': 1.3, 'full': 1.3}}
- native: split-seed SD of cross-fit point estimates: T_cf {'Nemotron-Terminal-14B': 1.2161883888976234e-16, 'Nemotron-Terminal-32B': 0.0, 'Qwen3-0.6B': 3.4399002279594067e-16, 'Qwen3-0.6B-Base': 2.1065000811460205e-16, 'Qwen3-14B': 0.0006872949017311654, 'Qwen3-32B': 7.021666937153402e-17}; rankrecal {'Nemotron-Terminal-14B': 0.0006007619896216318, 'Nemotron-Terminal-32B': 0.0004903182310488867, 'Qwen3-0.6B': 0.0006608166733631042, 'Qwen3-0.6B-Base': 0.0009558105209536618, 'Qwen3-14B': 0.00048361908580965877, 'Qwen3-32B': 0.000457383624025628}
