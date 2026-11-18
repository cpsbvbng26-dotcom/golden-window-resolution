#!/usr/bin/env python3
"""Every number printed in the paper must come from a script output.

Each entry below names a number as printed in paper/golden-window-resolution.tex and the
expected output (or script) that produces it. The check passes when
  1. the number is printed in the paper, and
  2. the named file contains a number that rounds to it (same number of decimals).
It also extracts every decimal with at least three digits after the point from the paper
and fails if one of them has no entry here. Integer counts are checked by the same rule
against the file named for them.

  python3 verification/check_numbers.py           # the check
  python3 verification/check_numbers.py --break   # changes one printed number in memory, must fail
"""
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "paper", "golden-window-resolution.tex")

C = "expected/curve/"
E = "expected/edges/"
R = "expected/symbolic-referee/"

ENTRIES = [
    # Theorem A (lower end)
    ("0.1317585615", C + "t1_lower.out"), ("0.0244019292", C + "t1_lower.out"),
    ("44", C + "t1_lower.out"), ("379", C + "t1_lower.out"),
    # Theorem B (upper end)
    ("1.9341796243876", C + "t2_parry.out"), ("11.4760443557125", C + "t2_parry.out"),
    ("11.4760", C + "t2_parry.out"),
    ("1.00359", C + "t2_upper.out"), ("1.0000695", C + "t2_upper.out"), ("1.000000015", C + "t2_upper.out"),
    # Theorem C (plateaus)
    ("0.638413352921706", C + "t3_plateaus.out"), ("0.645200388386225", C + "t3_plateaus.out"),
    ("0.32228461597103", C + "t3_plateaus.out"), ("0.718152", C + "t3_plateaus.out"),
    ("0.735483", C + "t3_plateaus.out"), ("1133", C + "t3_plateaus.out"),
    ("20000", "scripts/curve/t3_plateaus.py"),
    # Theorem E numerics
    ("1.80193773580484", C + "t5_hole0.out"), ("0.30797852837", C + "t5_hole0.out"),
    ("0.445041867913", C + "t5_hole0.out"), ("0.376510198141", C + "t5_hole0.out"),
    ("0.32709354", C + "t5_hole0.out"), ("0.10797978", C + "t5_hole0.out"),
    # Reduction check
    ("50000", C + "membership.out"),
    # Proposition 9 table
    ("0.272410", E + "examples.out"), ("0.404196", E + "examples.out"), ("0.608610", E + "examples.out"),
    ("0.722146", E + "examples.out"), ("0.825510", E + "examples.out"), ("0.919930", E + "examples.out"),
    ("0.999233", E + "examples.out"), ("0.2722", E + "examples.out"), ("0.4042", E + "examples.out"),
    ("0.6086", E + "examples.out"), ("0.7221", E + "examples.out"), ("0.8255", E + "examples.out"),
    ("0.9199", E + "examples.out"), ("0.9992", E + "examples.out"),
    ("0.6181", E + "examples.out"), ("0.6666", E + "examples.out"),
    # Windows table
    ("0.2071", E + "examples.out"), ("0.3660", E + "examples.out"), ("0.5000", E + "examples.out"),
    ("0.5833", E + "examples.out"), ("0.6180", E + "examples.out"), ("0.6667", E + "examples.out"),
    ("0.7247", E + "examples.out"), ("0.7500", E + "examples.out"), ("0.8229", E + "examples.out"),
    ("0.8333", E + "examples.out"), ("0.9142", E + "examples.out"), ("0.9167", E + "examples.out"),
    ("0.6250", E + "examples.out"), ("0.7071", E + "examples.out"), ("0.8660", E + "examples.out"),
    ("0.8750", E + "examples.out"),
    # Monotonicity grids (599 points = 598 consecutive pairs)
    ("598", E + "monotone.out"),
    # Section 7
    ("0.76449", R + "cases.out"), ("0.481212", R + "cases.out"), ("150", R + "theta.out"),
]

NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")


def numbers_in(text):
    return NUM.findall(text)


def matches(printed, candidate, truncated=False):
    if "." not in printed:
        return candidate == printed
    if truncated and candidate.startswith(printed):
        return True
    places = len(printed.split(".")[1])
    try:
        c = Decimal(candidate)
    except Exception:
        return False
    q = Decimal(1).scaleb(-places)
    return any(str(c.quantize(q, rounding=m)) == printed for m in (ROUND_HALF_UP, ROUND_HALF_EVEN))


def tex_plain(tex):
    # 1{,}133 -> 1133, 20{,}000 -> 20000. Identifiers are not numbers: the bibliography,
    # DOIs, URLs and arXiv identifiers are removed before numbers are extracted.
    tex = tex.split(r"\begin{thebibliography}")[0]
    tex = re.sub(r"\\(doi|url|href)\{[^}]*\}", " ", tex)
    tex = re.sub(r"arXiv:\S+|DOI \S+|\d{4}\.\d{4,5}", " ", tex)
    return tex.replace("{,}", "")


def run(tex):
    plain = tex_plain(tex)
    errors = []
    printed_in_paper = set(numbers_in(plain))
    for printed, rel in ENTRIES:
        if printed not in printed_in_paper:
            errors.append(f"{printed}: not printed in the paper")
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            src = fh.read()
        trunc = (printed + r"\ldots") in plain
        if not any(matches(printed, c, trunc) for c in numbers_in(src)):
            errors.append(f"{printed}: no number in {rel} rounds to it")
    covered = {p for p, _ in ENTRIES}
    for n in sorted(printed_in_paper):
        if "." in n and len(n.split(".")[1]) >= 3 and n not in covered:
            errors.append(f"{n}: printed in the paper but has no entry in check_numbers.py")
    errors += counted_claims(plain)
    return errors


def counted_claims(plain):
    """Counts stated in words, recomputed from the outputs."""
    errs = []
    # Theorem A: "(41 values)", every row has A_delta = {1, N}.
    rows = []
    with open(os.path.join(ROOT, C + "t1_lower.out"), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*(\d+)\s+(\d+)\s+\[1, (\d+)\]\s", line)
            if m:
                rows.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    ks = sorted({k for k, _, _ in rows})
    if f"({len(ks)} values)" not in plain:
        errs.append(f"Theorem A: the paper's count of values differs from the {len(ks)} rows in t1_lower.out")
    if any(n != a for _, n, a in rows):
        errs.append("Theorem A: a row of t1_lower.out has A_delta other than {1, N}")
    # Reduction check: six values of delta, 0 mismatches each.
    with open(os.path.join(ROOT, C + "membership.out"), encoding="utf-8") as fh:
        mem = [l for l in fh if l.startswith("delta")]
    if "at each of six values" not in plain or len(mem) != 6:
        errs.append("reduction check: the paper's six values of delta do not match membership.out")
    if any(not l.rstrip().endswith("mismatches 0") for l in mem):
        errs.append("reduction check: a mismatch in membership.out")
    return errs


def main(argv):
    with open(TEX, encoding="utf-8") as fh:
        tex = fh.read()
    if "--break" in argv:
        tex = tex.replace("0.32228461597103", "0.32228461597104", 1)
        errs = run(tex)
        if errs:
            print("break test: the check failed as it should")
            for e in errs:
                print("  " + e)
            return 0
        print("break test: the check did NOT fail")
        return 1
    errs = run(tex)
    print(f"{len(ENTRIES)} printed numbers checked against script outputs, {len(errs)} problems")
    for e in errs:
        print("  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
