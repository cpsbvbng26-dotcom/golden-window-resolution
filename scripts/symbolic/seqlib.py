# Shared utilities for the scout round (Q4.10 of Kuang-Li-Xiao).
# Sequences over {0..M} are eventually periodic and stored as (pre, per) tuples of ints.
from fractions import Fraction
from itertools import product
import random

def digit(s, n):            # n >= 0, 0-based
    pre, per = s
    return pre[n] if n < len(pre) else per[(n - len(pre)) % len(per)]

def prefix(s, n):
    return tuple(digit(s, i) for i in range(n))

def shift(s, k):
    pre, per = s
    if k <= len(pre):
        return (pre[k:], per)
    k -= len(pre); k %= len(per)
    return ((), per[k:] + per[:k])

def cmp(s, t):
    """exact lexicographic comparison of two eventually periodic sequences: -1, 0, 1"""
    D = len(s[0]) + len(t[0]) + 2 * len(s[1]) * len(t[1]) + 2
    for i in range(D):
        x, y = digit(s, i), digit(t, i)
        if x != y:
            return -1 if x < y else 1
    return 0

def shifts(s):
    pre, per = s
    return [shift(s, k) for k in range(len(pre) + len(per))]

def hypothesis(a, b):
    """a, b in Sigma_{a,b}: a <= sigma^n a <= b and a <= sigma^n b <= b for all n"""
    for x in shifts(a) + shifts(b):
        if cmp(a, x) > 0 or cmp(x, b) > 0:
            return False
    return True

def series_formula(a, b, n):
    """coefficients N_0..N_n of 1/((1-z)(1-K(z))), K(z) = sum_{k>=1} (b_k - a_k) z^k, exact integers"""
    K = [0] + [digit(b, k - 1) - digit(a, k - 1) for k in range(1, n + 1)]
    # P = 1/(1-K): P_0 = 1, P_m = sum_{k=1}^m K_k P_{m-k}
    P = [1] + [0] * n
    for m in range(1, n + 1):
        P[m] = sum(K[k] * P[m - k] for k in range(1, m + 1))
    N = [sum(P[:m + 1]) for m in range(n + 1)]
    return N

def admissible_word(w, a, b):
    """every suffix w[i:] satisfies a[:L] <= w[i:] <= b[:L] (L = its length), as words"""
    n = len(w)
    for i in range(n):
        L = n - i
        seg = tuple(w[i:])
        if seg < prefix(a, L) or seg > prefix(b, L):
            return False
    return True

def brute_counts(a, b, M, nmax, K):
    """N_n = number of words of length n over {0..M} that extend to an admissible word of
    length n+K (independent of the automaton; prefix-closed DFS)."""
    ap = prefix(a, nmax + K + 1); bp = prefix(b, nmax + K + 1)
    def ok(w):
        n = len(w)
        for i in range(n):
            seg = w[i:]
            L = n - i
            if seg < ap[:L] or seg > bp[:L]:
                return False
        return True
    # only the last suffixes need checking when extending an ok word by one letter? No: all suffixes
    # change length, but prefix comparisons of an ok word stay ok unless equal; check fully (small n).
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def extendable(w, depth):
        if depth == 0:
            return True
        for c in range(M + 1):
            w2 = w + (c,)
            if ok(w2) and extendable(w2, depth - 1):
                return True
        return False
    counts = [0] * (nmax + 1)
    def dfs(w):
        n = len(w)
        if extendable(w, K):
            counts[n] += 1
        else:
            return
        if n == nmax:
            return
        for c in range(M + 1):
            w2 = w + (c,)
            if ok(w2):
                dfs(w2)
    dfs(())
    return counts

def smallest_root(a, b, dps=40, terms=4000):
    """smallest z in (0,1) with sum_{k>=1} (b_k - a_k) z^k = 1, by bisection on the exact
    eventually periodic closed form; None if no root in (0,1)."""
    from mpmath import mp, mpf
    mp.dps = dps
    pre_a, per_a = a; pre_b, per_b = b
    def K(z):
        # sum over the first P digits exactly, then periodic tail via geometric series of period lcm
        from math import lcm
        P = max(len(pre_a), len(pre_b))
        q = lcm(len(per_a), len(per_b))
        s = mpf(0)
        for k in range(1, P + 1):
            s += (digit(b, k - 1) - digit(a, k - 1)) * z ** k
        blk = mpf(0)
        for k in range(P + 1, P + q + 1):
            blk += (digit(b, k - 1) - digit(a, k - 1)) * z ** k
        return s + blk / (1 - z ** q)
    # scan for the first sign change of K(z) - 1 on (0,1)
    N = 4000
    prev = mpf(0)
    for i in range(1, N):
        z = mpf(i) / N
        v = K(z) - 1
        if v >= 0:
            lo, hi = mpf(i - 1) / N, z
            for _ in range(200):
                mid = (lo + hi) / 2
                if K(mid) - 1 >= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
    return None
