# Terminal token classes in neutral rendering

```text
[1] tail concentration of observation bits
  Qwen3-4B-Base          ALL obs  mean=0.383 b/tok median=0.0004 | share of bits from top 1%/5%/20% tokens: 31.2%/80.4%/99.8% | tok frac loss<0.01:78.3% <0.1:86.9% >1:7.7% >2:6.1% >8:1.04% | bits share from tok>2b:87.7% >8b:32.1% | 50% of bits in top 2.10%
  Qwen3-4B-Base          novel    mean=0.656 b/tok median=0.0010 | share of bits from top 1%/5%/20% tokens: 21.0%/61.2%/99.2% | tok frac loss<0.01:68.3% <0.1:79.2% >1:13.0% >2:10.6% >8:1.83% | bits share from tok>2b:89.3% >8b:33.0% | 50% of bits in top 3.52%
  Qwen3-4B-Base          CONTENT  mean=0.687 b/tok median=0.0026 | share of bits from top 1%/5%/20% tokens: 21.6%/58.5%/97.9% | tok frac loss<0.01:61.2% <0.1:75.1% >1:14.7% >2:11.2% >8:1.83% | bits share from tok>2b:86.0% >8b:32.6% | 50% of bits in top 3.71%
  Qwen3-8B-Base          ALL obs  mean=0.359 b/tok median=0.0004 | share of bits from top 1%/5%/20% tokens: 32.3%/82.4%/99.8% | tok frac loss<0.01:79.3% <0.1:87.7% >1:7.3% >2:5.8% >8:0.98% | bits share from tok>2b:87.6% >8b:31.8% | 50% of bits in top 1.98%
  Qwen3-8B-Base          novel    mean=0.616 b/tok median=0.0010 | share of bits from top 1%/5%/20% tokens: 22.0%/62.8%/99.3% | tok frac loss<0.01:69.8% <0.1:80.4% >1:12.4% >2:10.0% >8:1.72% | bits share from tok>2b:89.1% >8b:32.7% | 50% of bits in top 3.34%
  Qwen3-8B-Base          CONTENT  mean=0.615 b/tok median=0.0019 | share of bits from top 1%/5%/20% tokens: 23.7%/61.3%/98.4% | tok frac loss<0.01:64.2% <0.1:77.1% >1:13.2% >2:10.0% >8:1.55% | bits share from tok>2b:85.5% >8b:31.6% | 50% of bits in top 3.36%
  Qwen3-4B               ALL obs  mean=0.554 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 34.4%/84.1%/100.0% | tok frac loss<0.01:86.7% <0.1:89.2% >1:8.1% >2:7.0% >8:2.19% | bits share from tok>2b:95.1% >8b:56.9% | 50% of bits in top 1.75%
  Qwen3-4B               novel    mean=0.931 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 23.6%/67.1%/100.0% | tok frac loss<0.01:78.9% <0.1:82.4% >1:13.4% >2:11.8% >8:3.72% | bits share from tok>2b:95.5% >8b:57.4% | 50% of bits in top 2.94%
  Qwen3-4B               CONTENT  mean=1.144 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 21.6%/62.8%/99.6% | tok frac loss<0.01:73.5% <0.1:78.6% >1:16.0% >2:13.8% >8:4.86% | bits share from tok>2b:95.1% >8b:61.9% | 50% of bits in top 3.38%
  Qwen3-8B               ALL obs  mean=0.504 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 37.5%/86.8%/100.0% | tok frac loss<0.01:87.8% <0.1:90.2% >1:7.4% >2:6.6% >8:1.93% | bits share from tok>2b:95.5% >8b:56.5% | 50% of bits in top 1.56%
  Qwen3-8B               novel    mean=0.857 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 26.1%/70.0%/100.0% | tok frac loss<0.01:80.4% <0.1:83.8% >1:12.5% >2:11.1% >8:3.32% | bits share from tok>2b:95.8% >8b:57.2% | 50% of bits in top 2.63%
  Qwen3-8B               CONTENT  mean=0.954 b/tok median=0.0000 | share of bits from top 1%/5%/20% tokens: 25.1%/67.6%/99.8% | tok frac loss<0.01:75.8% <0.1:80.8% >1:14.1% >2:12.0% >8:3.74% | bits share from tok>2b:94.4% >8b:58.4% | 50% of bits in top 2.84%
  Nemotron-Terminal-8B   ALL obs  mean=0.861 b/tok median=0.0005 | share of bits from top 1%/5%/20% tokens: 22.9%/64.3%/99.1% | tok frac loss<0.01:67.6% <0.1:77.6% >1:14.1% >2:11.4% >8:3.20% | bits share from tok>2b:91.3% >8b:50.2% | 50% of bits in top 3.17%
  Nemotron-Terminal-8B   novel    mean=1.054 b/tok median=0.0014 | share of bits from top 1%/5%/20% tokens: 18.9%/55.4%/97.4% | tok frac loss<0.01:61.2% <0.1:72.1% >1:18.0% >2:14.7% >8:3.71% | bits share from tok>2b:91.4% >8b:46.6% | 50% of bits in top 4.17%
  Nemotron-Terminal-8B   CONTENT  mean=0.932 b/tok median=0.0019 | share of bits from top 1%/5%/20% tokens: 19.2%/55.1%/96.8% | tok frac loss<0.01:59.8% <0.1:71.5% >1:17.9% >2:14.1% >8:2.94% | bits share from tok>2b:89.0% >8b:40.4% | 50% of bits in top 4.20%

[2] by class: token share | per model: share of obs bits, mean bits/token
  class                              tok%  copy%          Qwen3-4B-Base          Qwen3-8B-Base               Qwen3-4B               Qwen3-8B         on-Terminal-8B
  ws                                 8.6%  32.0%      4.9% of bits, 0.221     4.9% of bits, 0.207     4.9% of bits, 0.316     5.2% of bits, 0.305     9.9% of bits, 0.998
  boiler                             3.3%  19.6%     20.6% of bits, 2.355    21.3% of bits, 2.283    19.2% of bits, 3.177    21.9% of bits, 3.293     3.2% of bits, 0.827
  prompt                            14.2%  73.5%      2.7% of bits, 0.072     2.2% of bits, 0.056     3.9% of bits, 0.152     3.1% of bits, 0.111    31.0% of bits, 1.883
  cmd_echo                          34.0%  38.9%      4.3% of bits, 0.049     4.2% of bits, 0.044     6.4% of bits, 0.105     6.1% of bits, 0.090    16.4% of bits, 0.416
  rand_hash                          2.4%  23.1%     24.0% of bits, 3.832    25.3% of bits, 3.786    17.4% of bits, 4.003    18.7% of bits, 3.922    11.3% of bits, 4.048
  rand_time                          2.5%  59.1%      4.9% of bits, 0.759     5.2% of bits, 0.745     4.0% of bits, 0.878     4.3% of bits, 0.858     2.6% of bits, 0.897
  rand_misc                          0.1%  12.1%      0.3% of bits, 1.813     0.3% of bits, 1.825     0.2% of bits, 1.991     0.3% of bits, 2.253     0.2% of bits, 2.175
  err_line                           1.1%  40.9%      1.4% of bits, 0.487     1.3% of bits, 0.444     1.7% of bits, 0.851     1.6% of bits, 0.768     1.4% of bits, 1.079
  test_line                          1.5%  38.2%      0.8% of bits, 0.195     0.7% of bits, 0.162     1.0% of bits, 0.343     0.9% of bits, 0.282     0.6% of bits, 0.350
  number                             6.2%  45.2%      9.7% of bits, 0.595     9.8% of bits, 0.564     9.4% of bits, 0.834     9.3% of bits, 0.747     5.2% of bits, 0.720
  path                               3.0%  46.5%      2.1% of bits, 0.261     2.0% of bits, 0.238     2.7% of bits, 0.499     2.5% of bits, 0.414     1.8% of bits, 0.504
  other                             23.1%  39.4%     24.3% of bits, 0.403    22.7% of bits, 0.353    29.3% of bits, 0.702    26.2% of bits, 0.571    16.4% of bits, 0.611
  ALL obs                          100.0%  43.4%    100.0% of bits, 0.383   100.0% of bits, 0.359   100.0% of bits, 0.554   100.0% of bits, 0.504   100.0% of bits, 0.861
  novel                             56.6%   0.0%     96.8% of bits, 0.656    97.0% of bits, 0.616    95.2% of bits, 0.931    96.3% of bits, 0.857    69.3% of bits, 1.054
  copy                              43.4% 100.0%      3.2% of bits, 0.028     3.0% of bits, 0.025     4.8% of bits, 0.061     3.7% of bits, 0.043    30.7% of bits, 0.608
  first16                            3.3%  64.6%      6.9% of bits, 0.809     6.9% of bits, 0.764     6.8% of bits, 1.163     7.9% of bits, 1.224     3.7% of bits, 0.978
  outstart4                          1.5%  10.3%      4.8% of bits, 1.199     4.7% of bits, 1.098     5.4% of bits, 1.967     5.3% of bits, 1.736     2.5% of bits, 1.399
  rand(all 3)                        5.0%  41.1%     29.3% of bits, 2.262    30.8% of bits, 2.232    21.6% of bits, 2.406    23.2% of bits, 2.360    14.1% of bits, 2.440
  rand&novel                         2.9%   0.0%     28.9% of bits, 3.786    30.4% of bits, 3.737    21.2% of bits, 4.019    23.0% of bits, 3.956    13.2% of bits, 3.886
  CONTENT(novel output,non-rand)    20.6%   0.0%     37.0% of bits, 0.687    35.4% of bits, 0.615    42.6% of bits, 1.144    39.1% of bits, 0.954    22.3% of bits, 0.932
  outcome-bearing                    5.0%   0.0%     11.1% of bits, 0.850    11.1% of bits, 0.795    11.3% of bits, 1.246    11.0% of bits, 1.105     6.2% of bits, 1.070

[2b] within NOVEL tokens only: share of novel bits by class
  ws           tok  10.3%   4.9%/0.310   4.9%/0.292   4.9%/0.447   5.2%/0.432  12.0%/1.234
  boiler       tok   4.8%  21.2%/2.917  21.9%/2.830  20.1%/3.930  22.6%/4.075   4.4%/0.980
  prompt       tok   6.6%   1.8%/0.180   1.5%/0.141   1.8%/0.257   1.9%/0.248  14.4%/2.282
  cmd_echo     tok  36.7%   4.1%/0.073   3.9%/0.066   6.1%/0.154   5.8%/0.136  17.9%/0.514
  rand_hash    tok   3.3%  24.8%/4.980  26.1%/4.920  18.2%/5.191  19.4%/5.098  15.7%/5.063
  rand_time    tok   1.8%   4.7%/1.717   4.9%/1.685   3.9%/1.990   4.1%/1.961   3.1%/1.831
  rand_misc    tok   0.1%   0.3%/2.057   0.3%/2.073   0.2%/2.265   0.3%/2.561   0.2%/2.453
  err_line     tok   1.1%   1.3%/0.773   1.3%/0.706   1.6%/1.341   1.6%/1.202   1.4%/1.309
  test_line    tok   1.7%   0.8%/0.305   0.7%/0.253   1.0%/0.532   0.9%/0.438   0.8%/0.501
  number       tok   6.0%   9.4%/1.017   9.4%/0.962   9.3%/1.427   9.0%/1.273   6.8%/1.184
  path         tok   2.9%   2.1%/0.469   2.0%/0.430   2.7%/0.892   2.5%/0.743   1.9%/0.707
  other        tok  24.8%  24.7%/0.654  23.0%/0.573  30.2%/1.137  26.7%/0.924  21.3%/0.908

[3] entropy vs loss (bits/token; equal if calibrated). gap=loss-entropy>0 means overconfident
  ALL obs                          Qwen3-4B-Base: loss 0.383 ent 0.367 gap +0.016 | Qwen3-8B-Base: loss 0.359 ent 0.340 gap +0.019 | Qwen3-4B: loss 0.554 ent 0.234 gap +0.320 | Qwen3-8B: loss 0.504 ent 0.216 gap +0.287 | on-Terminal-8B: loss 0.861 ent 0.432 gap +0.429
  novel                            Qwen3-4B-Base: loss 0.656 ent 0.610 gap +0.045 | Qwen3-8B-Base: loss 0.616 ent 0.564 gap +0.051 | Qwen3-4B: loss 0.931 ent 0.399 gap +0.533 | Qwen3-8B: loss 0.857 ent 0.370 gap +0.487 | on-Terminal-8B: loss 1.054 ent 0.588 gap +0.466
  CONTENT(novel output,non-rand)   Qwen3-4B-Base: loss 0.687 ent 0.592 gap +0.095 | Qwen3-8B-Base: loss 0.615 ent 0.518 gap +0.097 | Qwen3-4B: loss 1.144 ent 0.366 gap +0.778 | Qwen3-8B: loss 0.954 ent 0.328 gap +0.626 | on-Terminal-8B: loss 0.932 ent 0.592 gap +0.339
  rand&novel                       Qwen3-4B-Base: loss 3.786 ent 3.692 gap +0.094 | Qwen3-8B-Base: loss 3.737 ent 3.644 gap +0.094 | Qwen3-4B: loss 4.019 ent 3.312 gap +0.707 | Qwen3-8B: loss 3.956 ent 3.361 gap +0.595 | on-Terminal-8B: loss 3.886 ent 3.634 gap +0.253
  copy                             Qwen3-4B-Base: loss 0.028 ent 0.051 gap -0.022 | Qwen3-8B-Base: loss 0.025 ent 0.047 gap -0.023 | Qwen3-4B: loss 0.061 ent 0.019 gap +0.042 | Qwen3-8B: loss 0.043 ent 0.016 gap +0.027 | on-Terminal-8B: loss 0.608 ent 0.229 gap +0.379

[4] paired differences b-a (bits/token unless noted) [95% traj-bootstrap CI], z
  --- Qwen3-8B-Base -> Qwen3-8B   (total obs delta +62837 bits over 435322 tok)
    ws                               +0.0981 [+0.0836,+0.1150] z= +12.7  share of total delta   +5.8%  rel +47.3%
    boiler                           +1.0100 [+0.9686,+1.0523] z= +45.7  share of total delta  +23.4%  rel +44.2%
    prompt                           +0.0559 [+0.0493,+0.0633] z= +15.6  share of total delta   +5.5%  rel +100.6%
    cmd_echo                         +0.0457 [+0.0400,+0.0516] z= +14.9  share of total delta  +10.8%  rel +103.8%
    rand_hash                        +0.1360 [+0.0950,+0.1857] z=  +5.8  share of total delta   +2.3%  rel  +3.6%
    rand_time                        +0.1132 [+0.0921,+0.1360] z=  +9.8  share of total delta   +2.0%  rel +15.2%
    rand_misc                        +0.4280 [+0.2572,+0.6560] z=  +4.2  share of total delta   +0.2%  rel +23.5%
    err_line                         +0.3234 [+0.2642,+0.4113] z=  +8.7  share of total delta   +2.4%  rel +72.8%
    test_line                        +0.1207 [+0.0917,+0.1651] z=  +6.3  share of total delta   +1.3%  rel +74.7%
    number                           +0.1831 [+0.1541,+0.2165] z= +11.3  share of total delta   +7.9%  rel +32.4%
    path                             +0.1758 [+0.1420,+0.2186] z=  +8.8  share of total delta   +3.7%  rel +73.8%
    other                            +0.2172 [+0.1872,+0.2547] z= +12.4  share of total delta  +34.8%  rel +61.5%
    ALL obs                          +0.1443 [+0.1347,+0.1554] z= +27.2  share of total delta +100.0%  rel +40.2%
    novel                            +0.2411 [+0.2256,+0.2579] z= +29.1  share of total delta  +94.5%  rel +39.2%
    copy                             +0.0183 [+0.0161,+0.0210] z= +14.2  share of total delta   +5.5%  rel +73.7%
    first16                          +0.4602 [+0.4247,+0.5009] z= +23.5  share of total delta  +10.4%  rel +60.2%
    outstart4                        +0.6380 [+0.5586,+0.7300] z= +14.8  share of total delta   +6.7%  rel +58.1%
    rand(all 3)                      +0.1283 [+0.1066,+0.1538] z= +10.3  share of total delta   +4.4%  rel  +5.7%
    rand&novel                       +0.2183 [+0.1837,+0.2731] z=  +9.5  share of total delta   +4.4%  rel  +5.8%
    CONTENT(novel output,non-rand)   +0.3386 [+0.3079,+0.3732] z= +20.3  share of total delta  +48.4%  rel +55.0%
    outcome-bearing                  +0.3100 [+0.2793,+0.3449] z= +18.2  share of total delta  +10.8%  rel +39.0%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3592 b=0.5035 diff +0.1443 [+0.1347,+0.1554] z= +27.2
      ALL obs  capped@2           a=0.1598 b=0.1539 diff -0.0059 [-0.0072,-0.0047] z=  -9.4
      ALL obs  capped@8           a=0.3231 b=0.3734 diff +0.0503 [+0.0449,+0.0556] z= +18.1
      ALL obs  mean p             a=0.9232 b=0.9267 diff +0.0034 [+0.0028,+0.0041] z= +11.1
      ALL obs  top1 hit(p>.5)     a=0.9268 b=0.9257 diff -0.0011 [-0.0018,-0.0005] z=  -3.5
      ALL obs  bits @T*obs        a=0.3592 b=0.4355 diff +0.0763 [+0.0686,+0.0851] z= +17.9
      ALL obs  entropy            a=0.3398 b=0.2163 diff -0.1235 [-0.1336,-0.1139] z= -24.7
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.8558 diff +0.8558 [+0.8377,+0.8701] z=+103.8
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.27   7.929 15.381] b=[ 0.     0.08  12.556 26.149]
      CONTENT  mean bits          a=0.6153 b=0.9539 diff +0.3386 [+0.3079,+0.3732] z= +20.3
      CONTENT  capped@2           a=0.2895 b=0.2923 diff +0.0027 [-0.0012,+0.0070] z=  +1.3
      CONTENT  capped@8           a=0.5449 b=0.6959 diff +0.1511 [+0.1349,+0.1684] z= +17.6
      CONTENT  mean p             a=0.8624 b=0.8609 diff -0.0015 [-0.0036,+0.0004] z=  -1.5
      CONTENT  top1 hit(p>.5)     a=0.8676 b=0.8589 diff -0.0087 [-0.0108,-0.0066] z=  -8.1
      CONTENT  bits @T*obs        a=0.6153 b=0.7934 diff +0.1781 [+0.1592,+0.1991] z= +17.2
      CONTENT  entropy            a=0.5179 b=0.3279 diff -0.1900 [-0.2204,-0.1618] z= -12.7
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.6929 diff +0.6929 [+0.6606,+0.7239] z= +42.3
      CONTENT  quantiles 50/90/99/99.9: a=[2.0000e-03 2.0070e+00 9.8960e+00 2.1154e+01] b=[ 0.     3.049 16.952 33.317]
      outcome  mean bits          a=0.7948 b=1.1049 diff +0.3100 [+0.2793,+0.3449] z= +18.2
      outcome  capped@2           a=0.4396 b=0.4388 diff -0.0008 [-0.0063,+0.0049] z=  -0.3
      outcome  capped@8           a=0.7615 b=0.9157 diff +0.1541 [+0.1370,+0.1735] z= +16.7
      outcome  mean p             a=0.7969 b=0.7960 diff -0.0009 [-0.0033,+0.0015] z=  -0.7
      outcome  top1 hit(p>.5)     a=0.7867 b=0.7843 diff -0.0024 [-0.0063,+0.0010] z=  -1.3
      outcome  bits @T*obs        a=0.7948 b=0.9276 diff +0.1328 [+0.1170,+0.1513] z= +14.9
      outcome  entropy            a=0.6717 b=0.5208 diff -0.1509 [-0.1680,-0.1361] z= -18.4
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.6638 diff +0.6638 [+0.6353,+0.6869] z= +48.6
      outcome  quantiles 50/90/99/99.9: a=[2.0000e-03 3.3250e+00 7.9050e+00 1.5707e+01] b=[ 0.     3.511 14.968 28.923]
    |delta| concentration: top 1% tokens hold 48.6% of |delta|, top 5% 89.3%; net delta from top-1% |delta| tokens +72.2%, from the other 99% +27.8%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  61.2% a=0.003 b=0.020 diff +0.0177 [+0.0126,+0.0234] z=+6.7 | capped@8 diff +0.0126 z=+7.0
      ref bits in [0.01,0.1): tok  13.9% a=0.055 b=0.158 diff +0.1021 [+0.0782,+0.1269] z=+8.2 | capped@8 diff +0.0688 z=+7.8
      ref bits in [0.1,1): tok  10.2% a=0.419 b=0.741 diff +0.3219 [+0.2634,+0.3925] z=+9.8 | capped@8 diff +0.2408 z=+9.9
      ref bits in [1,4): tok   9.4% a=2.195 b=3.130 diff +0.9341 [+0.8382,+1.0344] z=+19.0 | capped@8 diff +0.6569 z=+20.8
      ref bits in [4,1000000000.0): tok   5.3% a=6.767 b=10.426 diff +3.6592 [+3.4082,+3.9876] z=+25.5 | capped@8 diff +0.8980 z=+20.0
  --- Qwen3-8B -> Nemotron-Terminal-8B   (total obs delta +155461 bits over 435322 tok)
    ws                               +0.6924 [+0.5893,+0.8060] z= +12.3  share of total delta  +16.6%  rel +226.7%
    boiler                           -2.4656 [-2.5934,-2.3363] z= -37.5  share of total delta  -23.1%  rel -74.9%
    prompt                           +1.7717 [+1.6774,+1.8907] z= +34.4  share of total delta  +70.2%  rel +1590.1%
    cmd_echo                         +0.3266 [+0.2821,+0.3774] z= +13.2  share of total delta  +31.1%  rel +363.6%
    rand_hash                        +0.1262 [-0.0449,+0.5360] z=  +0.8  share of total delta   +0.8%  rel  +3.2%
    rand_time                        +0.0385 [-0.0045,+0.0823] z=  +1.8  share of total delta   +0.3%  rel  +4.5%
    rand_misc                        -0.0775 [-0.2657,+0.0968] z=  -0.8  share of total delta   -0.0%  rel  -3.4%
    err_line                         +0.3109 [+0.1375,+0.4309] z=  +4.1  share of total delta   +0.9%  rel +40.5%
    test_line                        +0.0677 [+0.0205,+0.1131] z=  +2.9  share of total delta   +0.3%  rel +24.0%
    number                           -0.0268 [-0.0580,+0.0019] z=  -1.7  share of total delta   -0.5%  rel  -3.6%
    path                             +0.0898 [-0.0084,+0.1884] z=  +1.8  share of total delta   +0.8%  rel +21.7%
    other                            +0.0404 [+0.0115,+0.0698] z=  +2.7  share of total delta   +2.6%  rel  +7.1%
    ALL obs                          +0.3571 [+0.3218,+0.3959] z= +18.6  share of total delta +100.0%  rel +70.9%
    novel                            +0.1973 [+0.1549,+0.2443] z=  +8.7  share of total delta  +31.3%  rel +23.0%
    copy                             +0.5654 [+0.5206,+0.6152] z= +24.0  share of total delta  +68.7%  rel +1313.6%
    first16                          -0.2466 [-0.3415,-0.1528] z=  -5.0  share of total delta   -2.2%  rel -20.1%
    outstart4                        -0.3374 [-0.4188,-0.2586] z=  -8.0  share of total delta   -1.4%  rel -19.4%
    rand(all 3)                      +0.0795 [-0.0089,+0.2512] z=  +1.1  share of total delta   +1.1%  rel  +3.4%
    rand&novel                       -0.0695 [-0.1137,-0.0398] z=  -3.6  share of total delta   -0.6%  rel  -1.8%
    CONTENT(novel output,non-rand)   -0.0222 [-0.0542,+0.0090] z=  -1.4  share of total delta   -1.3%  rel  -2.3%
    outcome-bearing                  -0.0348 [-0.0751,+0.0061] z=  -1.7  share of total delta   -0.5%  rel  -3.1%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.5035 b=0.8606 diff +0.3571 [+0.3218,+0.3959] z= +18.6
      ALL obs  capped@2           a=0.1539 b=0.3034 diff +0.1495 [+0.1420,+0.1586] z= +35.4
      ALL obs  capped@8           a=0.3734 b=0.6842 diff +0.3108 [+0.2894,+0.3362] z= +25.6
      ALL obs  mean p             a=0.9267 b=0.8542 diff -0.0724 [-0.0768,-0.0688] z= -35.7
      ALL obs  top1 hit(p>.5)     a=0.9257 b=0.8592 diff -0.0665 [-0.0710,-0.0628] z= -31.7
      ALL obs  bits @T*obs        a=0.4355 b=0.7941 diff +0.3586 [+0.3312,+0.3902] z= +23.7
      ALL obs  entropy            a=0.2163 b=0.4321 diff +0.2158 [+0.2029,+0.2300] z= +31.4
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=-0.7770 diff -0.7770 [-0.7904,-0.7632] z=-112.5
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.08  12.556 26.149] b=[1.0000e-03 2.7320e+00 1.4517e+01 2.6051e+01]
      CONTENT  mean bits          a=0.9539 b=0.9317 diff -0.0222 [-0.0542,+0.0090] z=  -1.4
      CONTENT  capped@2           a=0.2923 b=0.3837 diff +0.0915 [+0.0840,+0.0998] z= +22.9
      CONTENT  capped@8           a=0.6959 b=0.7907 diff +0.0948 [+0.0770,+0.1161] z=  +9.3
      CONTENT  mean p             a=0.8609 b=0.8177 diff -0.0432 [-0.0472,-0.0397] z= -23.5
      CONTENT  top1 hit(p>.5)     a=0.8589 b=0.8211 diff -0.0378 [-0.0421,-0.0341] z= -19.0
      CONTENT  bits @T*obs        a=0.7934 b=0.9060 diff +0.1126 [+0.0916,+0.1364] z=  +9.7
      CONTENT  entropy            a=0.3279 b=0.5923 diff +0.2644 [+0.2335,+0.2997] z= +15.4
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=-0.6884 diff -0.6884 [-0.7119,-0.6645] z= -56.2
      CONTENT  quantiles 50/90/99/99.9: a=[ 0.     3.049 16.952 33.317] b=[2.0000e-03 3.2880e+00 1.3176e+01 2.3263e+01]
      outcome  mean bits          a=1.1049 b=1.0701 diff -0.0348 [-0.0751,+0.0061] z=  -1.7
      outcome  capped@2           a=0.4388 b=0.5285 diff +0.0898 [+0.0786,+0.1020] z= +15.3
      outcome  capped@8           a=0.9157 b=0.9866 diff +0.0710 [+0.0439,+0.1002] z=  +4.9
      outcome  mean p             a=0.7960 b=0.7548 diff -0.0413 [-0.0470,-0.0361] z= -15.3
      outcome  top1 hit(p>.5)     a=0.7843 b=0.7451 diff -0.0392 [-0.0453,-0.0337] z= -12.9
      outcome  bits @T*obs        a=0.9276 b=1.0264 diff +0.0988 [+0.0692,+0.1316] z=  +6.0
      outcome  entropy            a=0.5208 b=0.7388 diff +0.2180 [+0.1962,+0.2409] z= +19.3
      outcome  win(b<a)-win(a<b)  a=0.0000 b=-0.6525 diff -0.6525 [-0.6723,-0.6309] z= -59.3
      outcome  quantiles 50/90/99/99.9: a=[ 0.     3.511 14.968 28.923] b=[3.0000e-03 3.5670e+00 1.0748e+01 2.0145e+01]
    |delta| concentration: top 1% tokens hold 26.2% of |delta|, top 5% 70.5%; net delta from top-1% |delta| tokens +29.1%, from the other 99% +70.9%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  61.2% a=0.020 b=0.192 diff +0.1721 [+0.1463,+0.1983] z=+13.1 | capped@8 diff +0.1386 z=+14.3
      ref bits in [0.01,0.1): tok  13.9% a=0.158 b=0.438 diff +0.2806 [+0.2421,+0.3244] z=+13.1 | capped@8 diff +0.2628 z=+15.7
      ref bits in [0.1,1): tok  10.2% a=0.741 b=0.938 diff +0.1967 [+0.1405,+0.2592] z=+6.7 | capped@8 diff +0.2319 z=+9.6
      ref bits in [1,4): tok   9.4% a=3.130 b=2.757 diff -0.3729 [-0.4782,-0.2814] z=-7.6 | capped@8 diff -0.1733 z=-4.8
      ref bits in [4,1000000000.0): tok   5.3% a=10.426 b=7.547 diff -2.8785 [-3.2151,-2.5713] z=-17.2 | capped@8 diff -0.6452 z=-12.8
  --- Qwen3-8B-Base -> Nemotron-Terminal-8B   (total obs delta +218298 bits over 435322 tok)
    ws                               +0.7905 [+0.6904,+0.9044] z= +14.2  share of total delta  +13.5%  rel +381.1%
    boiler                           -1.4556 [-1.5534,-1.3628] z= -30.4  share of total delta   -9.7%  rel -63.8%
    prompt                           +1.8276 [+1.7372,+1.9464] z= +36.0  share of total delta  +51.6%  rel +3290.3%
    cmd_echo                         +0.3723 [+0.3278,+0.4212] z= +15.3  share of total delta  +25.2%  rel +844.8%
    rand_hash                        +0.2622 [+0.0853,+0.6499] z=  +1.7  share of total delta   +1.3%  rel  +6.9%
    rand_time                        +0.1517 [+0.1220,+0.1819] z= +10.0  share of total delta   +0.8%  rel +20.4%
    rand_misc                        +0.3505 [+0.1884,+0.5611] z=  +3.6  share of total delta   +0.0%  rel +19.2%
    err_line                         +0.6343 [+0.4949,+0.7212] z= +11.1  share of total delta   +1.4%  rel +142.7%
    test_line                        +0.1884 [+0.1399,+0.2482] z=  +7.1  share of total delta   +0.6%  rel +116.6%
    number                           +0.1563 [+0.1363,+0.1804] z= +13.9  share of total delta   +1.9%  rel +27.7%
    path                             +0.2656 [+0.1863,+0.3532] z=  +6.2  share of total delta   +1.6%  rel +111.5%
    other                            +0.2576 [+0.2282,+0.2932] z= +15.9  share of total delta  +11.9%  rel +72.9%
    ALL obs                          +0.5015 [+0.4688,+0.5399] z= +27.3  share of total delta +100.0%  rel +139.6%
    novel                            +0.4384 [+0.4024,+0.4833] z= +21.5  share of total delta  +49.5%  rel +71.2%
    copy                             +0.5837 [+0.5390,+0.6349] z= +24.3  share of total delta  +50.5%  rel +2355.1%
    first16                          +0.2136 [+0.1485,+0.2794] z=  +6.1  share of total delta   +1.4%  rel +27.9%
    outstart4                        +0.3005 [+0.2449,+0.3534] z= +10.9  share of total delta   +0.9%  rel +27.4%
    rand(all 3)                      +0.2078 [+0.1198,+0.3654] z=  +3.0  share of total delta   +2.1%  rel  +9.3%
    rand&novel                       +0.1488 [+0.1105,+0.2001] z=  +6.5  share of total delta   +0.9%  rel  +4.0%
    CONTENT(novel output,non-rand)   +0.3164 [+0.2849,+0.3535] z= +18.2  share of total delta  +13.0%  rel +51.4%
    outcome-bearing                  +0.2753 [+0.2388,+0.3159] z= +14.0  share of total delta   +2.8%  rel +34.6%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3592 b=0.8606 diff +0.5015 [+0.4688,+0.5399] z= +27.3
      ALL obs  capped@2           a=0.1598 b=0.3034 diff +0.1436 [+0.1358,+0.1531] z= +32.7
      ALL obs  capped@8           a=0.3231 b=0.6842 diff +0.3610 [+0.3397,+0.3868] z= +30.2
      ALL obs  mean p             a=0.9232 b=0.8542 diff -0.0690 [-0.0736,-0.0652] z= -32.7
      ALL obs  top1 hit(p>.5)     a=0.9268 b=0.8592 diff -0.0676 [-0.0723,-0.0638] z= -31.8
      ALL obs  bits @T*obs        a=0.3592 b=0.7941 diff +0.4349 [+0.4070,+0.4680] z= +28.3
      ALL obs  entropy            a=0.3398 b=0.4321 diff +0.0923 [+0.0825,+0.1029] z= +17.8
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.1366 diff +0.1366 [+0.1101,+0.1632] z= +10.2
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.27   7.929 15.381] b=[1.0000e-03 2.7320e+00 1.4517e+01 2.6051e+01]
      CONTENT  mean bits          a=0.6153 b=0.9317 diff +0.3164 [+0.2849,+0.3535] z= +18.2
      CONTENT  capped@2           a=0.2895 b=0.3837 diff +0.0942 [+0.0851,+0.1044] z= +18.2
      CONTENT  capped@8           a=0.5449 b=0.7907 diff +0.2458 [+0.2211,+0.2742] z= +18.2
      CONTENT  mean p             a=0.8624 b=0.8177 diff -0.0447 [-0.0497,-0.0404] z= -18.1
      CONTENT  top1 hit(p>.5)     a=0.8676 b=0.8211 diff -0.0465 [-0.0516,-0.0419] z= -18.4
      CONTENT  bits @T*obs        a=0.6153 b=0.9060 diff +0.2906 [+0.2612,+0.3254] z= +17.5
      CONTENT  entropy            a=0.5179 b=0.5923 diff +0.0744 [+0.0605,+0.0911] z=  +9.5
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.1540 diff +0.1540 [+0.1182,+0.1904] z=  +8.5
      CONTENT  quantiles 50/90/99/99.9: a=[2.0000e-03 2.0070e+00 9.8960e+00 2.1154e+01] b=[2.0000e-03 3.2880e+00 1.3176e+01 2.3263e+01]
      outcome  mean bits          a=0.7948 b=1.0701 diff +0.2753 [+0.2388,+0.3159] z= +14.0
      outcome  capped@2           a=0.4396 b=0.5285 diff +0.0890 [+0.0784,+0.1007] z= +15.9
      outcome  capped@8           a=0.7615 b=0.9866 diff +0.2251 [+0.1974,+0.2553] z= +15.4
      outcome  mean p             a=0.7969 b=0.7548 diff -0.0422 [-0.0479,-0.0370] z= -15.9
      outcome  top1 hit(p>.5)     a=0.7867 b=0.7451 diff -0.0416 [-0.0477,-0.0360] z= -14.3
      outcome  bits @T*obs        a=0.7948 b=1.0264 diff +0.2315 [+0.2006,+0.2655] z= +14.0
      outcome  entropy            a=0.6717 b=0.7388 diff +0.0670 [+0.0529,+0.0818] z=  +9.5
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.1271 diff +0.1271 [+0.0853,+0.1698] z=  +5.9
      outcome  quantiles 50/90/99/99.9: a=[2.0000e-03 3.3250e+00 7.9050e+00 1.5707e+01] b=[3.0000e-03 3.5670e+00 1.0748e+01 2.0145e+01]
    |delta| concentration: top 1% tokens hold 27.1% of |delta|, top 5% 70.3%; net delta from top-1% |delta| tokens +36.9%, from the other 99% +63.1%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  61.2% a=0.003 b=0.192 diff +0.1898 [+0.1633,+0.2170] z=+13.6 | capped@8 diff +0.1512 z=+14.4
      ref bits in [0.01,0.1): tok  13.9% a=0.055 b=0.438 diff +0.3827 [+0.3364,+0.4360] z=+14.7 | capped@8 diff +0.3316 z=+15.3
      ref bits in [0.1,1): tok  10.2% a=0.419 b=0.938 diff +0.5187 [+0.4452,+0.6053] z=+12.5 | capped@8 diff +0.4728 z=+13.1
      ref bits in [1,4): tok   9.4% a=2.195 b=2.757 diff +0.5612 [+0.4938,+0.6387] z=+14.5 | capped@8 diff +0.4836 z=+14.6
      ref bits in [4,1000000000.0): tok   5.3% a=6.767 b=7.547 diff +0.7807 [+0.6192,+0.9575] z=+9.2 | capped@8 diff +0.2528 z=+3.9
  --- Qwen3-4B-Base -> Qwen3-4B   (total obs delta +74178 bits over 435322 tok)
    ws                               +0.0948 [+0.0799,+0.1106] z= +11.9  share of total delta   +4.8%  rel +42.9%
    boiler                           +0.8222 [+0.7874,+0.8590] z= +45.5  share of total delta  +16.2%  rel +34.9%
    prompt                           +0.0797 [+0.0700,+0.0904] z= +15.7  share of total delta   +6.6%  rel +110.8%
    cmd_echo                         +0.0557 [+0.0490,+0.0623] z= +16.4  share of total delta  +11.1%  rel +113.5%
    rand_hash                        +0.1710 [+0.1273,+0.2109] z=  +7.9  share of total delta   +2.4%  rel  +4.5%
    rand_time                        +0.1181 [+0.0963,+0.1404] z= +10.7  share of total delta   +1.7%  rel +15.6%
    rand_misc                        +0.1783 [+0.0857,+0.3059] z=  +3.2  share of total delta   +0.1%  rel  +9.8%
    err_line                         +0.3632 [+0.2933,+0.4652] z=  +8.4  share of total delta   +2.3%  rel +74.5%
    test_line                        +0.1480 [+0.1159,+0.2007] z=  +6.8  share of total delta   +1.3%  rel +75.9%
    number                           +0.2382 [+0.2037,+0.2760] z= +12.9  share of total delta   +8.7%  rel +40.0%
    path                             +0.2379 [+0.1955,+0.2904] z=  +9.8  share of total delta   +4.2%  rel +91.1%
    other                            +0.2989 [+0.2596,+0.3445] z= +13.7  share of total delta  +40.5%  rel +74.2%
    ALL obs                          +0.1704 [+0.1585,+0.1845] z= +25.4  share of total delta +100.0%  rel +44.5%
    novel                            +0.2759 [+0.2557,+0.2963] z= +26.2  share of total delta  +91.6%  rel +42.1%
    copy                             +0.0329 [+0.0293,+0.0371] z= +16.6  share of total delta   +8.4%  rel +116.1%
    first16                          +0.3538 [+0.3175,+0.3948] z= +17.6  share of total delta   +6.8%  rel +43.8%
    outstart4                        +0.7683 [+0.6731,+0.8702] z= +15.3  share of total delta   +6.9%  rel +64.1%
    rand(all 3)                      +0.1445 [+0.1184,+0.1695] z= +11.3  share of total delta   +4.2%  rel  +6.4%
    rand&novel                       +0.2325 [+0.2012,+0.2701] z= +13.2  share of total delta   +4.0%  rel  +6.1%
    CONTENT(novel output,non-rand)   +0.4571 [+0.4215,+0.4987] z= +22.8  share of total delta  +55.4%  rel +66.6%
    outcome-bearing                  +0.3955 [+0.3627,+0.4355] z= +20.7  share of total delta  +11.6%  rel +46.5%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3833 b=0.5537 diff +0.1704 [+0.1585,+0.1845] z= +25.4
      ALL obs  capped@2           a=0.1694 b=0.1675 diff -0.0018 [-0.0033,-0.0001] z=  -2.1
      ALL obs  capped@8           a=0.3436 b=0.4134 diff +0.0699 [+0.0633,+0.0771] z= +20.0
      ALL obs  mean p             a=0.9186 b=0.9198 diff +0.0013 [+0.0004,+0.0020] z=  +3.1
      ALL obs  top1 hit(p>.5)     a=0.9230 b=0.9195 diff -0.0036 [-0.0044,-0.0029] z=  -9.1
      ALL obs  bits @T*obs        a=0.3833 b=0.4807 diff +0.0974 [+0.0887,+0.1067] z= +20.8
      ALL obs  entropy            a=0.3673 b=0.2340 diff -0.1333 [-0.1469,-0.1213] z= -19.8
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.8201 diff +0.8201 [+0.8031,+0.8347] z=+100.3
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.362  8.221 15.892] b=[ 0.     0.195 13.345 26.435]
      CONTENT  mean bits          a=0.6869 b=1.1440 diff +0.4571 [+0.4215,+0.4987] z= +22.8
      CONTENT  capped@2           a=0.3189 b=0.3320 diff +0.0130 [+0.0074,+0.0199] z=  +4.0
      CONTENT  capped@8           a=0.6091 b=0.8249 diff +0.2158 [+0.1972,+0.2365] z= +21.7
      CONTENT  mean p             a=0.8485 b=0.8416 diff -0.0070 [-0.0102,-0.0043] z=  -4.7
      CONTENT  top1 hit(p>.5)     a=0.8531 b=0.8396 diff -0.0135 [-0.0167,-0.0108] z=  -9.0
      CONTENT  bits @T*obs        a=0.6869 b=0.9509 diff +0.2640 [+0.2414,+0.2906] z= +20.8
      CONTENT  entropy            a=0.5915 b=0.3665 diff -0.2251 [-0.2669,-0.1868] z= -10.9
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.6378 diff +0.6378 [+0.6038,+0.6699] z= +37.3
      CONTENT  quantiles 50/90/99/99.9: a=[3.0000e-03 2.4470e+00 1.0568e+01 2.0381e+01] b=[ 0.     3.46  18.225 32.531]
      outcome  mean bits          a=0.8504 b=1.2460 diff +0.3955 [+0.3627,+0.4355] z= +20.7
      outcome  capped@2           a=0.4690 b=0.4729 diff +0.0039 [-0.0023,+0.0097] z=  +1.3
      outcome  capped@8           a=0.8175 b=1.0272 diff +0.2097 [+0.1926,+0.2296] z= +21.8
      outcome  mean p             a=0.7838 b=0.7797 diff -0.0041 [-0.0066,-0.0015] z=  -3.0
      outcome  top1 hit(p>.5)     a=0.7728 b=0.7659 diff -0.0069 [-0.0103,-0.0032] z=  -3.8
      outcome  bits @T*obs        a=0.8504 b=1.0494 diff +0.1990 [+0.1801,+0.2222] z= +18.3
      outcome  entropy            a=0.7281 b=0.5496 diff -0.1785 [-0.1978,-0.1611] z= -18.8
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.6273 diff +0.6273 [+0.6000,+0.6507] z= +47.8
      outcome  quantiles 50/90/99/99.9: a=[3.0000e-03 3.3730e+00 8.0010e+00 1.5746e+01] b=[ 0.     3.781 15.519 27.501]
    |delta| concentration: top 1% tokens hold 44.6% of |delta|, top 5% 87.8%; net delta from top-1% |delta| tokens +64.9%, from the other 99% +35.1%
  --- Qwen3-4B-Base -> Qwen3-8B-Base   (total obs delta -10494 bits over 435322 tok)
    ws                               -0.0137 [-0.0183,-0.0092] z=  -5.8  share of total delta   +4.9%  rel  -6.2%
    boiler                           -0.0717 [-0.0806,-0.0628] z= -15.3  share of total delta  +10.0%  rel  -3.0%
    prompt                           -0.0164 [-0.0188,-0.0142] z= -14.5  share of total delta   +9.6%  rel -22.8%
    cmd_echo                         -0.0050 [-0.0064,-0.0037] z=  -7.2  share of total delta   +7.1%  rel -10.2%
    rand_hash                        -0.0460 [-0.1198,-0.0145] z=  -1.7  share of total delta   +4.6%  rel  -1.2%
    rand_time                        -0.0143 [-0.0203,-0.0092] z=  -5.0  share of total delta   +1.5%  rel  -1.9%
    rand_misc                        +0.0122 [-0.0508,+0.0708] z=  +0.4  share of total delta   -0.0%  rel  +0.7%
    err_line                         -0.0429 [-0.0634,-0.0242] z=  -4.3  share of total delta   +1.9%  rel  -8.8%
    test_line                        -0.0333 [-0.0545,-0.0181] z=  -3.6  share of total delta   +2.1%  rel -17.1%
    number                           -0.0312 [-0.0406,-0.0238] z=  -7.3  share of total delta   +8.1%  rel  -5.2%
    path                             -0.0229 [-0.0337,-0.0128] z=  -4.2  share of total delta   +2.9%  rel  -8.8%
    other                            -0.0495 [-0.0689,-0.0356] z=  -5.7  share of total delta  +47.5%  rel -12.3%
    ALL obs                          -0.0241 [-0.0299,-0.0196] z=  -9.1  share of total delta +100.0%  rel  -6.3%
    novel                            -0.0399 [-0.0492,-0.0322] z=  -9.1  share of total delta  +93.6%  rel  -6.1%
    copy                             -0.0036 [-0.0042,-0.0028] z=  -9.7  share of total delta   +6.4%  rel -12.6%
    first16                          -0.0444 [-0.0514,-0.0369] z= -11.8  share of total delta   +6.0%  rel  -5.5%
    outstart4                        -0.1011 [-0.1238,-0.0792] z=  -8.7  share of total delta   +6.4%  rel  -8.4%
    rand(all 3)                      -0.0293 [-0.0541,-0.0133] z=  -2.8  share of total delta   +6.0%  rel  -1.3%
    rand&novel                       -0.0486 [-0.0948,-0.0218] z=  -2.6  share of total delta   +5.9%  rel  -1.3%
    CONTENT(novel output,non-rand)   -0.0715 [-0.0918,-0.0548] z=  -7.5  share of total delta  +61.3%  rel -10.4%
    outcome-bearing                  -0.0556 [-0.0695,-0.0433] z=  -8.3  share of total delta  +11.6%  rel  -6.5%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.3833 b=0.3592 diff -0.0241 [-0.0299,-0.0196] z=  -9.1
      ALL obs  capped@2           a=0.1694 b=0.1598 diff -0.0095 [-0.0115,-0.0080] z= -10.2
      ALL obs  capped@8           a=0.3436 b=0.3231 diff -0.0204 [-0.0255,-0.0165] z=  -8.7
      ALL obs  mean p             a=0.9186 b=0.9232 diff +0.0047 [+0.0039,+0.0056] z= +10.6
      ALL obs  top1 hit(p>.5)     a=0.9230 b=0.9268 diff +0.0038 [+0.0029,+0.0049] z=  +7.0
      ALL obs  bits @T*obs        a=0.3833 b=0.3592 diff -0.0241 [-0.0299,-0.0196] z=  -9.1
      ALL obs  entropy            a=0.3673 b=0.3398 diff -0.0275 [-0.0335,-0.0232] z= -10.5
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=-0.0990 diff -0.0990 [-0.1221,-0.0743] z=  -8.0
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.362  8.221 15.892] b=[ 0.     0.27   7.929 15.381]
      CONTENT  mean bits          a=0.6869 b=0.6153 diff -0.0715 [-0.0918,-0.0548] z=  -7.5
      CONTENT  capped@2           a=0.3189 b=0.2895 diff -0.0294 [-0.0358,-0.0241] z=  -9.6
      CONTENT  capped@8           a=0.6091 b=0.5449 diff -0.0642 [-0.0813,-0.0496] z=  -7.7
      CONTENT  mean p             a=0.8485 b=0.8624 diff +0.0139 [+0.0114,+0.0169] z=  +9.5
      CONTENT  top1 hit(p>.5)     a=0.8531 b=0.8676 diff +0.0145 [+0.0114,+0.0182] z=  +8.4
      CONTENT  bits @T*obs        a=0.6869 b=0.6153 diff -0.0715 [-0.0918,-0.0548] z=  -7.5
      CONTENT  entropy            a=0.5915 b=0.5179 diff -0.0736 [-0.0936,-0.0581] z=  -7.9
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.0900 diff +0.0900 [+0.0645,+0.1146] z=  +6.8
      CONTENT  quantiles 50/90/99/99.9: a=[3.0000e-03 2.4470e+00 1.0568e+01 2.0381e+01] b=[2.0000e-03 2.0070e+00 9.8960e+00 2.1154e+01]
      outcome  mean bits          a=0.8504 b=0.7948 diff -0.0556 [-0.0695,-0.0433] z=  -8.3
      outcome  capped@2           a=0.4690 b=0.4396 diff -0.0294 [-0.0343,-0.0257] z= -13.7
      outcome  capped@8           a=0.8175 b=0.7615 diff -0.0560 [-0.0681,-0.0456] z=  -9.8
      outcome  mean p             a=0.7838 b=0.7969 diff +0.0131 [+0.0116,+0.0152] z= +14.6
      outcome  top1 hit(p>.5)     a=0.7728 b=0.7867 diff +0.0139 [+0.0112,+0.0169] z=  +9.2
      outcome  bits @T*obs        a=0.8504 b=0.7948 diff -0.0556 [-0.0695,-0.0433] z=  -8.3
      outcome  entropy            a=0.7281 b=0.6717 diff -0.0564 [-0.0643,-0.0496] z= -15.0
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.1147 diff +0.1147 [+0.0813,+0.1466] z=  +6.9
      outcome  quantiles 50/90/99/99.9: a=[3.0000e-03 3.3730e+00 8.0010e+00 1.5746e+01] b=[2.0000e-03 3.3250e+00 7.9050e+00 1.5707e+01]
    |delta| concentration: top 1% tokens hold 40.2% of |delta|, top 5% 83.1%; net delta from top-1% |delta| tokens +51.9%, from the other 99% +48.1%
  --- Qwen3-4B -> Qwen3-8B   (total obs delta -21834 bits over 435322 tok)
    ws                               -0.0104 [-0.0227,+0.0020] z=  -1.7  share of total delta   +1.8%  rel  -3.3%
    boiler                           +0.1161 [+0.0804,+0.1529] z=  +6.4  share of total delta   -7.8%  rel  +3.7%
    prompt                           -0.0402 [-0.0488,-0.0312] z=  -9.0  share of total delta  +11.3%  rel -26.5%
    cmd_echo                         -0.0150 [-0.0185,-0.0114] z=  -8.1  share of total delta  +10.1%  rel -14.3%
    rand_hash                        -0.0809 [-0.1315,-0.0501] z=  -3.8  share of total delta   +3.9%  rel  -2.0%
    rand_time                        -0.0192 [-0.0397,+0.0002] z=  -1.9  share of total delta   +1.0%  rel  -2.2%
    rand_misc                        +0.2619 [+0.1124,+0.4587] z=  +2.9  share of total delta   -0.3%  rel +13.2%
    err_line                         -0.0827 [-0.1532,-0.0178] z=  -2.4  share of total delta   +1.8%  rel  -9.7%
    test_line                        -0.0606 [-0.0936,-0.0340] z=  -3.9  share of total delta   +1.9%  rel -17.7%
    number                           -0.0863 [-0.1108,-0.0673] z=  -7.7  share of total delta  +10.7%  rel -10.4%
    path                             -0.0850 [-0.1135,-0.0577] z=  -5.9  share of total delta   +5.1%  rel -17.0%
    other                            -0.1312 [-0.1575,-0.1088] z= -10.1  share of total delta  +60.5%  rel -18.7%
    ALL obs                          -0.0502 [-0.0592,-0.0424] z= -11.8  share of total delta +100.0%  rel  -9.1%
    novel                            -0.0747 [-0.0894,-0.0618] z= -10.5  share of total delta  +84.3%  rel  -8.0%
    copy                             -0.0182 [-0.0214,-0.0149] z= -11.3  share of total delta  +15.7%  rel -29.7%
    first16                          +0.0620 [+0.0395,+0.0822] z=  +5.4  share of total delta   -4.0%  rel  +5.3%
    outstart4                        -0.2315 [-0.2926,-0.1676] z=  -7.1  share of total delta   +7.0%  rel -11.8%
    rand(all 3)                      -0.0456 [-0.0689,-0.0239] z=  -4.0  share of total delta   +4.5%  rel  -1.9%
    rand&novel                       -0.0628 [-0.0965,-0.0318] z=  -3.8  share of total delta   +3.7%  rel  -1.6%
    CONTENT(novel output,non-rand)   -0.1900 [-0.2186,-0.1659] z= -14.1  share of total delta  +78.2%  rel -16.6%
    outcome-bearing                  -0.1411 [-0.1762,-0.1102] z=  -8.3  share of total delta  +14.1%  rel -11.3%
    robust aggregations on ALL obs / CONTENT:
      ALL obs  mean bits          a=0.5537 b=0.5035 diff -0.0502 [-0.0592,-0.0424] z= -11.8
      ALL obs  capped@2           a=0.1675 b=0.1539 diff -0.0137 [-0.0157,-0.0121] z= -14.6
      ALL obs  capped@8           a=0.4134 b=0.3734 diff -0.0400 [-0.0463,-0.0350] z= -13.7
      ALL obs  mean p             a=0.9198 b=0.9267 diff +0.0068 [+0.0060,+0.0078] z= +15.3
      ALL obs  top1 hit(p>.5)     a=0.9195 b=0.9257 diff +0.0062 [+0.0054,+0.0073] z= +12.9
      ALL obs  bits @T*obs        a=0.4807 b=0.4355 diff -0.0452 [-0.0523,-0.0390] z= -13.3
      ALL obs  entropy            a=0.2340 b=0.2163 diff -0.0177 [-0.0215,-0.0142] z=  -9.5
      ALL obs  win(b<a)-win(a<b)  a=0.0000 b=0.0741 diff +0.0741 [+0.0595,+0.0883] z= +10.1
      ALL obs  quantiles 50/90/99/99.9: a=[ 0.     0.195 13.345 26.435] b=[ 0.     0.08  12.556 26.149]
      CONTENT  mean bits          a=1.1440 b=0.9539 diff -0.1900 [-0.2186,-0.1659] z= -14.1
      CONTENT  capped@2           a=0.3320 b=0.2923 diff -0.0397 [-0.0459,-0.0344] z= -13.4
      CONTENT  capped@8           a=0.8249 b=0.6959 diff -0.1289 [-0.1483,-0.1129] z= -13.8
      CONTENT  mean p             a=0.8416 b=0.8609 diff +0.0193 [+0.0168,+0.0223] z= +13.7
      CONTENT  top1 hit(p>.5)     a=0.8396 b=0.8589 diff +0.0193 [+0.0167,+0.0223] z= +13.1
      CONTENT  bits @T*obs        a=0.9509 b=0.7934 diff -0.1575 [-0.1821,-0.1369] z= -13.6
      CONTENT  entropy            a=0.3665 b=0.3279 diff -0.0385 [-0.0503,-0.0281] z=  -6.8
      CONTENT  win(b<a)-win(a<b)  a=0.0000 b=0.1514 diff +0.1514 [+0.1362,+0.1685] z= +18.1
      CONTENT  quantiles 50/90/99/99.9: a=[ 0.     3.46  18.225 32.531] b=[ 0.     3.049 16.952 33.317]
      outcome  mean bits          a=1.2460 b=1.1049 diff -0.1411 [-0.1762,-0.1102] z=  -8.3
      outcome  capped@2           a=0.4729 b=0.4388 diff -0.0341 [-0.0401,-0.0286] z= -11.7
      outcome  capped@8           a=1.0272 b=0.9157 diff -0.1115 [-0.1328,-0.0929] z= -11.3
      outcome  mean p             a=0.7797 b=0.7960 diff +0.0163 [+0.0139,+0.0189] z= +12.6
      outcome  top1 hit(p>.5)     a=0.7659 b=0.7843 diff +0.0184 [+0.0151,+0.0218] z= +10.8
      outcome  bits @T*obs        a=1.0494 b=0.9276 diff -0.1219 [-0.1454,-0.1015] z= -10.9
      outcome  entropy            a=0.5496 b=0.5208 diff -0.0288 [-0.0391,-0.0195] z=  -5.7
      outcome  win(b<a)-win(a<b)  a=0.0000 b=0.1163 diff +0.1163 [+0.0964,+0.1367] z= +11.1
      outcome  quantiles 50/90/99/99.9: a=[ 0.     3.781 15.519 27.501] b=[ 0.     3.511 14.968 28.923]
    |delta| concentration: top 1% tokens hold 43.9% of |delta|, top 5% 90.3%; net delta from top-1% |delta| tokens +58.6%, from the other 99% +41.4%
    stratified by reference surprisal (Qwen3-4B-Base), CONTENT tokens:
      ref bits in [0,0.01): tok  61.2% a=0.032 b=0.020 diff -0.0120 [-0.0180,-0.0067] z=-4.2 | capped@8 diff -0.0121 z=-6.0
      ref bits in [0.01,0.1): tok  13.9% a=0.288 b=0.158 diff -0.1307 [-0.1699,-0.0937] z=-6.7 | capped@8 diff -0.1135 z=-7.5
      ref bits in [0.1,1): tok  10.2% a=1.038 b=0.741 diff -0.2971 [-0.3672,-0.2326] z=-8.7 | capped@8 diff -0.2380 z=-9.4
      ref bits in [1,4): tok   9.4% a=3.727 b=3.130 diff -0.5973 [-0.6944,-0.5093] z=-12.3 | capped@8 diff -0.4855 z=-12.3
      ref bits in [4,1000000000.0): tok   5.3% a=11.905 b=10.426 diff -1.4788 [-1.6666,-1.3122] z=-16.3 | capped@8 diff -0.6763 z=-17.2
```
