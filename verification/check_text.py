#!/usr/bin/env python3
"""Text checks for every file in this repository, and for the text of the PDF.

1. No institutional affiliation. The name of one particular university must not appear in
   any form: Latin or full-width letters, any letter case, with or without spaces, hyphens
   or a Japanese ending. The terms are assembled from parts below, so this file does not
   itself contain them.
2. No self-assigned titles and none of the items excluded by the owner's rules.
3. CITATION.cff has no affiliation field and does not list Claude as an author.
4. Each paper (the published one and continuity/paper/joint-continuity.tex) names Takuya Nemoto as its only
   author, keeps the disclosure of the use of a language model with the sentence "Claude is not an author.",
   and keeps the licence section (CC BY 4.0 for the paper, MIT for the scripts). Both PDFs are scanned.

  python3 verification/check_text.py           # the check
  python3 verification/check_text.py --break   # injects each variant in memory; every one must fail
"""
import os
import re
import sys
import unicodedata

def u(*cps):
    return "".join(chr(c) for c in cps)


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__"}
TEXT_EXT = {".md", ".tex", ".py", ".yml", ".yaml", ".cff", ".txt", ".json", ".log", ".out", ""}

Z = "z" + "en"
UNI = "univ"
DAI = (u(0x5927, 0x5b66))          # the two characters for "university"
KATA = (u(0x30bc, 0x30f3))          # katakana reading of the first part

PATTERNS = [
    (re.compile(Z + r"[\s\-_." + u(0x30fb) + "]*(" + DAI + "|" + UNI + ")"), "affiliation (university name)"),
    (re.compile(KATA + r"[\s" + u(0x30fb) + "]*" + DAI), "affiliation (university name, katakana)"),
    (re.compile(Z + r"\s*\.\s*ac\s*\.\s*jp"), "affiliation (university domain)"),
    (re.compile((u(0x72ec, 0x7acb, 0x7814, 0x7a76, 0x8005))), "self-assigned title"),
    (re.compile("independent" + r"\s+" + "researcher"), "self-assigned title"),
    (re.compile("consult" + ("ant|" + u(0x30b3, 0x30f3, 0x30b5, 0x30eb, 0x30bf, 0x30f3, 0x30c8))), "excluded title (rule 10)"),
    (re.compile((u(0x30e9, 0x30a4, 0x30d6, 0x914d, 0x4fe1) + "|live") + r"[\s-]*" + "stream"), "excluded activity (rule 10)"),
    (re.compile("sea" + ("land|" + u(0x30b7, 0x30fc, 0x30e9, 0x30f3, 0x30c9))), "excluded title (rule 10, the principality)"),
]


def norm(text):
    return unicodedata.normalize("NFKC", text).casefold()


def scan_text(name, text):
    hits = []
    t = norm(text)
    for pat, what in PATTERNS:
        for m in pat.finditer(t):
            line = t.count("\n", 0, m.start()) + 1
            hits.append(f"{name}:{line}: {what}")
    return hits


def files():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            yield os.path.join(dp, fn)


def pdf_text(path):
    try:
        import pypdf
    except ImportError:
        return None
    r = pypdf.PdfReader(path)
    meta = " ".join(str(v) for v in (r.metadata or {}).values())
    return meta + "\n" + "\n".join(p.extract_text() or "" for p in r.pages)


def citation_problems():
    p = os.path.join(ROOT, "CITATION.cff")
    if not os.path.exists(p):
        return ["CITATION.cff: missing"]
    t = open(p, encoding="utf-8").read()
    out = []
    if re.search(r"^\s*affiliation\s*:", t, re.M):
        out.append("CITATION.cff: has an affiliation field")
    authors = t.split("authors:", 1)[1].split("\n\S", 1)[0] if "authors:" in t else ""
    if "claude" in authors.lower() or "anthropic" in authors.lower():
        out.append("CITATION.cff: Claude or Anthropic listed among the authors")
    return out


PAPERS = ["paper/golden-window-resolution.tex", "continuity/paper/joint-continuity.tex"]
PDFS = ["paper/golden-window-resolution.pdf", "continuity/paper/joint-continuity.pdf"]


def paper_problems(rel, t):
    out = []
    authors = re.findall(r"\\author\{([^}]*)\}", t)
    if authors != ["Takuya Nemoto"]:
        out.append(f"{rel}: the author line is not exactly Takuya Nemoto ({authors})")
    for needle in (r"\section*{Disclosure of the use of a language model}", "Claude Code (Anthropic)",
                   "Claude is not an author.", r"\section*{Licence}", "(CC BY 4.0)", "MIT licence"):
        if needle not in " ".join(t.split()):
            out.append(f"{rel}: missing '{needle}'")
    return out


def papers():
    out = []
    for rel in PAPERS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            out.append(f"{rel}: missing")
            continue
        out += paper_problems(rel, open(p, encoding="utf-8").read())
    for rel in PDFS:
        if not os.path.exists(os.path.join(ROOT, rel)):
            out.append(f"{rel}: missing")
    return out


def run():
    hits = []
    pdfs = 0
    for path in files():
        rel = os.path.relpath(path, ROOT)
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            t = pdf_text(path)
            if t is None:
                hits.append(f"{rel}: pypdf is not installed, PDF not checked")
            else:
                pdfs += 1
                hits += scan_text(rel, t)
        elif ext in TEXT_EXT:
            try:
                t = open(path, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            hits += scan_text(rel, t)
    hits += citation_problems()
    hits += papers()
    return hits, pdfs


def break_test():
    variants = [
        Z.upper() + DAI, Z.upper() + " University", Z.capitalize() + " university",
        unicodedata.normalize("NFKC", Z.upper()).translate({ord(c): ord(c) + 0xFEE0 for c in "ZEN"}) + DAI,
        Z.upper() + "-Univ.", KATA + DAI, Z + ".ac.jp",
        "Independent " + "Researcher", (u(0x72ec, 0x7acb, 0x7814, 0x7a76, 0x8005)),
    ]
    bad = 0
    for v in variants:
        caught = bool(scan_text("injected", "Affiliation: " + v + "\n"))
        print(f"  {'caught' if caught else 'MISSED'}: {v!r}")
        bad += not caught
    if scan_text("clean", "Takuya Nemoto. No affiliation. citizen, frozen, Zenodo.\n"):
        print("  false positive on clean text")
        bad += 1
    for rel in PAPERS:
        t = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for old, new, what in (("Claude is not an author.", "", "disclosure sentence removed"),
                               (r"\author{Takuya Nemoto}", r"\author{Takuya Nemoto}\n\\author{Claude}", "Claude added as author"),
                               ("(CC BY 4.0)", "(CC BY-NC 4.0)", "licence changed")):
            caught = bool(paper_problems(rel, t.replace(old, new, 1)))
            print(f"  {'caught' if caught else 'MISSED'}: {rel}: {what}")
            bad += not caught
    return bad


def main(argv):
    if "--break" in argv:
        bad = break_test()
        print("break test: " + ("every variant failed the check, as it should" if not bad else f"{bad} problems"))
        return 1 if bad else 0
    hits, pdfs = run()
    print(f"text check: {pdfs} PDF(s) and all text files scanned, {len(hits)} problems")
    for h in hits:
        print("  " + h)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
