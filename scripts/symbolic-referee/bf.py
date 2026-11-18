# Referee A: independent brute-force word counter for Sigma_{a,b} (not using scout code).
# Sequences are eventually periodic: (prefix tuple, period tuple).
import random, sys
from math import gcd

def dig(s, i):  # i >= 0, 0-based
    p, q = s
    return p[i] if i < len(p) else q[(i - len(p)) % len(q)]

def pref(s, L):
    return tuple(dig(s, i) for i in range(L))

def shift(s, k):
    p, q = s
    if k <= len(p):
        return (p[k:], q)
    k2 = (k - len(p)) % len(q)
    return ((), q[k2:] + q[:k2])

def cmp(x, y):
    L = max(len(x[0]), len(y[0])) + len(x[1]) * len(y[1]) // gcd(len(x[1]), len(y[1])) + 1
    for i in range(L):
        u, v = dig(x, i), dig(y, i)
        if u != v:
            return -1 if u < v else 1
    return 0

def in_set(z, a, b):
    for k in range(len(z[0]) + len(z[1]) + 1):
        s = shift(z, k)
        if cmp(a, s) > 0 or cmp(s, b) > 0:
            return False
    return True

def normalized(a, b):
    return in_set(a, a, b) and in_set(b, a, b)

def series(a, b, n):
    c = [0] + [dig(b, k - 1) - dig(a, k - 1) for k in range(1, n + 1)]
    g = [1]
    for m in range(1, n + 1):
        g.append(sum(c[k] * g[m - k] for k in range(1, m + 1)))
    N, s = [], 0
    for m in range(n + 1):
        s += g[m]
        N.append(s)
    return N

def brute(a, b, M, n, D):
    """Number of words of length 0..n having an extension of total length n+D
    in which every suffix w[i:] satisfies a[:len] <=lex w[i:] <=lex b[:len] (prefix order)."""
    L = n + D
    A = pref(a, L); B = pref(b, L)
    w = [0] * L
    # state for each start position i: 0 = still equal to a-prefix, 1 = already strictly above
    def ok_add(depth, c):
        # check constraints for all starts i <= depth with new letter c at position depth
        return True
    counts = [0] * (n + 1)
    # iterative DFS with per-start flags: lo[i] True if w[i:depth] == A[:depth-i], hi[i] likewise for B
    def ext(depth, lo, hi):
        # returns True if word w[:depth] extends to length L
        if depth == L:
            return True
        for c in range(M + 1):
            nlo, nhi = [], []
            good = True
            for i in range(depth + 1):
                li = lo[i] if i < depth else True
                hii = hi[i] if i < depth else True
                j = depth - i
                if li:
                    if c < A[j]: good = False; break
                    li = (c == A[j])
                if hii:
                    if c > B[j]: good = False; break
                    hii = (c == B[j])
                nlo.append(li); nhi.append(hii)
            if not good:
                continue
            w[depth] = c
            if ext(depth + 1, nlo, nhi):
                return True
        return False
    def walk(depth, lo, hi):
        if not ext(depth, lo, hi):
            return
        counts[depth] += 1
        if depth == n:
            return
        for c in range(M + 1):
            nlo, nhi = [], []
            good = True
            for i in range(depth + 1):
                li = lo[i] if i < depth else True
                hii = hi[i] if i < depth else True
                j = depth - i
                if li:
                    if c < A[j]: good = False; break
                    li = (c == A[j])
                if hii:
                    if c > B[j]: good = False; break
                    hii = (c == B[j])
                nlo.append(li); nhi.append(hii)
            if good:
                w[depth] = c
                walk(depth + 1, nlo, nhi)
    walk(0, [], [])
    return counts

def rand_seq(M, rng, maxpre=3, maxper=5):
    p = tuple(rng.randint(0, M) for _ in range(rng.randint(0, maxpre)))
    q = tuple(rng.randint(0, M) for _ in range(rng.randint(1, maxper)))
    return (p, q)

def show(s):
    return ''.join(map(str, s[0])) + '(' + ''.join(map(str, s[1])) + ')^inf'

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    tested = {1: 0, 2: 0, 3: 0}
    bad = 0
    stab_fail = 0
    want = {1: 40, 2: 80, 3: 60}
    nmax = {1: 10, 2: 8, 3: 7}
    tries = 0
    while any(tested[k] < want[k] for k in tested) and tries < 2000000:
        tries += 1
        M = rng.choice([k for k in tested if tested[k] < want[k]])
        a = rand_seq(M, rng); b = rand_seq(M, rng)
        if dig(a, 0) >= dig(b, 0):
            continue
        if not normalized(a, b):
            continue
        n = nmax[M]
        S = series(a, b, n)
        c1 = brute(a, b, M, n, 10)
        c2 = brute(a, b, M, n, 16)
        if c1 != c2:
            stab_fail += 1
        if c2 != S:
            bad += 1
            print('MISMATCH', M, show(a), show(b), c2, S)
        tested[M] += 1
    print('tested', tested, 'mismatches', bad, 'D=10 vs D=16 differ', stab_fail)
