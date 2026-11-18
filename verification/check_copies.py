#!/usr/bin/env python3
"""Copies and metadata that must stay fixed.

1. SECURITY.md and .github/ISSUE_TEMPLATE/error-report.yml are byte-identical copies of the
   canonical files in cpsbvbng26-dotcom. Their SHA-256 at the time of copying is recorded here.
   When the canonical files change, the copies and these hashes change together; the
   cross-repository comparison itself is made from cpsbvbng26-dotcom.
2. The title in the LaTeX source, CITATION.cff and both READMEs is the same string.
3. The PDF exists and its metadata title matches.
"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIES = {
    "SECURITY.md": "973a9630e16e0e5f91efa9ebb870ed3bfb51cd4a2e53693c94e68e321187785d",
    ".github/ISSUE_TEMPLATE/error-report.yml": "1549c3901f58d162eefe6b414e9b09bb5975cab2377c7962fd4e93967f3ec19a",
}
TITLE = "Resolution of the Golden-Window Conjecture and Related Results on"
TITLE_END = "with a Hole and on the Trinity-Infinity Series II Game"
PDF = "paper/golden-window-resolution.pdf"


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def main():
    errs = []
    for rel, want in COPIES.items():
        with open(os.path.join(ROOT, rel), "rb") as fh:
            got = hashlib.sha256(fh.read()).hexdigest()
        if got != want:
            errs.append(f"{rel}: differs from the canonical copy (sha256 {got})")
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
    print(f"copies and metadata: {len(errs)} problems")
    for e in errs:
        print("  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
