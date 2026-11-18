# golden-window-resolution

Source, PDF and verification scripts of the paper "Resolution of the Golden-Window Conjecture and Related Results on β-Transformations with a Hole and on the Trinity-Infinity Series II Game".

[日本語](README.md)

The paper is on Figshare. Its DOI is [`10.6084/m9.figshare.35050300`](https://doi.org/10.6084/m9.figshare.35050300).
The number was received from the owner on 2026-11-18.
The content of the Figshare record it points to has not been checked.
It is a separate item, not a new version of the Figshare preprint of 2026-10-13 (`10.6084/m9.figshare.34419198`).

## About the paper

In a three-player repeated game with discount factor 1/φ < δ < 2/3, the pure-strategy equilibrium payoffs on one edge form a fractal.
The Figshare preprint `10.6084/m9.figshare.34419198` (2026-10-13) stated the golden-window conjecture about this set.
That preprint is frozen and keeps the conjecture as a conjecture.
This paper is a separate record that resolves it and adds results on the underlying open dynamical system.

Up to scaling, the set is the survivor set of the greedy β-transformation y ↦ βy mod 1, β = 1/δ, with the hole (t(β), 1), t(β) = (2 − β)/(β − 1).
This observation is not new mathematics.
Measure zero, the dimension formula and the bound dim < 1 are special cases of Lu, Steiner and Zou, Theorem 1.2 and Proposition 2.5.
The paper gives elementary proofs and credits these results to them.

## What is known and what is new

This is the status table of the paper (Status of each result).
"New" means "not found in the texts read", and nothing more is claimed.

| Result | Status |
| --- | --- |
| Measure zero (Proposition 8) | known (Lu–Steiner–Zou Prop. 2.5; Rényi, Parry) |
| Dimension formula and dim < 1 | known (Lu–Steiner–Zou Thm. 1.2) |
| Monotonicity, continuity and end limits along the curve | not found in the texts read |
| Theorems A and B (end rates), C (devil's staircase and plateaus), D (why 1/φ appears twice) | not found in the texts read |
| Exposed edges, the universal window, windows of linear dilemmas | not found in the texts read (application) |
| Theorem E (joint continuity for the hole at 0, β ≤ 2) | conditional on Lu–Steiner–Zou Thm. 1.4 |
| Entropy identity for lexicographic shifts on finite alphabets | map-level form due to Oliveira; a symbolic proof is given |
| The Trinity-Infinity papers checked, and the Series II game | the table of that part separates known results, results not found, and a result proved only at nine values |

## Contents

| Path | Contents |
| --- | --- |
| `paper/` | LaTeX source and the built PDF |
| `scripts/curve/` | numbers along the golden curve (Theorems A–E, the table of Proposition 9) |
| `scripts/edges/` | the generalization and the window tables |
| `scripts/symbolic/`, `scripts/symbolic-referee/` | the section on lexicographic shifts; the latter was written separately for the referee pass |
| `scripts/trinity/` | the part on the Trinity-Infinity papers and the Series II game |
| `expected/` | the output of each script; the checks compare byte for byte |
| `verification/` | the checks |

Every number printed in the paper is in the output of one of the scripts.
`verification/check_numbers.py` compares them, and it fails on any decimal with three or more places that has no entry.

```
python3 -m pip install -r requirements.txt
python3 verification/run_scripts.py
python3 verification/check_numbers.py
python3 verification/check_text.py
python3 verification/check_copies.py
```

## The three checks each result passed

In the referee pass, each part was put through three checks.
The first is a re-derivation of the proof.
The second and third are the scripts below.

| Result | Second (evaluating the formula) | Third (a computation that does not use it) |
| --- | --- | --- |
| Reduction to the β-transformation | `curve/membership.py` (exact rationals) | `edges/examples.py` (three roots and word counts) |
| Measure zero (Proposition 8) | `edges/check_misc.py` (hole sizes) | `edges/check_dichotomy.py` (shrinking lengths) |
| Proposition 9 | `edges/examples.py` (renewal and LSZ roots) | `curve/check_count.py` (cylinder counts), `edges/monotone.py` |
| Theorem A | `curve/t1_lower.py` | `curve/check_count2.py` |
| Theorem B | `curve/t2_upper.py`, `curve/t2_parry.py` | `curve/check_count2.py` |
| Theorem C | `curve/t3_plateaus.py` | `curve/check_count.py` (value on a plateau) |
| Theorem D | `curve/t4_why_phi.py` (symbolic) | `curve/t4_why_phi.py` (direct simulation of discounted sums, bisection) |
| Edge reduction, universal window | `edges/check_reduction.py`, `edges/check_universal.py` | `edges/check_misc.py` (Proposition 5 recovered) |
| Dilemma windows, monotonicity | `edges/examples.py` (closed forms) | `edges/edges.py` (exhaustive search), `edges/monotone.py` |
| Theorem E (conditional) | `curve/t5_hole0.py` | `curve/t5_jump.py` |
| Identity for lexicographic shifts | `symbolic/check1_series.py` | `symbolic-referee/bf.py` (separately written brute force) |
| Corollary and the β-rational fix | `symbolic-referee/cases.py` | `symbolic-referee/theta.py`, `symbolic-referee/empty.py` |
| Trinity-Infinity claims checked | `trinity/s2_claims.py` | `trinity/s1_s3_claims.py` |
| Equilibrium set on the face, payoff-gap bound | `trinity/face_check.py` | `trinity/run_diff_check.py` (outer approximation by the self-generation operator) |
| Never-sustainable payoffs | `trinity/run_aps_test.py` | `trinity/run_aps_face1.py` |
| The whole set for δ ≤ 1/√2 | `trinity/run_p23_exact.py`, `trinity/run_p23_infeas.py` (exact rational certificate) | `trinity/run_p23_scan.py`, `trinity/run_p23_gen.py`, `trinity/run_p23_facets.py` |
| Switching of the operator | `trinity/jsr_check.py` | `trinity/jsr_cycle.py` |
| Rotation thresholds for many players | `trinity/rot_asym.py` (200 digits) | `trinity/rot_asym.py` (direct sums of payoffs) |

## How the literature was read

The literature check was made on 2026-11-18.
The literature section of the paper separates what was read in full, what was read as an abstract only, and what is recalled.
The full texts of Berg–Kitti and of Mailath–Obara–Sekiguchi were not read.

## Use of a language model

Claude Code (Anthropic) was used to search and read the literature, to draft and check the proofs, to write the verification scripts and to draft the text.
The author is responsible for the content.
Claude is not an author.

## Licence

The paper and the prose are CC BY 4.0 (`LICENSE`); the scripts and checks are MIT (`LICENSE-CODE`).
