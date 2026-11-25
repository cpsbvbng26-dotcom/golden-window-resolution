#!/usr/bin/env python3
"""Text checks for every file in this repository, and for the text of the PDF.

1. No institutional affiliation. The name of one particular university must not appear in
   any form: Latin or full-width letters, any letter case, with or without spaces, hyphens
   or a Japanese ending. The terms are assembled from parts below, so this file does not
   itself contain them.
2. No self-assigned titles and none of the items excluded by the owner's rules.
3. CITATION.cff has no affiliation field and does not list Claude as an author.
   Its version is the latest tag v* of this repository without the "v" (git must see the tags: the CI checks out
   with fetch-tags), the description of the Zenodo DOI of that version names it, and its date-released is the date
   that CHANGELOG.md gives for the publication of that version on GitHub (Japan time).
4. Each paper (the published one and continuity/paper/joint-continuity.tex) names Takuya Nemoto as its only
   author, keeps the disclosure of the use of a language model with the sentence "Claude is not an author.",
   and keeps the licence section (CC BY 4.0 for the paper, MIT for the scripts). Both PDFs are scanned.

  python3 verification/check_text.py           # the check
  python3 verification/check_text.py --break   # injects each variant in memory; every one must fail
"""
import os
import re
import subprocess
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
    out += version_problems(t, tags(), read_root("CHANGELOG.md"))
    return out


def tags():
    """The tags v* of this repository, newest version first, or None if git cannot list them."""
    try:
        out = subprocess.run(["git", "-C", ROOT, "tag", "--list", "v*"], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    vs = [t.strip() for t in out.splitlines() if re.fullmatch(r"v\d+(\.\d+)*", t.strip())]
    return sorted(vs, key=lambda t: tuple(int(x) for x in t[1:].split(".")), reverse=True)


def version_problems(t, tag_list, changelog):
    """CITATION.cff text t against the tags and CHANGELOG.md."""
    m = re.search(r'^version:\s*"?([^"\n]*?)"?\s*$', t, re.M)
    if not m:
        return ["CITATION.cff: no version field"]
    v = m.group(1)
    if not tag_list:
        return ["CITATION.cff: no tag v* is visible to git, so the version cannot be compared (fetch the tags)"]
    out = []
    if "v" + v != tag_list[0]:
        out.append(f"CITATION.cff: version {v} is not the latest tag {tag_list[0]}")
    if f'Zenodo archive of this repository, v{v}"' not in t:
        out.append(f"CITATION.cff: no identifier described as the Zenodo archive of v{v}")
    d = re.search(r'^date-released:\s*"?(\d{4}-\d{2}-\d{2})"?\s*$', t, re.M)
    c = re.search("版 v" + re.escape(v) + r" は、(\d{4}-\d{2}-\d{2})（日本時間）に GitHub で公開しました。", changelog or "")
    if not c:
        out.append(f"CHANGELOG.md: no date of the publication of v{v}")
    elif not d or d.group(1) != c.group(1):
        out.append(f"CITATION.cff: date-released {d.group(1) if d else 'missing'} is not the date of v{v} in CHANGELOG.md ({c.group(1)})")
    return out


def read_root(rel):
    p = os.path.join(ROOT, rel)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


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
    cff, log, tl = read_root("CITATION.cff"), read_root("CHANGELOG.md"), tags()
    if version_problems(cff, tl, log):
        print("  CITATION.cff already fails the version check")
        return bad + 1
    v = re.search(r'^version:\s*"?([^"\n]*?)"?\s*$', cff, re.M).group(1)
    nxt = "v" + ".".join(v.split(".")[:-1] + [str(int(v.split(".")[-1]) + 1)])
    for what, (t2, tl2, log2) in (
            ("version differs from the latest tag", (cff.replace(f'version: "{v}"', 'version: "9.9.9"'), tl, log)),
            ("version field removed", (re.sub(r"^version:.*\n", "", cff, flags=re.M), tl, log)),
            ("a newer tag " + nxt + " than the version", (cff, [nxt] + tl, log)),
            ("no tag visible", (cff, [], log)),
            ("the Zenodo DOI described for another version", (cff.replace(f"repository, v{v}\"", "repository, v0.9.0\""), tl, log)),
            ("date-released differs from CHANGELOG.md", (re.sub(r"^date-released:.*$", "date-released: 2026-11-18", cff, flags=re.M), tl, log)),
            ("CHANGELOG.md does not date the version", (cff, tl, log.replace(f"版 v{v} は、", f"版 v{v} を、"))),
    ):
        caught = bool(version_problems(t2, tl2, log2))
        print(f"  {'caught' if caught else 'MISSED'}: CITATION.cff: {what}")
        bad += not caught
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
