"""Check of Theorem B (interval or porous) without the classification.
S_N = points with a legal path of N steps, computed backwards as a union of intervals
(S_0 = [0,1], S_{k+1} = U_e Finv_e(S_k n I_e)), exact Fractions, merged.
Predictions from classify():
  'interval' -> S_N = [u*, v*] exactly, for every N checked;
  'gap'      -> every component of S_N has length <= delta^N (no interval survives), and
                the total length is non-increasing;
  'empty'    -> S_N empty for large N.
Random games; the constants vlow_i are taken below the minmax (any constants are allowed by
Theorem A), so that both intervals are often non-empty."""
import random, itertools
from fractions import Fraction as Fr
from gen import Game, Edge, Gn
from check_reduction import rand_game

random.seed(7)

def merge(iv):
    iv = sorted(iv)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out

def backward(E, N, cap=20000):
    S = [(Fr(0), Fr(1))]
    hist = []
    for k in range(N):
        new = []
        for e in (0, 1):
            I = E.I[e]
            if I is None: continue
            for a, b in S:
                lo, hi = max(a, I[0]), min(b, I[1])
                if lo <= hi:
                    new.append((E.Finv(e, lo), E.Finv(e, hi)))
        S = merge(new)
        if len(S) > cap:
            return None, hist
        hist.append((len(S), sum(b - a for a, b in S), max((b - a for a, b in S), default=0)))
    return S, hist

if __name__ == '__main__':
    res = {}
    bad = []
    games = []
    for _ in range(150):
        n = random.choice([2, 3])
        G = rand_game(n)
        profs = list(itertools.product(*[G.actions] * n))
        games.append((G, *random.sample(profs, 2)))
    for G, A, B in games:
        vlow = [G.pure_minmax(i) - Fr(random.randint(0, 6), 2) for i in range(G.n)]
        for _ in range(4):
            d = Fr(random.randint(20, 95), 100)
            E = Edge(G, A, B, d, vlow=vlow)
            kind, data = E.classify()
            N = 30
            S, hist = backward(E, N)
            if S is None:
                res.setdefault(kind + ' (skipped: too many pieces)', 0)
                res[kind + ' (skipped: too many pieces)'] += 1
                continue
            if kind == 'interval':
                ok = S == [data]
            elif kind == 'gap':
                ok = hist[-1][2] <= d ** N and all(hist[i + 1][1] <= hist[i][1] for i in range(N - 1))
            elif kind == 'empty':
                ok = S == []
            else:
                ok = hist[-1][2] <= d ** N        # one action only: at most a fixed point
            key = kind + (' ok' if ok else ' FAIL')
            res[key] = res.get(key, 0) + 1
            if not ok: bad.append((kind, d, hist[-3:], data))
    print(res)
    print('failures', bad[:3])
