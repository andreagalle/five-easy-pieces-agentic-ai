#!/usr/bin/env python3
"""Draw an article's charts from a recorded run.

    .venv/bin/python scripts/plots.py 01        (make plots-01)

Reads examples/NN-*/out/results.json and RUNINFO.json, left by `make run-NN` or `make compare-NN`,
and writes PNG figures to articles/NN-*/assets/, plus plots.json recording which run they come
from. No number in a figure is typed by hand (CLAUDE.md §3.2), and each figure says in its footer
which run it was drawn from.

Colours come from the illustration palette, checked with the dataviz validator on a white
surface (Medium): cerulean + coral pass every categorical check; the teal ramp passes the
ordinal checks; text uses plum-navy (15:1) and a secondary plum-grey (7:1).
Colour follows the agent in every figure: coral is the blind reflex agent, the one that loops;
cerulean is every agent that works.
"""

from __future__ import annotations

import hashlib
import json
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgb  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPO = "github.com/andreagalle/five-easy-pieces-agentic-ai"

SURFACE = "#FFFFFF"
TEXT = "#2B2238"  # plum-navy, 15.1:1 on white
TEXT_2 = "#5B5668"  # secondary text, 7.1:1
GRID = "#E6E4EA"  # hairline grid and axes
STONE = "#F1ECDF"  # a grid square, as in the illustrations
NEVER = "#E9E5DC"  # a square that was never cleaned
CERULEAN = "#2F80C0"
CORAL = "#E8574A"
RAMP = ["#84BFB8", "#5FA9A2", "#3E918B", "#2B7678", "#1F5C6B"]  # teal, light to dark
DPI = 200
WIDTH = 7.5  # inches: 1500 px

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "text.color": TEXT,
    "axes.labelcolor": TEXT_2,
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "xtick.color": TEXT_2,
    "ytick.color": TEXT_2,
    "xtick.major.size": 0,
    "ytick.major.size": 0,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


# ---------------------------------------------------------------- shared helpers

def load_run(piece: str) -> tuple[Path, dict, dict, str]:
    example = next(iter(sorted((ROOT / "examples").glob(f"{piece}-*"))), None)
    if example is None:
        sys.exit(f"plots: no examples/{piece}-* directory")
    out = example / "out"
    if not (out / "results.json").exists() or not (out / "RUNINFO.json").exists():
        sys.exit(f"plots: no recorded run in {out.relative_to(ROOT)}; run `make run-{piece}` or `make compare-{piece}` first")
    raw = (out / "results.json").read_bytes()
    runinfo = json.loads((out / "RUNINFO.json").read_text())
    if runinfo.get("git_dirty"):
        print("plots: warning: the run was made from a dirty working tree; redo it on a clean commit before publishing")
    return example, json.loads(raw), runinfo, hashlib.sha256(raw).hexdigest()


def footer(fig, runinfo: dict) -> None:
    note = (f"Data: {runinfo['tier']} sandbox run, {runinfo['timestamp_utc'][:10]}, "
            f"commit {runinfo['git_commit'][:7]}, sbx {runinfo['sbx_version']}  ·  {REPO}")
    fig.text(0.01, 0.012, note, fontsize=6.5, color=TEXT_2, ha="left", va="bottom")


def title(fig, text: str, subtitle: str | None = None) -> None:
    fig.text(0.01, 0.985, text, fontsize=12, weight="bold", ha="left", va="top")
    if subtitle:
        # Wrapped so it never runs off a 1500 px figure.
        fig.text(0.01, 0.935, textwrap.fill(subtitle, 110), fontsize=9, color=TEXT_2, ha="left", va="top",
                 linespacing=1.4)


def clean_axes(ax, keep=("bottom",)) -> None:
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


def cleaned_at(scenario: dict) -> dict[tuple[int, int], int]:
    """Step at which each initially dirty square was first cleaned (no dynamic dirt in piece 01)."""
    dirty = {tuple(sq) for sq in scenario["dirty_start"]}
    found = {}
    for t, (action, where) in enumerate(zip(scenario["actions"], scenario["path"]), 1):
        square = tuple(where)
        if action == "Suck" and square in dirty:
            found[square] = t
            dirty.discard(square)
    return found


def text_on(fill: str) -> str:
    r, g, b = to_rgb(fill)
    return "white" if 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.45 else TEXT


def save(fig, assets: Path, name: str, made: list) -> None:
    path = assets / name
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    made.append(path)


# ---------------------------------------------------------------- piece 01

COLORS_01 = {"sighted": CERULEAN, "blind": CORAL, "blind-random": CERULEAN,
             "grid-blind": CORAL, "grid-random": CERULEAN}
LABELS_01 = {"sighted": "With a location sensor", "blind": "Blind, same rules",
             "blind-random": "Blind, coin flip on clean squares",
             "grid-blind": "Blind, same rules", "grid-random": "Blind, random move on clean squares"}


def outcome(s: dict) -> str:
    if s["all_clean_at"]:
        return f"all clean at step {s['all_clean_at']} · score {s['score']}/{s['max_score']}"
    left = len(s["final_dirty"])
    return f"{left} square{'s' if left != 1 else ''} dirty forever · score {s['score']}/{s['max_score']}"


def fig_two_squares(scenarios: dict, runinfo: dict, assets: Path, made: list) -> None:
    names = ["sighted", "blind", "blind-random"]
    fig, axes = plt.subplots(3, 1, figsize=(WIDTH, 5.0), sharex=True)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.79, bottom=0.12, hspace=0.75)
    title(fig, "Two squares, ten steps: where the agent is",
          "The line is the agent's square after each step; a dot marks a Suck. Without a location sensor, "
          "the same rules leave the agent pushing against the wall.")
    for ax, name in zip(axes, names):
        s = scenarios[name]
        xs = list(range(0, len(s["path"]) + 1))
        ys = [s["start"][0]] + [p[0] for p in s["path"]]
        color = COLORS_01[name]
        ax.step(xs, ys, where="post", color=color, lw=2, solid_joinstyle="round", solid_capstyle="round")
        sucks = [t for t, a in enumerate(s["actions"], 1) if a == "Suck"]
        ax.plot(sucks, [ys[t] for t in sucks], "o", ms=7, color=color, mec=SURFACE, mew=2, zorder=3)
        ax.set_yticks([0, 1], ["A", "B"])
        ax.set_ylim(-0.45, 1.45)
        ax.set_xlim(0, xs[-1])
        ax.grid(axis="y", color=GRID, lw=0.8)
        clean_axes(ax, keep=())
        ax.set_title(f"{LABELS_01[name]}: {outcome(s)}", loc="left", fontsize=9, color=TEXT, pad=4)
    axes[-1].set_xlabel("time step")
    axes[-1].set_xticks(range(0, len(scenarios["sighted"]["path"]) + 1))
    footer(fig, runinfo)
    save(fig, assets, "fig-two-squares.png", made)


def draw_grid(ax, width: int, height: int, fill=lambda sq: STONE) -> None:
    for y in range(height):
        for x in range(width):
            ax.add_patch(FancyBboxPatch((x - 0.46, y - 0.46), 0.92, 0.92,
                                        boxstyle="round,pad=0,rounding_size=0.08",
                                        fc=fill((x, y)), ec="none", zorder=0))
    ax.set_xlim(-0.6, width - 0.4)
    ax.set_ylim(height - 0.4, -0.6)  # row 0 at the top
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    clean_axes(ax, keep=())


def fig_grid_paths(scenarios: dict, runinfo: dict, assets: Path, made: list) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 4.6))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.80, bottom=0.08, wspace=0.08)
    title(fig, "4×4 grid, no location sensor: where each agent went",
          "Darker lines are squares crossed more often. Dark specks are squares still dirty at the end.")
    for ax, name in zip(axes, ["grid-blind", "grid-random"]):
        s = scenarios[name]
        width, height = map(int, s["world"].split("x"))
        draw_grid(ax, width, height)
        color = COLORS_01[name]
        points = [tuple(s["start"])] + [tuple(p) for p in s["path"]]
        end = s["all_clean_at"] or len(s["path"])
        for (x0, y0), (x1, y1) in zip(points[:end], points[1:end + 1]):
            if (x0, y0) != (x1, y1):
                ax.plot([x0, x1], [y0, y1], color=color, lw=2.6, alpha=0.22 if name == "grid-random" else 0.9,
                        solid_capstyle="round", zorder=1)
        for sq in s["final_dirty"]:
            for dx, dy in ((-0.12, -0.08), (0.1, 0.05), (-0.02, 0.14)):
                ax.plot(sq[0] + dx, sq[1] + dy, "o", ms=2.6, color=TEXT, zorder=2)
        sx, sy = points[0]
        ax.plot(sx, sy, "o", ms=9, mfc=SURFACE, mec=color, mew=2, zorder=3)
        ax.annotate("start", (sx, sy), xytext=(0, 11), textcoords="offset points", ha="center", fontsize=8, color=TEXT_2)
        ex, ey = points[end]
        ax.plot(ex, ey, "o", ms=9, color=color, mec=SURFACE, mew=2, zorder=3)
        if s["all_clean_at"]:
            note = f"all clean at step {s['all_clean_at']}"
        else:
            stuck = sum(1 for p in reversed(points) if p == points[-1]) - 1
            note = f"stuck at the wall for {stuck} of {len(s['path'])} steps"
        # Right-aligned so the label stays inside its own panel.
        ax.annotate(note, (ex, ey), xytext=(8, -14), textcoords="offset points", ha="right", va="top",
                    fontsize=8, color=TEXT)
        ax.set_title(f"{LABELS_01[name]}\n{outcome(s)}", loc="left", fontsize=9, color=TEXT)
    footer(fig, runinfo)
    save(fig, assets, "fig-grid-paths.png", made)


def fig_grid_cleaned_at(scenarios: dict, runinfo: dict, assets: Path, made: list) -> None:
    names = ["grid-blind", "grid-random"]
    found = {n: cleaned_at(scenarios[n]) for n in names}
    vmax = max(max(f.values(), default=1) for f in found.values())
    norm = Normalize(vmin=1, vmax=vmax)
    cmap = LinearSegmentedColormap.from_list("teal", RAMP)
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 5.0))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.80, bottom=0.25, wspace=0.08)
    title(fig, "4×4 grid: the step at which each square was first cleaned",
          "Same colour scale in both panels. Grey squares were never cleaned in 200 steps.")
    for ax, name in zip(axes, names):
        s = scenarios[name]
        width, height = map(int, s["world"].split("x"))
        steps = found[name]

        def fill(sq, steps=steps):
            return matplotlib.colors.to_hex(cmap(norm(steps[sq]))) if sq in steps else NEVER

        draw_grid(ax, width, height, fill)
        for y in range(height):
            for x in range(width):
                if (x, y) in steps:
                    ax.text(x, y, str(steps[(x, y)]), ha="center", va="center", fontsize=10,
                            color=text_on(fill((x, y))))
                else:
                    ax.text(x, y, "never", ha="center", va="center", fontsize=8, color=TEXT_2)
        ax.set_title(f"{LABELS_01[name]}\n{len(steps)} of {width * height} squares cleaned",
                     loc="left", fontsize=9, color=TEXT)
    bar_ax = fig.add_axes([0.3, 0.15, 0.4, 0.022])
    bar = fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), cax=bar_ax, orientation="horizontal")
    bar.outline.set_visible(False)
    bar.set_label("time step of the first Suck on that square", fontsize=8, color=TEXT_2)
    footer(fig, runinfo)
    save(fig, assets, "fig-grid-cleaned-at.png", made)


def fig_grid_performance(scenarios: dict, runinfo: dict, assets: Path, made: list) -> None:
    names = ["grid-random", "grid-blind"]
    fig, ax = plt.subplots(figsize=(WIDTH, 4.2))
    fig.subplots_adjust(left=0.08, right=0.84, top=0.80, bottom=0.17)
    size = scenarios[names[0]]["max_score"] // len(scenarios[names[0]]["path"])
    title(fig, "AIMA's performance measure, step by step: clean squares on the 4×4 grid",
          "One point per clean square per time step, so each agent's score is the area under its line.")
    for name in names:
        s = scenarios[name]
        xs = list(range(0, len(s["clean"]) + 1))
        ys = [size - len(s["dirty_start"])] + s["clean"]
        color = COLORS_01[name]
        ax.plot(xs, ys, color=color, lw=2, solid_joinstyle="round", label=f"{LABELS_01[name]} (score {s['score']})")
        ax.annotate(f"{ys[-1]} clean", (xs[-1], ys[-1]), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=TEXT)
        if s["all_clean_at"]:
            t = s["all_clean_at"]
            ax.plot(t, ys[t], "o", ms=8, color=color, mec=SURFACE, mew=2, zorder=3)
            ax.annotate(f"all {size} clean at step {t}", (t, ys[t]), xytext=(0, 9), textcoords="offset points",
                        ha="center", fontsize=8, color=TEXT)
        else:
            t = next(i for i in range(len(ys)) if all(v == ys[-1] for v in ys[i:]))
            ax.plot(t, ys[t], "o", ms=8, color=color, mec=SURFACE, mew=2, zorder=3)
            # Below the line, where the other agent's line has already climbed away.
            ax.annotate(f"no change after step {t}", (t, ys[t]), xytext=(8, -10), textcoords="offset points",
                        ha="left", va="top", fontsize=8, color=TEXT)
    ax.set_xlim(0, len(scenarios[names[0]]["clean"]))
    ax.set_ylim(0, size + 1.5)
    ax.set_yticks(range(0, size + 1, 4))
    ax.grid(axis="y", color=GRID, lw=0.8)
    clean_axes(ax, keep=("bottom",))
    ax.set_xlabel("time step")
    ax.set_ylabel("clean squares")
    ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=TEXT)
    footer(fig, runinfo)
    save(fig, assets, "fig-grid-performance.png", made)


def plots_01(results: dict, runinfo: dict, assets: Path) -> list[Path]:
    scenarios = {s["name"]: s for s in results["scenarios"]}
    made: list[Path] = []
    fig_two_squares(scenarios, runinfo, assets, made)
    fig_grid_paths(scenarios, runinfo, assets, made)
    fig_grid_cleaned_at(scenarios, runinfo, assets, made)
    fig_grid_performance(scenarios, runinfo, assets, made)
    return made


PIECES = {"01": plots_01}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in PIECES:
        sys.exit(f"usage: scripts/plots.py {{{','.join(PIECES)}}}")
    piece = sys.argv[1]
    example, results, runinfo, digest = load_run(piece)
    assets = next(iter(sorted((ROOT / "articles").glob(f"{piece}-*")))) / "assets"
    made = PIECES[piece](results, runinfo, assets)
    provenance = {
        "piece": piece,
        "results": str((example / "out" / "results.json").relative_to(ROOT)),
        "results_sha256": digest,
        "run": {k: runinfo.get(k) for k in ("timestamp_utc", "tier", "sbx_version", "git_commit", "git_dirty", "python")},
        "matplotlib": matplotlib.__version__,
        "figures": [p.name for p in made],
    }
    (assets / "plots.json").write_text(json.dumps(provenance, indent=2) + "\n")
    for p in made:
        print(f"plots: wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
