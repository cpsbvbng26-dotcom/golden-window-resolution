#!/usr/bin/env python3
"""Every number printed in the continuity paper must come from a script output.

The paper is continuity/paper/joint-continuity.tex. Each entry below names a number as printed there and
the expected output (or script) that produces it. Three kinds of number are checked:
  * decimals, such as 0.6094: some number in the named file rounds to it (same number of decimals);
  * powers of ten written m\\cdot10^{e}, such as 5.3\\cdot10^{-9}: some number in the file, in Python's
    e-notation, rounds to m at the exponent e;
  * integers (counts): the named file contains the integer as a whole token, or, when a regular expression
    is given, the regular expression matches in the file (it pins the count to its line).
The check fails if an entry is not printed in the paper, if the named file does not support it, or if the
paper prints a decimal with at least three digits after the point, or any m\\cdot10^{e}, that has no entry.
A few statements made in words (intervals, counts of cases) are recomputed from the outputs.

  python3 verification/check_numbers_continuity.py           # the check
  python3 verification/check_numbers_continuity.py --break   # changes printed numbers in memory; each must fail
"""
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "continuity", "paper", "joint-continuity.tex")

E = "continuity/expected/"
S = "continuity/scripts/"
OR, IA, WI, HU, RM = E + "oracle.out", E + "ia_witness.out", E + "witnesses.out", E + "hunt.out", E + "realmap.out"

# (printed, file, optional regex that must match in the file)
ENTRIES = [
    # Example 3.3 and the continuity hunt (hunt.py)
    ("0.6094", HU, None), ("0.6760", HU, None), ("0.6922", HU, None), ("0.6931", HU, None),
    ("0.0680", HU, None), ("0.0404", HU, None), ("0.0235", HU, None),
    ("400", HU, r"all random pairs: 400 pairs"), ("390", HU, r"400 pairs, 390 not normalized"),
    ("81", HU, r"390 not normalized, 81 with h > 0"),
    ("200", HU, r"200 pairs, 167 not normalized, 200 with h > 0"),
    ("1.9e-2", HU, r"pairs with h > 0: 1\.9e-02, 6\.4e-04, 2\.5e-05, 1\.0e-06"),
    ("6.4e-4", HU, None), ("2.5e-5", HU, None), ("1.0e-6", HU, None),
    ("5.6e-2", HU, r"pairs with h > 0: 5\.6e-02, 1\.8e-03, 1\.2e-04, 8\.1e-06"),
    ("1.8e-3", HU, None), ("1.2e-4", HU, None), ("8.1e-6", HU, None),
    # Theorem A against the raw automaton (oracle.py)
    ("240", OR, r"all: 240 pairs, 0 word-count mismatches, entropies agree to 1e-12: True"),
    ("60", OR, r"M=4: 60 normalized pairs"),
    ("30", OR, r"n <= 30: 0 mismatches"),
    ("3041", OR, r"Lemma P: 3041 edges of the automata checked, 0 where"),
    ("1e-12", OR, None),
    # Theorem IA (ia_witness.py)
    ("50", IA, r"M = 1\.\.4, 50 each"),
    ("1e-12", IA, r"agree to 1e-12: True"),
    ("5.3e-9", IA, r"M=2, spread >= 2:  40 pairs, max 5\.3e-09 and <1e-11"),
    ("2.0e-9", IA, r"M=3, spread >= 2:  44 pairs, max 2\.0e-09 and <1e-11"),
    ("1.4e-11", IA, r"M=4, spread >= 2:  48 pairs, max 1\.4e-11 and <1e-11"),
    ("1e-11", IA, None),
    ("1.3e-1", IA, r"b = \(10000000000000000\)\^inf, h = 0\.125665: 1\.3e-01, 6\.8e-02, 1\.5e-02, 2\.7e-03, 2\.2e-04"),
    ("6.8e-2", IA, None), ("1.5e-2", IA, None), ("2.7e-3", IA, None), ("2.2e-4", IA, None),
    ("2.6e-8", IA, r"a = \(02\)\^inf, b = \(210\)\^inf, h = 0\.281199574: 5\.6e-02, 1\.8e-03, 1\.2e-04, 8\.1e-06, 2\.6e-08"),
    ("4.6e-3", IA, r"b = \(201010101010101\)\^inf, h = 0\.482059634: 4\.6e-03, 7\.6e-05, 1\.2e-06, 5\.3e-09, <1e-11"),
    ("7.6e-5", IA, None), ("1.2e-6", IA, None),
    ("14", S + "ia_witness.py", r"canon\(\(\), \(2,\) \+ \(0, 1\) \* 7\)"),
    ("16", IA, r"b = \(10{16}\)\^inf, h = 0\.125665"),
    # the witnesses (witnesses.py)
    ("31", WI, r"summary over 31 pairs and 93 values"), ("93", WI, r"93 of 93"),
    ("20", S + "witnesses.py", r"while len\(rand\) < 20:"),
    ("28", WI, r"end a, in a component of radius > 1, agreement >= 30: 28"),
    ("27", WI, r"end b, in a component of radius > 1, agreement >= 30: 27"),
    # the point with spread 3 (realmap.py)
    ("3.30277563773", RM, None), ("0.091673086804", RM, None), ("0.9195230258", RM, None),
    ("0.91517", RM, None), ("0.92949", RM, None), ("0.91948", RM, None), ("0.91966", RM, None),
    ("0.91952", RM, None), ("0.91953", RM, None),
    ("1e-2", RM, None), ("1e-4", RM, None), ("1e-6", RM, None), ("1e-8", RM, None),
    ("150", S + "realmap.py", r"def dim_est\(beta, t, n=150, m=50\)"),
    ("80", S + "realmap.py", r"mp\.dps = 80"),
    ("60", S + "lexlib.py", r"mp\.workdps\(60\)"),
]

NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")
SCI_TEX = re.compile(r"(\d+(?:\.\d+)?)\s*\\cdot\s*10\^\{(-?\d+)\}|(?<![\d.])10\^\{(-\d+)\}")
SCI_OUT = re.compile(r"(\d+(?:\.\d+)?)e([+-]\d+)")


def tex_plain(tex):
    tex = tex.split(r"\begin{thebibliography}")[0]
    tex = re.sub(r"(\\[A-Za-z]+)(?=\d)", r"\1 ", tex)   # \le30 -> \le 30, \approx3.3 -> \approx 3.3
    tex = re.sub(r"\\(doi|url|href)\{[^}]*\}", " ", tex)
    tex = re.sub(r"arXiv:\S+|DOI \S+|\d{4}\.\d{4,5}", " ", tex)
    return tex


def sci_in_tex(plain):
    """Every m\\cdot10^{e} and bare 10^{-e} in the paper, as 'me<e>' strings, e.g. '5.3e-9', '1e-12'."""
    out = []
    for m in SCI_TEX.finditer(plain):
        if m.group(1):
            out.append(f"{m.group(1)}e{int(m.group(2))}")
        else:
            out.append(f"1e{int(m.group(3))}")
    return out


def rounds_to(printed, candidate):
    places = len(printed.split(".")[1]) if "." in printed else 0
    try:
        c = Decimal(candidate)
    except Exception:
        return False
    q = Decimal(1).scaleb(-places)
    return any(str(c.quantize(q, rounding=r)) == printed for r in (ROUND_HALF_UP, ROUND_HALF_EVEN))


def sci_supported(printed, src):
    mant, exp = printed.split("e")
    exp = int(exp)
    for m in SCI_OUT.finditer(src):
        if int(m.group(2)) == exp and rounds_to(mant, m.group(1)):
            return True
        val = Decimal(m.group(1)).scaleb(int(m.group(2)))
        if rounds_to(mant, str(val.scaleb(-exp))) and mant != "1":
            return True
    # "1e-12" style statements: the output must print the same bound
    if mant == "1":
        return f"1e{exp:03d}" in src or f"1e-{abs(exp)}" in src
    return False


def run(tex):
    plain = tex_plain(tex)
    errors = []
    decimals = set(NUM.findall(plain))
    sci = set(sci_in_tex(plain))
    for printed, rel, pattern in ENTRIES:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            src = fh.read()
        if "e" in printed:
            if printed not in sci:
                errors.append(f"{printed}: not printed in the paper")
                continue
            if not sci_supported(printed, src):
                errors.append(f"{printed}: no number in {rel} rounds to it")
        elif "." in printed:
            if printed not in decimals:
                errors.append(f"{printed}: not printed in the paper")
                continue
            if not any(rounds_to(printed, c) for c in NUM.findall(src)):
                errors.append(f"{printed}: no number in {rel} rounds to it")
        else:
            if printed not in decimals:
                errors.append(f"{printed}: not printed in the paper")
                continue
            if pattern is None and printed not in NUM.findall(src):
                errors.append(f"{printed}: not in {rel}")
        if pattern and not re.search(pattern, src):
            errors.append(f"{printed}: the line /{pattern}/ is not in {rel}")
    covered = {p for p, _, _ in ENTRIES}
    for n in sorted(decimals):
        if "." in n and len(n.split(".")[1]) >= 3 and n not in covered:
            errors.append(f"{n}: printed in the paper but has no entry in check_numbers_continuity.py")
    for n in sorted(sci):
        if n not in covered:
            errors.append(f"{n}: printed in the paper but has no entry in check_numbers_continuity.py")
    errors += counted_claims(plain)
    return errors


def counted_claims(plain):
    """Statements in words, recomputed from the outputs."""
    errs = []
    flat = " ".join(plain.split())
    # realmap: the intervals [min, max] over the eight directions at each e.
    rows = {}
    with open(os.path.join(ROOT, RM), encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*1e-(\d)\s+((?:\d\.\d{5}\s*){8})$", line)
            if m:
                rows[int(m.group(1))] = [x for x in m.group(2).split()]
    for k, phrase in ((2, "in $[{lo},{hi}]$ at $e=10^{{-2}}$"), (4, "in $[{lo},{hi}]$ at $e=10^{{-4}}$"),
                      (6, "in $[{lo},{hi}]$ at $e=10^{{-6}}$")):
        if k not in rows:
            errs.append(f"realmap.out: no row for e = 1e-{k}")
            continue
        vals = sorted(rows[k], key=float)
        if phrase.format(lo=vals[0], hi=vals[-1]) not in flat:
            errs.append(f"realmap: the interval at e = 1e-{k} is [{vals[0]}, {vals[-1]}] in the output, not as printed")
    if 8 not in rows or len(set(rows[8])) != 1 or f"all equal ${rows[8][0]}$ at $e=10^{{-8}}$" not in flat:
        errs.append("realmap: the row e = 1e-8 is not constant, or its value is not the printed one")
    # oracle: four values of M, 60 pairs each, 0 mismatches.
    with open(os.path.join(ROOT, OR), encoding="utf-8") as fh:
        orc = fh.read()
    if len(re.findall(r"M=\d: 60 normalized pairs \(\d+ with h > 0\); word counts N_n, n <= 30: 0 mismatches; "
                      r"max \|h\(Theorem A\) - h\(automaton\)\| < 1e-12: True", orc)) != 4:
        errs.append("oracle: not every M has 60 pairs with 0 mismatches and agreement to 1e-12")
    if "starts $1,3,6,9,9,0,-27$" not in flat or "series of Theorem A, n <= 12: [1, 3, 6, 9, 9, 0, -27," not in orc:
        errs.append("oracle: the negative control series differs")
    if "start $1,2,3,4,5,6,7$" not in flat or "word counts,         n <= 12: [1, 2, 3, 4, 5, 6, 7," not in orc:
        errs.append("oracle: the negative control word counts differ")
    # witnesses: every check passed, and the support-lemma table has no mixed case.
    with open(os.path.join(ROOT, WI), encoding="utf-8") as fh:
        wit = fh.read()
    for needle in ("first difference at index <= D: 93 of 93", "(p_D, q_D) normalized: 93 of 93",
                   "max |Theorem A(p_D, q_D) - h(Y_D)|: <1e-11;  max |raw(p_D, q_D) - h(Y_D)|: <1e-11",
                   "end a, in no such component, agreement < 30: 3", "end b, in no such component, agreement < 30: 4"):
        if needle not in wit:
            errs.append(f"witnesses.out: '{needle}' missing")
    if re.search(r"in a component of radius > 1, agreement < 30|in no such component, agreement >= 30", wit):
        errs.append("witnesses.out: a mixed case in the support-lemma table")
    if "remaining $3$ and $4$ cases" not in flat:
        errs.append("witnesses: the paper's count of remaining cases is not 3 and 4")
    # ia_witness: no decrease, every spread >= 2 gap below 1e-11 at D = 60.
    with open(os.path.join(ROOT, IA), encoding="utf-8") as fh:
        iaw = fh.read()
    if "pairs where h(Y_D) decreases in D: 0" not in iaw:
        errs.append("ia_witness: some h(Y_D) decreases")
    if len(re.findall(r"spread >= 2:\s+\d+ pairs, max \S+ and <1e-11", iaw)) != 3:
        errs.append("ia_witness: a spread >= 2 gap at D = 60 is not below 1e-11")
    return errs


BREAKS = [("0.6922", "0.6923"), ("5.3\\cdot10^{-9}", "5.3\\cdot10^{-8}"), ("$3041$", "$3042$"),
          ("[0.91948,0.91966]", "[0.91948,0.91967]"), ("$1.4\\cdot10^{-11}$", "$1.4\\cdot10^{-11}$ and $7.7\\cdot10^{-4}$")]


def main(argv):
    with open(TEX, encoding="utf-8") as fh:
        tex = fh.read()
    if "--break" in argv:
        bad = 0
        for old, new in BREAKS:
            if old not in tex:
                print(f"  break text not found: {old}")
                bad += 1
                continue
            errs = run(tex.replace(old, new, 1))
            print(f"  {'failed, as it should' if errs else 'did NOT fail'}: {old} -> {new}")
            bad += not errs
        print("break test: " + ("every change made the check fail, as it should" if not bad else f"{bad} problems"))
        return 1 if bad else 0
    errs = run(tex)
    print(f"{len(ENTRIES)} printed numbers checked against script outputs, {len(errs)} problems")
    for e in errs:
        print("  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
