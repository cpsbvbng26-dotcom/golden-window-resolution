import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Referee A: specific and near-degenerate pairs, a negative control, and the
# beta-rational counterexample to Corollary B (greedy a = b(t,beta) not in K~).
import math
from bf import dig, pref, normalized, series, brute, show

def smallest_root(a, b, terms=3000):
    c = [dig(b, k - 1) - dig(a, k - 1) for k in range(1, terms + 1)]
    K = lambda z: sum(ci * z ** (i + 1) for i, ci in enumerate(c))
    # scan for the first sign change of K - 1 on (0,1)
    prev = 0.0; z0 = 0.0
    N = 2000
    for j in range(1, N):
        z = j / N * 0.999
        v = K(z) - 1
        if v >= 0:
            lo, hi = z0, z
            for _ in range(80):
                mid = (lo + hi) / 2
                if K(mid) - 1 >= 0: hi = mid
                else: lo = mid
            return hi
        z0 = z
    return None

def h_of(a, b):
    r = smallest_root(a, b)
    return 0.0 if r is None else -math.log(r)

S = lambda p, q: (tuple(p), tuple(q))
cases = [
    ('full ternary', 2, S([], [0]), S([], [2])),
    ('full quaternary', 3, S([], [0]), S([], [3])),
    ('h=0 (12)/(21)', 2, S([], [1, 2]), S([], [2, 1])),
    ('h=0 (02)/(20)', 2, S([], [0, 2]), S([], [2, 0])),
    ('(112)/(21)', 2, S([], [1, 1, 2]), S([], [2, 1])),
    ('0 1^inf / 2 1^inf', 2, S([0], [1]), S([2], [1])),
    ('(0 2^5)/(2^5 0)', 2, S([], [0, 2, 2, 2, 2, 2]), S([], [2, 2, 2, 2, 2, 0])),
    ('(0^5 1)/(1 0^5) quaternary', 3, S([], [0, 0, 0, 0, 0, 1]), S([], [1, 0, 0, 0, 0, 0])),
    ('(0 3^4)/(3^4 0)', 3, S([], [0, 3, 3, 3, 3]), S([], [3, 3, 3, 3, 0])),
    ('(1 2 2)/(2 2 1) near-equal', 2, S([], [1, 2, 2]), S([], [2, 2, 1])),
    ('(1 2)/(2 1 1 ... ) h small', 2, S([], [1, 2]), S([], [2, 1, 1])),
    ('(1 1 1 2)/(2 1)', 2, S([], [1, 1, 1, 2]), S([], [2, 1])),
    ('(1 3)/(3 1) quaternary', 3, S([], [1, 3]), S([], [3, 1])),
    ('(1 2 3)/(3 2 1)', 3, S([], [1, 2, 3]), S([], [3, 2, 1])),
    ('(0 2)/(2^inf)', 2, S([], [0, 2]), S([], [2])),
    ('0^inf/(2 1 0)', 2, S([], [0]), S([], [2, 1, 0])),
    ('a=b=(1)', 2, S([], [1]), S([], [1])),
    ('(1 2 2 2 2 2 2)/(2 1)', 2, S([], [1, 2, 2, 2, 2, 2, 2]), S([], [2, 1])),
    ('01^5 0 ... ternary (0 1 1 1 1 1)/(2 0 0 0 0 0)', 2, S([], [0, 1, 1, 1, 1, 1]), S([], [2, 0, 0, 0, 0, 0])),
]
print('== specific / near-degenerate pairs')
for name, M, a, b in cases:
    nz = normalized(a, b)
    n = {1: 11, 2: 9, 3: 7}[M]
    Sx = series(a, b, n)
    c1 = brute(a, b, M, n, 10); c2 = brute(a, b, M, n, 18)
    print(f'{name:45s} M={M} normalized={nz} stable={c1==c2} match={c2==Sx} h={h_of(a,b):.6f}')
    print('   brute ', c2)
    if c2 != Sx: print('   series', Sx)

print('== negative control: KLX Example 4.9 raw pair (not normalized)')
t = S([0,1,0,1,1,0,1,1,1], [0]); u = S([1,1,1,0,1,0,0,1,0,0,0], [1])
print(' normalized', normalized(t, u))
print(' series', series(t, u, 12))
print(' brute ', brute(t, u, 1, 12, 20))
a = S([], [0,1,1]); b = S([], [1,1,0])
print(' normalized pair', normalized(a, b), series(a, b, 12), brute(a, b, 1, 12, 20))

print('== Corollary B, beta-rational t in U (KLX hole (0,t))')
# alpha(beta) = (220)^inf, greedy expansion of 1 is 221 => beta^3 = 2beta^2 + 2beta + 1
f = lambda x: x**3 - 2*x*x - 2*x - 1
lo, hi = 2.0, 3.0
for _ in range(200):
    mid = (lo+hi)/2
    if f(mid) > 0: hi = mid
    else: lo = mid
beta = lo
alpha = S([], [2,2,0])
print(' beta =', beta)
for label, tgreedy, tmin, bmax in [
    ('t = 1/beta  (greedy 1 0^inf, Lyndon "1")', S([1], [0]), S([], [1]), S([], [2, 1])),
    ('t = 1/beta^2 (greedy 01 0^inf, Lyndon "01")', S([0, 1], [0]), S([], [0, 1]), alpha),
]:
    print(' ', label)
    print('   greedy a in K~? ', normalized(tgreedy, alpha) and False or 'a in K~:',
          __import__('bf').in_set(tgreedy, tgreedy, alpha))
    print('   claimed b = max K~ =', show(bmax), ' (a_min, b) normalized:', normalized(tmin, bmax))
    # brute count of K~ = {z : a_greedy <= sigma^n z <= alpha}
    n = 9
    cb = brute(tgreedy, alpha, 2, n, 18)
    print('   brute N_n of K~(t) with greedy a      ', cb)
    print('   series with a = b(t,beta) (scout)     ', series(tgreedy, bmax, n), ' h =', round(h_of(tgreedy, bmax), 6))
    print('   series with a = min K~               ', series(tmin, bmax, n), ' h =', round(h_of(tmin, bmax), 6))
    tq = S([d for d in tgreedy[0][:-1]] + [tgreedy[0][-1] - 1], [2, 2, 0])
    print('   series with a = quasi-greedy t       ', series(tq, bmax, n), ' h =', round(h_of(tq, bmax), 6))

    # real map: survivors of T_beta with hole (0,t), count interval components
    tv = sum(dig(tgreedy, i) / beta ** (i + 1) for i in range(60))
    D = math.ceil(beta)
    cur = [(0.0, 1.0)]
    counts = []
    for step in range(40):
        if len(cur) > 150000: break
        new = []
        for (l, r) in cur:
            for d in range(D):
                L = (d + l) / beta; R = min((d + r) / beta, 1.0)
                if L >= 1.0 or L >= R: continue
                L = max(L, tv)
                if L < R: new.append((L, R))
        new.sort()
        merged = []
        for (l, r) in new:
            if merged and l <= merged[-1][1] + 1e-15:
                merged[-1] = (merged[-1][0], max(merged[-1][1], r))
            else:
                merged.append((l, r))
        cur = merged
        counts.append(len(cur))
    rates = [math.log(counts[i] / counts[i - 1]) for i in range(len(counts) - 4, len(counts))]
    print('   real map: interval counts', counts[-6:], ' growth logs', [round(x, 4) for x in rates])

print('== beta = 3 (integer), t = 1/3: greedy a = 1 0^inf, alpha = 2^inf')
a = S([1], [0]); al = S([], [2])
print('   a in K~:', __import__('bf').in_set(a, a, al))
print('   brute ', brute(a, al, 2, 9, 18))
print('   scout series', series(a, al, 9), ' h =', round(h_of(a, al), 6), ' vs log 2 =', round(math.log(2), 6))
print('   min-K~ series', series(S([], [1]), al, 9), ' h =', round(h_of(S([], [1]), al), 6))
