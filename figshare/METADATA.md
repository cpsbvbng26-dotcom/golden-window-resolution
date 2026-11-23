# Figshare に置く五つの品の欄

このファイルは `figshare/build.py` が書いています。手で直さず、台本を直して作り直します。
Figshare の登録の欄に貼る文面を、品ごとに並べました。欄の値は英語です。
Figshare への登録は、所有者のアカウントで行うものです。Claude には触れられません。
DOI は、リポジトリにすでにある二つだけを書いています。新しい品の DOI は、登録のあとで決まります。

## 五つに共通する欄

- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- Keywords: golden-window conjecture; beta-transformation; open dynamical system; survivor set; Hausdorff dimension; repeated game; subgame-perfect equilibrium; golden ratio
- Categories (candidates, not verified): Ordinary differential equations, difference equations and dynamical systems; Pure mathematics not elsewhere classified; Mathematical economics
- Funding: none
- Related materials:
  - DOI 10.6084/m9.figshare.35050300: the paper that resolves the conjecture (relation: IsSupplementTo)
  - DOI 10.6084/m9.figshare.34419198: the preprint that stated the conjecture (relation: References)
  - URL https://github.com/cpsbvbng26-dotcom/golden-window-resolution: the repository of the scripts and of these files (relation: IsSupplementTo)

分類（Categories）の名は確かめていません。
作業の環境から figshare.com と api.figshare.com に届かず、2026-11-24（日本時間）に分類の一覧を読めませんでした。
上の三つは、Figshare が使う分類の体系（ANZSRC FoR 2020）にあると記憶している名で、候補です。
関係の名（IsSupplementTo、References）も、DataCite の関係の型の名として記憶しているもので、Figshare の画面での表記は確かめていません。

開示の文は、五つの description の末尾に同じものを置いています。

## Figure

- Item type: Figure
- Title: Survivor sets and dimension across the window of the golden-window conjecture
- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- License: CC BY 4.0
- Files: `figshare/figure/golden-window-figure.png`, `figshare/figure/golden-window-figure.svg`
- Description:

```
Two panels sharing the axis of the discount factor delta over the window 1/phi < delta < 2/3 of the golden-window conjecture. (a) The survivor set K_delta = {y in [0,1): T_beta^n(y) <= t(beta) for all n >= 0} of the greedy beta-transformation T_beta(y) = beta*y mod 1, beta = 1/delta, with the hole (t(beta), 1), t(beta) = (2 - beta)/(beta - 1), shaded above the curve t(beta). K_delta is delta times the survivor set S of the game recursion of the paper; the set T_delta of equilibrium payoffs on one edge of the three-player game is contained in two affine images of S and contains one of them, so it has the same dimension. It is drawn at 480 values of delta as 39947 vertical segments. This is a finite computation, not the limit set: pieces of the survivor set are subdivided until shorter than 1/2000 and gaps shorter than 1/2000 are closed, so every point of K_delta lies on a drawn segment and every drawn point lies within 0.00075 of a point of K_delta. Gaps narrower than that are not shown. (b) dim_H K_delta = h(delta)/log beta from the renewal equation sum_{n in A_delta} delta^(n s) = 1 (Theorem 3.2 of the paper), at the same values of delta, with the forced path cut after 800 steps; the points are the 7 values of Table 5 of the paper, which the script checks against the curve to 10^-6. The plateaus of the entropy (Theorem C) are visible as flat stretches. The figure does not show the set T_delta itself, the dimension at the two ends of the window, or any delta outside the window. Made with matplotlib by figshare/build.py in the repository. Measure zero, the dimension formula and the bound dim < 1 are special cases of a theorem of Lu, Steiner and Zou; the credit for them is theirs. The monotonicity, continuity and end limits along the curve t = t(beta), Theorems A, B, C and D, and the applications to exposed edges were not found in the texts read; nothing more is claimed. Theorem E is conditional on Theorem 1.4 of Lu, Steiner and Zou. This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write and run the verification scripts, and to draft the text. The author is responsible for the content. Claude is not an author.
```

## Dataset

- Item type: Dataset
- Title: Numerical tables for the resolution of the golden-window conjecture (CSV)
- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- License: CC BY 4.0
- Files: `figshare/dataset/*.csv`, `figshare/dataset/README.md`
- Description:

```
The tables of the paper as 11 CSV files: dimension along the curve by three methods (Table 5 of the paper), the lower and upper ends (Theorems A and B), a plateau of the entropy (Theorem C), the thresholds of Theorem D, the windows on the three-player edges (Table 1), the check of the reduction, the monotonicity scan on edges, and the printed constants. Every value is the character string printed by a script of the repository (expected/ at the commit of the software item); the column `source` names the file and line. One column (entropy_h in prop9_dimension.csv) is derived and marked as such. README.md is the data dictionary. Measure zero, the dimension formula and the bound dim < 1 are special cases of a theorem of Lu, Steiner and Zou; the credit for them is theirs. The monotonicity, continuity and end limits along the curve t = t(beta), Theorems A, B, C and D, and the applications to exposed edges were not found in the texts read; nothing more is claimed. Theorem E is conditional on Theorem 1.4 of Lu, Steiner and Zou. This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write and run the verification scripts, and to draft the text. The author is responsible for the content. Claude is not an author.
```

## Software

- Item type: Software
- Title: Verification scripts for the resolution of the golden-window conjecture (commit c2a47fd)
- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- License: MIT
- Files: `figshare/software/golden-window-resolution-scripts-c2a47fd.zip`, `figshare/software/README.md`
- Description:

```
git archive of commit c2a47fd9fd1a4cbd9940e0ec78895b47689f9313 of https://github.com/cpsbvbng26-dotcom/golden-window-resolution: 54 Python scripts and modules that compute the numbers of the paper, the 38 expected outputs of the scripts that print, and the runner that compares the two byte for byte (95 files). The scripts use exact rationals (Python fractions) and mpmath at 30 to 250 digits, with fixed seeds. README.md lists the contents and how to run them. Measure zero, the dimension formula and the bound dim < 1 are special cases of a theorem of Lu, Steiner and Zou; the credit for them is theirs. The monotonicity, continuity and end limits along the curve t = t(beta), Theorems A, B, C and D, and the applications to exposed edges were not found in the texts read; nothing more is claimed. Theorem E is conditional on Theorem 1.4 of Lu, Steiner and Zou. This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write and run the verification scripts, and to draft the text. The author is responsible for the content. Claude is not an author.
```

## Poster

- Item type: Poster
- Title: Resolution of the golden-window conjecture: poster
- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- License: CC BY 4.0
- Files: `figshare/poster/golden-window-poster.pdf`, `figshare/poster/golden-window-poster.tex`
- Description:

```
An A0 portrait poster (1 page) of the paper: the game and the golden-window conjecture, the reduction to a beta-transformation with a hole, the known results with their credit, the results along the curve, the applications, the conditional Theorem E, the status of each result, and Table 5. LaTeX source included. Measure zero, the dimension formula and the bound dim < 1 are special cases of a theorem of Lu, Steiner and Zou; the credit for them is theirs. The monotonicity, continuity and end limits along the curve t = t(beta), Theorems A, B, C and D, and the applications to exposed edges were not found in the texts read; nothing more is claimed. Theorem E is conditional on Theorem 1.4 of Lu, Steiner and Zou. This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write and run the verification scripts, and to draft the text. The author is responsible for the content. Claude is not an author.
```

## Presentation

- Item type: Presentation
- Title: Resolution of the golden-window conjecture: slides
- Authors: Takuya Nemoto (ORCID 0009-0000-1406-0547)
- License: CC BY 4.0
- Files: `figshare/slides/golden-window-slides.pdf`, `figshare/slides/golden-window-slides.tex`
- Description:

```
11 slides (16:9) on the paper, in the same order as the poster, ending with the status of each result and the disclosure. LaTeX source included. Measure zero, the dimension formula and the bound dim < 1 are special cases of a theorem of Lu, Steiner and Zou; the credit for them is theirs. The monotonicity, continuity and end limits along the curve t = t(beta), Theorems A, B, C and D, and the applications to exposed edges were not found in the texts read; nothing more is claimed. Theorem E is conditional on Theorem 1.4 of Lu, Steiner and Zou. This work has not been peer reviewed. How much of it is new will be settled by peer review and by formalization. The work was done without an advisor. Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write and run the verification scripts, and to draft the text. The author is responsible for the content. Claude is not an author.
```
