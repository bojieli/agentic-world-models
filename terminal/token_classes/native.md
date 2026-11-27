# Terminal token classes in native rendering

```text
[1] tail concentration of observation bits
  Qwen3-4B-Base          ALL obs  mean=0.394 b/tok median=0.0005 | share of bits from top 1%/5%/20% tokens: 31.7%/80.4%/99.7% | tok frac loss<0.01:77.7% <0.1:86.9% >1:7.7% >2:6.2% >8:1.10% | bits share from tok>2b:88.2% >8b:33.9% | 50% of bits in top 2.06%
  Qwen3-4B-Base          novel    mean=0.675 b/tok median=0.0013 | share of bits from top 1%/5%/20% tokens: 21.3%/61.3%/99.1% | tok frac loss<0.01:67.7% <0.1:79.0% >1:13.2% >2:10.7% >8:1.93% | bits share from tok>2b:89.4% >8b:34.6% | 50% of bits in top 3.49%
  Qwen3-4B-Base          CONTENT  mean=0.694 b/tok median=0.0029 | share of bits from top 1%/5%/20% tokens: 21.7%/58.5%/97.8% | tok frac loss<0.01:60.5% <0.1:74.8% >1:14.7% >2:11.2% >8:1.86% | bits share from tok>2b:86.1% >8b:33.0% | 50% of bits in top 3.71%
  Qwen3-8B-Base          ALL obs  mean=0.361 b/tok median=0.0006 | share of bits from top 1%/5%/20% tokens: 31.9%/81.7%/99.7% | tok frac loss<0.01:78.0% <0.1:87.4% >1:7.4% >2:5.9% >8:0.97% | bits share from tok>2b:87.5% >8b:31.3% | 50% of bits in top 2.00%
  Qwen3-8B-Base          novel    mean=0.620 b/tok median=0.0014 | share of bits from top 1%/5%/20% tokens: 21.6%/62.2%/99.2% | tok frac loss<0.01:68.4% <0.1:79.9% >1:12.7% >2:10.2% >8:1.71% | bits share from tok>2b:88.9% >8b:32.1% | 50% of bits in top 3.39%
  Qwen3-8B-Base          CONTENT  mean=0.616 b/tok median=0.0023 | share of bits from top 1%/5%/20% tokens: 23.3%/60.8%/98.3% | tok frac loss<0.01:62.9% <0.1:76.7% >1:13.4% >2:10.1% >8:1.55% | bits share from tok>2b:85.1% >8b:31.2% | 50% of bits in top 3.42%
  Qwen3-4B               ALL obs  mean=0.644 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 36.8%/86.2%/100.0% | tok frac loss<0.01:87.7% <0.1:89.8% >1:8.0% >2:7.2% >8:2.67% | bits share from tok>2b:96.6% >8b:66.2% | 50% of bits in top 1.63%
  Qwen3-4B               novel    mean=1.082 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 25.6%/69.8%/100.0% | tok frac loss<0.01:80.1% <0.1:83.1% >1:13.4% >2:12.1% >8:4.47% | bits share from tok>2b:96.8% >8b:66.1% | 50% of bits in top 2.73%
  Qwen3-4B               CONTENT  mean=1.283 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 22.4%/64.4%/99.8% | tok frac loss<0.01:74.9% <0.1:79.3% >1:15.8% >2:13.9% >8:5.56% | bits share from tok>2b:96.1% >8b:68.1% | 50% of bits in top 3.24%
  Qwen3-8B               ALL obs  mean=0.559 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 40.5%/89.2%/100.0% | tok frac loss<0.01:88.8% <0.1:90.8% >1:7.2% >2:6.4% >8:2.17% | bits share from tok>2b:96.4% >8b:63.9% | 50% of bits in top 1.40%
  Qwen3-8B               novel    mean=0.953 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 28.2%/73.1%/100.0% | tok frac loss<0.01:81.8% <0.1:84.6% >1:12.3% >2:10.9% >8:3.70% | bits share from tok>2b:96.6% >8b:63.9% | 50% of bits in top 2.38%
  Qwen3-8B               CONTENT  mean=1.079 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 26.4%/69.9%/99.9% | tok frac loss<0.01:77.1% <0.1:81.6% >1:14.0% >2:12.1% >8:4.34% | bits share from tok>2b:95.6% >8b:65.3% | 50% of bits in top 2.66%
  Nemotron-Terminal-8B   ALL obs  mean=0.732 b/tok median=0.0005 | share of bits from top 1%/5%/20% tokens: 24.5%/67.4%/99.3% | tok frac loss<0.01:69.4% <0.1:79.4% >1:12.5% >2:10.0% >8:2.63% | bits share from tok>2b:90.4% >8b:47.4% | 50% of bits in top 2.88%
  Nemotron-Terminal-8B   novel    mean=0.966 b/tok median=0.0013 | share of bits from top 1%/5%/20% tokens: 19.4%/57.1%/97.9% | tok frac loss<0.01:62.3% <0.1:73.4% >1:16.8% >2:13.7% >8:3.36% | bits share from tok>2b:91.0% >8b:45.5% | 50% of bits in top 3.94%
  Nemotron-Terminal-8B   CONTENT  mean=0.906 b/tok median=0.0019 | share of bits from top 1%/5%/20% tokens: 19.6%/55.7%/97.1% | tok frac loss<0.01:60.3% <0.1:72.1% >1:17.4% >2:13.7% >8:2.83% | bits share from tok>2b:89.0% >8b:40.1% | 50% of bits in top 4.11%

[2] by class: token share | per model: share of obs bits, mean bits/token
  class                              tok%  copy%          Qwen3-4B-Base          Qwen3-8B-Base               Qwen3-4B               Qwen3-8B         on-Terminal-8B
  ws                                 8.6%  32.0%      5.8% of bits, 0.266     5.2% of bits, 0.220     5.1% of bits, 0.380     5.8% of bits, 0.378     9.6% of bits, 0.825
  boiler                             3.3%  19.8%     20.7% of bits, 2.429    21.2% of bits, 2.287    24.0% of bits, 4.613    22.1% of bits, 3.684     4.6% of bits, 1.013
  prompt                            14.2%  73.5%      2.1% of bits, 0.058     2.0% of bits, 0.052     3.0% of bits, 0.134     2.6% of bits, 0.103    27.2% of bits, 1.408
  cmd_echo                          34.0%  38.9%      5.5% of bits, 0.063     4.3% of bits, 0.046     6.5% of bits, 0.123     6.5% of bits, 0.107    14.0% of bits, 0.302
  rand_hash                          2.4%  23.1%     23.4% of bits, 3.831    25.2% of bits, 3.788    15.0% of bits, 4.011    17.0% of bits, 3.941    13.0% of bits, 3.977
  rand_time                          2.5%  59.1%      4.8% of bits, 0.754     5.1% of bits, 0.742     3.9% of bits, 0.997     4.4% of bits, 0.984     2.9% of bits, 0.851
  rand_misc                          0.1%  12.1%      0.3% of bits, 1.817     0.3% of bits, 1.824     0.2% of bits, 2.170     0.3% of bits, 2.545     0.2% of bits, 2.164
  err_line                           1.1%  40.9%      1.3% of bits, 0.490     1.3% of bits, 0.438     1.6% of bits, 0.945     1.7% of bits, 0.895     1.5% of bits, 1.044
  test_line                          1.5%  38.2%      0.8% of bits, 0.198     0.7% of bits, 0.162     0.9% of bits, 0.392     0.9% of bits, 0.335     0.7% of bits, 0.337
  number                             6.2%  45.2%      9.4% of bits, 0.595     9.8% of bits, 0.565     9.5% of bits, 0.977     9.4% of bits, 0.842     6.1% of bits, 0.713
  path                               3.0%  46.5%      2.0% of bits, 0.262     2.0% of bits, 0.240     2.6% of bits, 0.550     2.5% of bits, 0.463     1.9% of bits, 0.452
  other                             23.1%  39.4%     24.0% of bits, 0.408    22.7% of bits, 0.354    27.9% of bits, 0.779    26.8% of bits, 0.647    18.2% of bits, 0.577
  ALL obs                          100.0%  43.4%    100.0% of bits, 0.394   100.0% of bits, 0.361   100.0% of bits, 0.644   100.0% of bits, 0.559   100.0% of bits, 0.732
  novel                             56.6%   0.0%     97.0% of bits, 0.675    97.2% of bits, 0.620    95.0% of bits, 1.082    96.6% of bits, 0.953    74.6% of bits, 0.966
  copy                              43.4% 100.0%      3.0% of bits, 0.028     2.8% of bits, 0.023     5.0% of bits, 0.074     3.4% of bits, 0.044    25.4% of bits, 0.428
  first16                            3.3%  64.7%      7.1% of bits, 0.858     7.2% of bits, 0.795    10.0% of bits, 1.975     7.9% of bits, 1.361     4.2% of bits, 0.952
  outstart4                          1.5%  10.3%      4.7% of bits, 1.225     4.6% of bits, 1.091     5.3% of bits, 2.255     5.5% of bits, 2.031     2.9% of bits, 1.411
  rand(all 3)                        5.0%  41.1%     28.4% of bits, 2.259    30.7% of bits, 2.232    19.0% of bits, 2.472    21.6% of bits, 2.437    16.1% of bits, 2.383
  rand&novel                         2.9%   0.0%     28.1% of bits, 3.780    30.3% of bits, 3.734    18.7% of bits, 4.124    21.2% of bits, 4.057    15.4% of bits, 3.869
  CONTENT(novel output,non-rand)    20.6%   0.0%     36.4% of bits, 0.694    35.3% of bits, 0.616    41.1% of bits, 1.283    39.9% of bits, 1.079    25.5% of bits, 0.906
  outcome-bearing                    5.0%   0.0%     10.8% of bits, 0.852    11.0% of bits, 0.794    11.2% of bits, 1.440    11.2% of bits, 1.248     7.3% of bits, 1.063

[2b] within NOVEL tokens only: share of novel bits by class
  ws           tok  10.3%   5.7%/0.374   5.2%/0.312   5.1%/0.540   5.8%/0.538  11.1%/1.046
  boiler       tok   4.7%  21.2%/3.008  21.7%/2.832  23.9%/5.450  22.7%/4.551   5.9%/1.203
  prompt       tok   6.6%   1.8%/0.182   1.7%/0.154   1.9%/0.306   2.1%/0.301  13.1%/1.903
  cmd_echo     tok  36.7%   4.9%/0.090   4.1%/0.069   6.1%/0.181   6.1%/0.160  15.0%/0.395
  rand_hash    tok   3.3%  24.1%/4.979  25.9%/4.923  15.7%/5.211  17.6%/5.123  17.1%/5.062
  rand_time    tok   1.8%   4.5%/1.700   4.9%/1.670   3.7%/2.246   4.1%/2.187   3.3%/1.788
  rand_misc    tok   0.1%   0.3%/2.061   0.3%/2.072   0.2%/2.469   0.3%/2.895   0.2%/2.429
  err_line     tok   1.1%   1.3%/0.778   1.3%/0.692   1.6%/1.491   1.6%/1.389   1.5%/1.288
  test_line    tok   1.7%   0.8%/0.311   0.7%/0.254   0.9%/0.607   0.9%/0.513   0.8%/0.482
  number       tok   6.0%   9.1%/1.017   9.4%/0.963   9.3%/1.662   9.0%/1.426   7.4%/1.184
  path         tok   2.9%   2.0%/0.471   2.0%/0.432   2.6%/0.980   2.5%/0.828   2.0%/0.680
  other        tok  24.8%  24.3%/0.663  22.9%/0.574  28.9%/1.261  27.2%/1.048  22.4%/0.876

[3] entropy vs loss (bits/token; equal if calibrated). gap=loss-entropy>0 means overconfident
  ALL obs                          Qwen3-4B-Base: loss 0.394 ent 0.389 gap +0.005 | Qwen3-8B-Base: loss 0.361 ent 0.361 gap +0.000 | Qwen3-4B: loss 0.644 ent 0.204 gap +0.440 | Qwen3-8B: loss 0.559 ent 0.192 gap +0.366 | on-Terminal-8B: loss 0.732 ent 0.403 gap +0.329
  novel                            Qwen3-4B-Base: loss 0.675 ent 0.642 gap +0.032 | Qwen3-8B-Base: loss 0.620 ent 0.596 gap +0.023 | Qwen3-4B: loss 1.082 ent 0.349 gap +0.733 | Qwen3-8B: loss 0.953 ent 0.331 gap +0.623 | on-Terminal-8B: loss 0.966 ent 0.566 gap +0.400
  CONTENT(novel output,non-rand)   Qwen3-4B-Base: loss 0.694 ent 0.602 gap +0.092 | Qwen3-8B-Base: loss 0.616 ent 0.536 gap +0.080 | Qwen3-4B: loss 1.283 ent 0.322 gap +0.960 | Qwen3-8B: loss 1.079 ent 0.285 gap +0.794 | on-Terminal-8B: loss 0.906 ent 0.583 gap +0.323
  rand&novel                       Qwen3-4B-Base: loss 3.780 ent 3.700 gap +0.080 | Qwen3-8B-Base: loss 3.734 ent 3.653 gap +0.081 | Qwen3-4B: loss 4.124 ent 3.269 gap +0.856 | Qwen3-8B: loss 4.057 ent 3.315 gap +0.742 | on-Terminal-8B: loss 3.869 ent 3.621 gap +0.248
  copy                             Qwen3-4B-Base: loss 0.028 ent 0.059 gap -0.032 | Qwen3-8B-Base: loss 0.023 ent 0.054 gap -0.030 | Qwen3-4B: loss 0.074 ent 0.016 gap +0.058 | Qwen3-8B: loss 0.044 ent 0.012 gap +0.032 | on-Terminal-8B: loss 0.428 ent 0.191 gap +0.237

[4] paired differences b-a (bits/token unless noted) [95% traj-bootstrap CI], z
  --- Qwen3-8B-Base -> Qwen3-8B   (total obs delta +86107 bits over 435322 tok)
    ws                               +0.1582 [+0.1387,+0.1794] z= +15.6  share of total delta   +6.8%  rel +71.8%
    boiler                           +1.3965 [+1.3423,+1.4490] z= +50.2  share of total delta  +23.6%  rel +61.1%
    prompt                           +0.0510 [+0.0418,+0.0621] z=  +9.8  share of total delta   +3.6%  rel +97.9%
    cmd_echo                         +0.0612 [+0.0527,+0.0698] z= +13.8  share of total delta  +10.5%  rel +132.5%
    rand_hash                        +0.1534 [+0.1121,+0.2052] z=  +6.4  share of total delta   +1.9%  rel  +4.0%
    rand_time                        +0.2422 [+0.2005,+0.2909] z= +10.9  share of total delta   +3.1%  rel +32.6%
    rand_misc                        +0.7207 [+0.4439,+1.0681] z=  +4.6  share of total delta   +0.2%  rel +39.5%
    err_line                         +0.4574 [+0.3733,+0.5787] z=  +8.8  share of total delta   +2.5%  rel +104.5%
    test_line                        +0.1726 [+0.1316,+0.2270] z=  +7.0  share of total delta   +1.3%  rel +106.3%
    number                           +0.2774 [+0.2375,+0.3223] z= +12.3  share of total delta   +8.8%  rel +49.1%
    path                             +0.2232 [+0.1777,+0.2762] z=  +8.7  share of total delta   +3.4%  rel +93.2%
    other                            +0.2926 [+0.2532,+0.3386] z= +13.1  share of total delta  +34.2%  rel +82.6%
    ALL obs                          +0.1978 [+0.1848,+0.2121] z= +27.8  share of total delta +100.0%  rel +54.8%
    novel                            +0.3337 [+0.3119,+0.3564] z= +29.5  share of total delta  +95.5%  rel +53.9%
    copy                             +0.0207 [+0.0171,+0.0250] z= +10.3  share of total delta   +4.5%  rel +88.3%
    first16                          +0.5663 [+0.5171,+0.6184] z= +22.5  share of total delta   +9.3%  rel +71.2%
    outstart4                        +0.9407 [+0.8216,+1.0550] z= +15.8  share of total delta   +7.2%  rel +86.2%
    rand(all 3)                      +0.2052 [+0.1738,+0.2477] z= +10.8  share of total delta   +5.1%  rel  +9.2%
    rand&novel                       +0.3230 [+0.2634,+0.4373] z=  +7.1  share of total delta   +4.8%  rel  +8.6%
    CONTENT(novel output,non-rand)   +0.4628 [+0.4201,+0.5045] z= +21.7  share of total delta  +48.3%  rel +75.1%
    outcome-bearing                  +0.4539 [+0.4118,+0.5034] z= +19.8  share of total delta  +11.5%  rel +57.2%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3608 b=0.5586 diff +0.1978 [+0.1848,+0.2121] z= +27.8
      ALL obs  capped@2           a=0.1623 b=0.1482 diff -0.0141 [-0.0156,-0.0127] z= -19.0
      ALL obs  capped@8           a=0.3256 b=0.3753 diff +0.0497 [+0.0434,+0.0560] z= +15.5
      ALL obs  mean p             a=0.9221 b=0.9292 diff +0.0071 [+0.0064,+0.0078] z= +19.7
      ALL obs  top1 hit(p>.5)     a=0.9259 b=0.9277 diff +0.0018 [+0.0011,+0.0024] z=  +5.4
      ALL obs  bits @T*obs        a=0.3608 b=0.4480 diff +0.0872 [+0.0790,+0.0969] z= +18.9
      ALL obs  entropy            a=0.3606 b=0.1923 diff -0.1683 [-0.1814,-0.1558] z= -26.4
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.8671 diff +0.8671 [+0.8498,+0.8814] z=+107.8
      ALL obs  quantiles 50/90/99/99.9: a=[1.0000e-03 2.8300e-01 7.8840e+00 1.5148e+01] b=[ 0.     0.035 14.607 32.506]
      CONTENT  mean bits          a=0.6161 b=1.0790 diff +0.4628 [+0.4201,+0.5045] z= +21.7
      CONTENT  capped@2           a=0.2933 b=0.2882 diff -0.0051 [-0.0095,-0.0002] z=  -2.2
      CONTENT  capped@8           a=0.5477 b=0.7214 diff +0.1738 [+0.1561,+0.1922] z= +18.9
      CONTENT  mean p             a=0.8606 b=0.8623 diff +0.0017 [-0.0006,+0.0038] z=  +1.5
      CONTENT  top1 hit(p>.5)     a=0.8659 b=0.8604 diff -0.0055 [-0.0076,-0.0034] z=  -5.3
      CONTENT  bits @T*obs        a=0.6161 b=0.8291 diff +0.2130 [+0.1933,+0.2331] z= +20.6
      CONTENT  entropy            a=0.5361 b=0.2850 diff -0.2510 [-0.2887,-0.2145] z= -13.2
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.7055 diff +0.7055 [+0.6737,+0.7352] z= +44.4
      CONTENT  quantiles 50/90/99/99.9: a=[2.000e-03 2.029e+00 9.898e+00 2.075e+01] b=[ 0.     3.122 19.837 39.404]
      outcome  mean bits          a=0.7939 b=1.2478 diff +0.4539 [+0.4118,+0.5034] z= +19.8
      outcome  capped@2           a=0.4439 b=0.4325 diff -0.0115 [-0.0170,-0.0056] z=  -3.9
      outcome  capped@8           a=0.7631 b=0.9624 diff +0.1993 [+0.1801,+0.2210] z= +18.8
      outcome  mean p             a=0.7952 b=0.7979 diff +0.0027 [+0.0002,+0.0053] z=  +2.1
      outcome  top1 hit(p>.5)     a=0.7849 b=0.7876 diff +0.0027 [-0.0011,+0.0065] z=  +1.4
      outcome  bits @T*obs        a=0.7939 b=0.9701 diff +0.1762 [+0.1574,+0.1983] z= +17.2
      outcome  entropy            a=0.6874 b=0.4710 diff -0.2164 [-0.2392,-0.1951] z= -19.2
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.6676 diff +0.6676 [+0.6396,+0.6912] z= +49.1
      outcome  quantiles 50/90/99/99.9: a=[2.0000e-03 3.3220e+00 7.7130e+00 1.5858e+01] b=[ 0.     3.719 17.991 33.806]
    |delta| concentration: top 1% tokens hold 50.7% of |delta|, top 5% 90.5%; net delta from top-1% |delta| tokens +72.9%, from the other 99% +27.1%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  60.5% a=0.003 b=0.022 diff +0.0190 [+0.0133,+0.0252] z=+6.5 | capped@8 diff +0.0126 z=+6.7
      ref bits in [0.01,0.1): tok  14.3% a=0.057 b=0.171 diff +0.1137 [+0.0872,+0.1420] z=+8.2 | capped@8 diff +0.0704 z=+7.4
      ref bits in [0.1,1): tok  10.5% a=0.428 b=0.799 diff +0.3710 [+0.3075,+0.4480] z=+10.3 | capped@8 diff +0.2442 z=+9.9
      ref bits in [1,4): tok   9.4% a=2.188 b=3.409 diff +1.2208 [+1.0953,+1.3483] z=+18.5 | capped@8 diff +0.7830 z=+21.2
      ref bits in [4,1000000000.0): tok   5.3% a=6.706 b=12.013 diff +5.3070 [+4.8891,+5.8411] z=+22.9 | capped@8 diff +1.0731 z=+23.4
  --- Qwen3-8B -> Nemotron-Terminal-8B   (total obs delta +75695 bits over 435322 tok)
    ws                               +0.4462 [+0.3679,+0.5388] z= +10.0  share of total delta  +22.0%  rel +117.9%
    boiler                           -2.6714 [-2.7967,-2.5425] z= -41.0  share of total delta  -51.4%  rel -72.5%
    prompt                           +1.3048 [+1.2314,+1.3928] z= +32.6  share of total delta +106.2%  rel +1265.9%
    cmd_echo                         +0.1945 [+0.1682,+0.2242] z= +13.0  share of total delta  +38.0%  rel +181.2%
    rand_hash                        +0.0364 [-0.0754,+0.2646] z=  +0.4  share of total delta   +0.5%  rel  +0.9%
    rand_time                        -0.1332 [-0.1880,-0.0834] z=  -5.1  share of total delta   -1.9%  rel -13.5%
    rand_misc                        -0.3813 [-0.7350,-0.0872] z=  -2.3  share of total delta   -0.1%  rel -15.0%
    err_line                         +0.1485 [-0.0416,+0.2825] z=  +1.8  share of total delta   +0.9%  rel +16.6%
    test_line                        +0.0020 [-0.0497,+0.0473] z=  +0.1  share of total delta   +0.0%  rel  +0.6%
    number                           -0.1294 [-0.1695,-0.0957] z=  -6.7  share of total delta   -4.6%  rel -15.4%
    path                             -0.0108 [-0.1002,+0.0782] z=  -0.2  share of total delta   -0.2%  rel  -2.3%
    other                            -0.0698 [-0.1033,-0.0376] z=  -4.2  share of total delta   -9.3%  rel -10.8%
    ALL obs                          +0.1739 [+0.1491,+0.2023] z= +12.5  share of total delta +100.0%  rel +31.1%
    novel                            +0.0129 [-0.0191,+0.0505] z=  +0.7  share of total delta   +4.2%  rel  +1.4%
    copy                             +0.3836 [+0.3522,+0.4214] z= +21.5  share of total delta  +95.8%  rel +868.4%
    first16                          -0.4088 [-0.4876,-0.3333] z= -10.2  share of total delta   -7.7%  rel -30.0%
    outstart4                        -0.6207 [-0.7261,-0.5178] z= -11.4  share of total delta   -5.4%  rel -30.6%
    rand(all 3)                      -0.0542 [-0.1272,+0.0403] z=  -1.3  share of total delta   -1.5%  rel  -2.2%
    rand&novel                       -0.1874 [-0.2963,-0.1325] z=  -4.2  share of total delta   -3.2%  rel  -4.6%
    CONTENT(novel output,non-rand)   -0.1730 [-0.2084,-0.1357] z=  -9.1  share of total delta  -20.5%  rel -16.0%
    outcome-bearing                  -0.1844 [-0.2275,-0.1421] z=  -8.5  share of total delta   -5.3%  rel -14.8%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.5586 b=0.7325 diff +0.1739 [+0.1491,+0.2023] z= +12.5
      ALL obs  capped@2           a=0.1482 b=0.2711 diff +0.1229 [+0.1170,+0.1299] z= +37.2
      ALL obs  capped@8           a=0.3753 b=0.5958 diff +0.2205 [+0.2046,+0.2393] z= +24.2
      ALL obs  mean p             a=0.9292 b=0.8696 diff -0.0596 [-0.0630,-0.0568] z= -37.5
      ALL obs  top1 hit(p>.5)     a=0.9277 b=0.8751 diff -0.0526 [-0.0559,-0.0498] z= -32.7
      ALL obs  bits @T*obs        a=0.4480 b=0.6876 diff +0.2396 [+0.2210,+0.2611] z= +22.6
      ALL obs  entropy            a=0.1923 b=0.4032 diff +0.2109 [+0.1966,+0.2256] z= +29.1
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=-0.8042 diff -0.8042 [-0.8165,-0.7904] z=-118.9
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.035 14.607 32.506] b=[ 0.     2.016 13.198 23.97 ]
      CONTENT  mean bits          a=1.0790 b=0.9059 diff -0.1730 [-0.2084,-0.1357] z=  -9.1
      CONTENT  capped@2           a=0.2882 b=0.3747 diff +0.0865 [+0.0790,+0.0947] z= +22.1
      CONTENT  capped@8           a=0.7214 b=0.7695 diff +0.0480 [+0.0306,+0.0678] z=  +5.0
      CONTENT  mean p             a=0.8623 b=0.8219 diff -0.0404 [-0.0440,-0.0370] z= -22.7
      CONTENT  top1 hit(p>.5)     a=0.8604 b=0.8257 diff -0.0347 [-0.0389,-0.0311] z= -17.5
      CONTENT  bits @T*obs        a=0.8291 b=0.8838 diff +0.0547 [+0.0347,+0.0775] z=  +5.0
      CONTENT  entropy            a=0.2850 b=0.5828 diff +0.2978 [+0.2596,+0.3384] z= +14.5
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=-0.7002 diff -0.7002 [-0.7237,-0.6760] z= -57.2
      CONTENT  quantiles 50/90/99/99.9: a=[ 0.     3.122 19.837 39.404] b=[2.0000e-03 3.2400e+00 1.3012e+01 2.3489e+01]
      outcome  mean bits          a=1.2478 b=1.0634 diff -0.1844 [-0.2275,-0.1421] z=  -8.5
      outcome  capped@2           a=0.4325 b=0.5238 diff +0.0913 [+0.0807,+0.1033] z= +16.1
      outcome  capped@8           a=0.9624 b=0.9795 diff +0.0172 [-0.0066,+0.0450] z=  +1.3
      outcome  mean p             a=0.7979 b=0.7568 diff -0.0410 [-0.0467,-0.0359] z= -15.9
      outcome  top1 hit(p>.5)     a=0.7876 b=0.7480 diff -0.0396 [-0.0456,-0.0343] z= -14.0
      outcome  bits @T*obs        a=0.9701 b=1.0205 diff +0.0504 [+0.0212,+0.0818] z=  +3.2
      outcome  entropy            a=0.4710 b=0.7351 diff +0.2640 [+0.2394,+0.2909] z= +20.0
      outcome  win(b<a)-win(a<b)  a=0.0000 b=-0.6621 diff -0.6621 [-0.6848,-0.6378] z= -54.2
      outcome  quantiles 50/90/99/99.9: a=[ 0.     3.719 17.991 33.806] b=[3.0000e-03 3.5530e+00 1.0836e+01 1.9927e+01]
    |delta| concentration: top 1% tokens hold 29.4% of |delta|, top 5% 74.6%; net delta from top-1% |delta| tokens +3.4%, from the other 99% +96.6%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  60.5% a=0.022 b=0.157 diff +0.1354 [+0.1144,+0.1553] z=+13.0 | capped@8 diff +0.1114 z=+14.3
      ref bits in [0.01,0.1): tok  14.3% a=0.171 b=0.391 diff +0.2206 [+0.1847,+0.2629] z=+11.1 | capped@8 diff +0.2201 z=+14.5
      ref bits in [0.1,1): tok  10.5% a=0.799 b=0.919 diff +0.1207 [+0.0641,+0.1787] z=+4.1 | capped@8 diff +0.1993 z=+8.6
      ref bits in [1,4): tok   9.4% a=3.409 b=2.755 diff -0.6541 [-0.7975,-0.5238] z=-9.8 | capped@8 diff -0.2946 z=-7.2
      ref bits in [4,1000000000.0): tok   5.3% a=12.013 b=7.533 diff -4.4801 [-5.0110,-4.0352] z=-18.3 | capped@8 diff -0.8302 z=-15.8
  --- Qwen3-8B-Base -> Nemotron-Terminal-8B   (total obs delta +161802 bits over 435322 tok)
    ws                               +0.6043 [+0.5257,+0.6981] z= +13.8  share of total delta  +13.9%  rel +274.3%
    boiler                           -1.2748 [-1.3581,-1.1942] z= -30.5  share of total delta  -11.5%  rel -55.7%
    prompt                           +1.3558 [+1.2879,+1.4404] z= +34.9  share of total delta  +51.6%  rel +2603.7%
    cmd_echo                         +0.2557 [+0.2287,+0.2843] z= +17.9  share of total delta  +23.4%  rel +553.8%
    rand_hash                        +0.1897 [+0.0798,+0.3996] z=  +2.2  share of total delta   +1.2%  rel  +5.0%
    rand_time                        +0.1090 [+0.0864,+0.1318] z=  +9.7  share of total delta   +0.7%  rel +14.7%
    rand_misc                        +0.3393 [+0.1840,+0.5404] z=  +3.6  share of total delta   +0.1%  rel +18.6%
    err_line                         +0.6059 [+0.4594,+0.7313] z=  +9.1  share of total delta   +1.8%  rel +138.5%
    test_line                        +0.1746 [+0.1237,+0.2280] z=  +6.7  share of total delta   +0.7%  rel +107.5%
    number                           +0.1480 [+0.1279,+0.1728] z= +13.0  share of total delta   +2.5%  rel +26.2%
    path                             +0.2124 [+0.1514,+0.2816] z=  +6.3  share of total delta   +1.7%  rel +88.7%
    other                            +0.2228 [+0.1960,+0.2548] z= +15.0  share of total delta  +13.9%  rel +62.9%
    ALL obs                          +0.3717 [+0.3499,+0.3982] z= +29.3  share of total delta +100.0%  rel +103.0%
    novel                            +0.3466 [+0.3217,+0.3767] z= +24.2  share of total delta  +52.8%  rel +55.9%
    copy                             +0.4044 [+0.3727,+0.4430] z= +22.2  share of total delta  +47.2%  rel +1723.1%
    first16                          +0.1575 [+0.1164,+0.1992] z=  +7.3  share of total delta   +1.4%  rel +19.8%
    outstart4                        +0.3200 [+0.2601,+0.3785] z= +10.7  share of total delta   +1.3%  rel +29.3%
    rand(all 3)                      +0.1510 [+0.0965,+0.2359] z=  +4.0  share of total delta   +2.0%  rel  +6.8%
    rand&novel                       +0.1355 [+0.0985,+0.1834] z=  +6.3  share of total delta   +1.1%  rel  +3.6%
    CONTENT(novel output,non-rand)   +0.2898 [+0.2608,+0.3251] z= +17.4  share of total delta  +16.1%  rel +47.0%
    outcome-bearing                  +0.2695 [+0.2326,+0.3108] z= +13.6  share of total delta   +3.6%  rel +34.0%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3608 b=0.7325 diff +0.3717 [+0.3499,+0.3982] z= +29.3
      ALL obs  capped@2           a=0.1623 b=0.2711 diff +0.1088 [+0.1029,+0.1159] z= +31.7
      ALL obs  capped@8           a=0.3256 b=0.5958 diff +0.2702 [+0.2548,+0.2885] z= +30.1
      ALL obs  mean p             a=0.9221 b=0.8696 diff -0.0525 [-0.0559,-0.0496] z= -31.7
      ALL obs  top1 hit(p>.5)     a=0.9259 b=0.8751 diff -0.0508 [-0.0542,-0.0480] z= -31.2
      ALL obs  bits @T*obs        a=0.3608 b=0.6876 diff +0.3268 [+0.3084,+0.3494] z= +29.8
      ALL obs  entropy            a=0.3606 b=0.4032 diff +0.0426 [+0.0333,+0.0527] z=  +8.4
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.2327 diff +0.2327 [+0.2083,+0.2561] z= +18.8
      ALL obs  quantiles 50/90/99/99.9: a=[1.0000e-03 2.8300e-01 7.8840e+00 1.5148e+01] b=[ 0.     2.016 13.198 23.97 ]
      CONTENT  mean bits          a=0.6161 b=0.9059 diff +0.2898 [+0.2608,+0.3251] z= +17.4
      CONTENT  capped@2           a=0.2933 b=0.3747 diff +0.0814 [+0.0725,+0.0917] z= +16.4
      CONTENT  capped@8           a=0.5477 b=0.7695 diff +0.2218 [+0.1985,+0.2499] z= +17.0
      CONTENT  mean p             a=0.8606 b=0.8219 diff -0.0387 [-0.0436,-0.0343] z= -16.4
      CONTENT  top1 hit(p>.5)     a=0.8659 b=0.8257 diff -0.0402 [-0.0450,-0.0360] z= -17.0
      CONTENT  bits @T*obs        a=0.6161 b=0.8838 diff +0.2677 [+0.2395,+0.3015] z= +16.7
      CONTENT  entropy            a=0.5361 b=0.5828 diff +0.0468 [+0.0330,+0.0628] z=  +6.1
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.2083 diff +0.2083 [+0.1746,+0.2425] z= +12.2
      CONTENT  quantiles 50/90/99/99.9: a=[2.000e-03 2.029e+00 9.898e+00 2.075e+01] b=[2.0000e-03 3.2400e+00 1.3012e+01 2.3489e+01]
      outcome  mean bits          a=0.7939 b=1.0634 diff +0.2695 [+0.2326,+0.3108] z= +13.6
      outcome  capped@2           a=0.4439 b=0.5238 diff +0.0798 [+0.0697,+0.0911] z= +15.2
      outcome  capped@8           a=0.7631 b=0.9795 diff +0.2164 [+0.1886,+0.2475] z= +14.8
      outcome  mean p             a=0.7952 b=0.7568 diff -0.0384 [-0.0438,-0.0334] z= -15.1
      outcome  top1 hit(p>.5)     a=0.7849 b=0.7480 diff -0.0369 [-0.0425,-0.0315] z= -13.5
      outcome  bits @T*obs        a=0.7939 b=1.0205 diff +0.2266 [+0.1952,+0.2617] z= +13.6
      outcome  entropy            a=0.6874 b=0.7351 diff +0.0476 [+0.0350,+0.0617] z=  +7.2
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.1737 diff +0.1737 [+0.1349,+0.2129] z=  +8.6
      outcome  quantiles 50/90/99/99.9: a=[2.0000e-03 3.3220e+00 7.7130e+00 1.5858e+01] b=[3.0000e-03 3.5530e+00 1.0836e+01 1.9927e+01]
    |delta| concentration: top 1% tokens hold 28.9% of |delta|, top 5% 72.4%; net delta from top-1% |delta| tokens +42.2%, from the other 99% +57.8%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  60.5% a=0.003 b=0.157 diff +0.1544 [+0.1323,+0.1769] z=+13.6 | capped@8 diff +0.1240 z=+14.4
      ref bits in [0.01,0.1): tok  14.3% a=0.057 b=0.391 diff +0.3343 [+0.2891,+0.3861] z=+12.8 | capped@8 diff +0.2905 z=+13.6
      ref bits in [0.1,1): tok  10.5% a=0.428 b=0.919 diff +0.4917 [+0.4194,+0.5776] z=+11.8 | capped@8 diff +0.4435 z=+12.4
      ref bits in [1,4): tok   9.4% a=2.188 b=2.755 diff +0.5666 [+0.4958,+0.6485] z=+14.1 | capped@8 diff +0.4885 z=+14.4
      ref bits in [4,1000000000.0): tok   5.3% a=6.706 b=7.533 diff +0.8269 [+0.6807,+0.9905] z=+10.7 | capped@8 diff +0.2429 z=+4.1
  --- Qwen3-4B-Base -> Qwen3-4B   (total obs delta +109091 bits over 435322 tok)
    ws                               +0.1146 [+0.0954,+0.1354] z= +10.7  share of total delta   +3.9%  rel +43.1%
    boiler                           +2.1843 [+2.1104,+2.2611] z= +58.5  share of total delta  +29.2%  rel +89.9%
    prompt                           +0.0761 [+0.0645,+0.0885] z= +12.2  share of total delta   +4.3%  rel +130.5%
    cmd_echo                         +0.0597 [+0.0520,+0.0670] z= +15.5  share of total delta   +8.1%  rel +94.2%
    rand_hash                        +0.1793 [+0.1335,+0.2242] z=  +7.6  share of total delta   +1.7%  rel  +4.7%
    rand_time                        +0.2429 [+0.2033,+0.2844] z= +12.0  share of total delta   +2.4%  rel +32.2%
    rand_misc                        +0.3538 [+0.2147,+0.5164] z=  +4.6  share of total delta   +0.1%  rel +19.5%
    err_line                         +0.4550 [+0.3638,+0.5852] z=  +8.2  share of total delta   +2.0%  rel +92.9%
    test_line                        +0.1936 [+0.1526,+0.2520] z=  +7.6  share of total delta   +1.2%  rel +97.8%
    number                           +0.3818 [+0.3321,+0.4392] z= +13.7  share of total delta   +9.5%  rel +64.1%
    path                             +0.2880 [+0.2370,+0.3515] z= +10.1  share of total delta   +3.5%  rel +109.9%
    other                            +0.3701 [+0.3220,+0.4259] z= +14.0  share of total delta  +34.1%  rel +90.6%
    ALL obs                          +0.2506 [+0.2353,+0.2680] z= +30.0  share of total delta +100.0%  rel +63.6%
    novel                            +0.4071 [+0.3824,+0.4317] z= +32.0  share of total delta  +91.9%  rel +60.3%
    copy                             +0.0467 [+0.0424,+0.0515] z= +20.2  share of total delta   +8.1%  rel +169.7%
    first16                          +1.1170 [+1.0465,+1.1940] z= +29.5  share of total delta  +14.5%  rel +130.2%
    outstart4                        +1.0306 [+0.8975,+1.1689] z= +15.0  share of total delta   +6.3%  rel +84.2%
    rand(all 3)                      +0.2135 [+0.1855,+0.2464] z= +14.0  share of total delta   +4.2%  rel  +9.5%
    rand&novel                       +0.3442 [+0.2878,+0.4438] z=  +8.9  share of total delta   +4.0%  rel  +9.1%
    CONTENT(novel output,non-rand)   +0.5890 [+0.5461,+0.6377] z= +24.7  share of total delta  +48.5%  rel +84.9%
    outcome-bearing                  +0.5876 [+0.5394,+0.6418] z= +21.9  share of total delta  +11.7%  rel +69.0%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3938 b=0.6444 diff +0.2506 [+0.2353,+0.2680] z= +30.0
      ALL obs  capped@2           a=0.1703 b=0.1647 diff -0.0056 [-0.0073,-0.0038] z=  -6.1
      ALL obs  capped@8           a=0.3486 b=0.4316 diff +0.0830 [+0.0761,+0.0904] z= +22.2
      ALL obs  mean p             a=0.9181 b=0.9210 diff +0.0029 [+0.0020,+0.0037] z=  +6.6
      ALL obs  top1 hit(p>.5)     a=0.9226 b=0.9202 diff -0.0024 [-0.0032,-0.0017] z=  -6.0
      ALL obs  bits @T*obs        a=0.3938 b=0.5120 diff +0.1183 [+0.1075,+0.1305] z= +20.5
      ALL obs  entropy            a=0.3892 b=0.2042 diff -0.1849 [-0.2011,-0.1702] z= -23.2
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.8339 diff +0.8339 [+0.8172,+0.8488] z=+102.8
      ALL obs  quantiles 50/90/99/99.9: a=[1.000e-03 3.580e-01 8.425e+00 1.679e+01] b=[ 0.     0.13  15.689 32.183]
      CONTENT  mean bits          a=0.6936 b=1.2826 diff +0.5890 [+0.5461,+0.6377] z= +24.7
      CONTENT  capped@2           a=0.3208 b=0.3276 diff +0.0067 [+0.0006,+0.0141] z=  +2.0
      CONTENT  capped@8           a=0.6131 b=0.8533 diff +0.2402 [+0.2204,+0.2616] z= +22.8
      CONTENT  mean p             a=0.8476 b=0.8431 diff -0.0045 [-0.0078,-0.0017] z=  -2.9
      CONTENT  top1 hit(p>.5)     a=0.8530 b=0.8419 diff -0.0110 [-0.0142,-0.0082] z=  -7.1
      CONTENT  bits @T*obs        a=0.6936 b=0.9950 diff +0.3015 [+0.2756,+0.3321] z= +20.9
      CONTENT  entropy            a=0.6019 b=0.3221 diff -0.2798 [-0.3276,-0.2361] z= -11.8
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.6515 diff +0.6515 [+0.6176,+0.6839] z= +37.8
      CONTENT  quantiles 50/90/99/99.9: a=[3.0000e-03 2.4670e+00 1.0724e+01 2.0707e+01] b=[ 0.     3.683 21.109 38.373]
      outcome  mean bits          a=0.8522 b=1.4398 diff +0.5876 [+0.5394,+0.6418] z= +21.9
      outcome  capped@2           a=0.4715 b=0.4651 diff -0.0064 [-0.0134,-0.0002] z=  -1.9
      outcome  capped@8           a=0.8193 b=1.0835 diff +0.2642 [+0.2439,+0.2880] z= +23.1
      outcome  mean p             a=0.7827 b=0.7819 diff -0.0008 [-0.0036,+0.0022] z=  -0.6
      outcome  top1 hit(p>.5)     a=0.7723 b=0.7705 diff -0.0018 [-0.0053,+0.0023] z=  -1.0
      outcome  bits @T*obs        a=0.8522 b=1.1049 diff +0.2527 [+0.2311,+0.2788] z= +20.2
      outcome  entropy            a=0.7374 b=0.4929 diff -0.2445 [-0.2695,-0.2228] z= -20.2
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.6330 diff +0.6330 [+0.6026,+0.6570] z= +46.4
      outcome  quantiles 50/90/99/99.9: a=[3.0000e-03 3.3760e+00 7.9860e+00 1.6301e+01] b=[ 0.     4.173 19.476 31.757]
    |delta| concentration: top 1% tokens hold 44.2% of |delta|, top 5% 89.4%; net delta from top-1% |delta| tokens +59.8%, from the other 99% +40.2%
  --- Qwen3-4B-Base -> Qwen3-8B-Base   (total obs delta -14360 bits over 435322 tok)
    ws                               -0.0456 [-0.0538,-0.0386] z= -12.1  share of total delta  +11.8%  rel -17.2%
    boiler                           -0.1412 [-0.1547,-0.1288] z= -20.8  share of total delta  +14.3%  rel  -5.8%
    prompt                           -0.0062 [-0.0089,-0.0039] z=  -4.8  share of total delta   +2.7%  rel -10.7%
    cmd_echo                         -0.0171 [-0.0196,-0.0150] z= -14.0  share of total delta  +17.7%  rel -27.1%
    rand_hash                        -0.0438 [-0.1126,-0.0147] z=  -1.7  share of total delta   +3.2%  rel  -1.1%
    rand_time                        -0.0120 [-0.0181,-0.0066] z=  -4.2  share of total delta   +0.9%  rel  -1.6%
    rand_misc                        +0.0077 [-0.0475,+0.0609] z=  +0.3  share of total delta   -0.0%  rel  +0.4%
    err_line                         -0.0524 [-0.0765,-0.0320] z=  -4.5  share of total delta   +1.7%  rel -10.7%
    test_line                        -0.0356 [-0.0555,-0.0215] z=  -4.1  share of total delta   +1.7%  rel -18.0%
    number                           -0.0309 [-0.0397,-0.0238] z=  -7.6  share of total delta   +5.8%  rel  -5.2%
    path                             -0.0226 [-0.0332,-0.0123] z=  -4.3  share of total delta   +2.1%  rel  -8.6%
    other                            -0.0544 [-0.0736,-0.0406] z=  -6.4  share of total delta  +38.1%  rel -13.3%
    ALL obs                          -0.0330 [-0.0385,-0.0286] z= -12.6  share of total delta +100.0%  rel  -8.4%
    novel                            -0.0552 [-0.0643,-0.0479] z= -13.2  share of total delta  +94.7%  rel  -8.2%
    copy                             -0.0040 [-0.0052,-0.0029] z=  -6.7  share of total delta   +5.3%  rel -14.7%
    first16                          -0.0630 [-0.0739,-0.0522] z= -11.4  share of total delta   +6.2%  rel  -7.3%
    outstart4                        -0.1340 [-0.1589,-0.1102] z= -10.9  share of total delta   +6.2%  rel -10.9%
    rand(all 3)                      -0.0272 [-0.0507,-0.0121] z=  -2.8  share of total delta   +4.1%  rel  -1.2%
    rand&novel                       -0.0462 [-0.0911,-0.0213] z=  -2.6  share of total delta   +4.1%  rel  -1.2%
    CONTENT(novel output,non-rand)   -0.0774 [-0.0981,-0.0617] z=  -8.3  share of total delta  +48.5%  rel -11.2%
    outcome-bearing                  -0.0583 [-0.0722,-0.0463] z=  -8.8  share of total delta   +8.9%  rel  -6.8%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3938 b=0.3608 diff -0.0330 [-0.0385,-0.0286] z= -12.6
      ALL obs  capped@2           a=0.1703 b=0.1623 diff -0.0080 [-0.0100,-0.0065] z=  -8.6
      ALL obs  capped@8           a=0.3486 b=0.3256 diff -0.0230 [-0.0281,-0.0191] z=  -9.9
      ALL obs  mean p             a=0.9181 b=0.9221 diff +0.0040 [+0.0033,+0.0049] z=  +9.2
      ALL obs  top1 hit(p>.5)     a=0.9226 b=0.9259 diff +0.0033 [+0.0025,+0.0043] z=  +6.9
      ALL obs  bits @T*obs        a=0.3938 b=0.3608 diff -0.0330 [-0.0385,-0.0286] z= -12.6
      ALL obs  entropy            a=0.3892 b=0.3606 diff -0.0286 [-0.0347,-0.0239] z= -10.2
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=-0.1948 diff -0.1948 [-0.2199,-0.1697] z= -15.1
      ALL obs  quantiles 50/90/99/99.9: a=[1.000e-03 3.580e-01 8.425e+00 1.679e+01] b=[1.0000e-03 2.8300e-01 7.8840e+00 1.5148e+01]
      CONTENT  mean bits          a=0.6936 b=0.6161 diff -0.0774 [-0.0981,-0.0617] z=  -8.3
      CONTENT  capped@2           a=0.3208 b=0.2933 diff -0.0275 [-0.0339,-0.0224] z=  -9.2
      CONTENT  capped@8           a=0.6131 b=0.5477 diff -0.0654 [-0.0828,-0.0514] z=  -8.1
      CONTENT  mean p             a=0.8476 b=0.8606 diff +0.0131 [+0.0107,+0.0160] z=  +9.3
      CONTENT  top1 hit(p>.5)     a=0.8530 b=0.8659 diff +0.0130 [+0.0101,+0.0162] z=  +8.1
      CONTENT  bits @T*obs        a=0.6936 b=0.6161 diff -0.0774 [-0.0981,-0.0617] z=  -8.3
      CONTENT  entropy            a=0.6019 b=0.5361 diff -0.0658 [-0.0851,-0.0508] z=  -7.2
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.0412 diff +0.0412 [+0.0124,+0.0691] z=  +2.8
      CONTENT  quantiles 50/90/99/99.9: a=[3.0000e-03 2.4670e+00 1.0724e+01 2.0707e+01] b=[2.000e-03 2.029e+00 9.898e+00 2.075e+01]
      outcome  mean bits          a=0.8522 b=0.7939 diff -0.0583 [-0.0722,-0.0463] z=  -8.8
      outcome  capped@2           a=0.4715 b=0.4439 diff -0.0275 [-0.0319,-0.0238] z= -13.3
      outcome  capped@8           a=0.8193 b=0.7631 diff -0.0562 [-0.0678,-0.0464] z= -10.2
      outcome  mean p             a=0.7827 b=0.7952 diff +0.0124 [+0.0109,+0.0143] z= +14.1
      outcome  top1 hit(p>.5)     a=0.7723 b=0.7849 diff +0.0126 [+0.0099,+0.0157] z=  +8.3
      outcome  bits @T*obs        a=0.8522 b=0.7939 diff -0.0583 [-0.0722,-0.0463] z=  -8.8
      outcome  entropy            a=0.7374 b=0.6874 diff -0.0500 [-0.0573,-0.0431] z= -13.6
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.0750 diff +0.0750 [+0.0389,+0.1073] z=  +4.2
      outcome  quantiles 50/90/99/99.9: a=[3.0000e-03 3.3760e+00 7.9860e+00 1.6301e+01] b=[2.0000e-03 3.3220e+00 7.7130e+00 1.5858e+01]
    |delta| concentration: top 1% tokens hold 40.8% of |delta|, top 5% 84.1%; net delta from top-1% |delta| tokens +60.5%, from the other 99% +39.5%
  --- Qwen3-4B -> Qwen3-8B   (total obs delta -37344 bits over 435322 tok)
    ws                               -0.0020 [-0.0161,+0.0132] z=  -0.3  share of total delta   +0.2%  rel  -0.5%
    boiler                           -0.9289 [-0.9746,-0.8848] z= -40.9  share of total delta  +36.3%  rel -20.1%
    prompt                           -0.0313 [-0.0421,-0.0211] z=  -6.1  share of total delta   +5.2%  rel -23.3%
    cmd_echo                         -0.0156 [-0.0201,-0.0113] z=  -7.0  share of total delta   +6.2%  rel -12.7%
    rand_hash                        -0.0698 [-0.1168,-0.0411] z=  -3.6  share of total delta   +2.0%  rel  -1.7%
    rand_time                        -0.0127 [-0.0473,+0.0220] z=  -0.7  share of total delta   +0.4%  rel  -1.3%
    rand_misc                        +0.3746 [+0.1311,+0.6638] z=  +2.8  share of total delta   -0.3%  rel +17.3%
    err_line                         -0.0500 [-0.1401,+0.0283] z=  -1.2  share of total delta   +0.6%  rel  -5.3%
    test_line                        -0.0565 [-0.0921,-0.0264] z=  -3.3  share of total delta   +1.0%  rel -14.4%
    number                           -0.1353 [-0.1697,-0.1072] z=  -8.4  share of total delta   +9.8%  rel -13.8%
    path                             -0.0875 [-0.1199,-0.0571] z=  -5.3  share of total delta   +3.1%  rel -15.9%
    other                            -0.1319 [-0.1606,-0.1080] z=  -9.3  share of total delta  +35.5%  rel -16.9%
    ALL obs                          -0.0858 [-0.0947,-0.0778] z= -19.6  share of total delta +100.0%  rel -13.3%
    novel                            -0.1286 [-0.1423,-0.1158] z= -19.5  share of total delta  +84.8%  rel -11.9%
    copy                             -0.0300 [-0.0341,-0.0261] z= -14.9  share of total delta  +15.2%  rel -40.4%
    first16                          -0.6137 [-0.6597,-0.5737] z= -28.3  share of total delta  +23.3%  rel -31.1%
    outstart4                        -0.2239 [-0.3068,-0.1393] z=  -5.1  share of total delta   +4.0%  rel  -9.9%
    rand(all 3)                      -0.0354 [-0.0614,-0.0084] z=  -2.6  share of total delta   +2.0%  rel  -1.4%
    rand&novel                       -0.0674 [-0.1024,-0.0343] z=  -3.9  share of total delta   +2.3%  rel  -1.6%
    CONTENT(novel output,non-rand)   -0.2036 [-0.2362,-0.1764] z= -13.6  share of total delta  +49.0%  rel -15.9%
    outcome-bearing                  -0.1920 [-0.2380,-0.1514] z=  -8.8  share of total delta  +11.2%  rel -13.3%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.6444 b=0.5586 diff -0.0858 [-0.0947,-0.0778] z= -19.6
      ALL obs  capped@2           a=0.1647 b=0.1482 diff -0.0165 [-0.0185,-0.0149] z= -17.5
      ALL obs  capped@8           a=0.4316 b=0.3753 diff -0.0563 [-0.0622,-0.0513] z= -19.9
      ALL obs  mean p             a=0.9210 b=0.9292 diff +0.0083 [+0.0075,+0.0092] z= +18.7
      ALL obs  top1 hit(p>.5)     a=0.9202 b=0.9277 diff +0.0075 [+0.0067,+0.0085] z= +15.9
      ALL obs  bits @T*obs        a=0.5120 b=0.4480 diff -0.0641 [-0.0724,-0.0574] z= -16.9
      ALL obs  entropy            a=0.2042 b=0.1923 diff -0.0119 [-0.0158,-0.0088] z=  -6.6
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.0657 diff +0.0657 [+0.0525,+0.0779] z= +10.1
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.13  15.689 32.183] b=[ 0.     0.035 14.607 32.506]
      CONTENT  mean bits          a=1.2826 b=1.0790 diff -0.2036 [-0.2362,-0.1764] z= -13.6
      CONTENT  capped@2           a=0.3276 b=0.2882 diff -0.0393 [-0.0457,-0.0336] z= -12.6
      CONTENT  capped@8           a=0.8533 b=0.7214 diff -0.1319 [-0.1516,-0.1150] z= -13.8
      CONTENT  mean p             a=0.8431 b=0.8623 diff +0.0192 [+0.0166,+0.0222] z= +13.2
      CONTENT  top1 hit(p>.5)     a=0.8419 b=0.8604 diff +0.0185 [+0.0158,+0.0215] z= +12.0
      CONTENT  bits @T*obs        a=0.9950 b=0.8291 diff -0.1659 [-0.1945,-0.1421] z= -12.5
      CONTENT  entropy            a=0.3221 b=0.2850 diff -0.0370 [-0.0491,-0.0265] z=  -6.4
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.1271 diff +0.1271 [+0.1123,+0.1417] z= +17.0
      CONTENT  quantiles 50/90/99/99.9: a=[ 0.     3.683 21.109 38.373] b=[ 0.     3.122 19.837 39.404]
      outcome  mean bits          a=1.4398 b=1.2478 diff -0.1920 [-0.2380,-0.1514] z=  -8.8
      outcome  capped@2           a=0.4651 b=0.4325 diff -0.0326 [-0.0383,-0.0272] z= -11.5
      outcome  capped@8           a=1.0835 b=0.9624 diff -0.1211 [-0.1443,-0.1012] z= -11.2
      outcome  mean p             a=0.7819 b=0.7979 diff +0.0159 [+0.0134,+0.0187] z= +12.2
      outcome  top1 hit(p>.5)     a=0.7705 b=0.7876 diff +0.0171 [+0.0142,+0.0204] z= +10.6
      outcome  bits @T*obs        a=1.1049 b=0.9701 diff -0.1348 [-0.1604,-0.1111] z= -10.6
      outcome  entropy            a=0.4929 b=0.4710 diff -0.0219 [-0.0325,-0.0121] z=  -4.3
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.0801 diff +0.0801 [+0.0635,+0.0989] z=  +9.0
      outcome  quantiles 50/90/99/99.9: a=[ 0.     4.173 19.476 31.757] b=[ 0.     3.719 17.991 33.806]
    |delta| concentration: top 1% tokens hold 43.3% of |delta|, top 5% 92.0%; net delta from top-1% |delta| tokens +49.4%, from the other 99% +50.6%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  60.5% a=0.036 b=0.022 diff -0.0140 [-0.0207,-0.0077] z=-4.3 | capped@8 diff -0.0136 z=-6.2
      ref bits in [0.01,0.1): tok  14.3% a=0.300 b=0.171 diff -0.1293 [-0.1702,-0.0865] z=-6.3 | capped@8 diff -0.1084 z=-7.3
      ref bits in [0.1,1): tok  10.5% a=1.130 b=0.799 diff -0.3315 [-0.4078,-0.2605] z=-8.8 | capped@8 diff -0.2480 z=-9.8
      ref bits in [1,4): tok   9.4% a=4.100 b=3.409 diff -0.6911 [-0.8176,-0.5784] z=-10.9 | capped@8 diff -0.5099 z=-11.8
      ref bits in [4,1000000000.0): tok   5.3% a=13.465 b=12.013 diff -1.4515 [-1.7014,-1.2113] z=-11.4 | capped@8 diff -0.6465 z=-16.7
```
