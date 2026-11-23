"""The Dataset item: the tables of the paper as CSV, transcribed from expected/.

Every value in a column marked "transcribed" is the exact character string printed by a script
(expected/<group>/<name>.out). Nothing is rounded again or re-typed. The column `source` gives the
file and line it was read from. The only computed column is `entropy_h` in the first table, computed from the
transcribed A_delta; it is marked "derived" in the data dictionary and recomputed by verification/check_figshare.py.

  python3 figshare/build.py         # writes figshare/dataset/ together with the other items
"""
import csv
import io
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = r"[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?"


def lines(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read().splitlines()


def rows_matching(rel, pattern):
    """(line number, match) for each line of expected/<rel> that matches the pattern, in order."""
    pat = re.compile(pattern)
    out = []
    for i, line in enumerate(lines(rel), start=1):
        m = pat.match(line)
        if m:
            out.append((f"{rel}:{i}", m))
    return out


def a_set(s):
    """'[1, 3, 9]' -> '1 3 9' (the listed elements, space-separated)."""
    return " ".join(x.strip() for x in s.strip("[]").split(","))


def entropy(A_listed):
    """h = -log z, z the root in (0, 1) of sum_{n in A} z^n = 1, for a listed set A; six decimals.
    The scripts print at most six elements of A_delta, so a list of six may be cut; then the cell is empty."""
    A = [int(x) for x in A_listed.split()]
    if len(A) >= 6:
        return ""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(mid ** n for n in A) > 1:
            hi = mid
        else:
            lo = mid
    return f"{-math.log((lo + hi) / 2):.6f}"


# Each table: file name, title, column list [(name, kind, description)], builder -> rows (dicts).
# kind is "transcribed" (string copied from the source line), "derived" (computed here) or "source".

def t_prop9():
    rel = "expected/edges/examples.out"
    pat = (r"  delta (" + NUM + r"): gap, renewal (" + NUM + r"), LSZ (" + NUM + r"), count\(n=110\.\.120\) ("
           + NUM + r"), A (\[[\d, ]+\])$")
    rows = []
    for src, m in rows_matching(rel, pat):
        d, ren, lsz, cnt, A = m.groups()
        rows.append({"delta": d, "dim_renewal": ren, "dim_lsz": lsz, "dim_word_count": cnt,
                     "A_delta_listed": a_set(A), "entropy_h": entropy(a_set(A)), "source": src})
    return rows


def t_count():
    rel = "expected/curve/check_count.out"
    pat = (r"delta=\s*(" + NUM + r")  dim by counting=(" + NUM + r")  dim by first-return formula=(" + NUM
           + r")  1-dim\(count\)=(" + NUM + r")$")
    return [{"delta": a, "dim_counting": b, "dim_formula": c, "one_minus_dim_counting": e, "source": src}
            for src, m in rows_matching(rel, pat) for a, b, c, e in [m.groups()]]


def t_lower():
    rel = "expected/curve/t1_lower.out"
    pat = (r"\s*(\d+)\s+(\d+) (\[[\d, ]+\])\s+(" + NUM + r") (" + NUM + r") (" + NUM + r") (" + NUM
           + r") (" + NUM + r") (" + NUM + r")$")
    return [{"k": k, "N": n, "A_delta_listed": a_set(A), "dim": dim, "lower_bound": lo, "upper_bound": up,
             "W_N_over_N_log_beta": w, "dim_L_over_log_L": dl, "loglog_approximation": ll, "source": src}
            for src, m in rows_matching(rel, pat) for k, n, A, dim, lo, up, w, dl, ll in [m.groups()]]


def t_lower_rate():
    rel = "expected/curve/t1_lower.out"
    pat = r"\s*(\d+) (" + NUM + r") (" + NUM + r") (" + NUM + r") (" + NUM + r")$"
    return [{"k": k, "dim_times_L": a, "W_of_L_over_log_phi": b, "difference": c,
             "difference_L_over_log_L_squared": e, "source": src}
            for src, m in rows_matching(rel, pat) for k, a, b, c, e in [m.groups()]]


def t_upper():
    rel = "expected/curve/t2_upper.out"
    pat = r"\s*(\d+)\s+(" + NUM + r")\s+(" + NUM + r")\s+(" + NUM + r")\s+(" + NUM + r")$"
    return [{"k": k, "one_minus_dim": a, "one_minus_dim_over_eps": b, "ratio_to_C": c, "kappa_over_9eps": e,
             "source": src}
            for src, m in rows_matching(rel, pat) for k, a, b, c, e in [m.groups()]]


def t_plateau():
    rel = "expected/curve/t3_plateaus.out"
    pat = r"  delta (" + NUM + r") A (\[[\d, ]+\]) h (" + NUM + r") dim (" + NUM + r")$"
    return [{"delta": d, "A_delta_listed": a_set(A), "entropy_h": h, "dim": dim, "source": src}
            for src, m in rows_matching(rel, pat) for d, A, h, dim in [m.groups()]]


def t_constants():
    out = []
    specs = [
        ("expected/curve/t2_parry.out", r"M1 via Parry sum = (" + NUM + r")$", "M", "Theorem B: M = sum over A* of n (2/3)^n"),
        ("expected/curve/t2_parry.out", r"C = (" + NUM + r")$", "C", "Theorem B: C = 9 / (M log(3/2))"),
        ("expected/curve/t3_plateaus.out", r"plateau A=\{1,4\}: \[ (" + NUM + r") , " + NUM + r" \]$",
         "plateau_1_4_left", "left end of the plateau with A_delta = {1, 4}"),
        ("expected/curve/t3_plateaus.out", r"plateau A=\{1,4\}: \[ " + NUM + r" , (" + NUM + r") \]$",
         "plateau_1_4_right", "right end of the plateau with A_delta = {1, 4}"),
        ("expected/curve/t3_plateaus.out", r"h on it = -log z, z\+z\^4=1: (" + NUM + r")$",
         "plateau_1_4_entropy", "entropy h on that plateau (root of z + z^4 = 1)"),
        ("expected/curve/t3_plateaus.out", r"admissibility violations: \d+ ; distinct finite A seen: (\d+)$",
         "distinct_finite_A", "distinct finite sets A_delta in a scan of 20,000 parameters"),
    ]
    for rel, pat, name, what in specs:
        (src, m), = rows_matching(rel, pat)
        out.append({"name": name, "value": m.group(1), "meaning": what, "source": src})
    return out


def t_windows():
    rel = "expected/edges/examples.out"
    pat = (r"  r=(\d+(?:/\d+)?) edge (\w+)-(\w+) \(k=(\d)\): grid (" + NUM + r")\.\.(" + NUM
           + r")  closed form \((" + NUM + r"), (" + NUM + r")\)(?:  rotation delta_3\(r\) = (" + NUM + r"))?$")
    return [{"r": r, "edge": f"{a}-{b}", "k": k, "grid_low": gl, "grid_high": gh, "theta_k": tk, "U_k": uk,
             "delta_3": d3 or "", "source": src}
            for src, m in rows_matching(rel, pat) for r, a, b, k, gl, gh, tk, uk, d3 in [m.groups()]]


def t_theorem_d():
    rel = "expected/curve/t4_why_phi.out"
    pat = r" (" + NUM + r")\s+(" + NUM + r")\s+(" + NUM + r")\s+(" + NUM + r")$"
    return [{"r": r, "rotation_threshold": a, "segment_threshold": b, "closed_form": c, "source": src}
            for src, m in rows_matching(rel, pat) for r, a, b, c in [m.groups()]]


def t_membership():
    rel = "expected/curve/membership.out"
    pat = r"delta (" + NUM + r"): points (\d+), depth (\d+), survivors (\d+), mismatches (\d+)$"
    return [{"delta": d, "points": p, "depth": dp, "survivors": s, "mismatches": mm, "source": src}
            for src, m in rows_matching(rel, pat) for d, p, dp, s, mm in [m.groups()]]


def t_monotone():
    rel = "expected/edges/monotone.out"
    pat = (r"(.+): decreases (\d+)/(\d+); first (" + NUM + r"):(" + NUM + r")  last (" + NUM + r"):(" + NUM + r")$")
    return [{"edge": e, "decreases": a, "comparisons": b, "first_delta": fd, "first_dim": fs, "last_delta": ld,
             "last_dim": ls, "source": src}
            for src, m in rows_matching(rel, pat) for e, a, b, fd, fs, ld, ls in [m.groups()]]


SRC = ("source", "source", "file and line of expected/ from which the row was transcribed")
TABLES = [
    ("prop9_dimension.csv", "Theorem 3.2 (Proposition 9 of the earlier note) and Table 5 (Section 10, Numerics): dim_H S along the curve, three ways", t_prop9, [
        ("delta", "transcribed", "discount factor delta (as printed)"),
        ("dim_renewal", "transcribed", "dim_H S from the renewal equation sum_{n in A_delta} delta^(n s) = 1 (Theorem 3.2)"),
        ("dim_lsz", "transcribed", "the same from the root of Lu, Steiner and Zou, Theorem 1.2"),
        ("dim_word_count", "transcribed", "growth rate of exact word counts at depth 110 to 120"),
        ("A_delta_listed", "transcribed", "first-return set A_delta as printed (space-separated); at most the first six elements are printed"),
        ("entropy_h", "derived", "entropy h = -ln z*, z* the root in (0, 1) of sum over A_delta_listed of z^n = 1, rounded to six decimals; empty when six elements are listed, since the list may then be cut; not printed in the paper"),
        SRC]),
    ("curve_dimension_by_counting.csv", "Dimension along the curve by counting cylinders, against the first-return formula", t_count, [
        ("delta", "transcribed", "discount factor delta (ten significant digits as printed)"),
        ("dim_counting", "transcribed", "dimension estimated by counting cylinders of the greedy map (no first-return formula used)"),
        ("dim_formula", "transcribed", "dimension by the first-return formula"),
        ("one_minus_dim_counting", "transcribed", "1 - dim_counting"),
        SRC]),
    ("theorem_A_lower_end.csv", "Theorem A: the lower end, delta = 1/phi + 10^(-k)", t_lower, [
        ("k", "transcribed", "delta = 1/phi + 10^(-k)"),
        ("N", "transcribed", "N(delta) = ceil(log(X/(X-1))/log beta)"),
        ("A_delta_listed", "transcribed", "first-return set A_delta as printed"),
        ("dim", "transcribed", "dim_H S"),
        ("lower_bound", "transcribed", "log(1/zeta_N)/log beta, zeta_N the root of z + z^N = 1"),
        ("upper_bound", "transcribed", "log(1/eta_N)/log beta, eta_N the root of z + z^N/(1 - z^(N-1)) = 1"),
        ("W_N_over_N_log_beta", "transcribed", "W(N)/(N log beta), W the Lambert function"),
        ("dim_L_over_log_L", "transcribed", "dim * L / log L with L = log(1/(delta - 1/phi))"),
        ("loglog_approximation", "transcribed", "(log N - log log N)/(N log beta)"),
        SRC]),
    ("theorem_A_rate.csv", "Theorem A(3): dim * L against W(L/log phi)", t_lower_rate, [
        ("k", "transcribed", "delta = 1/phi + 10^(-k)"),
        ("dim_times_L", "transcribed", "dim * L, L = log(1/(delta - 1/phi))"),
        ("W_of_L_over_log_phi", "transcribed", "W(L/log phi)"),
        ("difference", "transcribed", "dim_times_L - W_of_L_over_log_phi"),
        ("difference_L_over_log_L_squared", "transcribed", "difference * L/(log L)^2 (bounded, as Theorem A(3) states)"),
        SRC]),
    ("theorem_B_upper_end.csv", "Theorem B: the upper end, delta = 2/3 - 10^(-k)", t_upper, [
        ("k", "transcribed", "delta = 2/3 - eps, eps = 10^(-k)"),
        ("one_minus_dim", "transcribed", "1 - dim_H S"),
        ("one_minus_dim_over_eps", "transcribed", "(1 - dim)/eps"),
        ("ratio_to_C", "transcribed", "(1 - dim)/(eps C)"),
        ("kappa_over_9eps", "transcribed", "kappa/(9 eps), kappa = 1 - G_delta(delta)"),
        SRC]),
    ("theorem_C_plateau_1_4.csv", "Theorem C: points on the plateau with A_delta = {1, 4}", t_plateau, [
        ("delta", "transcribed", "discount factor delta (twelve significant digits as printed)"),
        ("A_delta_listed", "transcribed", "first-return set A_delta as printed"),
        ("entropy_h", "transcribed", "entropy h = -log z*"),
        ("dim", "transcribed", "dim_H S = h/log beta"),
        SRC]),
    ("constants.csv", "Constants printed in the paper (Theorems B and C)", t_constants, [
        ("name", "transcribed", "name of the constant (assigned here)"),
        ("value", "transcribed", "value as printed by the script"),
        ("meaning", "transcribed", "what the constant is (written here)"),
        SRC]),
    ("windows_three_players.csv", "Table 1 (windows on the three-player edges) and the grid search behind it", t_windows, [
        ("r", "transcribed", "cost-benefit ratio r = c/b"),
        ("edge", "transcribed", "the edge (two pure profiles)"),
        ("k", "transcribed", "number of other cooperators on the edge"),
        ("grid_low", "transcribed", "lowest delta of the fractal window found on a grid"),
        ("grid_high", "transcribed", "highest delta of the fractal window found on a grid"),
        ("theta_k", "transcribed", "closed-form lower end theta_k(r) (Proposition 5.3)"),
        ("U_k", "transcribed", "closed-form upper end U_k(r)"),
        ("delta_3", "transcribed", "rotation threshold delta_3(r) = (sqrt(1+4r)-1)/2 (k = 2 only; empty otherwise)"),
        SRC]),
    ("theorem_D_thresholds.csv", "Theorem D: the rotation threshold and the segment threshold coincide", t_theorem_d, [
        ("r", "transcribed", "r = c/b"),
        ("rotation_threshold", "transcribed", "threshold of the three-player rotation"),
        ("segment_threshold", "transcribed", "threshold of the (C,D,C) branch on the segment"),
        ("closed_form", "transcribed", "(sqrt(1+4r)-1)/2"),
        SRC]),
    ("reduction_check.csv", "Section 2.2: the game recursion against the beta-transformation criterion", t_membership, [
        ("delta", "transcribed", "discount factor delta"),
        ("points", "transcribed", "random points tested (exact rationals, fixed seed)"),
        ("depth", "transcribed", "number of steps"),
        ("survivors", "transcribed", "points that survive the game recursion"),
        ("mismatches", "transcribed", "points on which the two criteria disagree"),
        SRC]),
    ("monotonicity_edges.csv", "Proposition 5.4 and the remark after it: dim along each window on a grid of 599 points", t_monotone, [
        ("edge", "transcribed", "the edge (r for the three-player edge CCC-CCD, or the main edge of G_4, G_5)"),
        ("decreases", "transcribed", "consecutive comparisons in which dim decreased"),
        ("comparisons", "transcribed", "consecutive comparisons made"),
        ("first_delta", "transcribed", "first grid point"),
        ("first_dim", "transcribed", "dim at the first grid point"),
        ("last_delta", "transcribed", "last grid point"),
        ("last_dim", "transcribed", "dim at the last grid point"),
        SRC]),
]


def csv_text(columns, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow([c[0] for c in columns])
    for r in rows:
        w.writerow([r.get(c[0], "") for c in columns])
    return buf.getvalue()


def readme(built):
    out = ["# Dataset: numerical tables for the resolution of the golden-window conjecture", "",
           "Generated by `figshare/build.py` from the outputs in `expected/` of the repository",
           "https://github.com/cpsbvbng26-dotcom/golden-window-resolution. It is not edited by hand.", "",
           "Each CSV file is UTF-8, comma-separated, with one header row. A column marked *transcribed* holds the exact",
           "character string printed by a script; nothing was rounded again or re-typed. The column `source` names the",
           "file and line of `expected/` from which the row was read. A column marked *derived* is computed here and is",
           "not printed in the paper. `verification/check_figshare.py` compares every transcribed cell with its source line",
           "and recomputes every derived cell.", "",
           "The paper is 10.6084/m9.figshare.35050300; the conjecture was stated in 10.6084/m9.figshare.34419198.",
           "Licence: CC BY 4.0.", "",
           f"There are {len(built)} CSV files.", ""]
    for fname, title, rows, columns in built:
        out += [f"## {fname}", "", title + ".", "", f"{len(rows)} rows.", "",
                "| column | kind | meaning |", "| --- | --- | --- |"]
        out += [f"| `{c}` | {k} | {d} |" for c, k, d in columns]
        out.append("")
    return "\n".join(out)


def build(outdir):
    os.makedirs(outdir, exist_ok=True)
    built = []
    for fname, title, fn, columns in TABLES:
        rows = fn()
        assert rows, fname
        with open(os.path.join(outdir, fname), "w", encoding="utf-8", newline="") as fh:
            fh.write(csv_text(columns, rows))
        built.append((fname, title, rows, columns))
    with open(os.path.join(outdir, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(readme(built))
    return built
