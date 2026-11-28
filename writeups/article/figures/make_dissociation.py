"""figures/dissociation.png -- benchmark gain vs tool-output prediction gain.

From article/, run:  ../.venv/bin/python figures/make_dissociation.py

Reads only figures/dissociation_data.json (numbers copied from the study files
on the study host, with provenance in that JSON and in DISSOCIATION_NOTES.md), so the
figure is reproducible without access to the study host. Style matches make_cover.py:
white background, colour-blind-safe pair (validated with the dataviz palette
checker: #ad450b / #1a6bb0 pass lightness, chroma, CVD separation, contrast),
1600 px wide, large type readable on a phone.
"""

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parent
INK = "#16252d"
ORANGE = "#ad450b"   # sandbox binding test (validated pair with BLUE)
BLUE = "#1a6bb0"     # SWE tool-output metrics (snapped from the article #1c618c, which failed the chroma floor)
DPI = 100

DATA = json.loads((OUT / "dissociation_data.json").read_text())
SIZES = DATA["ladders"]["sizes"]
PARAMS = [DATA["non_embedding_params"][s] for s in SIZES]
LOG2P = np.log2(np.array(PARAMS, dtype=float))


def base_band():
    """The same-size Base model's level, as a size multiplier over each Instruct
    start: inverse-interpolate the Instruct ladder at the Base ladder value.
    Only the start sizes of the plotted models are used; where the Base value
    sits outside the Instruct ladder the result is a censored bound."""
    starts = {m["benchmark"]["start"].split("-")[-1] for m in DATA["plotted"]}
    out = []
    for key in ("sandbox_binding_acc_primary", "swe_m1_content_bits"):
        lad = DATA["ladders"][key]
        y = np.array(lad["inst"], dtype=float)
        if not lad["higher_is_better"]:
            y = -y  # invert so that larger = larger x
        for size, yb in zip(lad["base_sizes"], lad["base"]):
            if size not in starts:
                continue
            yb = yb if lad["higher_is_better"] else -yb
            censored = bool(yb > y[-1] or yb < y[0])  # outside the Instruct ladder -> a bound only
            xstar = np.interp(yb, y, LOG2P)  # y is monotone increasing in x; clamps at the ends
            log2n = xstar - LOG2P[SIZES.index(size)]
            out.append((key, size, 2 ** log2n, censored))
    return out


def render(filename, width, height):
    scale = width / 1600
    h = height / scale
    fig = plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI, facecolor="white")

    def pt(px):
        return px * scale * 72 / DPI

    def label(x, y, words, size, **options):
        fig.text(x / 1600, 1 - y / h, words, fontsize=pt(size), va="top",
                 color=options.pop("color", INK), **options)

    def rule(y):
        fig.add_artist(plt.Line2D([60 / 1600, 1540 / 1600], [1 - y / h] * 2,
                                  transform=fig.transFigure, color=INK,
                                  linewidth=pt(1.3), alpha=0.36))

    # ---- header ----------------------------------------------------------
    label(57, 36, "Agents got much better at solving.", 56, weight="bold")
    label(57, 103, "Not at predicting what comes back.", 56, weight="bold")
    label(61, 192, "Agentic post-training multiplies benchmark success 2–8×. Forecasting the tools' output moves", 27)
    label(61, 232, "0–1 doubling of model size — and never past the model's own pretrained base.", 27)
    rule(292)

    # ---- legend row ------------------------------------------------------
    ly = 322
    legend = [
        ("o", ORANGE, True, "Sandbox binding test (3,600 executed pairs)"),
        ("^", BLUE, True, "SWE tool-output bits (M1)"),
        ("D", BLUE, False, "SWE output given true action (M2)"),
    ]
    lx = 61
    for marker, color, filled, text in legend:
        fig.add_artist(Line2D([lx / 1600], [1 - (ly + 12) / h], transform=fig.transFigure,
                              marker=marker, markersize=pt(15),
                              markerfacecolor=color if filled else "white",
                              markeredgecolor=color, markeredgewidth=pt(1.8),
                              linestyle="none"))
        label(lx + 32, ly, text, 25)
        lx += 62 + int(len(text) * 13.2)

    # ---- axes ------------------------------------------------------------
    top, bottom, left, right = 386, h - 218, 218, 1548
    ax = fig.add_axes([left / 1600, 1 - bottom / h, (right - left) / 1600, (bottom - top) / h])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.22, 12.5)
    ax.set_ylim(0.6, 3.9)
    ax.spines[:].set_visible(False)
    ax.minorticks_off()
    ax.set_xticks([1.5, 2, 3, 5, 8], ["1.5×", "2×", "3×", "5×", "8×"])
    ax.set_yticks([0.7, 1, 1.5, 2, 3], ["0.7×", "1×", "1.5×", "2×", "3×"])
    ax.tick_params(length=0, labelsize=pt(25), colors=INK, pad=pt(11))

    band = base_band()
    blo, bhi = min(n for *_, n, _c in band), max(n for *_, n, _c in band)

    for y in (0.7, 1, 1.5, 2, 3):
        ax.axhline(y, color=INK, alpha=0.13, lw=pt(1), zorder=0)

    # base-model band and reference lines
    ax.axhspan(blo, bhi, color=INK, alpha=0.07, linewidth=0, zorder=1)
    ax.axhline(1, color=INK, alpha=0.55, lw=pt(1.6), ls=(0, (6, 4)), zorder=2)
    ax.axhline(2, color=INK, alpha=0.45, lw=pt(1.4), ls=(0, (2, 3)), zorder=2)
    ax.text(1.27, 0.965, "y = 1: no gain over the chat model", ha="left", va="top",
            fontsize=pt(22), color=INK)
    ax.text(12.2, 2.07, "2× = one size doubling of pretraining", ha="right", va="bottom",
            fontsize=pt(22), color=INK)
    ax.text(12.2, 2.52, "the same-size Base model sits at 2.0–2.8×", ha="right", va="center",
            fontsize=pt(22), color=INK)

    # ---- points ----------------------------------------------------------
    for m in DATA["plotted"]:
        x = m["benchmark"]["multiplier"]
        ys = [m["sandbox"].get("n"), m["swe_m1"].get("n"), m["swe_m2"].get("n")]
        ys = [v for v in ys if v]
        # light connector grouping the three measurements of one model
        ax.plot([x, x], [min(ys) * 0.97, max(ys) * 1.03], color=INK, alpha=0.22,
                lw=pt(1.6), zorder=2)

        # sandbox: filled circle (open + up-arrow when censored above 1)
        s = m["sandbox"]
        if s["censored"]:
            ax.plot([x], [1.03], marker="o", markersize=pt(15), markerfacecolor="white",
                    markeredgecolor=ORANGE, markeredgewidth=pt(2.4), zorder=5)
            ax.annotate("", xy=(x, 1.30), xytext=(x, 1.10),
                        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=pt(2.2)))
            ax.text(x * 1.02, 1.33, "> 1× (censored)", ha="left", va="bottom",
                    fontsize=pt(19), color=ORANGE)
        else:
            ax.errorbar([x], [s["n"]], yerr=[[s["n"] - s["ci"][0]], [s["ci"][1] - s["n"]]],
                        fmt="o", color=ORANGE, markersize=pt(15), markeredgecolor="white",
                        markeredgewidth=pt(1.5), elinewidth=pt(1.6), capsize=pt(5),
                        capthick=pt(1.6), alpha=0.95, zorder=5)

        # SWE M1: filled triangle; SWE M2: open diamond
        for key, marker, filled in (("swe_m1", "^", True), ("swe_m2", "D", False)):
            d = m[key]
            ax.errorbar([x], [d["n"]], yerr=[[d["n"] - d["ci"][0]], [d["ci"][1] - d["n"]]],
                        fmt=marker, color=BLUE,
                        markerfacecolor=BLUE if filled else "white",
                        markersize=pt(14), markeredgewidth=pt(1.9),
                        elinewidth=pt(1.5), capsize=pt(5), capthick=pt(1.5),
                        alpha=0.95, zorder=4)

    # ---- annotations -----------------------------------------------------
    def note(x, y, words, xytext, ha="left", color=INK):
        ax.annotate(words, xy=(x, y), xytext=xytext, ha=ha, va="center",
                    fontsize=pt(23), color=color,
                    arrowprops=dict(arrowstyle="-", color=color, lw=pt(1.5),
                                    alpha=0.7, shrinkA=pt(6), shrinkB=pt(9),
                                    connectionstyle="arc3,rad=0"))

    # per-model labels (placed near each model's sandbox marker)
    ax.text(1.66, 2.42, "tmax-sft-8b", fontsize=pt(23), color=INK, ha="left", va="center")
    ax.text(2.58, 1.62, "tmax-8b", fontsize=pt(23), color=INK, ha="left", va="center")
    ax.text(4.82, 2.46, "Nemotron-Terminal-14B", fontsize=pt(23), color=INK, ha="right", va="center")
    ax.text(5.52, 1.72, "Nemotron-Terminal-8B", fontsize=pt(23), color=INK, ha="left", va="center")

    note(8.13, 0.85, "Nemotron-Terminal-32B:\n8× on Terminal-Bench 2.0,\n0.8× at predicting tool output",
         xytext=(7.95, 1.40), ha="right", color=INK)
    note(2.425, 1.04, "tmax RL step: TB-Lite 11.5 → 17.7,\nforecasts flat (SWE 1.31 → 1.04×)",
         xytext=(1.32, 0.72), color=INK)

    # ---- axis captions and footer ---------------------------------------
    label(left + (right - left) / 2, bottom + 70,
          "Agentic benchmark gain: score ÷ its own paper's starting checkpoint (log scale)",
          25, ha="center")
    fig.text((left - 118) / 1600, 1 - (top + (bottom - top) / 2) / h,
             "Tool-output prediction gain: size-equivalent × vs its own Instruct start (log scale)",
             fontsize=pt(25), rotation=90, va="center", ha="center", color=INK)

    rule(h - 92)
    label(61, h - 74,
          "Qwen3 family · benchmark multipliers are within each paper's own harness — Terminal-Bench 2.0 (Terminus-2) for Nemotron-Terminal,",
          22)
    label(61, h - 42,
          "Terminal-Bench Lite for tmax; harnesses are never compared. Not plotted: CodeScout-14B, OpenThinker-Agent-v1, OpenThinkerAgent-32B — see DISSOCIATION_NOTES.md.",
          22)

    fig.savefig(OUT / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    for key, size, n, censored in base_band():
        bound = "> " if censored else ""
        print(f"base-model level: {key} / {size} start -> {bound}{n:.2f}x")
    render("dissociation.png", 1600, 1060)
    print("wrote", OUT / "dissociation.png")
