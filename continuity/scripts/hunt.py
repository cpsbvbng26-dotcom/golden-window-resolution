# A hunt for discontinuities of H on all pairs (Corollary C), pairs that are not normalized included.
#
# H(A, B) is non-increasing in A and non-decreasing in B. So for eventually periodic (A, B), every pair that
# agrees with (A, B) on the first k digits has entropy in [inner_k, outer_k], where
#     inner_k = H(A|k M^inf, B|k 0^inf),   outer_k = H(A|k 0^inf, B|k M^inf).
# H is continuous at (A, B) exactly when outer_k - inner_k -> 0. All entropies come from the raw automaton
# (no normalization, no Theorem A). The gap printed is max(h - inner_k, outer_k - h); gaps below 1e-11 are
# printed as "<1e-11". Pairs: 400 random pairs over {0..M}, M = 2, 3, 4 (seed 4242), of which those with h > 0
# are the hard cases, plus 200 random pairs with h > 0 and first digits differing by at least 2 (seed 5151).
import random

from lexlib import fmt, fixed, canon, dig, normalized, prefix, raw_H

KS = (10, 20, 30, 40)


def rnd(M):
    return canon(tuple(random.randint(0, M) for _ in range(random.randint(0, 4))),
                 tuple(random.randint(0, M) for _ in range(random.randint(1, 5))))


def gaps(A, B, M, h):
    out = []
    for k in KS:
        hi = raw_H(canon(prefix(A, k), (M,)), canon(prefix(B, k), (0,)), M)
        ho = raw_H(canon(prefix(A, k), (0,)), canon(prefix(B, k), (M,)), M)
        assert hi <= h + 1e-9 and ho >= h - 1e-9
        out.append(max(h - hi, ho - h, 0.0))
    return out


def run(rows, title):
    worst_pos = [0.0] * len(KS)
    worst_zero = [0.0] * len(KS)
    npos = nraw = 0
    for M, A, B in rows:
        h = raw_H(A, B, M)
        nraw += not normalized(A, B)
        g = gaps(A, B, M, h)
        if h > 0:
            npos += 1
            worst_pos = [max(x, y) for x, y in zip(worst_pos, g)]
        else:
            worst_zero = [max(x, y) for x, y in zip(worst_zero, g)]
    print('%s: %d pairs, %d not normalized, %d with h > 0' % (title, len(rows), nraw, npos))
    print('   worst gap at k = %s, pairs with h > 0: %s' % (', '.join(map(str, KS)), ', '.join(fmt(x) for x in worst_pos)))
    if len(rows) > npos:
        print('   worst gap at k = %s, pairs with h = 0: %s' % (', '.join(map(str, KS)), ', '.join(fmt(x) for x in worst_zero)))


random.seed(4242)
rows = []
while len(rows) < 400:
    M = random.choice([2, 3, 4])
    rows.append((M, rnd(M), rnd(M)))
run(rows, 'all random pairs')

random.seed(5151)
rows = []
while len(rows) < 200:
    M = random.choice([2, 3, 4])
    A, B = rnd(M), rnd(M)
    if dig(B, 0) - dig(A, 0) < 2 or raw_H(A, B, M) <= 0:
        continue
    rows.append((M, A, B))
run(rows, 'random pairs with h > 0 and spread >= 2')

print('\nentropy 0: (A, B) = (1(2)^inf, (2)^inf), M = 2, h = 0; outer_k at k = 40, 80, 160: %s'
      % ', '.join(fixed(raw_H(canon(prefix(((1,), (2,)), k), (0,)), ((), (2,)), 2), 4) for k in (40, 80, 160)))
print('normalization jumps: (A, B) = ((0)^inf, 2(0)^inf), M = 2; H(0^k 1 0^inf, B) at k = 2, 4, 8, 12: %s; H(A, B) = %s'
      % (', '.join(fixed(raw_H(canon((0,) * k + (1,), (0,)), ((2,), (0,)), 2), 4) for k in (2, 4, 8, 12)),
         fixed(raw_H(((), (0,)), ((2,), (0,)), 2), 4)))
