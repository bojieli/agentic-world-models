"""Build every article figure from figure_data.json (+ dissociation_data.json).

Run:  ~/agentic-wm-review/.venv/bin/python ~/agentic-wm-review/article/figures/make_figures.py [name ...]

One visual system: Avenir Next, white surface, left-aligned headline + subtitle,
small grey footer. Colour roles (validated with the dataviz palette checker,
light mode, all-pairs: lightness, chroma, CVD >= 8.3, normal-vision >= 21.8):
  pretrained  #257de0 (blue)    chat model #f2a600 (amber)
  agent, supervised #008a17 (green)    agent, reinforcement learning #ec4647 (red)
  fine-tune not for agents: neutral grey #8c8c8c (the "other" slot, always labelled)
Every colour is backed by a direct text label, so identity is never colour alone.
"""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
from matplotlib.text import Text

HERE = Path(__file__).resolve().parent
D = json.loads((HERE / "figure_data.json").read_text())
DIS = json.loads((HERE / "dissociation_data.json").read_text())

import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore")
plt.rcParams.update({
    "font.family": ["Avenir Next", "Arial Unicode MS"],
    "axes.unicode_minus": True,
    "svg.fonttype": "none",
})
MONO = "Menlo"
DPI = 100
PT = 72 / DPI  # points per pixel

# ---- type scale (in px at 1600 px width) ----
TITLE_PX, SUB_PX, LABEL_PX, FOOT_PX = 56, 32, 31, 24

SURF, INK, INK2, GRID, AXIS = "#ffffff", "#191919", "#666666", "#e7e7e7", "#c2c2c2"
WASH = "#f3f3f3"
ROLE = {"pretrained": "#257de0", "chat": "#f2a600", "agent_sup": "#008a17",
        "agent_rl": "#ec4647", "nonagent": "#8c8c8c"}
ROLE_NAME = {"pretrained": "Pretrained", "chat": "Chat model",
             "agent_sup": "Agent (supervised training)",
             "agent_rl": "Agent (reinforcement learning)",
             "nonagent": "Fine-tune, not for agents"}


def mnum(v, d=1, plus=True):
    s = f"{abs(v):.{d}f}"
    if v < 0 and float(s) != 0:
        return "−" + s
    return ("+" if plus else "") + s


# --------------------------------------------------------------------------
class Canvas:
    """A figure with a full-size overlay axis in pixel coordinates (y down)."""

    def __init__(self, H, W=1600):
        self.W, self.H = W, H
        self.fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=SURF)
        ov = self.fig.add_axes([0, 0, 1, 1], zorder=10)
        ov.set_xlim(0, W); ov.set_ylim(H, 0); ov.axis("off"); ov.patch.set_alpha(0)
        self.ov = ov

    def t(self, x, y, s, px=LABEL_PX, color=INK, weight="regular", ha="left", va="top", family=None, small=False, **kw):
        if not small:
            px = max(px, 30 * self.W / 1600)  # phone-readable floor for every label
        kw2 = dict(fontsize=px * PT, color=color, weight=weight, ha=ha, va=va)
        if family:
            kw2["family"] = family
        kw2.update(kw)
        return self.ov.text(x, y, s, **kw2)

    def axes(self, left, top, w, h):
        return self.fig.add_axes([left / self.W, 1 - (top + h) / self.H, w / self.W, h / self.H])

    def d2p(self, ax, x, y):
        X, Y = ax.transData.transform((x, y))
        return X, self.H - Y

    def bottom(self, txt):
        r = self.fig.canvas.get_renderer()
        bb = txt.get_window_extent(r)
        return self.H - bb.y0

    def stack(self, x, y, items, gap=6, **common):
        """Place text blocks one under another; returns the bottom y (px)."""
        for s_, kw in items:
            k = dict(common); k.update(kw)
            y = self.bottom(self.t(x, y, s_, **k)) + gap
        return y

    def lines(self, x, y, text, px, lh=1.18, **kw):
        """Multi-line text with exact baseline spacing; y = top of the first line. Returns bottom y."""
        ls = text.split("\n")
        for i, line in enumerate(ls):
            self.t(x, y + px * 0.92 + i * px * lh, line, px=px, va="baseline", **kw)
        return y + px * 0.92 + (len(ls) - 1) * px * lh + px * 0.28

    def header(self, title, sub=None, x=60, y=46, tpx=TITLE_PX):
        yy = self.lines(x, y, title, tpx, lh=1.2, weight="demibold")
        if sub:
            yy = self.lines(x, yy + 20, sub, SUB_PX, lh=1.25, color=INK2)
        return yy

    def footer(self, s, x=60):
        tt = self.t(x, self.H - 28, s, px=FOOT_PX, color=INK2, linespacing=1.02, va="bottom", small=True)
        r = self.fig.canvas.get_renderer()
        top = self.H - tt.get_window_extent(r).y1
        self.ov.plot([x, self.W - 60], [top - 16, top - 16], color=GRID, lw=2)
        self.foot_top = top - 16

    def box(self, x, y, w, h, fc=SURF, ec=AXIS, lw=2, r=14, ls="-", z=1):
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                           fc=fc, ec=ec, lw=lw, ls=ls, zorder=z, mutation_aspect=1)
        self.ov.add_patch(p)
        return p

    def arrow(self, x0, y0, x1, y1, color=INK, lw=3, ms=28, ls="-", rad=0.0, style="-|>"):
        self.ov.annotate("", xy=(x1, y1), xytext=(x0, y0),
                         arrowprops=dict(arrowstyle=style, color=color, lw=lw, ls=ls,
                                         mutation_scale=ms, shrinkA=0, shrinkB=0,
                                         connectionstyle=f"arc3,rad={rad}"), zorder=5)

    def chip(self, x, yc, role, s=22):
        self.ov.add_patch(Rectangle((x, yc - s / 2), s, s, fc=ROLE[role], ec="none", zorder=6))

    def check(self, x, y, s=34, color=INK):
        self.ov.plot([x, x + s * .38, x + s], [y + s * .55, y + s * .9, y + s * .1], color=color, lw=6,
                     solid_capstyle="round", solid_joinstyle="round", zorder=6)

    def cross(self, x, y, s=30, color=INK):
        self.ov.plot([x, x + s], [y, y + s], color=color, lw=6, solid_capstyle="round", zorder=6)
        self.ov.plot([x, x + s], [y + s, y], color=color, lw=6, solid_capstyle="round", zorder=6)

    def save(self, name):
        qa(self.fig, name)
        self.fig.savefig(HERE / name, dpi=DPI, facecolor=SURF)
        plt.close(self.fig)
        from PIL import Image  # flatten to opaque RGB so X's dark theme never shows through
        Image.open(HERE / name).convert("RGB").save(HERE / name, optimize=True)
        print("wrote", name, f"{self.W}x{self.H}")


def style_ax(ax, grid_axis="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS); ax.spines[s].set_linewidth(1.5)
    ax.tick_params(colors=INK2, labelsize=LABEL_PX * PT * 0.92, length=0, pad=10)
    ax.set_facecolor("none")
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, lw=1.5)
        ax.set_axisbelow(True)


def qa(fig, name):
    """Report text that is clipped by the canvas or overlaps other text."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    items = []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        try:
            bb = t.get_window_extent(r)
        except Exception:
            continue
        if bb.width < 1:
            continue
        items.append((t.get_text().replace("\n", " ")[:40], bb))
        if bb.x0 < -1 or bb.x1 > W + 1 or bb.y0 < -1 or bb.y1 > H + 1:
            print(f"  [{name}] CLIPPED: {t.get_text()[:50]!r}")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            ox = min(a.x1, b.x1) - max(a.x0, b.x0)
            oy = min(a.y1, b.y1) - max(a.y0, b.y0)
            if ox > 3 and oy > 9:
                print(f"  [{name}] OVERLAP: {items[i][0]!r} <> {items[j][0]!r}")


SIZES = D["sizes"]
SX = {"0.6B": 0.6, "1.7B": 1.7, "4B": 4, "8B": 8, "14B": 14, "32B": 32}


# ==========================================================================
def cover(name, W, H):
    s = W / 1600
    c = Canvas(H, W)
    acc = D["matching_accuracy"]
    x0 = 64 * s
    tpx = 60 * s
    yb = c.lines(x0, 78 * s, "Pretraining builds\nthe world model\nof tool outputs.", tpx, lh=1.16, weight="demibold")
    c.lines(x0, yb + 30 * s, "Agentic post-training\ndoesn't.", tpx, lh=1.16, weight="demibold", color=INK2)
    c.lines(x0, H - 132 * s, "Qwen3 models: share of command\u2013output\npairs matched correctly (50% = guessing)",
            27 * s, lh=1.3, color=INK2)
    L, T, Wd, Ht = 800 * s, 64 * s, 740 * s, H - 150 * s
    ax = c.axes(L, T, Wd, Ht)
    style_ax(ax)
    xs = [SX[k] for k in SIZES[:5]]
    pre = [acc["pretrained"][k] for k in SIZES[:5]]
    cha = [acc["chat"][k] for k in SIZES[:5]]
    ax.fill_between(xs, cha, pre, color=ROLE["pretrained"], alpha=0.10, lw=0)
    for ys, role in ((pre, "pretrained"), (cha, "chat")):
        ax.plot(xs, ys, color=ROLE[role], lw=8 * s, solid_capstyle="round", zorder=3)
        ax.scatter(xs, ys, s=(18 * s) ** 2, color=ROLE[role], zorder=4, ec=SURF, lw=3 * s)
    ag = []
    for g in D["gains"]["groups"]:
        if not g["role"].startswith("agent"):
            continue
        for m in g["models"]:
            sz = "8B" if "8B" in m["name"] else ("14B" if "14B" in m["name"] else None)
            if sz:
                ag.append((sz, round(acc["chat"][sz] + m["vs_chat"], 1), g["role"], m["name"]))
    for sz, v, role, nm in ag:
        ax.scatter([SX[sz] * 1.16], [v], s=(15 * s) ** 2, color=ROLE[role], zorder=5, ec=SURF, lw=3 * s)
    ax.set_xscale("log")
    ax.set_xlim(0.5, 30)
    ax.set_ylim(59, 81.5)
    ax.set_xticks(xs); ax.set_xticklabels(SIZES[:5])
    ax.set_yticks([60, 70, 80]); ax.set_yticklabels(["60%", "70%", "80%"])
    ax.tick_params(labelsize=27 * s * PT)
    ax.minorticks_off()
    lp = 34 * s
    px, py = c.d2p(ax, 1.15, 70.0)
    c.t(px, py, "Pretrained", px=lp, weight="demibold", ha="center", va="bottom")
    px, py = c.d2p(ax, 1.15, 61.6)
    c.t(px, py, "Chat model", px=lp, weight="demibold", ha="left", va="top")
    px, py = c.d2p(ax, 4.6, 66.2)
    yb = c.lines(px, py, "Agents (built on\nthe chat model)", 30 * s, lh=1.12, weight="demibold")
    for i, role in enumerate(("agent_sup", "agent_rl")):
        yy = yb + 8 * s + i * 36 * s
        c.ov.add_patch(Circle((px + 10 * s, yy + 14 * s), 10 * s, fc=ROLE[role], ec="none", zorder=6))
        c.t(px + 30 * s, yy + 14 * s, ["supervised training", "reinforcement learning"][i], px=26 * s, va="center", color=INK2)
    x1, y1 = c.d2p(ax, 14 * 1.16, 78.7)
    c.lines(x1 - 26 * s, y1 - 58 * s, "best agent: only ties", 30 * s, color=INK, weight="medium", ha="right")
    c.save(name)


def cover52(name, W=2000, H=800):
    """X article cover, 5:2 (X's recommended header ratio). Minimal text so it reads at thumbnail size."""
    c = Canvas(H, W)
    acc = D["matching_accuracy"]
    x0 = 80
    yb = c.lines(x0, 92, "Pretraining builds the world\nmodel of tool outputs.", 70, lh=1.13, weight="demibold")
    yb = c.lines(x0, yb + 26, "Agentic post-training doesn't.", 70, weight="demibold", color=INK2)
    c.lines(x0, yb + 56, "None of 14 public agent and fine-tuned Qwen3\nmodels beat the pretrained model of its size\nat predicting what a command will print.",
            40, lh=1.3, color=INK2)
    c.t(x0, H - 62, "Chart: share of command\u2013output pairs matched correctly (50% = random guessing)",
        px=26, color=INK2, small=True)
    L, T, Wd, Ht = 1210, 70, 730, H - 170
    ax = c.axes(L, T, Wd, Ht)
    style_ax(ax)
    xs = [SX[k] for k in SIZES[:5]]
    pre = [acc["pretrained"][k] for k in SIZES[:5]]
    cha = [acc["chat"][k] for k in SIZES[:5]]
    ax.fill_between(xs, cha, pre, color=ROLE["pretrained"], alpha=0.10, lw=0)
    for ys, role in ((pre, "pretrained"), (cha, "chat")):
        ax.plot(xs, ys, color=ROLE[role], lw=8, solid_capstyle="round", zorder=3)
        ax.scatter(xs, ys, s=17 ** 2, color=ROLE[role], zorder=4, ec=SURF, lw=3)
    for g in D["gains"]["groups"]:
        if not g["role"].startswith("agent"):
            continue
        for m in g["models"]:
            sz = "8B" if "8B" in m["name"] else ("14B" if "14B" in m["name"] else None)
            if sz:
                v = round(acc["chat"][sz] + m["vs_chat"], 1)
                ax.scatter([SX[sz] * 1.17], [v], s=15 ** 2, color=ROLE[g["role"]], zorder=5, ec=SURF, lw=3)
    ax.set_xscale("log"); ax.set_xlim(0.5, 22); ax.set_ylim(59, 81.5)
    ax.set_xticks(xs); ax.set_xticklabels(SIZES[:5])
    ax.set_yticks([60, 70, 80]); ax.set_yticklabels(["60%", "70%", "80%"])
    ax.tick_params(labelsize=30 * PT); ax.minorticks_off()
    px, py = c.d2p(ax, 1.15, 70.3)
    c.t(px, py, "Pretrained", px=40, weight="demibold", ha="center", va="bottom", color=ROLE["pretrained"])
    px, py = c.d2p(ax, 0.8, 60.9)
    c.t(px, py, "Chat model", px=40, weight="demibold", ha="left", va="top", color=INK)
    px, py = c.d2p(ax, 2.55, 65.4)
    c.t(px, py, "Agents", px=38, weight="demibold", va="top")
    for i, role in enumerate(("agent_sup", "agent_rl")):
        yy = py + 50 + i * 46
        c.ov.add_patch(Circle((px + 12, yy + 20), 12, fc=ROLE[role], ec="none", zorder=6))
        c.t(px + 36, yy + 20, ["supervised training", "reinforcement learning"][i], px=38, va="center", color=INK2)
    x1, y1 = c.d2p(ax, 14 * 1.17, 78.7)
    c.t(x1 - 24, y1 - 30, "best agent only ties", px=38, color=INK, weight="medium", ha="right", va="bottom")
    c.save(name)

# ==========================================================================
def training_stages():
    c = Canvas(1120)
    st = D["training_stages_8b"]["stages"]
    y0 = c.header("Chat training costs accuracy.\nAgent training wins back only part of it.",
                  "How well Qwen3-8B matches commands to their outputs, at each stage of training")
    L, T, Wd, Ht = 150, y0 + 70, 1330, 1120 - y0 - 70 - 340
    ax = c.axes(L, T, Wd, Ht)
    style_ax(ax)
    xs = np.arange(4)
    vals = [s_["acc"] for s_ in st]
    ax.bar(xs, [v - 50 for v in vals], bottom=50, width=0.56, color=[ROLE[s_["key"]] for s_ in st], zorder=2)
    ax.set_ylim(50, 81); ax.set_xlim(-0.55, 3.75)
    ax.set_yticks([50, 60, 70, 80]); ax.set_yticklabels(["50%", "60%", "70%", "80%"])
    ax.set_xticks([])
    pre = vals[0]
    ax.axhline(pre, color=ROLE["pretrained"], lw=3, ls=(0, (6, 4)), zorder=3)
    px, py = c.d2p(ax, 3.75, pre)
    c.t(px, py - 10, "pretrained level", px=LABEL_PX, color=ROLE["pretrained"], ha="right", va="bottom", weight="demibold")
    for i, v in enumerate(vals):
        px, py = c.d2p(ax, i, v)
        c.t(px, py + 16, f"{v:.1f}%", px=40, weight="demibold", ha="center", va="top",
            color=INK if st[i]["key"] == "chat" else SURF)
    # step arrows between bars
    steps = [(0, 1, "−5.4", "chat training"), (1, 2, "+3.6", "agent training"), (2, 3, "−0.4", "reinforcement")]
    for a, b, lab, why in steps:
        xa, ya = c.d2p(ax, a + 0.3, vals[a] - 2.2 if a == 0 else vals[a] - 2.2)
        xb, yb = c.d2p(ax, b - 0.3, vals[b] - 2.2)
        c.arrow(xa + 6, ya + 40, xb - 6, yb + 40, color=INK2, lw=3, ms=26)
        c.t((xa + xb) / 2, max(ya, yb) + 66, lab, px=34, weight="demibold", ha="center", va="top", color=INK)
    # shortfall brackets
    for i in (2, 3):
        xq, yt = c.d2p(ax, i + 0.36, pre)
        _, yb = c.d2p(ax, i + 0.36, vals[i])
        c.ov.plot([xq, xq], [yt + 3, yb - 3], color=ROLE["pretrained"], lw=3)
        c.ov.plot([xq - 8, xq + 8], [yt + 3, yt + 3], color=ROLE["pretrained"], lw=3)
        c.ov.plot([xq - 8, xq + 8], [yb - 3, yb - 3], color=ROLE["pretrained"], lw=3)
    # stage labels under the bars
    names = [("Pretrained", "Qwen3-8B-Base"), ("Chat model", "Qwen3-8B"),
             ("Agent:\nsupervised\ntraining", "TMax-8B, step 1"),
             ("Agent: +\nreinforcement\nlearning", "TMax-8B, step 2")]
    for i, (n1, n2) in enumerate(names):
        px, py = c.d2p(ax, i, 50)
        c.stack(px, py + 20, [(n1, dict(weight="demibold")), (n2, dict(color=INK2))], gap=4,
                px=LABEL_PX, ha="center", linespacing=0.95)
    xq, yt = c.d2p(ax, 2.36, pre)
    c.t(xq + 0, yt - 52, "", px=LABEL_PX)
    _, yb2 = c.d2p(ax, 2.36, vals[2])
    c.t(xq + 14, (yt + yb2) / 2, "1.8 short", px=30, color=ROLE["pretrained"], weight="demibold", va="center")
    xq3, _ = c.d2p(ax, 3.36, pre)
    _, yb3 = c.d2p(ax, 3.36, vals[3])
    c.t(xq3 + 14, (yt + yb3) / 2, "2.2 short", px=30, color=ROLE["pretrained"], weight="demibold", va="center")
    c.footer("Matching accuracy on 3,600 command–output pairs; random guessing scores 50%. Changes are in percentage points.\n"
             "Agent stages: Ai2's TMax-8B, built on Qwen3-8B (step 1 supervised training, step 2 reinforcement learning).")
    c.save("training-stages.png")


# ==========================================================================
def what_we_measure():
    c = Canvas(1150)
    y0 = c.header("AgenticPPL scores the agent's next command.\nWe score the tool's reply, before it appears.",
                  "One step of an agent session, scored two ways (illustrative example)")
    bw, gap = 440, 80
    xs = [60, 60 + bw + gap, 60 + 2 * (bw + gap)]
    heads = ["Agent's command", "Tool's output", "Agent's next command"]
    lanes = [("AgenticPPL", "scores the next command, after the model has seen the output", 2),
             ("Our test", "scores the output itself, before the model has seen it", 1)]
    y = y0 + 40
    for li, (lname, ldesc, scored) in enumerate(lanes):
        tt = c.t(60, y, lname, px=38, weight="demibold")
        r_ = c.fig.canvas.get_renderer()
        c.t(tt.get_window_extent(r_).x1 + 16, y + 6, ldesc, px=LABEL_PX, color=INK2)
        by = y + 70
        bh = 250
        for k in range(3):
            hot = k == scored
            dim = (li == 1 and k == 2)
            c.box(xs[k], by, bw, bh, fc=WASH if hot else SURF, ec=INK if hot else AXIS, lw=5 if hot else 2)
            c.t(xs[k] + 24, by + 20, heads[k], px=LABEL_PX, weight="demibold", color=INK2 if dim else INK)
            if hot:
                c.box(xs[k] + bw - 150, by - 22, 130, 44, fc=INK, ec=INK, lw=0, r=22, z=3)
                c.t(xs[k] + bw - 85, by, "scored", px=26, color=SURF, ha="center", va="center", weight="demibold")
            if k < 2:
                c.arrow(xs[k] + bw + 10, by + bh / 2, xs[k + 1] - 10, by + bh / 2, color=INK2, lw=4, ms=30)
        mp = dict(family=MONO, px=LABEL_PX)
        c.t(xs[0] + 24, by + 90, "$ ls data/", **mp)
        if li == 0:
            c.t(xs[1] + 24, by + 80, "config.yaml", **mp)
            c.t(xs[1] + 24, by + 124, "results.csv", **mp, weight="bold")
            c.t(xs[1] + 24, by + 168, "train.py", **mp)
            c.t(xs[2] + 24, by + 90, "$ cat data/", **mp)
            c.ov.add_patch(Rectangle((xs[2] + 18, by + 130), 238, 46, fc="#d9d9d9", ec="none", zorder=2))
            c.t(xs[2] + 24, by + 134, "results.csv", **mp, weight="bold")
            c.t(xs[2] + 24, by + 190, "seen in the output", px=LABEL_PX, color=INK2)
            c.arrow(xs[1] + 250, by + 160, xs[2] + 14, by + 162, color=INK, lw=3, ms=24, rad=0.45, ls=(0, (4, 3)))
        else:
            for j in range(3):
                c.ov.add_patch(Rectangle((xs[1] + 24, by + 80 + 44 * j), 220 - 40 * j, 32,
                                         fc="#d9d9d9", ec="none", zorder=2))
                c.t(xs[1] + 24 + 230 - 40 * j, by + 80 + 44 * j - 2, "?", px=LABEL_PX, weight="bold", family=MONO)
            c.t(xs[1] + 24, by + 206, "which files will it list?", px=LABEL_PX, color=INK)
            c.t(xs[2] + 24, by + 90, "(not used)", px=LABEL_PX, color=INK2)
        y = by + bh + 60
    c.footer("AgenticPPL (Wenhao Chai) scores command words that a tool's output made easier to predict, such as a filename from a listing.\n"
             "Our test asks the step before that: can the model predict what the tool will print?")
    c.save("what-we-measure.png")


# ==========================================================================
def surprise_breakdown():
    c = Canvas(990)
    sb = D["surprise_breakdown_8b_pretrained"]
    y0 = c.header("Only about a third of the prediction error\non terminal output is predictable at all",
                  "Where the pretrained Qwen3-8B loses bits on terminal output, by kind of text")
    segs = sb["segments"]
    x0, x1 = 60, 1540
    tot = sum(s_["pct"] for s_ in segs)
    scale = (x1 - x0) / tot
    fills = {"content": ROLE["pretrained"], "random": "#a3a3a3", "boiler": "#bdbdbd", "echo": "#d4d4d4", "copied": "#e3e3e3"}
    by, bh = y0 + 150, 170
    # top brackets
    cx = x0
    pos = {}
    for s_ in segs:
        w = s_["pct"] * scale
        pos[s_["key"]] = (cx, cx + w)
        c.ov.add_patch(Rectangle((cx + 2, by), w - 4, bh, fc=fills[s_["key"]], ec="none", zorder=2))
        cx += w
    a, b = pos["content"]
    c.ov.plot([a + 2, a + 2, b - 4, b - 4], [by - 18, by - 34, by - 34, by - 18], color=INK, lw=3)
    c.t(a + 2, by - 46, "Predictable: 35%", px=36, weight="demibold", va="bottom")
    a2 = pos["random"][0]
    c.ov.plot([a2 + 4, a2 + 4, x1 - 2, x1 - 2], [by - 18, by - 34, by - 34, by - 18], color=INK2, lw=3)
    c.t(a2 + 4, by - 46, "Random, fixed or already seen: 65%", px=36, weight="demibold", color=INK2, va="bottom")
    # percentages inside
    for s_ in segs:
        a, b = pos[s_["key"]]
        if s_["pct"] < 5:
            continue
        col = SURF if s_["key"] == "content" else INK
        c.t((a + b) / 2, by + bh / 2, f"{s_['pct']:.0f}%", px=46, weight="demibold", color=col, ha="center", va="center")
    # sub-part of content
    oc = sb["content_outcome"]
    a, _ = pos["content"]
    w = oc["pct"] * scale
    c.ov.add_patch(Rectangle((a + 2, by + bh - 34), w - 4, 34, fc="#1b64be", ec="none", zorder=3))
    c.ov.plot([a + 4, a + 4], [by + bh, by + bh + 24], color=INK, lw=2)
    # labels below
    ly = by + bh + 30
    lab = {"content": ("Content a model could predict", "incl. 11%: test results,\nerror lines, numbers"),
           "random": ("Random strings", "hashes, timestamps"),
           "boiler": ("Fixed text from the", "evaluation framework")}
    for k, (l1, l2) in lab.items():
        a, b = pos[k]
        c.t(a + 6, ly, l1, px=LABEL_PX, weight="demibold")
        c.t(a + 6, ly + 40, l2, px=LABEL_PX, color=INK2, linespacing=1.02)
    a, b = pos["echo"]
    ex = (a + b) / 2
    c.ov.plot([ex, ex], [by + bh, ly + 168], color=INK2, lw=2)
    c.t(ex - 14, ly + 150, "11%  prompts, echoed commands, whitespace", px=LABEL_PX, ha="right", color=INK)
    a, b = pos["copied"]
    cx_ = (a + b) / 2
    c.ov.plot([cx_, cx_], [by + bh, ly + 224], color=INK2, lw=2)
    c.t(cx_ - 14, ly + 206, "1%  output copied from earlier", px=LABEL_PX, ha="right", color=INK)
    c.footer("Shares of all prediction error (bits) of pretrained Qwen3-8B on terminal output in recorded agent sessions (the AgenticPPL data).\n"
             "A model can predict an error message and still lose many bits on a random hash printed inside it.")
    c.save("surprise-breakdown.png")


# ==========================================================================
def recalibration():
    c = Canvas(1120)
    r = D["recalibration_8b"]
    y0 = c.header("Correct the chat model's overconfidence\nand the ranking flips",
                  "Error on the same terminal replies, bits per token (lower is better)")
    L, T, Wd, Ht = 470, y0 + 150, 640, 1120 - y0 - 150 - 200
    ax = c.axes(L, T, Wd, Ht)
    style_ax(ax)
    ax.set_xlim(-0.08, 1.08); ax.set_ylim(0.56, 1.13)
    ax.set_xticks([]); ax.set_yticks([0.6, 0.8, 1.0])
    ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", labelleft=False)
    for xv in (0, 1):
        ax.axvline(xv, color=AXIS, lw=1.5, zorder=1)
    ax.axhline(r["pretrained_reference"], color=ROLE["pretrained"], lw=3, ls=(0, (6, 4)), zorder=2)
    for key, role, nm in (("chat", "chat", "Chat model (Qwen3-8B)"), ("nemotron8b", "agent_sup", "Nemotron-Terminal-8B")):
        a, b = r[key]["as_is"], r[key]["temp_set"]
        ax.plot([0, 1], [a, b], color=ROLE[role], lw=7, solid_capstyle="round", zorder=3)
        ax.scatter([0, 1], [a, b], s=24 ** 2, color=ROLE[role], ec=SURF, lw=4, zorder=4)
        px, py = c.d2p(ax, 0, a)
        c.t(px - 30, py - 20, nm, px=LABEL_PX, weight="demibold", ha="right", va="center")
        c.t(px - 30, py + 18, f"{a:.3f}", px=LABEL_PX, color=INK2, ha="right", va="center")
        px, py = c.d2p(ax, 1, b)
        dy = 22 if key == "chat" else -22
        c.t(px + 30, py + dy, f"{b:.3f}  {'Chat model' if key == 'chat' else 'Nemotron-Terminal-8B'}",
            px=LABEL_PX, weight="demibold", va="center")
    px, py = c.d2p(ax, 1.08, r["pretrained_reference"])
    c.t(px + 10, py - 4, f"{r['pretrained_reference']:.3f}  Pretrained Qwen3-8B\n(no correction needed)", px=LABEL_PX,
        color=INK, va="center", linespacing=1.02)
    for xv, h, s_ in ((0, "As the models are", "Nemotron-Terminal looks better"), (1, "Temperature set on\nseparate sessions", "Chat model is better")):
        px, _ = c.d2p(ax, xv, 0)
        c.t(px, T - 30, h, px=LABEL_PX, weight="demibold", ha="center", va="bottom", linespacing=0.95)
        c.box(px - 260, T + Ht + 14, 520, 56, fc=WASH, ec="none", r=28)
        c.t(px, T + Ht + 42, s_, px=LABEL_PX, ha="center", va="center", weight="medium")
    c.footer("Content of terminal replies in recorded terminal sessions. Temperature makes a model's probabilities more or less spread out\n"
             "without changing which outcome it ranks first; each model's temperature was fitted on sessions it was not scored on.")
    c.save("recalibration.png")


# ==========================================================================
def pair():
    c = Canvas(1230)
    pe = D["pair_example"]
    y0 = c.header("The test: match each output to\nthe command that produced it",
                  "A real item. Both commands were actually run in an isolated container.")
    # program
    py0 = y0 + 40
    c.box(60, py0, 860, 230, fc="#202020", ec="#202020", r=16)
    c.t(90, py0 + 26, "$ cat calc.py", family=MONO, px=LABEL_PX, color="#bdbdbd")
    for i, line in enumerate(pe["program"]):
        c.t(90, py0 + 74 + 44 * i, line, family=MONO, px=LABEL_PX, color="#ffffff")
    c.t(960, py0 + 30, "The program reverses its\nargument, makes it uppercase\nand prints its length.",
        px=LABEL_PX + 2, linespacing=1.02)
    # panels
    ty = py0 + 290
    pw = 720
    for pi, (title, swapped) in enumerate((("Correct matching", False), ("Swapped matching", True))):
        x = 60 + pi * (pw + 40)
        c.box(x, ty, pw, 390, fc=WASH if not swapped else SURF, ec=INK if not swapped else AXIS, lw=4 if not swapped else 2)
        if swapped:
            c.cross(x + 28, ty + 28, s=30, color=INK2)
        else:
            c.check(x + 24, ty + 24, s=38)
        c.t(x + 78, ty + 24, title, px=36, weight="demibold", color=INK if not swapped else INK2)
        cmds = [pe["a"]["cmd"], pe["b"]["cmd"]]
        outs = [pe["a"]["out"], pe["b"]["out"]]
        rows = [ty + 120, ty + 260]
        for j in range(2):
            c.box(x + 20, rows[j], 404, 76, fc=SURF, ec=AXIS, r=10)
            c.t(x + 36, rows[j] + 38, cmds[j], family=MONO, px=30, va="center")
            c.box(x + pw - 196, rows[j], 176, 76, fc="#202020", ec="#202020", r=10)
            c.t(x + pw - 108, rows[j] + 38, outs[j], family=MONO, px=30, va="center", ha="center", color="#fff")
        for j in range(2):
            k = 1 - j if swapped else j
            c.arrow(x + 432, rows[j] + 38, x + pw - 206, rows[k] + 38, color=INK if not swapped else INK2,
                    lw=4, ms=26, ls="-" if not swapped else (0, (5, 4)))
    vy = ty + 430
    c.t(60, vy, "The model wins the item if it gives more probability to the correct matching\nthan to the swapped one. "
        "Random guessing scores 50%.", px=34, weight="demibold", linespacing=1.02)
    c.footer("3,600 pairs like this, in shell and Python, each changing either the command or an earlier step.\n"
             "Words that also appear earlier in the session are not scored, since a model could simply copy them.")
    c.save("pair.png")


# ==========================================================================
def scale_fig():
    c = Canvas(1120)
    acc = D["matching_accuracy"]; sw = D["coding_sessions_bits"]
    y0 = c.header("Bigger pretrained models predict tool outputs\nbetter, and beat their chat versions at every size")
    T = y0 + 120
    Ht = 1080 - T - 200
    axL = c.axes(150, T, 760, Ht)
    axR = c.axes(1090, T, 430, Ht)
    for ax in (axL, axR):
        style_ax(ax)
        ax.set_xscale("log"); ax.minorticks_off()
    c.t(60, T - 70, "Matching test: pairs matched (higher is better)", px=LABEL_PX, weight="demibold")
    c.t(1010, T - 70, "Real coding sessions: error", px=LABEL_PX, weight="demibold")
    c.t(1010, T - 34, "bits per token (lower is better)", px=LABEL_PX - 3, color=INK2) if False else None
    xsP = [SX[k] for k in SIZES[:5]]; xsC = [SX[k] for k in SIZES]
    pre = [acc["pretrained"][k] for k in SIZES[:5]]; cha = [acc["chat"][k] for k in SIZES]
    axL.fill_between(xsP, cha[:5], pre, color=ROLE["pretrained"], alpha=0.10, lw=0)
    for xs, ys, role in ((xsP, pre, "pretrained"), (xsC, cha, "chat")):
        axL.plot(xs, ys, color=ROLE[role], lw=6, zorder=3, solid_capstyle="round")
        axL.scatter(xs, ys, s=18 ** 2, color=ROLE[role], ec=SURF, lw=3, zorder=4)
    axL.set_xlim(0.45, 45); axL.set_ylim(58, 82.5)
    axL.set_xticks(xsC); axL.set_xticklabels(SIZES)
    axL.set_yticks([60, 65, 70, 75, 80]); axL.set_yticklabels([f"{v}%" for v in (60, 65, 70, 75, 80)])
    # labels
    px, py = c.d2p(axL, 2.3, 73.6); c.t(px, py, "Pretrained", px=LABEL_PX + 2, weight="demibold", ha="right", va="bottom")
    px, py = c.d2p(axL, 11, 71.0); c.t(px, py, "Chat model", px=LABEL_PX + 2, weight="demibold", ha="left", va="top")
    # 4B pretrained ~ 14B chat
    xa, ya = c.d2p(axL, 4, 75.7); xb, yb = c.d2p(axL, 14, 75.3)
    c.ov.plot([xa + 16, xb - 16], [ya, yb], color=INK, lw=3, ls=(0, (2, 3)), zorder=6)
    tx, ty = c.d2p(axL, 0.5, 82.3)
    yb_ = c.lines(tx + 20, ty, "pretrained 4B \u2248 chat 14B", LABEL_PX, weight="demibold")
    c.lines(tx + 20, yb_ + 2, "75.7% vs 75.3%", LABEL_PX, color=INK2)
    mx, my = c.d2p(axL, 6.0, 75.55)
    c.ov.plot([tx + 150, mx], [yb_ + 44, my - 6], color=INK, lw=2)
    px, py = c.d2p(axL, 8.0, 62.3)
    c.t(px, py, "shaded gap: lost in chat training", px=30, color=ROLE["pretrained"], weight="demibold", ha="center", va="center")
    # right panel (inverted: up = better)
    pB = [sw["pretrained"][k] for k in SIZES[:5]]; cB = [sw["chat"][k] for k in SIZES]
    for xs, ys, role in ((xsP, pB, "pretrained"), (xsC, cB, "chat")):
        axR.plot(xs, ys, color=ROLE[role], lw=6, zorder=3)
        axR.scatter(xs, ys, s=16 ** 2, color=ROLE[role], ec=SURF, lw=3, zorder=4)
    axR.set_ylim(1.95, 0.9); axR.set_xlim(0.45, 45)
    axR.set_xticks([0.6, 4, 32]); axR.set_xticklabels(["0.6B", "4B", "32B"])
    axR.set_yticks([1.8, 1.4, 1.0]); axR.set_yticklabels(["1.8", "1.4", "1.0"])
    c.t(1010, T - 34, "bits per token, lower is better", px=26, color=INK2)
    for xv, yv, role in ((14, 0.987, "pretrained"), (32, 1.016, "chat")):
        px, py = c.d2p(axR, xv, yv)
        c.ov.add_patch(Circle((px, py), 22, fc="none", ec=INK, lw=3, zorder=12))
    tx, ty = c.d2p(axR, 3.2, 1.55)
    c.lines(tx, ty, "pretrained 14B\n(0.987) beats\nchat 32B (1.016)", 29, lh=1.15, weight="demibold")
    c.t(tx, ty + 112, "(circled)", px=26, color=INK2)
    c.footer("Qwen3 models. Matching test: 3,600 command\u2013output pairs, random guessing 50%. Coding sessions: 150 successful\n"
             "SWE-rebench runs; copyable text and fixed boilerplate ignored, temperature set on separate tasks. No pretrained 32B exists.")
    c.save("scale.png")


# ==========================================================================
def gains():
    G = D["gains"]
    rows = []
    for g in G["groups"]:
        rows.append(("head", g))
        for m in g["models"]:
            rows.append(("row", g["role"], m))
    rh, hh = 60, 66
    y0_guess = 300
    H = y0_guess + 110 + sum(rh if r[0] == "row" else hh for r in rows) + 60 + 110
    c = Canvas(H)
    y0 = c.header("Agent training wins back about one size doubling,\nbut never beats the pretrained model",
                  "Change in matching accuracy, percentage points")
    T = y0 + 110
    total = sum(rh if r[0] == "row" else hh for r in rows)
    lp = (520, 520); rp = (1100, 440)
    axL = c.axes(lp[0], T, lp[1], total); axR = c.axes(rp[0], T, rp[1], total)
    for ax in (axL, axR):
        style_ax(ax, grid_axis="x")
        ax.set_ylim(total, 0); ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    axL.set_xlim(-4.5, 5.2); axR.set_xlim(-10, 2.5)
    axL.set_xticks([-4, 0, 4]); axL.set_xticklabels(["−4", "0", "+4"])
    axR.set_xticks([-8, -4, 0]); axR.set_xticklabels(["−8", "−4", "0"])
    band = G["doubling_band"]
    axL.axvspan(band["lo"], band["hi"], color="#e3e3e3", zorder=0, lw=0)
    axL.axvline(0, color=ROLE["chat"], lw=4, zorder=1)
    axR.axvline(0, color=ROLE["pretrained"], lw=4, zorder=1)
    c.t(lp[0], T - 82, "vs its chat starting point", px=LABEL_PX, weight="demibold")
    c.t(rp[0], T - 82, "vs pretrained, same size", px=LABEL_PX, weight="demibold")
    px, _ = c.d2p(axL, (band["lo"] + band["hi"]) / 2, 0)
    c.t(px, T + 14, "one size doubling", px=30, color=INK2, ha="center", va="top")
    y = 0
    for r in rows:
        if r[0] == "head":
            g = r[1]
            yy = T + y + hh - 18
            c.chip(60, yy - 2, g["role"], s=26)
            c.t(98, yy, g["label"], px=LABEL_PX, weight="demibold", va="center")
            y += hh
            continue
        _, role, m = r
        yc = y + rh / 2
        col = ROLE[role]
        for ax, v in ((axL, m["vs_chat"]), (axR, m["vs_pre"])):
            if v is None:
                continue
            solid = m["sig"] if ax is axL else True
            ax.barh(yc, v, height=rh * 0.62, color=col if solid else SURF, ec=col, lw=3, zorder=3)
        px, py = c.d2p(axL, 0, yc)
        c.t(98, py, m["name"], px=LABEL_PX, va="center")
        v = m["vs_chat"]
        px, py = c.d2p(axL, v, yc)
        c.t(px + (12 if v >= 0 else -12), py, mnum(v), px=LABEL_PX - 2, ha="left" if v >= 0 else "right", va="center",
            color=INK if m["sig"] else INK2)
        if m["vs_pre"] is None:
            px, py = c.d2p(axR, -9.7, yc)
            c.t(px, py, "no pretrained 32B", px=26, color=INK2, va="center", style="italic")
        else:
            v = m["vs_pre"]
            if "vs_pre_range" in m:
                lo, hi = m["vs_pre_range"]
                axR.plot([lo, hi], [yc, yc], color=INK, lw=3, zorder=4)
                for e in (lo, hi):
                    axR.plot([e, e], [yc - 10, yc + 10], color=INK, lw=3, zorder=4)
                px, py = c.d2p(axR, lo, yc)
                c.t(px - 12, py, "+0.3, a tie", px=LABEL_PX - 2, ha="right", va="center", weight="demibold")
            else:
                px, py = c.d2p(axR, v, yc)
                c.t(px - 12, py, mnum(v), px=LABEL_PX - 2, ha="right", va="center")
        y += rh
    c.footer("Outlined bars: change within noise (95% range includes zero). Grey band: gain from doubling a chat model's size\n"
             "(8B\u219214B +3.6, 14B\u219232B +4.0). Nemotron-Terminal-14B vs pretrained 14B: +0.3, 95% range \u22121.1 to +1.9.\n"
             "Klear-8B was trained from the pretrained 8B model.")
    c.save("gains.png")


# ==========================================================================
def margin():
    M = D["margin"]["rows"]
    c = Canvas(1500)
    y0 = c.header("More pairs right, by smaller margins",
                  "Matching accuracy counts wins. The margin measures how decisively the model wins.")
    # explainer
    ey = y0 + 40
    for i, (ttl, a, b, note) in enumerate((("Close win", 0.56, 0.50, "small margin"), ("Clear win", 0.78, 0.38, "large margin"))):
        x = 60 + i * 750
        c.box(x, ey, 710, 330, fc=WASH, ec="none")
        c.t(x + 28, ey + 22, ttl, px=34, weight="demibold")
        c.t(x + 682, ey + 26, "counts as 1 win", px=30, color=INK2, ha="right")
        bx0, bscale = x + 300, 380 / 0.8
        for j, (lab, v, col) in enumerate((("correct matching", a, INK), ("swapped matching", b, "#a3a3a3"))):
            yy = ey + 100 + j * 80
            c.t(x + 28, yy + 22, lab, px=30, va="center", color=INK if j == 0 else INK2)
            c.ov.add_patch(Rectangle((bx0, yy), bscale * v, 44, fc=col, ec="none", zorder=3))
        xa = bx0 + bscale * b; xb = bx0 + bscale * a
        c.ov.plot([xa, xa], [ey + 180, ey + 236], color=INK, lw=2, ls=(0, (3, 3)))
        c.ov.plot([xa, xb], [ey + 250, ey + 250], color=INK, lw=3)
        for e in (xa, xb):
            c.ov.plot([e, e], [ey + 240, ey + 260], color=INK, lw=3)
        c.t(xb, ey + 270, note, px=30, weight="demibold", ha="right")
    c.t(60, ey + 352, "Bar length: probability the model gives each matching (schematic).", px=30, color=INK2)
    # data
    dy = ey + 430
    c.t(60, dy, "The five agents that improved accuracy all won by less", px=36, weight="demibold")
    T = dy + 160
    rh = 100
    ax = c.axes(560, T, 680, rh * len(M))
    style_ax(ax, grid_axis="x")
    ax.set_ylim(len(M) - 0.5, -0.5); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlim(0.36, 0.73); ax.set_xticks([0.4, 0.5, 0.6, 0.7])
    c.t(560, T - 96, "Margin, bits per byte of output", px=LABEL_PX, weight="demibold")
    c.t(1340, T - 96, "Accuracy", px=LABEL_PX, weight="demibold")
    c.t(60, T - 96, "Agent", px=LABEL_PX, weight="demibold")
    for i, m in enumerate(M):
        ax.annotate("", xy=(m["agent"] + 0.004, i), xytext=(m["chat"] - 0.008, i),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=3, mutation_scale=26, shrinkA=0, shrinkB=0))
        ax.scatter([m["chat"]], [i], s=24 ** 2, color=ROLE["chat"], ec=SURF, lw=3, zorder=4)
        ax.scatter([m["agent"]], [i], s=24 ** 2, color=ROLE[m["role"]], ec=SURF, lw=3, zorder=4)
        px, py = c.d2p(ax, 0, i)
        c.chip(60, py, m["role"])
        c.t(96, py, m["name"], px=LABEL_PX, va="center")
        px, py = c.d2p(ax, m["agent"], i)
        c.t(px - 22, py, f"{m['agent']:.3f}", px=LABEL_PX - 2, ha="right", va="center", weight="demibold")
        px, py = c.d2p(ax, m["chat"], i)
        c.t(px + 22, py, f"{m['chat']:.3f}", px=LABEL_PX - 2, ha="left", va="center", color=INK2)
        c.t(1340, py, f"{mnum(m['acc_gain'])} points", px=LABEL_PX, va="center")
    px, py = c.d2p(ax, M[0]["chat"], 0)
    c.t(px + 22, py - 48, "chat start", px=24, color=INK2, va="center")
    px, py = c.d2p(ax, M[0]["agent"], 0)
    c.t(px - 22, py - 48, "agent", px=24, color=INK2, ha="right", va="center")
    c.footer("Margin: how much more probability, in bits per byte of output, the model gives the correct matching than the swapped one.\n"
             "Starting points: Qwen3-8B 0.540, Qwen3-14B 0.693, Qwen3-32B 0.669. Accuracy: change in matching accuracy vs the same chat model.")
    c.save("margin.png")


# ==========================================================================
def base_level():
    """Same-size pretrained model's level as a chat-model size multiple (method of make_dissociation.py)."""
    sizes = DIS["ladders"]["sizes"]
    log2p = np.log2(np.array([DIS["non_embedding_params"][s] for s in sizes], dtype=float))
    out = {}
    for key, short in (("sandbox_binding_acc_primary", "matching"), ("swe_m1_content_bits", "coding")):
        lad = DIS["ladders"][key]
        y = np.array(lad["inst"], dtype=float)
        sgn = 1 if lad["higher_is_better"] else -1
        y = sgn * y
        for size, yb in zip(lad["base_sizes"], lad["base"]):
            yb = sgn * yb
            cens = bool(yb > y[-1])
            n = 2 ** (np.interp(yb, y, log2p) - log2p[sizes.index(size)])
            out[(short, size)] = (float(n), cens)
    return out


def dissociation():
    P = DIS["plotted"]
    lv = base_level()
    names = {"tmax-sft-8b": "TMax-8B (supervised)", "tmax-8b": "TMax-8B (reinforcement)"}
    roles = {"tmax-8b": "agent_rl"}
    bh, gap = 52, 44
    gsz = 3 * bh + gap
    H = 470 + gsz * len(P) + 290
    c = Canvas(H)
    y0 = c.header("Agent benchmark scores multiplied 1.6–8×.\nPrediction gained one size doubling at most.",
                  "Each agent compared with its own chat starting point, as a multiple")
    FILL = {"bench": "#3d3d3d", "match": "#a3a3a3", "code": SURF}
    # key
    ky = y0 + 34
    keys = [("bench", "agent benchmark score"), ("match", "prediction: matching test"), ("code", "prediction: real coding sessions")]
    kx = [60, 560, 1060]
    for (k, lab), x in zip(keys, kx):
        c.ov.add_patch(Rectangle((x, ky + 4), 44, 30, fc=FILL[k], ec="#3d3d3d" if k == "code" else "none", lw=2.5, zorder=3))
        c.t(x + 56, ky + 19, lab, px=30, va="center")
    c.ov.plot([66, 66], [ky + 60, ky + 98], color=ROLE["pretrained"], lw=6)
    c.t(84, ky + 79, "pretrained model of the same size, on the same prediction scale", px=30, va="center")
    T = ky + 200
    L, Wd = 470, 1040
    Ht = gsz * len(P)
    ax = c.axes(L, T, Wd, Ht)
    style_ax(ax, grid_axis="x")
    ax.set_xscale("log"); ax.minorticks_off()
    ax.set_xlim(0.6, 10.5); ax.set_ylim(Ht, 0)
    ax.set_xticks([1, 2, 4, 8]); ax.set_xticklabels(["1\u00d7", "2\u00d7", "4\u00d7", "8\u00d7"])
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.axvline(1, color=INK, lw=2.5, zorder=2)
    ax.axvspan(1.92, 2.08, color="#e3e3e3", lw=0, zorder=0)
    px, _ = c.d2p(ax, 2, 0)
    c.t(px, T - 12, "one doubling of\nmodel size", px=30, color=INK2, ha="center", va="bottom", linespacing=0.95)
    px, _ = c.d2p(ax, 1, 0)
    c.t(px, T - 12, "no change", px=30, color=INK2, ha="center", va="bottom")
    y = 0
    for gi, m in enumerate(P):
        role = roles.get(m["model"], "agent_sup")
        nm = names.get(m["model"], m["label"])
        b = m["benchmark"]
        size = b["start"].split("-")[-1]
        _, py = c.d2p(ax, 1, y + 4)
        c.chip(60, py + 18, role, s=24)
        yb = c.lines(96, py, nm, LABEL_PX, weight="demibold")
        yb = c.lines(96, yb + 4, b["name"], 30, color=INK2)
        c.lines(96, yb + 2, f"{b['start_score']:g} \u2192 {b['tuned_score']:g}", 30, color=INK2)
        bars = [("bench", b["multiplier"], False), ("match", m["sandbox"]["n"], m["sandbox"]["censored"]),
                ("code", m["swe_m1"]["n"], False)]
        for k, (key, v, cens) in enumerate(bars):
            yc = y + k * bh + bh / 2
            if cens:
                px, py = c.d2p(ax, 1, yc)
                c.t(px + 14, py, "above 1\u00d7 (no larger chat model to size it against)", px=30, va="center", color=INK2)
                continue
            ax.barh(yc, v - 1, left=1, height=bh * 0.74, color=FILL[key], ec="#3d3d3d" if key == "code" else "none",
                    lw=2.5, zorder=3)
            txt = f"{v:.1f}\u00d7" if key == "bench" else f"{v:.2f}\u00d7"
            px, py = c.d2p(ax, max(v, 1), yc)
            extra = ""
            if key == "match" and size == "14B":
                extra = "  (pretrained 1.95\u00d7: a tie)"
            c.t(px + 14, py, txt + extra, px=30, va="center", weight="demibold" if key == "bench" else "regular")
            if key in ("match", "code"):
                rec = lv.get(("matching" if key == "match" else "coding", size))
                if rec:
                    n, cen = rec
                    xa, ya = c.d2p(ax, n, yc)
                    c.ov.plot([xa, xa], [ya - bh * 0.46, ya + bh * 0.46], color=ROLE["pretrained"], lw=6,
                              solid_capstyle="butt", zorder=12)
                    if cen:
                        c.arrow(xa, ya, xa + 40, ya, color=ROLE["pretrained"], lw=3, ms=20)
        y += gsz
    c.footer("Benchmark multiples are within each team's own setup (Terminal-Bench 2.0 for Nemotron-Terminal, Terminal-Bench Lite\n"
             "for TMax) and are not comparable across teams. Prediction multiples: how much bigger a chat model would need to be to match.\n"
             "Blue arrow: pretrained level lies beyond the largest chat model. No pretrained 32B exists. Models without a published\n"
             "starting-model benchmark score are not shown.")
    c.save("dissociation.png")


# ==========================================================================
def chat():
    R = D["chat_format"]["rows"]
    A = D["chat_format"]["absolute_8b"]
    rh = 92
    c = Canvas(300 + 150 + rh * len(R) + 320 + 130)
    y0 = c.header("In chat format, the agents' advantage reverses",
                  "Change in matching accuracy vs the chat starting point, percentage points")
    T = y0 + 150
    L = 560
    ax = c.axes(L, T, 960, rh * len(R))
    style_ax(ax, grid_axis="x")
    ax.set_ylim(len(R) - 0.5, -0.5); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlim(-11.5, 5); ax.set_xticks([-10, -5, 0, 5]); ax.set_xticklabels(["−10", "−5", "0", "+5"])
    ax.axvline(0, color=ROLE["chat"], lw=4, zorder=1)
    px, _ = c.d2p(ax, 0, 0)
    c.t(px - 16, T - 70, "\u2190 worse than the chat model", px=30, color=INK2, ha="right", va="bottom")
    c.t(px + 16, T - 70, "better \u2192", px=30, color=INK2, ha="left", va="bottom")
    for i, r in enumerate(R):
        col = ROLE[r["role"]]
        ax.annotate("", xy=(r["chat"] + 0.25, i), xytext=(r["raw"] - 0.25, i),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=3, mutation_scale=26, shrinkA=0, shrinkB=0), zorder=2)
        ax.scatter([r["raw"]], [i], s=24 ** 2, color=col, ec=SURF, lw=3, zorder=4)
        ax.scatter([r["chat"]], [i], s=24 ** 2, color=SURF, ec=col, lw=5, zorder=4)
        px, py = c.d2p(ax, 0, i)
        c.chip(60, py, r["role"])
        c.t(96, py, r["name"], px=LABEL_PX, va="center")
        px, py = c.d2p(ax, r["raw"], i)
        c.t(px + 24, py, mnum(r["raw"]), px=LABEL_PX - 2, va="center", weight="demibold")
        px, py = c.d2p(ax, r["chat"], i)
        c.t(px - 24, py, mnum(r["chat"]) + (" (tie)" if not r["chat_sig"] else ""), px=LABEL_PX - 2, ha="right",
            va="center", weight="demibold")
    px, py = c.d2p(ax, R[0]["raw"], 0)
    c.t(px, py - 30, "raw transcript", px=24, color=INK2, ha="center", va="bottom")
    px, py = c.d2p(ax, R[0]["chat"], 0)
    c.t(px, py - 30, "chat format", px=24, color=INK2, ha="center", va="bottom")
    # callout: absolute 8B numbers
    by = T + rh * len(R) + 90
    c.box(60, by, 1480, 300, fc=WASH, ec="none")
    c.t(90, by + 24, "At 8B, matching accuracy", px=LABEL_PX + 2, weight="demibold")
    c.t(840, by + 24, "raw transcript", px=26, color=INK2, ha="center")
    c.t(1180, by + 24, "chat format", px=26, color=INK2, ha="center")
    rolemap = ["chat", "agent_sup", "agent_sup"]
    for j, a in enumerate(A):
        yy = by + 110 + j * 72
        c.chip(90, yy, rolemap[j])
        c.t(126, yy, a["name"], px=LABEL_PX, va="center")
        c.t(840, yy, f"{a['raw']:.1f}%", px=LABEL_PX, va="center", ha="center")
        c.arrow(920, yy, 1090, yy, color=INK2, lw=3, ms=24)
        c.t(1180, yy, f"{a['chat']:.1f}%", px=LABEL_PX, va="center", ha="center", weight="demibold")
    c.footer("Same files, commands and outputs; only the wrapping changes: a raw shell transcript, or the model's chat format\n"
             "asking for the exact output. Filled dot: raw transcript; open dot: chat format. Light-IF-14B had no agent training.")
    c.save("chat.png")


# ==========================================================================
def roles():
    R = D["roles"]["rows"]
    rh = 64
    groups = [("Supervised on full agent sessions", R[:4]), ("Other fine-tunes: no such shift", R[4:])]
    body = sum(70 + rh * len(g[1]) for g in groups)
    c = Canvas(300 + 360 + 60 + body + 150)
    y0 = c.header("Supervised agent training teaches the agent's lines,\nnot the terminal's replies",
                  "Change in probability given to each part of the same recorded sessions vs the chat starting point")
    # session strip
    sy = y0 + 40
    parts = [("Agent's reasoning", "The test fails. Check\nwhat the parser returns.", "reason"),
             ("Agent's command", "$ pytest -q", "cmd"),
             ("Terminal's reply", "1 failed, 14 passed", "reply")]
    bw = [560, 380, 460]
    x = 60
    centers = []
    for (lab, txt, kind), w in zip(parts, bw):
        fc = {"reason": SURF, "cmd": WASH, "reply": "#202020"}[kind]
        c.box(x, sy + 50, w, 150, fc=fc, ec=AXIS if kind != "reply" else "#202020", lw=2)
        c.t(x + 4, sy, lab, px=LABEL_PX, weight="demibold")
        c.t(x + 24, sy + 125, txt, px=LABEL_PX, va="center", color="#ffffff" if kind == "reply" else INK,
            family=MONO if kind != "reason" else None, style="italic" if kind == "reason" else "normal", linespacing=1.02)
        centers.append(x + w / 2)
        x += w + 40
    c.t(60, sy + 220, "Illustrative example. Every model scores the same recorded sessions.",
        px=24, color=INK2)
    # small multiples
    T = sy + 330
    cols = [("reasoning", "Reasoning"), ("commands", "Commands"), ("replies", "Terminal's replies")]
    cw, cg, cx0 = 300, 40, 560
    axs = []
    for k, (key, lab) in enumerate(cols):
        ax = c.axes(cx0 + k * (cw + cg), T + 60, cw, body)
        style_ax(ax, grid_axis=None)
        ax.set_xlim(-0.5, 1.0); ax.set_ylim(body, 0); ax.set_yticks([]); ax.set_xticks([])
        for sname in ("left", "bottom"):
            ax.spines[sname].set_visible(False)
        ax.axvline(0, color=ROLE["chat"], lw=3, zorder=1)
        c.t(cx0 + k * (cw + cg) + cw / 3, T, lab, px=LABEL_PX, weight="demibold", ha="center")
        axs.append(ax)
    y = 0
    for gname, rows_ in groups:
        _, py = c.d2p(axs[0], 0, y + 40)
        c.t(60, py, gname, px=LABEL_PX, weight="demibold", va="center", color=INK2)
        y += 70
        for r in rows_:
            yc = y + rh / 2
            _, py = c.d2p(axs[0], 0, yc)
            c.chip(60, py, r["role"])
            c.t(96, py, r["name"], px=LABEL_PX, va="center")
            for ax, (key, _) in zip(axs, cols):
                v = r[key]
                ax.barh(yc, v, height=rh * 0.62, color=ROLE[r["role"]], zorder=3)
                px, py = c.d2p(ax, v, yc)
                c.t(px + (10 if v >= 0 else -10), py, mnum(v, 2), px=26, ha="left" if v >= 0 else "right", va="center",
                    weight="demibold" if abs(v) >= 0.15 else "regular", color=INK if abs(v) >= 0.15 else INK2)
            y += rh
    _, py = c.d2p(axs[0], 0, body)
    c.footer("Bits per token; positive = more probability than the chat model it started from (orange line). Terminal replies\n"
             "mix copied and new text: Nemotron-Terminal-8B lost probability on both (\u22120.57 copied, \u22120.20 new).\n"
             "Arctic-AWM-8B and CodeScout-14B: agents trained mainly with reinforcement learning. Light-IF-8B: no agent training.")
    c.save("roles.png")


FIGS = {
    "cover": lambda: (cover52("cover.png", 2000, 800), cover("cover_2x1.png", 1200, 600)),
    "training-stages": training_stages, "what-we-measure": what_we_measure,
    "surprise-breakdown": surprise_breakdown, "recalibration": recalibration, "pair": pair,
    "scale": scale_fig, "gains": gains, "margin": margin, "dissociation": dissociation,
    "chat": chat, "roles": roles,
}

if __name__ == "__main__":
    for k in (sys.argv[1:] or FIGS):
        FIGS[k]()
