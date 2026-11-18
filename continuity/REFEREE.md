# Referee record: the continuity paper

Paper: `continuity/paper/joint-continuity.tex` and its PDF `continuity/paper/joint-continuity.pdf` (dated 19 November 2026).
`verification/check_copies.py` holds the SHA-256 of the PDF and checks it; the READMEs state its page count, which the same check compares with the PDF.
The paper is not yet deposited, and no DOI has been received.

The pass follows rule 14 of this repository: re-derive the main claims, compare every number with the scripts, compare every quotation with the texts read, and record which three checks each result passed.

## Who read what

- The proof of Theorem IA (support lemma) was read three times before this pass.
  The first reading is the author's draft and its second derivation for eventually periodic pairs.
  The second is a line-by-line reading in the main working session.
  The third is an independent referee in a separate session, with its own entropy code and its own numerics.
- That referee found the proof correct, with presentational gaps only.
  Its four fixes are in the paper:
  readable letters satisfy x_t ≥ ℓ_t (Lemma 4.5, synchronisation);
  the dichotomy is about the induced distribution of first-return words (Proposition 4.7, step 2);
  Y^μ_D is non-empty for large D (Theorem IA, step 3);
  and the third bullet of the product rule is proved from L ≽ a (Lemma 4.1).
- This pass was made after the draft was complete.
  It re-derived every statement of Sections 2 to 5 a second time, compared the numbers and the quotations, and cross-checked the entropy code against two codes written earlier and outside this repository.
  All of this pass, like the earlier readings, was carried out with Claude Code.
  It is not a specialist's check.

## What this pass found and changed

1. Lemma 4.1 (product rule).
   The second statement spoke of the left component "reaching σ^D a".
   For an eventually periodic a, different shifts can be equal, so the phrase was ambiguous.
   It now counts the letters read since the last reset (the depth index), which is also what the scripts compute.
2. Lemma 5.3 (sandwich).
   One sentence justified y ≼ g₀ by a tail bound proved later from y ≼ g₀.
   It is replaced by a direct argument: a greedy expansion is the lexicographically largest expansion of its number.
3. Lemma 3.1.
   Monotonicity of K was stated on [0, λ′) and used at λ′ in the proof of Theorem 3.2.
   The statement now covers [0, λ′] ∩ [0, 1), by continuity of K.
4. Lemma 5.2 (1) was reworded so that it states an inequality, not a characterization.
5. The example after Proposition 4.7.
   The draft said that the isolated end a = 02^∞ lies only in supports of measures of entropy 0.
   It lies in the support of no invariant measure; the paper now says so, with a one-line proof.
6. The inputs of Corollary E.
   The task named Lemmas 4.1(ii) and 4.2(i) of Allaart and Kong as conditions.
   The re-derivation uses Lemma 4.1(i) and the main statement of Lemma 4.2 (σⁿb(t, β) ≺ α(β)).
   Parts 4.1(ii) and 4.2(i) to (iii) describe the one-sided limits; they show that the sandwich of Lemma 5.3 cannot be narrowed, and are not needed for the inequalities.
   The corollary is stated as conditional on Lemmas 4.1 and 4.2 as a whole, and Remark 5.4(a) says which parts the proof uses.
7. The source of Lemma 6.2 of Allaart and Kong.
   The published paper (`10.6084/m9.figshare.35050300`, proof of Corollary 7.2 and its literature section) names Raith's 1989 paper.
   Allaart and Kong cite as [26] Raith's 1994 paper in Acta Math. Univ. Comenianae.
   The statement used is the same.
   The new paper records the discrepancy in its literature section.
   The published PDF is frozen and was not changed.
   No errata file for it exists in this repository.
8. Roots where K touches 1.
   The independent referee's root finder searches a grid for K ≥ 1 and misses a root where K touches 1 without crossing.
   This pass met one more such pair, (001^∞, 2(01)^∞) over {0, 1, 2}, where K touches 1 at 1/φ.
   There the grid gives 0, while the raw automaton and the exact isolation both give log φ.
   The mismatch that the referee recorded at (02^∞, 31^∞) is the same effect.
   The scripts of this repository isolate the roots exactly on the square-free part of an integer polynomial, and `oracle.py` prints the double root of (02^∞, 31^∞) as a test.
9. The number checker.
   A number glued to a macro (`\approx3.30…`, `\le30`) was invisible to the extraction of numbers from the source.
   `verification/check_numbers_continuity.py` now separates them; before the change it reported two printed numbers, β₀ and t₀ of Section 7, as missing from the paper.

## Three checks per result

Check (i) is always the proof, re-derived by this pass.

| Result | (ii) | (iii) |
| --- | --- | --- |
| Theorem A (recalled) | `oracle.py`: exact word counts against the series, entropies against the raw automaton | referee pass of the published paper; Oliveira's map-level formula |
| Proposition 2.2, Lemma 4.1 | `oracle.py`: the four-case rule and the product rule on every edge | the independent referee's reading |
| Theorem 3.2 | Example 3.3 in `hunt.py` (entropy moves continuously while the normalization jumps) | the binary analogue, Lu–Steiner–Zou Lemma 3.6, has the same two cases |
| Proposition 3.5 | `hunt.py`: the outer end of each bracket is never below h (asserted for every pair) | slow but monotone convergence at entropy 0 (`hunt.py`) |
| Proposition 3.7, Remark 3.8 | `hunt.py`: brackets close at every pair with h > 0 | the independent referee's continuity hunt |
| Lemmas 4.2, 4.3, Proposition 4.4 | `ia_witness.py`: h(Y_D) from the depth-bounded automaton equals the raw automaton of (a\|D M^∞, b\|D 0^∞) | `witnesses.py`: exact checks of (p_D, q_D) and Theorem A at (p_D, q_D) |
| Lemmas 4.5, 4.6, Proposition 4.7 | `witnesses.py`: the ends in a component of radius > 1 are approached, with no mixed case | second derivation for eventually periodic pairs (finite graphs) and the independent referee's reading |
| Theorem IA | `ia_witness.py` on random and delicate pairs, M = 1 to 4 | the independent referee's own numerics, including pairs that are not eventually periodic |
| Corollary C | `hunt.py` on pairs that are not normalized | for M = 1, Labarca–Moreira as quoted by Lu–Steiner–Zou |
| Lemmas 5.1, 5.2, 5.3 | re-derived twice (published Theorem E, β ≤ 2, and here for digits up to M) | `realmap.py`: both expansions jump at the test point |
| Corollary E | `realmap.py`: real-map estimates, no symbolic input, converge to Theorem A's value from eight directions | for β ≤ 2 it is Theorem E of the published paper, which had its own referee pass and numerics |

## Numbers

- `python3 verification/check_numbers_continuity.py`: every entry is supported by an output, and no decimal with three or more places and no m·10^{e} lacks an entry.
  `--break` changes five printed numbers in memory, one at a time, and each change fails.
- Every script was run twice; the outputs were byte-identical.
  With `LEXLIB_AUDIT=1`, no printed value lies within the rounding margin of a different printed text.
- Outside the repository, the raw automaton of `lexlib.py` was compared with the independent referee's code and with the author's earlier subset automaton on random pairs that are not normalized, and h(Y_D) with the referee's inner approximants.
  The two agree to rounding.
  These comparisons used files of the working session and are not part of CI.
- Several printed values coincide with outputs of earlier, separate code: the gaps of ((02)^∞, (210)^∞), the worst brackets of the second set of `hunt.py`, the values at entropy 0, and Example 3.3.

## Quotations

Each quotation was compared with the extracted text of its source, word by word.
Mathematical symbols were transcribed by hand and compared by eye.

| Quotation | Source text |
| --- | --- |
| Remark 1.10 | Allaart–Kong, arXiv 2109.10012v2 |
| Remark 1.2, Lemma 6.2, Lemmas 4.1, 4.2, the hole [0, t) | Allaart–Kong, arXiv 2411.03516v3 |
| the sentence on Labarca and Moreira | Lu–Steiner–Zou, arXiv 2509.04227v2 |
| Theorem 1.2 | Bandtlow–Rugh, arXiv 1510.06043v2 |
| the paragraph on Raith, Proposition 2.5 | Kalle–Kong–Langeveld–Li, arXiv 1803.07338v1 |

All match.
The two phrases in quotation marks that are not quotations ("Not found in the texts read", "pending comparison") are the paper's own terms.

## What remains uncertain

- Theorem A and Theorem IA have had no outside referee.
- Input (I1) rests on Raith's 1994 paper, which was not read.
- The translation from Bandtlow–Rugh's Theorem 1.2 to Corollary C for M ≥ 2 was not carried out.
  If it works, Corollary C is known as a statement, and only its symbolic proof is new.
- No new systematic literature search was run for this note.
  Bandtlow–Rugh was found by the independent referee, and Kalle–Kong–Langeveld–Li was among the texts fetched before.
  Raith's 1992 paper may treat perturbations of the map; it was not checked.
- The numerics cannot prove continuity.
  At the test point of `realmap.py` the entropy is log 3, so the point tests the jumps of the expansions, not a steep slope.
