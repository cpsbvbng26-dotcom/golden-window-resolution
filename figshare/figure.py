"""The Figure item: survivor sets and dimension across the golden window 1/phi < delta < 2/3.

Panel (a). For each of COLUMNS values of delta, the survivor set
    K_delta = {y in [0, 1) : T_beta^n(y) <= t(beta) for all n >= 0},  beta = 1/delta,  t(beta) = (2 - beta)/(beta - 1),
of the greedy beta-transformation with the hole (t(beta), 1), drawn as a union of intervals.
K_delta = delta * S with S the survivor set of the game recursion of Section 2 of the paper; the recursion
below is that of scripts/curve/membership.py (game_survives) and of the proof of Theorem 3.1.
A piece is a parameter interval I on which T^n is affine of slope beta^n onto an image [0, b]; every piece
contains a point of K_delta (its left end, which is mapped to the fixed point 0). Pieces are split until
their length in y is below EPS. Pieces whose gap is below EPS are then joined. So every point of K_delta lies
on a drawn segment, and every point of a drawn segment lies within 1.5 * EPS of a point of K_delta.

Panel (b). dim_H K_delta = h(delta)/log beta from the renewal equation of Theorem 3.2, computed with the
forced path and the bisection of scripts/curve/gw.py. The seven values of Table 5 are read from
expected/edges/examples.out and drawn as points; the script asserts that the curve agrees with them.

matplotlib output is made reproducible: no dates, fixed SVG hash salt, Type 42 fonts in the PDF.
The PNG (400 dpi) is the PDF rasterized by pdftoppm.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "curve"))

COLUMNS = 480
EPS = 1 / 2000
PATH_STEPS = 800


def survivor_segments(d):
    """Segments in y = delta * x covering K_delta (see the module docstring). d is a float."""
    X = (2 * d - 1) / (d * (1 - d))
    beta = 1 / d
    dX = d * X
    pieces = []
    stack = [(0.0, X, 0)]
    while stack:
        lo, b, n = stack.pop()
        dn = d ** n
        length = b * dn * d
        if length < EPS:
            pieces.append((d * lo, d * lo + length))
            continue
        stack.append((lo, beta * min(b, dX), n + 1))           # L-branch: [0, b] cap [0, dX]
        if b >= 1:
            stack.append((lo + dn, beta * (b - 1), n + 1))     # R-branch: [1, b]
    pieces.sort()
    merged = []
    for a, b in pieces:
        if merged and a - merged[-1][1] < EPS:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


def table5():
    out = []
    with open(os.path.join(ROOT, "expected", "edges", "examples.out"), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"  delta ([\d.]+): gap, renewal ([\d.]+),", line)
            if m:
                out.append((float(m.group(1)), float(m.group(2))))
    return out


def dimension_curve(deltas):
    from mpmath import mp, mpf, log
    from gw import path, zroot
    mp.dps = 30
    out = []
    for d in deltas:
        dm = mpf(d)
        A, _, _, _ = path(dm, PATH_STEPS)
        z = zroot(A, it=80)
        out.append(float(log(z) / log(dm)))
    return out


def build(outdir):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams.update({
        "svg.hashsalt": "golden-window", "svg.fonttype": "path", "pdf.fonttype": 42,
        "font.family": "DejaVu Sans", "font.size": 9, "axes.linewidth": 0.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "path.simplify": False,
    })
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.collections import PolyCollection

    # The fonts must be those bundled with matplotlib, not a system copy, or the bytes depend on the machine.
    assert "mpl-data" in font_manager.findfont("DejaVu Sans"), font_manager.findfont("DejaVu Sans")

    phi = (1 + 5 ** 0.5) / 2
    lo, hi = 1 / phi, 2 / 3
    w = (hi - lo) / COLUMNS
    deltas = [lo + (hi - lo) * (i + 0.5) / COLUMNS for i in range(COLUMNS)]

    ink, hole, accent, muted = "#1f3a5f", "#e9e5dc", "#b5532a", "#5f6b7a"
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(7.2, 7.6), sharex=True,
                                 gridspec_kw={"height_ratios": [3, 2], "hspace": 0.2})
    polys, segments = [], 0
    for d in deltas:
        for a, b in survivor_segments(d):
            polys.append([(d - w / 2, a), (d + w / 2, a), (d + w / 2, b), (d - w / 2, b)])
            segments += 1
    hole_poly = [(lo, 1.0)] + [(d, (2 - 1 / d) / (1 / d - 1)) for d in [lo] + deltas + [hi]] + [(hi, 1.0)]
    ax.fill(*zip(*hole_poly), color=hole, lw=0, zorder=0)
    ax.add_collection(PolyCollection(polys, facecolors=ink, edgecolors="none", antialiased=False, zorder=2))
    ts = [(2 - 1 / d) / (1 / d - 1) for d in [lo] + deltas + [hi]]
    ax.plot([lo] + deltas + [hi], ts, color=accent, lw=1.0, zorder=3)
    ax.text(0.6405, 0.935, r"hole $(t(\beta),\,1)$", color=muted, ha="center", va="center", fontsize=9)
    ax.annotate(r"$t(\beta)=(2-\beta)/(\beta-1)$", xy=(0.6236, (2 - 1 / 0.6236) / (1 / 0.6236 - 1)),
                xytext=(0.6195, 0.83), color=accent, fontsize=9,
                arrowprops={"arrowstyle": "-", "color": accent, "lw": 0.6})
    ax.set_ylim(0, 1)
    ax.set_xlim(lo, hi)
    ax.set_ylabel(r"$y$  (points of $K_\delta\subset[0,1)$)")
    ax.set_title(r"(a)  survivor set $K_\delta$ of $y\mapsto\beta y$ mod 1, $\beta=1/\delta$, with the hole $(t(\beta),1)$",
                 fontsize=9, loc="left")

    dims = dimension_curve(deltas)
    pts = table5()
    for dd, val in pts:
        got = dimension_curve([dd])[0]
        assert abs(got - val) < 1e-6, (dd, got, val)
    bx.plot(deltas, dims, color=ink, lw=1.4)
    bx.scatter([p[0] for p in pts], [p[1] for p in pts], s=22, color=accent, zorder=3,
               edgecolors="white", linewidths=0.8, label="Table 5 of the paper")
    bx.set_ylim(0, 1)
    bx.set_ylabel(r"$\dim_H K_\delta$")
    bx.set_xlabel(r"discount factor $\delta$   (window $1/\varphi<\delta<2/3$)")
    bx.set_title(r"(b)  $\dim_H K_\delta=h(\delta)/\log\beta$ from the renewal equation $\Sigma_{n\in A_\delta}\,\delta^{ns}=1$",
                 fontsize=9, loc="left")
    bx.legend(frameon=False, loc="lower right")
    ticks = [lo, 0.625, 0.635, 0.645, 0.655, hi]
    bx.set_xticks(ticks)
    bx.set_xticklabels([r"$1/\varphi$", "0.625", "0.635", "0.645", "0.655", r"$2/3$"])
    for a_ in (ax, bx):
        a_.spines["top"].set_visible(False)
        a_.spines["right"].set_visible(False)
        a_.tick_params(length=3)
    bx.grid(axis="y", color="#d9d9d9", lw=0.5)
    bx.set_axisbelow(True)

    os.makedirs(outdir, exist_ok=True)
    fig.savefig(os.path.join(outdir, "golden-window-figure.svg"), metadata={"Date": None, "Creator": None},
                bbox_inches="tight", pad_inches=0.05)
    fig.savefig(os.path.join(outdir, "golden-window-figure.pdf"),
                metadata={"CreationDate": None, "ModDate": None, "Creator": None, "Producer": None},
                bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    # The PNG is the PDF rasterized by pdftoppm (poppler). Agg measures text slightly differently from machine to
    # machine, so a PNG saved by matplotlib with a tight bounding box changed size between machines; the PDF does not.
    subprocess.run(["pdftoppm", "-r", "400", "-png", "-singlefile", os.path.join(outdir, "golden-window-figure.pdf"),
                    os.path.join(outdir, "golden-window-figure")], check=True)
    return {"columns": COLUMNS, "segments": segments, "eps": EPS, "table5": len(pts),
            "dim_min": min(dims), "dim_max": max(dims)}


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "figshare", "figure")))
