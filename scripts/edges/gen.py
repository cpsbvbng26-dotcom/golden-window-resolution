"""Core of the generalisation: an edge [g(A), g(B)] of a finite game, its intervals I_a,
the map F, the classification, and three independent ways to get the dimension.

Coordinates: x in [0,1], p(x) = g(A) + x (g(B) - g(A)); digit 0 = A, 1 = B.
F_A(x) = x/delta on D_A = delta*I_A, F_B(x) = (x-(1-delta))/delta on D_B = (1-delta)+delta*I_B.
Exact arithmetic (Fraction) wherever a set is decided; mpmath only for roots.
"""
from fractions import Fraction as Fr
import itertools, math
from functools import lru_cache
from mpmath import mp, mpf

mp.dps = 40


# ------------------------------------------------------------------ games
class Game:
    def __init__(self, n, actions, payoff):
        self.n = n
        self.actions = actions            # list of action labels per player
        self.payoff = payoff              # profile tuple -> tuple of Fractions
        self.profiles = list(itertools.product(*[actions] * n)) if isinstance(actions[0], str) else None

    def g(self, a):
        return tuple(Fr(v) for v in self.payoff(a))

    def dev(self, a, i):
        """best one-shot deviation payoff d_i(a)"""
        best = None
        for b in self.actions:
            a2 = list(a); a2[i] = b
            v = self.g(tuple(a2))[i]
            best = v if best is None or v > best else best
        return best

    def pure_minmax(self, i):
        best = None
        others = itertools.product(*[self.actions] * (self.n - 1))
        for o in others:
            m = None
            for b in self.actions:
                a = list(o[:i]) + [b] + list(o[i:])
                v = self.g(tuple(a))[i]
                m = v if m is None or v > m else m
            best = m if best is None or m < best else best
        return best


def linear_dilemma(n, r, shift=0):
    """cooperator pays r, gives 1 to every co-player; payoffs + shift"""
    r = Fr(r)
    def pay(a):
        out = []
        for i in range(n):
            k = sum(1 for j in range(n) if j != i and a[j] == 'C')
            out.append(k - r + shift if a[i] == 'C' else k + shift)
        return tuple(out)
    return Game(n, ['C', 'D'], pay)


def Gn(n):
    """the note's G_n: piC(k) = k+1, piD(k) = k+2  (= linear dilemma r=1, shift 2)"""
    def pay(a):
        out = []
        for i in range(n):
            k = sum(1 for j in range(n) if j != i and a[j] == 'C')
            out.append(k + 1 if a[i] == 'C' else k + 2)
        return tuple(out)
    return Game(n, ['C', 'D'], pay)


def pd(gain, loss):
    """two-player PD normalised: CC=(1,1), DD=(0,0), DC=(1+g,-l), CD=(-l,1+g)"""
    g, l = Fr(gain), Fr(loss)
    tab = {('C', 'C'): (1, 1), ('D', 'D'): (0, 0), ('D', 'C'): (1 + g, -l), ('C', 'D'): (-l, 1 + g)}
    return Game(2, ['C', 'D'], lambda a: tab[a])


# ------------------------------------------------------------------ the edge
class Edge:
    def __init__(self, game, A, B, delta, vlow=None):
        self.G, self.A, self.B = game, A, B
        self.d = Fr(delta)
        n = game.n
        self.gA, self.gB = game.g(A), game.g(B)
        self.vlow = vlow if vlow is not None else [game.pure_minmax(i) for i in range(n)]
        self.I = {0: self.interval(A), 1: self.interval(B)}

    def p(self, x):
        return tuple(self.gA[i] + x * (self.gB[i] - self.gA[i]) for i in range(self.G.n))

    def c(self, a):
        d = self.d
        ga = self.G.g(a)
        return [self.vlow[i] + (1 - d) / d * (self.G.dev(a, i) - ga[i]) for i in range(self.G.n)]

    def interval(self, a):
        lo, hi = Fr(0), Fr(1)
        for i, ci in enumerate(self.c(a)):
            base, slope = self.gA[i], self.gB[i] - self.gA[i]
            if slope == 0:
                if base < ci:
                    return None
            elif slope > 0:
                lo = max(lo, (ci - base) / slope)
            else:
                hi = min(hi, (ci - base) / slope)
        return (lo, hi) if lo <= hi else None

    # domains
    def D(self, e):
        I = self.I[e]
        if I is None:
            return None
        d = self.d
        return (d * I[0], d * I[1]) if e == 0 else (1 - d + d * I[0], 1 - d + d * I[1])

    def F(self, e, x):
        d = self.d
        return x / d if e == 0 else (x - (1 - d)) / d

    def Finv(self, e, y):
        d = self.d
        return d * y if e == 0 else 1 - d + d * y

    # classification (Theorem B)
    def classify(self):
        if self.I[0] is None or self.I[1] is None:
            return 'one-action', None
        d = self.d
        aA, wA = self.I[0]; aB, wB = self.I[1]
        u, v = d * aA, 1 - d + d * wB
        if u >= v:
            return 'empty', None
        EA = (u, d * min(wA, v)) if aA <= v else None
        EB = (1 - d + d * max(aB, u), v) if wB >= u else None
        self.u, self.v, self.EA, self.EB = u, v, EA, EB
        if EA is not None and EB is not None and EA[1] >= EB[0]:
            return 'interval', (u, v)
        return 'gap', (EA, EB)


# ------------------------------------------------------------------ gap-case dynamics
class GapSystem:
    """survivor set of F on E_A u E_B (disjoint, E_A left of E_B), in x-coordinates"""

    def __init__(self, edge):
        kind, data = edge.classify()
        assert kind == 'gap', kind
        self.e = edge
        self.d = edge.d
        self.E = {0: data[0], 1: data[1]}
        self.u, self.v = edge.u, edge.v

    def step(self, K, e):
        """state K (interval) -> image of K n E_e under F_e, or None"""
        E = self.E[e]
        if E is None or K is None:
            return None
        lo, hi = max(K[0], E[0]), min(K[1], E[1])
        if lo > hi:
            return None
        return (self.e.F(e, lo), self.e.F(e, hi))

    @lru_cache(maxsize=None)
    def alive(self, K, m):
        if K is None:
            return False
        if m == 0:
            return True
        return self.alive(self.step(K, 1), m - 1) or self.alive(self.step(K, 0), m - 1)

    def counts(self, n, look=0, start=None):
        """DP over states: number of words of length k (k<=n) whose state survives `look`
        more steps, and total length of the level-k cylinders (exact)."""
        K0 = start or (self.u, self.v)
        cur = {K0: 1}
        out = []
        d = self.d
        for k in range(1, n + 1):
            nxt = {}
            for K, mult in cur.items():
                for e in (0, 1):
                    K2 = self.step(K, e)
                    if K2 is not None and (look == 0 or self.alive(K2, look)):
                        nxt[K2] = nxt.get(K2, 0) + mult
            cur = nxt
            N = sum(cur.values())
            L = sum(mult * (K[1] - K[0]) for K, mult in cur.items()) * d ** k
            out.append((k, N, L, len(cur)))
        return out

    def extreme_word(self, first, maximize, K, look):
        """lexicographically largest (maximize) / smallest word of length K in the language of
        the survivor subshift starting with `first`, with finite lookahead `look`"""
        order = (1, 0) if maximize else (0, 1)
        word = []
        state = (self.u, self.v)

        def dfs(state, depth):
            if depth == K:
                return self.alive(state, look)
            digits = (first,) if depth == 0 else order
            for e in digits:
                s2 = self.step(state, e)
                if s2 is not None and dfs(s2, depth + 1):
                    word.append(e)
                    return True
            return False
        import sys
        sys.setrecursionlimit(10000)
        ok = dfs(state, 0)
        return list(reversed(word)) if ok else None

    def member(self, x, steps):
        """deterministic test: does x survive `steps` steps? (gap case: unique branch)"""
        for _ in range(steps):
            if self.E[0] and self.E[0][0] <= x <= self.E[0][1]:
                x = self.e.F(0, x)
            elif self.E[1] and self.E[1][0] <= x <= self.E[1][1]:
                x = self.e.F(1, x)
            else:
                return False
        return True


# ------------------------------------------------------------------ dimension, three ways
def lsz_dim(a, b, beta, lo=mpf('1e-6')):
    """LSZ Thm 1.2 / Prop 2.5 with q0=q1=beta: maximal s with pi_{beta^s}(a) = pi_{beta^s}(b),
    pi_q(i) = sum_k i_k q^{-k} (k from 1).  a, b: finite prefixes (lists of digits)."""
    beta = mpf(beta)
    def f(s):
        z = beta ** (-s)
        return sum((bk - ak) * z ** (k + 1) for k, (ak, bk) in enumerate(zip(a, b)))
    # scan down from 1 for the first sign change
    N = 2000
    prev_s, prev_f = mpf(1), f(mpf(1))
    if prev_f <= 0:
        return None
    for i in range(1, N + 1):
        s = 1 - mpf(i) / N
        if s < lo:
            return mpf(0)
        fs = f(s)
        if fs <= 0:
            a_, b_ = s, prev_s
            for _ in range(100):
                m = (a_ + b_) / 2
                if f(m) <= 0:
                    a_ = m
                else:
                    b_ = m
            return (a_ + b_) / 2
        prev_s, prev_f = s, fs
    return mpf(0)


def renewal_set(edge, K=600):
    """anchored case (alpha_A = alpha_B = 0): forced path from the full continuation state.
    States are [0, s]. Returns A = {k+1 : s_k >= qA} (exact Fractions)."""
    gs = GapSystem(edge)
    EA, EB = gs.E[0], gs.E[1]
    assert edge.I[0][0] == 0 and edge.I[1][0] == 0 and EA[0] == 0 and EB[0] == 1 - edge.d
    qA, rB, vB = EA[1], EB[0], EB[1]
    s = edge.F(0, qA)                      # full state [0, F_A(qA)]
    A = []
    for k in range(K):
        if s >= qA:
            A.append(k + 1)
        if s >= rB:
            s = edge.F(1, min(s, vB))
        elif s < qA:
            s = edge.F(0, s)
        else:
            break
        if s == 0:
            break
    return A


def renewal_dim(A, delta):
    d = mpf(delta.numerator) / delta.denominator if isinstance(delta, Fr) else mpf(delta)
    if len(A) < 2:
        return mpf(0)
    f = lambda s: sum(d ** (n * s) for n in A) - 1
    lo, hi = mpf('1e-12'), mpf(1)
    for _ in range(150):
        m = (lo + hi) / 2
        if f(m) > 0:
            lo = m
        else:
            hi = m
    return lo


def count_dim(gs, n, look):
    """growth of word counts: log(N_n/N_{n-10})/(10 log beta)"""
    c = gs.counts(n, look)
    N1, N0 = c[-1][1], c[-11][1]
    beta = 1 / float(gs.d)
    return math.log(N1 / N0) / (10 * math.log(beta)), c


def lsz_from_system(gs, K=60, look=40):
    a = gs.extreme_word(0, True, K, look)
    b = gs.extreme_word(1, False, K, look)
    beta = Fr(1) / gs.d
    return lsz_dim(a, b, mpf(beta.numerator) / beta.denominator), a, b


def renewal_set_kappa(delta, kappa, K=250, dps=90):
    """Same forced path as renewal_set, for the class I_A = I_B = [0, kappa], in mpmath
    (dps digits; the error grows by at most beta per step, so dps=90 is safe for K=250
    with beta <= 2).  E_A = [0, delta*kappa], E_B = [1-delta, 1-delta+delta*kappa]."""
    with mp.workdps(dps):
        d, kap = mpf(delta), mpf(kappa)
        qA, rB, vB = d * kap, 1 - d, 1 - d + d * kap
        s = kap
        A = []
        for k in range(K):
            if s >= qA:
                A.append(k + 1)
            if s >= rB:
                s = (min(s, vB) - (1 - d)) / d
            elif s < qA:
                s = s / d
            else:
                break
            if s == 0:
                break
        return A
