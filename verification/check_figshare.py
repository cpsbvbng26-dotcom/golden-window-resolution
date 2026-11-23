#!/usr/bin/env python3
"""Checks for figshare/ (the five Figshare items of the golden-window conjecture, 2026-11-24).

1. SHA256SUMS lists every generated file of figshare/ and matches its bytes.
2. --rebuild: figshare/build.py, run into a temporary directory, gives the same files, byte for byte.
   (Needs matplotlib, pillow and fonttools as pinned in requirements.txt, pdflatex with tikzposter and beamer,
   and the full git history. CI runs it in the job figshare.)
3. Every transcribed cell of the CSV files is the exact string at its place in the line of expected/ named in the
   column `source`; every line of expected/ that a table covers is in the table; derived cells are recomputed.
   This parser is written separately from figshare/tables.py: it splits lines into tokens and does not use its patterns.
4. The software zip holds exactly the files of the pinned commit under the listed paths, each identical to
   `git show <commit>:<path>`.
5. Wording. METADATA.md, the poster and the slides keep the disclosure, the credit to Lu, Steiner and Zou, the phrase
   "not found in the texts read", the conditional status of Theorem E, the author (Takuya Nemoto, ORCID) and the
   licences (MIT for the software, CC BY 4.0 for the rest). No DOI other than the two Figshare DOIs of the papers.
   No claim words ("novel", "breakthrough", "for the first time", "new" except in "not new mathematics").
   No name of a university or a research institute. Every number with three or more decimals in the poster and
   the slides occurs in expected/.
6. The counts that README.md, README.en.md and METADATA.md state (items, CSV files, files in the zip, slides,
   poster pages) are the actual ones; the poster is A0 portrait.

  python3 verification/check_figshare.py              # 1, 3-6
  python3 verification/check_figshare.py --rebuild    # 1-6
  python3 verification/check_figshare.py --break      # changes each checked thing in memory; every change must fail
"""
import csv
import hashlib
import io
import math
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FS = os.path.join(ROOT, "figshare")
DOIS = {"10.6084/m9.figshare.35050300", "10.6084/m9.figshare.34419198"}
COMMIT = "c2a47fd9fd1a4cbd9940e0ec78895b47689f9313"
ZIP = f"software/golden-window-resolution-scripts-{COMMIT[:7]}.zip"
ZIP_PATHS = ["LICENSE-CODE", "requirements.txt", "verification/run_scripts.py", "scripts", "expected"]
ITEMS = ["Figure", "Dataset", "Software", "Poster", "Presentation"]
DISCLOSURE = ["This work has not been peer reviewed.",
              "How much of it is new will be settled by peer review and by formalization.",
              "The work was done without an advisor.",
              "Claude Code (Anthropic) was used to search and read the literature",
              "The author is responsible for the content.", "Claude is not an author."]

# Which lines of expected/ each table must cover: (file, a test on the line). Written from the files, not from tables.py.
COVER = {
    "prop9_dimension.csv": ("expected/edges/examples.out", lambda l: l.startswith("  delta ") and "renewal" in l),
    "curve_dimension_by_counting.csv": ("expected/curve/check_count.out", lambda l: l.startswith("delta=")),
    "theorem_A_lower_end.csv": ("expected/curve/t1_lower.out", lambda l: re.match(r"\s*\d+\s+\d+ \[", l)),
    "theorem_A_rate.csv": ("expected/curve/t1_lower.out", lambda l: re.match(r"\s*\d+ \S+ \S+ [+-]\S+ [+-]\S+$", l)),
    "theorem_B_upper_end.csv": ("expected/curve/t2_upper.out", lambda l: re.match(r"\s*\d+(\s+\S+){4}$", l)),
    "theorem_C_plateau_1_4.csv": ("expected/curve/t3_plateaus.out", lambda l: l.startswith("  delta ") and " dim " in l),
    "windows_three_players.csv": ("expected/edges/examples.out", lambda l: l.startswith("  r=") and " grid " in l and "closed form" in l),
    "theorem_D_thresholds.csv": ("expected/curve/t4_why_phi.out", lambda l: re.fullmatch(r" \d\.\d\d(\s+\d\.\d{9}){3}", l)),
    "reduction_check.csv": ("expected/curve/membership.out", lambda l: l.startswith("delta ") and "mismatches" in l),
    "monotonicity_edges.csv": ("expected/edges/monotone.out", lambda l: "decreases" in l),
    "constants.csv": (None, None),
}
DERIVED = {("prop9_dimension.csv", "entropy_h")}


def read(rel, base=FS, mode="r"):
    with open(os.path.join(base, rel), mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def generated(base):
    out = []
    for dp, dns, fns in os.walk(base):
        dns[:] = sorted(d for d in dns if d != "__pycache__")
        for fn in sorted(fns):
            rel = os.path.relpath(os.path.join(dp, fn), base)
            if not fn.endswith(".py") and rel != "SHA256SUMS":
                out.append(rel)
    return sorted(out)


def sums_problems(files, sums_text):
    """files: rel -> bytes."""
    listed = {}
    for line in sums_text.splitlines():
        h, rel = line.split("  ", 1)
        listed[rel] = h
    errs = []
    if set(listed) != set(files):
        errs.append(f"SHA256SUMS lists {sorted(set(listed) ^ set(files))} differently from the files present")
    for rel, data in files.items():
        if rel in listed and hashlib.sha256(data).hexdigest() != listed[rel]:
            errs.append(f"figshare/{rel}: sha256 differs from SHA256SUMS")
    return errs


def tokens(line):
    return [t for t in re.split(r"(?:[\s,:;=()\[\]{}/]|\.\.)+", line) if t]


def csv_problems(name, text, expected_lines):
    """expected_lines: rel -> list of lines."""
    errs = []
    rows = list(csv.reader(io.StringIO(text)))
    head, body = rows[0], rows[1:]
    if not body:
        return [f"{name}: no rows"]
    if "source" not in head:
        return [f"{name}: no column source"]
    si = head.index("source")
    seen = set()
    for r in body:
        if len(r) != len(head):
            errs.append(f"{name}: row of wrong length {r}")
            continue
        rel, ln = r[si].rsplit(":", 1)
        line = expected_lines[rel][int(ln) - 1]
        seen.add(r[si])
        toks = tokens(line)
        pos = 0
        for col, cell in zip(head, r):
            if col == "source" or (name, col) in DERIVED or name == "constants.csv" and col in ("name", "meaning"):
                continue
            for part in tokens(cell):  # a listed set or a fraction is several tokens
                try:
                    pos = toks.index(part, pos) + 1
                except ValueError:
                    errs.append(f"{name}: '{cell}' ({col}) is not in order in {r[si]}: {line.strip()}")
                    break
        if name == "prop9_dimension.csv":
            # h = -log z* with z* = exp(-h), where h is found here by Newton's method on f(h) = sum_n e^{-nh} - 1.
            A = [int(x) for x in r[head.index("A_delta_listed")].split()]
            want = ""
            if len(A) < 6:
                h = 0.5
                for _ in range(100):
                    f = sum(math.exp(-n * h) for n in A) - 1
                    h -= f / -sum(n * math.exp(-n * h) for n in A)
                want = f"{h:.6f}"
            # the renewal root itself must agree: dim = h / log(1/delta) to the six printed decimals
            if want and f"{h / math.log(1 / float(r[head.index('delta')])):.6f}" != r[head.index("dim_renewal")]:
                errs.append(f"{name}: dim_renewal {r[head.index('dim_renewal')]} is not h/log(1/delta) for the listed A")
            if r[head.index("entropy_h")] != want:
                errs.append(f"{name}: entropy_h {r[head.index('entropy_h')]} is not {want}")
    rel, test = COVER[name]
    if rel:
        must = {f"{rel}:{i}" for i, line in enumerate(expected_lines[rel], start=1) if test(line)}
        if must != seen:
            errs.append(f"{name}: rows {sorted(seen)} do not cover exactly the lines {sorted(must)}")
    return errs


def expected_lines():
    out = {}
    for dp, _, fns in os.walk(os.path.join(ROOT, "expected")):
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), ROOT)
            out[rel] = read(rel, ROOT).splitlines()
    return out


def zip_problems(data):
    errs = []
    try:
        names = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", COMMIT, "--", *ZIP_PATHS],
                               check=True, capture_output=True, text=True).stdout.split()
    except subprocess.CalledProcessError:
        return [f"commit {COMMIT} is not available (fetch the full history)"]
    z = zipfile.ZipFile(io.BytesIO(data))
    prefix = f"golden-window-resolution-{COMMIT[:7]}/"
    files = {n[len(prefix):]: n for n in z.namelist() if not n.endswith("/")}
    if sorted(files) != sorted(names):
        errs.append(f"{ZIP}: entries differ from the commit: {sorted(set(files) ^ set(names))[:5]}")
    for rel in names:
        if rel in files:
            want = subprocess.run(["git", "-C", ROOT, "show", f"{COMMIT}:{rel}"], check=True, capture_output=True).stdout
            if z.read(files[rel]) != want:
                errs.append(f"{ZIP}: {rel} differs from the commit")
    if z.comment.decode("ascii", "replace") != COMMIT:
        errs.append(f"{ZIP}: the zip comment is not the commit id")
    return errs


CLAIM = re.compile(r"novel|breakthrough|first time|for the first|groundbreaking|\bnew\b", re.I)
INSTITUTION = re.compile(r"universit|\binstitut|\bcollege\b|大学|研究所|研究機関", re.I)
DOI = re.compile(r"10\.\d{4,9}/[^\s,;)}\]`]+")


def wording_problems(texts):
    """texts: rel -> text for METADATA.md and the two .tex files."""
    errs = []
    meta = texts["METADATA.md"]
    exp = "\n".join("\n".join(v) for v in expected_lines().values())
    for rel, t in texts.items():
        flat = " ".join(t.split())
        for d in DOI.findall(t):
            if d.rstrip(".:") not in DOIS:
                errs.append(f"{rel}: DOI {d} is not one of the two DOIs of the papers")
        for m in CLAIM.finditer(flat):
            allowed = m.group().lower() == "new" and (
                flat[max(0, m.start() - 4):m.start()] == "not " and flat[m.end():m.end() + 12] == " mathematics"
                or flat[max(0, m.end() - 21):m.end()] == "How much of it is new")
            if not allowed:
                errs.append(f"{rel}: claim word '{m.group()}' ({flat[max(0, m.start() - 30):m.end() + 30]})")
        if INSTITUTION.search(flat):
            errs.append(f"{rel}: name of a university or institute")
        need = DISCLOSURE + ["Lu, Steiner and Zou", "not found in the texts read", "Takuya Nemoto", "0009-0000-1406-0547"]
        for n in need:
            if n not in flat:
                errs.append(f"{rel}: missing '{n}'")
        if rel.endswith(".tex"):
            if re.search(r"\\author(\[[^\]]*\])?\{(?![^}]*Takuya Nemoto)", t) or re.search(r"\\author[^\n]*Claude", t):
                errs.append(f"{rel}: the author is not Takuya Nemoto alone")
            for m in re.finditer(r"Claude", flat):
                if not (flat.startswith("Claude Code (Anthropic) was used", m.start()) or flat.startswith("Claude is not an author.", m.start())):
                    errs.append(f"{rel}: 'Claude' outside the disclosure ({flat[max(0, m.start() - 30):m.end() + 30]})")
            if "Theorem E (conditional)" not in flat and "\\block{Conditional}" not in t:
                errs.append(f"{rel}: Theorem E is not marked conditional")
            if "CC BY 4.0" not in flat:
                errs.append(f"{rel}: licence CC BY 4.0 missing")
            for num in re.findall(r"(?<![\d.])\d+\.\d{3,}", DOI.sub("", t)):
                if num not in exp:
                    errs.append(f"{rel}: the number {num} is not in expected/")
    # METADATA: one section per item, with its own disclosure, licence, title and author.
    sections = re.split(r"^## ", meta, flags=re.M)
    found = {}
    for s in sections[1:]:
        found[s.split("\n", 1)[0].strip()] = s
    for item in ITEMS:
        s = found.get(item)
        if s is None:
            errs.append(f"METADATA.md: no section for {item}")
            continue
        flat = " ".join(s.split())
        if f"- Item type: {item}" not in s:
            errs.append(f"METADATA.md: {item}: item type")
        title = re.search(r"^- Title: (.+)$", s, re.M)
        if not title or "golden-window conjecture" not in title.group(1).lower():
            errs.append(f"METADATA.md: {item}: the title does not name the golden-window conjecture")
        if "- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)" not in s or "Claude" in re.search(r"^- Authors: (.+)$", s, re.M).group(1):
            errs.append(f"METADATA.md: {item}: authors")
        lic = re.search(r"^- License: (.+)$", s, re.M)
        if not lic or lic.group(1) != ("MIT" if item == "Software" else "CC BY 4.0"):
            errs.append(f"METADATA.md: {item}: licence")
        for n in DISCLOSURE + ["Lu, Steiner and Zou", "not found in the texts read", "Theorem E is conditional"]:
            if n not in flat:
                errs.append(f"METADATA.md: {item}: missing '{n}'")
    for n in ["Funding: none", "Categories (candidates, not verified)", "分類（Categories）の名は確かめていません。"] + [f"DOI {d}" for d in sorted(DOIS)]:
        if n not in meta:
            errs.append(f"METADATA.md: missing '{n}'")
    return errs


def count_problems(readme_ja, readme_en, meta, actual):
    """actual: dict of the real counts."""
    errs = []
    checks = [
        ("README.md", readme_ja, r"Figshare に置く(五)つの品", "items", {"五": 5}),
        ("README.md", readme_ja, r"数表は (\d+) の CSV", "csv", None),
        ("README.md", readme_ja, r"(\d+) のファイルを含みます", "zipfiles", None),
        ("README.md", readme_ja, r"スライドは (\d+) 枚", "slides", None),
        ("README.md", readme_ja, r"縦で (\d+) 頁", "poster", None),
        ("README.en.md", readme_en, r"(five) items for Figshare", "items", {"five": 5}),
        ("README.en.md", readme_en, r"(\d+) CSV files", "csv", None),
        ("README.en.md", readme_en, r"holds (\d+) files", "zipfiles", None),
        ("README.en.md", readme_en, r"(\d+) slides", "slides", None),
        ("README.en.md", readme_en, r"portrait, (\d+) page", "poster", None),
        ("METADATA.md", meta, r"as (\d+) CSV files", "csv", None),
        ("METADATA.md", meta, r"\((\d+) files\)", "zipfiles", None),
        ("METADATA.md", meta, r"(\d+) slides \(16:9\)", "slides", None),
        ("METADATA.md", meta, r"poster \((\d+) page\)", "poster", None),
    ]
    for rel, text, pat, key, words in checks:
        m = re.search(pat, text)
        if not m:
            errs.append(f"{rel}: the sentence for {key} ('{pat}') is missing")
            continue
        got = words[m.group(1)] if words else int(m.group(1))
        if got != actual[key]:
            errs.append(f"{rel}: states {got} for {key}, actual {actual[key]}")
    if abs(actual["poster_w"] - 2383.94) > 2 or abs(actual["poster_h"] - 3370.39) > 2:
        errs.append(f"poster: page size {actual['poster_w']} x {actual['poster_h']} pt is not A0 portrait")
    return errs


def actual_counts():
    import pypdf
    p = pypdf.PdfReader(os.path.join(FS, "poster", "golden-window-poster.pdf"))
    box = p.pages[0].mediabox
    z = zipfile.ZipFile(os.path.join(FS, ZIP))
    return {"items": len([d for d in ("figure", "dataset", "software", "poster", "slides") if os.path.isdir(os.path.join(FS, d))]),
            "csv": len([f for f in os.listdir(os.path.join(FS, "dataset")) if f.endswith(".csv")]),
            "zipfiles": len([n for n in z.namelist() if not n.endswith("/")]),
            "slides": len(pypdf.PdfReader(os.path.join(FS, "slides", "golden-window-slides.pdf")).pages),
            "poster": len(p.pages), "poster_w": float(box.width), "poster_h": float(box.height)}


def wording_texts():
    return {"METADATA.md": read("METADATA.md"), "poster/golden-window-poster.tex": read("poster/golden-window-poster.tex"),
            "slides/golden-window-slides.tex": read("slides/golden-window-slides.tex")}


def png_note(a, b):
    """For a PNG that differs, say whether the pixels differ or only the encoding."""
    if not a.endswith(".png"):
        return ""
    from PIL import Image
    import zlib
    ia, ib = Image.open(a), Image.open(b)
    pa, pb = ia.tobytes(), ib.tobytes()
    same = ia.size == ib.size and ia.mode == ib.mode and pa == pb
    diff = sum(x != y for x, y in zip(pa, pb)) if len(pa) == len(pb) else -1
    return (f" (size {ia.size} {ia.mode} / {ib.size} {ib.mode}; pixels {'identical' if same else f'differ in {diff} bytes'};"
            f" info {sorted(ia.info.items())[:4]} / {sorted(ib.info.items())[:4]}; zlib {zlib.ZLIB_RUNTIME_VERSION})")


def rebuild_problems():
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, os.path.join(FS, "build.py"), "--out", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            return ["figshare/build.py failed:\n" + r.stdout[-2000:] + r.stderr[-2000:]]
        errs = []
        a, b = generated(FS), generated(tmp)
        if a != b:
            errs.append(f"the rebuild gives other files: {sorted(set(a) ^ set(b))}")
        for rel in sorted(set(a) & set(b)):
            if read(rel, FS, "rb") != read(rel, tmp, "rb"):
                errs.append(f"figshare/{rel}: the rebuild differs" + png_note(os.path.join(FS, rel), os.path.join(tmp, rel)))
        if read("SHA256SUMS") != read("SHA256SUMS", tmp):
            errs.append("figshare/SHA256SUMS: the rebuild differs")
        return errs


def all_problems():
    files = {rel: read(rel, FS, "rb") for rel in generated(FS)}
    errs = sums_problems(files, read("SHA256SUMS"))
    exp = expected_lines()
    for f in sorted(x for x in files if x.startswith("dataset/") and x.endswith(".csv")):
        name = os.path.basename(f)
        if name not in COVER:
            errs.append(f"{f}: no rule in COVER")
            continue
        errs += csv_problems(name, files[f].decode("utf-8"), exp)
    errs += zip_problems(files[ZIP])
    errs += wording_problems(wording_texts())
    errs += count_problems(read("README.md", ROOT), read("README.en.md", ROOT), read("METADATA.md"), actual_counts())
    return errs


def break_test():
    if all_problems():
        print("break test: the unbroken state already fails")
        return 1
    bad = 0

    def expect(what, errs):
        nonlocal bad
        print(f"  {'caught' if errs else 'MISSED'}: {what}")
        bad += not errs

    exp = expected_lines()
    t = read("dataset/theorem_B_upper_end.csv")
    t2 = t.replace("11.4760443557126", "11.4760443557127", 1)
    expect("a digit changed in a CSV cell", csv_problems("theorem_B_upper_end.csv", t2, exp))
    lines = t.splitlines(True)
    expect("a row dropped from a CSV file", csv_problems("theorem_B_upper_end.csv", "".join(lines[:5] + lines[6:]), exp))
    p = read("dataset/prop9_dimension.csv")
    row = p.splitlines()[1].split(",")
    expect("a derived cell changed", csv_problems("prop9_dimension.csv", p.replace("," + row[5] + ",", ",0.000001,", 1), exp))
    expect("a source line shifted", csv_problems("prop9_dimension.csv", p.replace("examples.out:2", "examples.out:3", 1), exp))
    files = {rel: read(rel, FS, "rb") for rel in generated(FS)}
    sums = read("SHA256SUMS")
    expect("a generated file changed after SHA256SUMS", sums_problems(dict(files, **{"METADATA.md": files["METADATA.md"] + b" "}), sums))
    expect("a generated file added", sums_problems(dict(files, **{"extra.txt": b"x"}), sums))
    zbuf = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(files[ZIP])) as zin, zipfile.ZipFile(zbuf, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info)
            if info.filename.endswith("scripts/curve/gw.py"):
                data += b"\n"
            zout.writestr(info, data)
        zout.comment = zin.comment
    expect("a script changed inside the zip", zip_problems(zbuf.getvalue()))
    w = wording_texts()
    for what, rel, old, new in (
            ("the disclosure sentence removed", "METADATA.md", "Claude is not an author.", "Claude helped."),
            ("Claude added as an author of the poster", "poster/golden-window-poster.tex", "Takuya Nemoto \\quad ORCID", "Takuya Nemoto and Claude \\quad ORCID"),
            ("Claude added as an author of the slides", "slides/golden-window-slides.tex", "\\author[Takuya Nemoto]{Takuya Nemoto", "\\author[Takuya Nemoto]{Claude and Takuya Nemoto"),
            ("the licence of the software changed", "METADATA.md", "- License: MIT", "- License: CC BY 4.0"),
            ("a DOI that was not received", "METADATA.md", "DOI 10.6084/m9.figshare.35050300:", "DOI 10.6084/m9.figshare.35050301:"),
            ("a claim word", "slides/golden-window-slides.tex", "not found in the texts read (application)", "a novel application"),
            ("'new' as a claim", "poster/golden-window-poster.tex", "Applications: not found in the texts read", "Applications: new"),
            ("a university named", "poster/golden-window-poster.tex", "Takuya Nemoto \\quad", "Takuya Nemoto, Some University \\quad"),
            ("a number not in expected/", "slides/golden-window-slides.tex", "0.32228461597103", "0.32228461597104"),
            ("the credit to Lu, Steiner and Zou removed", "poster/golden-window-poster.tex", "Lu, Steiner and Zou", "others"),
            ("the categories marked as verified", "METADATA.md", "(candidates, not verified)", "(verified)"),
            ("a title without the conjecture", "METADATA.md", "- Title: Resolution of the golden-window conjecture: poster", "- Title: A poster")):
        assert old in w[rel], (what, old)
        expect(what, wording_problems(dict(w, **{rel: w[rel].replace(old, new)})))
    ja, en, meta, act = read("README.md", ROOT), read("README.en.md", ROOT), read("METADATA.md"), actual_counts()
    expect("README states another number of CSV files", count_problems(ja.replace(f"数表は {act['csv']} の CSV", f"数表は {act['csv'] + 1} の CSV"), en, meta, act))
    expect("README.en states another number of slides", count_problems(ja, en.replace(f"{act['slides']} slides", f"{act['slides'] + 1} slides"), meta, act))
    expect("one more slide than stated", count_problems(ja, en, meta, dict(act, slides=act["slides"] + 1)))
    expect("the poster not A0", count_problems(ja, en, meta, dict(act, poster_w=2000.0)))
    print("break test: " + ("every change made the check fail, as it should" if not bad else f"{bad} problems"))
    return 1 if bad else 0


def main(argv):
    if "--break" in argv:
        return break_test()
    errs = all_problems()
    if "--rebuild" in argv:
        errs += rebuild_problems()
    print(f"figshare: {len(generated(FS))} generated files checked{' and rebuilt' if '--rebuild' in argv else ''}, {len(errs)} problems")
    for e in errs:
        print("  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
