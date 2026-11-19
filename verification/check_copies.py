#!/usr/bin/env python3
"""Copies and metadata that must stay fixed.

1. SECURITY.md, .github/ISSUE_TEMPLATE/error-report.yml and .github/workflows/empty-issue.yml (2026-11-19)
   are byte-identical copies of the canonical files in cpsbvbng26-dotcom. So are the two files of the checked intake,
   .github/checked-intake/verify.js and .github/workflows/checked-intake.yml (2026-11-19): the error report form says
   that from 2026-12-01 it is checked by the checked intake, and the intake has to be here for that to be true.
   Its .github/checked-intake/config.json is this repository's own and is checked by `verify.js --check`.
   Their SHA-256 at the time of copying is recorded here.
   When the canonical files change, the copies and these hashes change together; the
   cross-repository comparison itself is made from cpsbvbng26-dotcom.
2. The title in the LaTeX source, CITATION.cff and both READMEs is the same string.
3. The PDF exists and its metadata title matches.
4. The second paper (continuity/paper/joint-continuity.tex): its title is in the LaTeX source, in the PDF metadata
   and in both READMEs; the page count that both READMEs state is the page count of its PDF.
5. Both PDFs are the recorded ones (SHA-256). The published PDF is frozen (rule 2), and the second PDF is the
   one recorded in continuity/REFEREE.md. A rebuilt PDF changes the hash, and the record changes with it.
6. .zenodo.json (2026-11-19), which Zenodo's GitHub integration reads at a release: its title begins with the title of the
   paper, its one creator is Takuya Nemoto with the ORCID iD and no affiliation, its licence is that of LICENSE, its notes
   carry the disclosure ("Claude is not an author.") and say what the licence field covers, and it points to the Figshare
   DOI of the paper as the work this record supplements.

  python3 verification/check_copies.py           # the check
  python3 verification/check_copies.py --break   # changes titles, a page count, a hash and .zenodo.json in memory; each must fail
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIES = {
    "SECURITY.md": "973a9630e16e0e5f91efa9ebb870ed3bfb51cd4a2e53693c94e68e321187785d",
    ".github/ISSUE_TEMPLATE/error-report.yml": "804c65aaf92d2032cd63d9bd36cc5bd4cbaf7edf97de74faf8bdb76f03a04c96",
    ".github/workflows/empty-issue.yml": "8a5ce275946c4e9258d2775be2cccd0ee39d8c54bf16baf97885a1aef4d3b072",
    ".github/checked-intake/verify.js": "640a886749427c3a92ddde825ad93b9f616541b14c47ca1f49a3adcf3cb1ab8c",
    ".github/workflows/checked-intake.yml": "66a93337e8a56c3ab35a4045764fe54350b165ba97c0139ce5d9ed6b9f669a5d",
}
TITLE = "Resolution of the Golden-Window Conjecture and Related Results on"
TITLE_END = "with a Hole and on the Trinity-Infinity Series II Game"
PDF = "paper/golden-window-resolution.pdf"
CONT_TEX = "continuity/paper/joint-continuity.tex"
CONT_PDF = "continuity/paper/joint-continuity.pdf"
CONT_TITLE = ["Joint Continuity in", "of the Hausdorff Dimension of Survivor Sets of",
              "Transformations with a Hole at", "for All"]
PDF_SHA256 = {
    PDF: "2b1023bc348571ee01204e4810e4be9b1f1809049858014c631a260cde760b4c",
    CONT_PDF: "b10fbd7b0233bd1bf2322407a4a6d87708dea68d92d1dffa432eafdd22a7ec13",
}
PAGES = {"README.md": r"紙面は (\d+) 頁です", "README.en.md": r"The paper has (\d+) pages"}


def zenodo_problems(ztext, licence):
    import json
    try:
        z = json.loads(ztext)
    except ValueError:
        return [".zenodo.json: cannot be read"]
    errs = []
    if not z.get("title", "").startswith(TITLE) or TITLE_END not in z.get("title", ""):
        errs.append(".zenodo.json: the title does not begin with the title of the paper")
    if z.get("creators") != [{"name": "Nemoto, Takuya", "orcid": "0009-0000-1406-0547"}]:
        errs.append(".zenodo.json: the creator (one, with the ORCID iD, no affiliation)")
    if z.get("license") != ("cc-by-4.0" if licence.startswith("Creative Commons Attribution 4.0") else "?"):
        errs.append(".zenodo.json: the licence is not that of LICENSE")
    notes = z.get("notes", "")
    if "Claude is not an author." not in notes or not re.search(r"The licence field of this record covers .+? only\.", notes):
        errs.append(".zenodo.json: the notes lack the disclosure or the sentence on the licence field")
    if {"identifier": "10.6084/m9.figshare.35050300", "relation": "isSupplementTo", "scheme": "doi"} not in z.get("related_identifiers", []):
        errs.append(".zenodo.json: the Figshare DOI of the paper is not the work this record supplements")
    return errs


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def copy_problems(copy_hashes):
    """copy_hashes: rel -> sha256 of the file, or None when it is missing."""
    errs = []
    for rel, want in COPIES.items():
        got = copy_hashes.get(rel)
        if got is None:
            errs.append(f"{rel}: missing")
        elif got != want:
            errs.append(f"{rel}: differs from the canonical copy (sha256 {got})")
    return errs


def copy_hashes():
    out = {}
    for rel in COPIES:
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            with open(p, "rb") as fh:
                out[rel] = hashlib.sha256(fh.read()).hexdigest()
        else:
            out[rel] = None
    return out


def check(texts, pdf_meta, pdf_pages, pdf_hashes):
    """texts: rel -> text; pdf_meta: rel -> title; pdf_pages: rel -> page count; pdf_hashes: rel -> sha256."""
    errs = []
    for rel in [CONT_TEX, "README.md", "README.en.md"]:
        if any(part not in texts[rel] for part in CONT_TITLE):
            errs.append(f"{rel}: title of the second paper missing or changed")
    if any(part not in pdf_meta.get(CONT_PDF, "") for part in CONT_TITLE):
        errs.append(f"{CONT_PDF}: metadata title missing or changed")
    for rel, pat in PAGES.items():
        m = re.search(pat, texts[rel])
        if not m or int(m.group(1)) != pdf_pages.get(CONT_PDF):
            errs.append(f"{rel}: the stated page count of the second paper is not that of {CONT_PDF} ({pdf_pages.get(CONT_PDF)})")
    for rel, want in PDF_SHA256.items():
        if pdf_hashes.get(rel) != want:
            errs.append(f"{rel}: sha256 {pdf_hashes.get(rel)} is not the recorded {want}")
    return errs


def second_paper():
    texts = {rel: read(rel) for rel in [CONT_TEX, "README.md", "README.en.md"]}
    meta, pages, hashes = {}, {}, {}
    for rel in PDF_SHA256:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        with open(p, "rb") as fh:
            hashes[rel] = hashlib.sha256(fh.read()).hexdigest()
    try:
        import pypdf
        r = pypdf.PdfReader(os.path.join(ROOT, CONT_PDF))
        meta[CONT_PDF] = str((r.metadata or {}).get("/Title", ""))
        pages[CONT_PDF] = len(r.pages)
    except (ImportError, FileNotFoundError):
        pass
    return texts, meta, pages, hashes


def break_test():
    texts, meta, pages, hashes = second_paper()
    if check(texts, meta, pages, hashes):
        print("break test: the unbroken state already fails")
        return 1
    bad = 0
    t2 = dict(texts)
    t2[CONT_TEX] = t2[CONT_TEX].replace("Joint Continuity in", "Continuity in")
    m2 = {CONT_PDF: meta[CONT_PDF].replace("Survivor Sets", "Survivor sets")}
    p2 = {CONT_PDF: pages[CONT_PDF] + 1}
    h2 = dict(hashes)
    h2[PDF] = "0" * 64
    for what, args in (("title in the source", (t2, meta, pages, hashes)), ("title in the PDF", (texts, m2, pages, hashes)),
                       ("page count", (texts, meta, p2, hashes)), ("hash of the frozen PDF", (texts, meta, pages, h2))):
        caught = bool(check(*args))
        print(f"  {'caught' if caught else 'MISSED'}: {what}")
        bad += not caught
    ch = copy_hashes()
    if copy_problems(ch):
        print("break test: the unbroken copies already fail")
        return 1
    for what, broken in (("a changed copy of the checked intake", dict(ch, **{".github/checked-intake/verify.js": "0" * 64})),
                         ("a missing workflow of the checked intake", dict(ch, **{".github/workflows/checked-intake.yml": None}))):
        caught = bool(copy_problems(broken))
        print(f"  {'caught' if caught else 'MISSED'}: {what}")
        bad += not caught
    z, lic = read(".zenodo.json"), read("LICENSE")
    if zenodo_problems(z, lic):
        print("break test: .zenodo.json already fails")
        return 1
    for what, broken in (("the disclosure in .zenodo.json", z.replace("Claude is not an author.", "Claude helped.")),
                         ("an affiliation in .zenodo.json", z.replace('"orcid": "0009-0000-1406-0547"', '"orcid": "0009-0000-1406-0547", "affiliation": "x"')),
                         ("the licence in .zenodo.json", z.replace('"license": "cc-by-4.0"', '"license": "mit"')),
                         ("the title in .zenodo.json", z.replace('"title": "Resolution of the Golden-Window Conjecture', '"title": "On the Golden-Window Conjecture')),
                         ("the end of the title in .zenodo.json", z.replace("Trinity-Infinity Series II Game:", "Trinity-Infinity Game:")),
                         ("the Figshare DOI in .zenodo.json", z.replace("10.6084/m9.figshare.35050300\",\n      \"relation\": \"isSupplementTo", "10.6084/m9.figshare.35050301\",\n      \"relation\": \"isSupplementTo"))):
        caught = bool(zenodo_problems(broken, lic))
        print(f"  {'caught' if caught else 'MISSED'}: {what}")
        bad += not caught
    print("break test: " + ("every change made the check fail, as it should" if not bad else f"{bad} problems"))
    return 1 if bad else 0


def main():
    if "--break" in sys.argv[1:]:
        return break_test()
    errs = copy_problems(copy_hashes())
    for rel in ["paper/golden-window-resolution.tex", "CITATION.cff", "README.md", "README.en.md"]:
        text = read(rel).replace("Series~II", "Series II")
        if TITLE not in text or TITLE_END not in text:
            errs.append(f"{rel}: title missing or changed")
    try:
        import pypdf
        meta = pypdf.PdfReader(os.path.join(ROOT, PDF)).metadata or {}
        if TITLE not in str(meta.get("/Title", "")) or TITLE_END not in str(meta.get("/Title", "")):
            errs.append(f"{PDF}: metadata title missing or changed")
    except ImportError:
        errs.append("pypdf is not installed")
    except FileNotFoundError:
        errs.append(f"{PDF}: missing")
    errs += check(*second_paper())
    errs += zenodo_problems(read(".zenodo.json"), read("LICENSE"))
    print(f"copies and metadata: {len(errs)} problems")
    for e in errs:
        print("  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
