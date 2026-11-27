"""Markdown tables from results/summary.json -> results/tables.md"""
import json, os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze2 import GROUPS
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "results", "summary.json")))
DSN = {"tp": "Terminus (AgenticPPL)", "swe": "SWE-rebench 2026"}


def f(x, d=3):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{d}f}"


def fci(v, c, d=3):
    return f"{f(v, d)} [{f(c[0], d)},{f(c[1], d)}]" if c else f(v, d)


def ordered(ds):
    have = S["models"][ds]
    out = []
    for sz, g in GROUPS.items():
        for role, m in g.items():
            if m in have:
                out.append((sz, role, m))
    for m in sorted(have):
        if not any(m == x[2] for x in out):
            out.append(("8B", "LoRA/other", m))
    return out


BASES = {g.get("base") for g in GROUPS.values()}


def keep_pair(k):
    a = k.split(" vs ")[0]
    return a not in BASES


L = []
for ds in ["tp", "swe"]:
    M = S["models"][ds]; P = S["pairs"][ds]
    rows = ordered(ds)
    L.append(f"\n## {DSN[ds]}\n")
    L.append("### M1 recalibrated content code length (bits/token, eval split; T and histogram fitted per model on the calibration split)\n")
    L.append("| size | role | model | n content | raw | T* | @T* | rank×conf hist | top-1 rate | entropy | loss−entropy | outcome raw | outcome @T* | outcome hist | exec-content hist |")
    L.append("|" + "---|" * 15)
    for sz, role, m in rows:
        c, o, e = M[m]["m1"]["content"], M[m]["m1"]["outcome"], M[m]["m1"]["exec_content"]
        L.append(f"| {sz} | {role} | {m} | {c['n_tok']} | {f(c['bits'])} | {c['T']} | {f(c['bitsT'])} | {f(c['hist'])} | {f(c['top1hit'])} | {f(c['ent'])} | {f(c['gap'])} | {f(o['bits'])} | {f(o['bitsT'])} | {f(o['hist'])} | {f(e['hist'])} |")
    L.append("\n### M1 paired log2 ratio vs size-matched reference (negative = fewer bits than the reference; 95% trajectory bootstrap)\n")
    L.append("| comparison | content raw | content @T* | content hist | outcome @T* | outcome hist | exec-content hist |")
    L.append("|---|---|---|---|---|---|---|")
    for k, pr in [(k, v) for k, v in P.items() if keep_pair(k)]:
        g = lambda s: fci(pr[s]["log2ratio"], pr[s]["ci"]) if s in pr else "–"
        L.append(f"| {k} | {g('m1/content/bits')} | {g('m1/content/bitsT')} | {g('m1/content/hist')} | {g('m1/outcome/bitsT')} | {g('m1/outcome/hist')} | {g('m1/exec_content/hist')} |")
    L.append("\n### M2 action-conditional information gain = 1 − NLL(obs | true action) / NLL(obs | swapped action), content tokens\n")
    L.append("| size | role | model | n items | gain raw | gain @T* | gain outcome tokens | gain exec kinds | gain non-exec kinds | neg. control (swapA−swapB)/swap |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for sz, role, m in rows:
        d = M[m]["m2"]
        g = lambda k: fci(d[k]["gain"], d[k]["gain_ci"]) if k in d else "–"
        a = d.get("raw/content/all", {})
        L.append(f"| {sz} | {role} | {m} | {a.get('n_items','–')} | {g('raw/content/all')} | {g('T/content/all')} | {g('raw/outcome/all')} | {g('raw/content/exec')} | {g('raw/content/nonexec')} | {fci(a.get('control'), a.get('control_ci'))} |")
    L.append("\n### M3 outcome forced choice (true vs 3 foils differing only in the outcome span; LLR over the differing span)\n")
    L.append("| size | role | model | 4-way acc (n) | balanced | pairwise AUROC | LEAK acc (action+prev turn masked) | full−leak | AF subset acc full / leak (n) | err_class full/leak | number full/leak | first-pytest fail AUROC full / leak | bool False AUROC full / leak | grep no-hit AUROC full / leak |")
    L.append("|" + "---|" * 14)
    for sz, role, m in rows:
        d = M[m]["m3"]
        def a(k, key="acc"):
            return f(d[k][key]) if k in d else "–"
        n4 = d.get("full/4way", {}).get("n", "–")
        L.append(f"| {sz} | {role} | {m} | {fci(d['full/4way']['acc'], d['full/4way']['acc_ci']) if 'full/4way' in d else '–'} ({n4}) | {a('full/4way','acc_bal')} | {a('full/4way','auroc')} | "
                 f"{a('leak/4way')} | {fci(d['delta/4way']['acc'], d['delta/4way']['acc_ci']) if 'delta/4way' in d else '–'} | "
                 f"{a('full/4way_af')} / {a('leak/4way_af')} ({d.get('full/4way_af', {}).get('n', '–')}) | "
                 f"{a('full/err_class')}/{a('leak/err_class')} | {a('full/number')}/{a('leak/number')} | {a('full/pytest_first','auroc')} / {a('leak/pytest_first','auroc')} | "
                 f"{a('full/bool','auroc')} / {a('leak/bool','auroc')} | {a('full/grep','auroc')} / {a('leak/grep','auroc')} |")
    L.append("\n### M4 outcome probe (asked before the observation). n = native chat question, p = plain-text few-shot. Coverage = share with Yes+No mass ≥ 0.5; Platt fitted on cal; BSS vs logistic baseline (command type, previous error, kind); stacked = baseline features + model logit\n")
    L.append("| size | role | model | succ:n cov | succ:n AUROC | succ:n BSS | succ:n stacked BSS | succ:p cov | succ:p AUROC | succ:p BSS | succ:p stacked | tests:n AUROC/BSS | tests:p AUROC/BSS | err-class acc n / p (majority) |")
    L.append("|" + "---|" * 14)
    for sz, role, m in rows:
        d = M[m]["m4"]
        def q(k, key):
            return f(d[k].get(key), 2) if k in d else "–"
        def qc(k, key):
            return fci(d[k].get(key), d[k].get(key + "_ci"), 2) if k in d and key in d[k] else "–"
        L.append(f"| {sz} | {role} | {m} | {q('succ:n','coverage')} | {q('succ:n','auroc')} | {qc('succ:n','bss')} | {qc('succ:n','bss_stack')} | {q('succ:p','coverage')} | {q('succ:p','auroc')} | {qc('succ:p','bss')} | {qc('succ:p','bss_stack')} | "
                 f"{q('test:n','auroc')}/{q('test:n','bss')} | {q('test:p','auroc')}/{q('test:p','bss')} | {q('cls:n','acc_gated')} / {q('cls:p','acc_gated')} ({q('cls:p','acc_majority')}) |")
    L.append("\n### Paired differences (M2 gain, M3 accuracy) vs size-matched reference\n")
    L.append("| comparison | M2 gain raw | M2 gain @T* | M2 gain outcome | M3 4-way acc | M3 full−leak | M3 AF acc | M3 AF full−leak |")
    L.append("|---|---|---|---|---|---|---|---|")
    for k, pr in [(k, v) for k, v in P.items() if keep_pair(k)]:
        g = lambda s: fci(pr[s]["diff"], pr[s]["ci"]) if s in pr else "–"
        L.append(f"| {k} | {g('m2/raw/content/all')} | {g('m2/T/content/all')} | {g('m2/raw/outcome/all')} | {g('m3/full/4way')} | {g('m3/delta/4way')} | {g('m3/full/4way_af')} | {g('m3/delta/4way_af')} |")
open(os.path.join(HERE, "results", "tables.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
