# Referee A: test the KLX theta-step over larger alphabets against a brute-force max of K~.
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random
from bf import dig, pref, cmp, shift, in_set, show

def extends(w, A, B, M, L):
    # can word w be extended to length L with all suffix windows within [A,B] (prefix order)?
    w = list(w)
    def ok(word):
        n = len(word)
        for i in range(n):
            for j in range(n - i):
                c = word[i + j]
                if c != A[j]:
                    if c < A[j]: return False
                    break
            for j in range(n - i):
                c = word[i + j]
                if c != B[j]:
                    if c > B[j]: return False
                    break
        return True
    def rec(word):
        if not ok(word): return False
        if len(word) == L: return True
        for c in range(M, -1, -1):
            if rec(word + [c]): return True
        return False
    return rec(w)

def brute_max(a, b, M, n, D):
    L = n + D
    A = pref(a, L); B = pref(b, L)
    w = []
    for _ in range(n):
        for c in range(M, -1, -1):
            if extends(w + [c], A, B, M, L):
                w.append(c); break
        else:
            return None
    return w

def theta_iter(u, a):
    for _ in range(50):
        # u eventually periodic; find m = min{k>=1 : sigma^k u < a}
        m = None
        for k in range(1, len(u[0]) + len(u[1]) + 1):
            if cmp(shift(u, k), a) < 0:
                m = k; break
        if m is None:
            return u
        w = list(pref(u, m)); w[-1] -= 1
        if w[-1] < 0: return None
        u = ((), tuple(w))
    return None

def is_lyndon(w):
    return all(tuple(w[i:]) + tuple(w[:i]) > tuple(w) for i in range(1, len(w)))

rng = random.Random(7)
tested = 0; agree = 0; disagree = []
tries = 0
while tested < 150 and tries < 200000:
    tries += 1
    M = rng.choice([2, 3])
    # alpha: periodic, maximal rotation with first letter M
    q = [M] + [rng.randint(0, M) for _ in range(rng.randint(1, 5))]
    al = ((), tuple(q))
    if any(cmp(shift(al, k), al) > 0 for k in range(1, len(q))): continue
    w = [rng.randint(0, M) for _ in range(rng.randint(1, 5))]
    if not is_lyndon(w) or w[0] >= M: continue
    a = ((), tuple(w))
    if not in_set(a, a, al): continue   # need a in K~ (sigma^n a <= alpha)
    if in_set(al, a, al): continue      # only cases with alpha not in K~
    th = theta_iter(al, a)
    n = 24
    bm = brute_max(a, al, M, n, 12)
    tested += 1
    if th is not None and bm is not None and list(pref(th, n)) == bm and in_set(th, a, al):
        agree += 1
    else:
        disagree.append((M, show(al), show(a), th and show(th), bm))
print('cases with alpha not in K~:', tested, ' theta == brute max (24 digits):', agree)
for d in disagree[:10]: print('DIFF', d)
