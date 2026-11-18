# Check 1 (brute force): the number of words of length n of Sigma_{a,b} over {0..M} equals the
# n-th coefficient of 1/((1-z)(1-K(z))), K(z) = sum (b_k - a_k) z^k, whenever a, b in Sigma_{a,b}.
# Words are counted by an independent DFS (extension test to depth K), not by the automaton.
import random, sys
from seqlib import *

def lyndon_like(M, L, rng):
    while True:
        w = tuple(rng.randrange(M + 1) for _ in range(L))
        rots = [w[i:] + w[:i] for i in range(L)]
        if len(set(rots)) == L and w == min(rots):
            return w

def maxrot_like(M, L, rng):
    while True:
        w = tuple(rng.randrange(M + 1) for _ in range(L))
        rots = [w[i:] + w[:i] for i in range(L)]
        if len(set(rots)) == L and w == max(rots):
            return w

def rand_seq(M, rng, kind):
    L = rng.randrange(1, 6)
    if kind == 'low':
        w = lyndon_like(M, L, rng) if L > 1 else (rng.randrange(M + 1),)
        # optional preperiod: a prefix smaller than every shift is allowed only if it stays minimal
        if rng.random() < 0.4:
            p = tuple(rng.randrange(M + 1) for _ in range(rng.randrange(1, 4)))
            return (p, w)
        return ((), w)
    else:
        w = maxrot_like(M, L, rng) if L > 1 else (rng.randrange(M + 1),)
        if rng.random() < 0.4:
            p = tuple(rng.randrange(M + 1) for _ in range(rng.randrange(1, 4)))
            return (p, w)
        return ((), w)

def main(seed=1, trials=400, nmax=9, K=14):
    rng = random.Random(seed)
    tested = 0; bad = 0; byM = {}
    tried = 0
    while tested < trials and tried < 200000:
        tried += 1
        M = rng.choice([1, 2, 2, 3, 3, 4])
        a = rand_seq(M, rng, 'low'); b = rand_seq(M, rng, 'high')
        if cmp(a, b) >= 0 or not hypothesis(a, b):
            continue
        n = nmax if M <= 2 else (7 if M == 3 else 6)
        bc = brute_counts(a, b, M, n, K)
        fc = series_formula(a, b, n)
        tested += 1
        byM[M] = byM.get(M, 0) + 1
        if bc != fc:
            bad += 1
            print("MISMATCH", M, a, b, bc, fc)
    print("seed", seed, "pairs tested", tested, "by alphabet size-1:", byM, "mismatches", bad)

    # necessity of the hypothesis: KLX Example 4.9 raw pair (t,u) is not normalized
    t = ((0,1,0,1,1,0,1,1,1), (0,)); u = ((1,1,1,0,1,0,0,1,0,0,0), (1,))
    print("KLX Ex 4.9 raw pair satisfies hypothesis:", hypothesis(t, u))
    print("  brute :", brute_counts(t, u, 1, 12, 14))
    print("  formula raw (t,u):", series_formula(t, u, 12))
    a = ((), (0,1,1)); b = ((), (1,1,0))
    print("  normalized (a,b) = ((011)^inf,(110)^inf) hyp:", hypothesis(a, b), "formula:", series_formula(a, b, 12))

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
