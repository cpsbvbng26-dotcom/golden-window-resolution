# Theorem A against an automaton that uses neither Theorem A nor normalization.
#
# For random normalized pairs (a, b) over {0..M}, M = 1..4 (pre-period <= 3, period <= 5, seed 2611):
#   (1) the exact numbers of words N_n of Sigma_{a,b}, n <= 30, counted as paths of the raw automaton, equal the
#       coefficients of 1/((1 - z)(1 - K(z))), K = sum (b_n - a_n) z^n (exact integers);
#   (2) the entropy -log(lambda) of Theorem A (exact root isolation) equals the log of the spectral radius of
#       the raw automaton.
#   (3) Lemma P: on every edge of Theorem A's automaton (states (L, R) = shifts of a and b), the four-case rule of
#       Step 1 gives the same next state as the product rule L' = sigma L if c = L_1, L' = a if c > L_1, and
#       R' = sigma R if c = R_1, R' = b if c < R_1.
# Then three hand cases: a double root (K touches 1), the point of Section 6 where the spread is 3, and a
# pair that is not normalized, where the series of Theorem A does not count words (negative control).
import random

from lexlib import fixed, canon, dig, lexcmp, shift, normalized, raw_H, raw_counts, series_counts, thmA_h, thmA_root, show

random.seed(2611)
NMAX = 30
PER_M = 60


def rnd(M):
    return canon(tuple(random.randint(0, M) for _ in range(random.randint(0, 3))),
                 tuple(random.randint(0, M) for _ in range(random.randint(1, 5))))


def lemma_p_violations(a, b):
    """Explore Theorem A's automaton on actual sequences; count edges where the two rules disagree."""
    start = (a, b)
    seen, stack, edges, bad = {start}, [start], 0, 0
    while stack:
        L, R = stack.pop()
        l1, r1 = dig(L, 0), dig(R, 0)
        for c in range(l1, r1 + 1):
            if l1 < c < r1:
                four = (a, b)
            elif c == l1 < r1:
                four = (shift(L, 1), b)
            elif l1 < c == r1:
                four = (a, shift(R, 1))
            else:
                four = (shift(L, 1), shift(R, 1))
            prod = (shift(L, 1) if c == l1 else a, shift(R, 1) if c == r1 else b)
            edges += 1
            bad += four != prod
            if four not in seen:
                seen.add(four)
                stack.append(four)
    return edges, bad


total = bad_counts = 0
p_edges = p_bad = 0
worst = 0.0
for M in (1, 2, 3, 4):
    n = pos = mism = 0
    wM = 0.0
    while n < PER_M:
        a, b = rnd(M), rnd(M)
        if lexcmp(a, b) >= 0 or not normalized(a, b):
            continue
        n += 1
        if raw_counts(a, b, M, NMAX) != series_counts(a, b, NMAX):
            mism += 1
        e, v = lemma_p_violations(a, b)
        p_edges += e
        p_bad += v
        hr, ha = raw_H(a, b, M), thmA_h(a, b)
        pos += hr > 0
        wM = max(wM, abs(hr - ha))
    total += n
    bad_counts += mism
    worst = max(worst, wM)
    print('M=%d: %d normalized pairs (%d with h > 0); word counts N_n, n <= %d: %d mismatches; '
          'max |h(Theorem A) - h(automaton)| < 1e-12: %s' % (M, n, pos, NMAX, mism, wM < 1e-12))
print('all: %d pairs, %d word-count mismatches, entropies agree to 1e-12: %s' % (total, bad_counts, worst < 1e-12))
print('Lemma P: %d edges of the automata checked, %d where the four-case rule and the product rule differ' % (p_edges, p_bad))

print('\nhand cases')
a, b = canon((0,), (2,)), canon((3,), (1,))
r = thmA_root(a, b)
print('double root: a = %s, b = %s, normalized %s; K(z) - 1 = -(2z - 1)^2/(1 - z), root %s;'
      ' h(Theorem A) = %s, h(automaton) = %s'
      % (show(a), show(b), normalized(a, b), str(r)[:12], fixed(thmA_h(a, b), 9), fixed(raw_H(a, b, 3), 9)))
a, b = canon((), (0, 1)), canon((), (3, 0))
print('spread 3: a = %s, b = %s, normalized %s; root %s; h(Theorem A) = %s, h(automaton) = %s'
      % (show(a), show(b), normalized(a, b), str(thmA_root(a, b))[:12], fixed(thmA_h(a, b), 9), fixed(raw_H(a, b, 3), 9)))
a, b = canon((), (0, 1, 1, 1, 1, 1)), canon((), (2, 0, 0, 0, 0, 0))
print('not normalized: a = %s, b = %s, normalized %s' % (show(a), show(b), normalized(a, b)))
print('   series of Theorem A, n <= 12:', series_counts(a, b, 12))
print('   word counts,         n <= 12:', raw_counts(a, b, 2, 12))
