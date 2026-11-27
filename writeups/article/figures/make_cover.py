"""Run python writeups/article/figures/make_cover.py from the repository root."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import ScaledTranslation

OUT = Path(__file__).resolve().parent
INK = "#16252d"
BLUE = "#1c618c"
ORANGE = "#ad450b"
DPI = 100

# article/FACTS.md, experiment 1, plain sandbox transcripts. Accuracy in %.
SIZE = np.array([0.6, 1.7, 4, 8, 14, 32])
BASE = [63.6, 68.6, 75.7, 77.1, 78.4]
INSTRUCT = [60.4, 64.6, 68.7, 71.7, 75.3, 79.3]
# Each entry is (model, gain from same-size Instruct, horizontal dodge in px).
# The dodge separates overlapping markers within a size group.
AGENTS = {
    8: [("Nemotron", 3.1, -16), ("tmax", 3.2, 0), ("tmax-sft", 3.6, 16),
        ("SERA", 1.4, 0), ("Arctic", -0.2, 0)],
    14: [("Nemotron", 3.4, 0), ("CodeScout", -0.2, -8), ("FrogMini", 0.6, 8)],
    32: [("Nemotron", 2.9, 0), ("OpenThinkerAgent", -0.5, 0)],
}


def render(filename, width, height):
    # Work in a 1600-wide design space, adjusting plot height for the card.
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

    label(57, 36, "Pretraining builds the world model", 56, weight="bold")
    label(57, 103, "of tool outputs. Agentic post-training doesn't.", 56, weight="bold")
    label(61, 195, "On the sandbox test, the strongest agent gains matched roughly one doubling in model size.", 29)
    rule(257)
    label(60, 283, "Commands matched to the correct output", 29, weight="bold")

    label(848, 286, "◆", 24, color=ORANGE)
    label(884, 286, "Agent fine-tunes", 24)
    fig.add_artist(plt.Rectangle((1121 / 1600, 1 - 309 / h), 29 / 1600, 17 / h,
                                 transform=fig.transFigure, color=BLUE, alpha=0.20, lw=0))
    label(1161, 286, "Gain from doubling Instruct size", 23)

    top, bottom = 334, h - 150
    ax = fig.add_axes([130 / 1600, 1 - bottom / h, 1385 / 1600, (bottom - top) / h])
    ax.set_xscale("log")
    ax.set_xlim(0.55, 36)
    ax.set_ylim(59, 84.2)
    ax.spines[:].set_visible(False)
    ax.minorticks_off()
    ax.set_yticks([60, 70, 80], ["60%", "70%", "80%"])
    ax.set_xticks(SIZE, [f"{s:g}B" for s in SIZE])
    ax.tick_params(length=0, labelsize=pt(25), colors=INK, pad=pt(11))
    for y in (60, 70, 80):
        ax.axhline(y, color=INK, alpha=0.15, lw=pt(1), zorder=0)

    # Band from Instruct at x to Instruct at 2x, interpolating in log size.
    # It ends at 16B since the final measured Instruct checkpoint is 32B.
    x = np.unique(np.r_[SIZE, SIZE / 2])
    x = x[(x >= SIZE[0]) & (2 * x <= SIZE[-1])]

    def instruct_at(s):
        return np.interp(np.log(s), np.log(SIZE), INSTRUCT)

    ax.fill_between(x, instruct_at(x), instruct_at(2 * x), color=BLUE,
                    alpha=0.20, linewidth=0, zorder=1)
    for sizes, values, color in [(SIZE[:-1], BASE, INK), (SIZE, INSTRUCT, BLUE)]:
        ax.plot(sizes, values, color=color, solid_capstyle="round", lw=pt(5.5),
                marker="o", markersize=pt(12), markeredgewidth=0, zorder=2)
    for size, checkpoints in AGENTS.items():
        for _, gain, offset in checkpoints:
            shifted = ax.transData + ScaledTranslation(offset * scale / DPI, 0, fig.dpi_scale_trans)
            ax.plot(size, instruct_at(size) + gain, transform=shifted, marker="D",
                    markersize=pt(12), markerfacecolor=ORANGE, markeredgecolor="white",
                    markeredgewidth=pt(1.4), zorder=4)

    def chart_label(x, y, words, color):
        ax.text(x, y, words, color=color, size=pt(27), weight="bold")

    chart_label(2.15, 76.3, "Qwen3 Base", INK)
    chart_label(2.65, 63.7, "Qwen3 Instruct", BLUE)
    ax.annotate("14B agent tied its base", xy=(14, 78.7), xytext=(11.8, 82.4),
                ha="right", va="center", fontsize=pt(25), color=ORANGE, weight="bold",
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=pt(1.6),
                                connectionstyle="angle,angleA=0,angleB=75,rad=0",
                                shrinkA=pt(7), shrinkB=pt(10)))
    label(800, bottom + 49, "Model parameters (log scale)", 24, ha="center")
    rule(h - 63)
    label(61, h - 45, "Qwen3 · 3,600 executed command/output pairs · 14 public agent fine-tunes", 24)
    fig.savefig(OUT / filename, dpi=DPI, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render("cover.png", 1600, 900)
    render("cover_2x1.png", 1200, 600)
