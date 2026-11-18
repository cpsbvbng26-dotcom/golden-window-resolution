# The explicit IA witnesses of Lemma Y2 and the support lemma S3.
#
# For a normalized pair (a, b) and D = 10, 20, 40, the witness is p_D = min Y_D, q_D = max Y_D, read off the
# unfolded automaton of Theorem A by greedy walks (exact eventually periodic sequences). Checked exactly:
#   (i)   a < p_D and q_D < b, with the first difference at an index <= D;
#   (ii)  (p_D, q_D) is normalized;
# and in floating point, with gaps below 1e-11 printed as "<1e-11":
#   (iii) Theorem A applied to (p_D, q_D) gives h(Y_D) (Lemma Y2: Sigma_{p_D,q_D} = Y_D), and so does the raw
#         automaton of (p_D, q_D), which uses neither Theorem A nor normalization.
# Support lemma: if a is the label of an infinite path inside a strongly connected component C of radius > 1
# of the (folded) automaton, the measure of maximal entropy of C is an ergodic measure with positive entropy
# whose support contains a, and S3 predicts that p_D -> a. The table counts, for each end, whether it lies in
# such a component and whether p_40 (resp. q_40) agrees with it on at least 30 digits.
import random

from lexlib import (fmt, fixed, agree, canon, dig, firstdiff, in_positive_scc, lexcmp, normalized, raw_H, show, thmA_h, yd)

P = lambda pre, per: canon(tuple(pre), tuple(per))
HAND = [
    ('orbit of b near a, k = 3', 2, P([], [0, 1]), P([], [2, 0, 1, 0, 1, 0, 1])),
    ('orbit of b near a, k = 6', 2, P([], [0, 1]), P([], [2] + [0, 1] * 6)),
    ('b = 2a (orbit of b hits a)', 2, P([], [0, 1]), P([2], [0, 1])),
    ('b = 4a', 4, P([], [0, 2]), P([4], [0, 2])),
    ('a = 0b, a isolated', 2, P([0], [2]), P([], [2])),
    ('a = 1b, a isolated', 3, P([1], [3, 2]), P([], [3, 2])),
    ('tight, 01^inf / 21^inf', 2, P([0], [1]), P([2], [1])),
    ('double root, 02^inf / 31^inf', 3, P([0], [2]), P([3], [1])),
    ('a = (01)^inf, b = (220)^inf', 2, P([], [0, 1]), P([], [2, 2, 0])),
    ('spread 3 (Section 6)', 3, P([], [0, 1]), P([], [3, 0])),
    ('slow pair', 2, P([], [0, 2]), P([], [2, 1, 0])),
]


random.seed(5309)
rand = []
while len(rand) < 20:
    M = random.choice([2, 3, 4])
    a = P([random.randint(0, M) for _ in range(random.randint(0, 3))], [random.randint(0, M) for _ in range(random.randint(1, 4))])
    b = P([random.randint(0, M) for _ in range(random.randint(0, 3))], [random.randint(0, M) for _ in range(random.randint(1, 4))])
    if dig(b, 0) - dig(a, 0) < 2 or lexcmp(a, b) >= 0 or not normalized(a, b) or raw_H(a, b, M) <= 0.05:
        continue
    rand.append(('random %d' % (len(rand) + 1), M, a, b))

ok_strict = ok_norm = n_checks = 0
worst_A = worst_raw = 0.0
table = {}
for name, M, a, b in HAND + rand:
    h = raw_H(a, b, M)
    print('# %s: M=%d, a = %s, b = %s, h = %s' % (name, M, show(a), show(b), fixed(h, 9)))
    for D in (10, 20, 40):
        hD, p, q = yd(a, b, D)
        i, j = firstdiff(p, a), firstdiff(q, b)
        strict = lexcmp(a, p) < 0 and lexcmp(q, b) < 0 and i is not None and i <= D and j is not None and j <= D
        nm = normalized(p, q)
        dA = abs(thmA_h(p, q) - hD)
        dR = abs(raw_H(p, q, M) - hD)
        n_checks += 1
        ok_strict += strict
        ok_norm += nm
        worst_A, worst_raw = max(worst_A, dA), max(worst_raw, dR)
        print('   D=%d: p_D agrees with a on %d digits, q_D with b on %d; a < p_D and q_D < b: %s; normalized: %s; '
              'h - h(Y_D) %s; |Theorem A(p_D, q_D) - h(Y_D)| %s; |raw(p_D, q_D) - h(Y_D)| %s'
              % (D, agree(p, a), agree(q, b), strict, nm, fmt(max(h - hD, 0.0)), fmt(dA), fmt(dR)))
    p40, q40 = yd(a, b, 40)[1:]
    for side, end, w in (('a', a, p40), ('b', b, q40)):
        key = (side, 'in a component of radius > 1' if in_positive_scc(a, b, end) else 'in no such component',
               'agreement >= 30' if agree(w, end) >= 30 else 'agreement < 30')
        table[key] = table.get(key, 0) + 1

print('\nsummary over %d pairs and %d values of (pair, D):' % (len(HAND + rand), n_checks))
print('   a < p_D and q_D < b, first difference at index <= D: %d of %d' % (ok_strict, n_checks))
print('   (p_D, q_D) normalized: %d of %d' % (ok_norm, n_checks))
print('   max |Theorem A(p_D, q_D) - h(Y_D)|: %s;  max |raw(p_D, q_D) - h(Y_D)|: %s' % (fmt(worst_A), fmt(worst_raw)))
print('support lemma (D = 40):')
for key in sorted(table):
    print('   end %s, %s, %s: %d' % (key[0], key[1], key[2], table[key]))
