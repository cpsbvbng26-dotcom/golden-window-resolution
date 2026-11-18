"""Check of Theorem A (reduction) by a computation that does not use the intervals I_a:
for eventually periodic A/B paths, decide SPE directly from the raw stage payoffs
(continuation values summed exactly, deviation payoffs from the payoff table), and compare
with the map test x_t in D_{e_t}.  Random games, random edges, random delta (exact Fractions)."""
import random
from fractions import Fraction as Fr
from gen import Game, Edge, Gn, linear_dilemma, pd

random.seed(20261118)

def value(seq_pre, seq_cyc, d, f):
    """(1-d) sum d^t f(e_t) for path pre + cyc^inf, exact"""
    v = Fr(0); w = Fr(1)
    for e in seq_pre:
        v += (1 - d) * w * f(e); w *= d
    m = len(seq_cyc)
    cyc = sum((1 - d) * d ** k * f(e) for k, e in enumerate(seq_cyc))
    return v + w * cyc / (1 - d ** m)

def direct_ok(E, pre, cyc):
    """Abreu/grim-trigger test straight from payoffs: every t in pre + one cycle"""
    G, d = E.G, E.d
    prof = {0: E.A, 1: E.B}
    path = pre + cyc
    for t in range(len(path)):
        tail_pre = path[t + 1:len(pre)] if t + 1 < len(pre) else []
        # continuation after t: remaining pre then cycle, rotated if t>=len(pre)
        if t + 1 <= len(pre):
            tp, tc = pre[t + 1:], cyc
        else:
            k = (t + 1 - len(pre)) % len(cyc)
            tp, tc = [], cyc[k:] + cyc[:k]
        a = prof[path[t]]
        ga = G.g(a)
        for i in range(G.n):
            Vi = value(tp, tc, d, lambda e: G.g(prof[e])[i])
            if (1 - d) * ga[i] + d * Vi < (1 - d) * G.dev(a, i) + d * E.vlow[i]:
                return False
    return True

def map_ok(E, pre, cyc):
    path = pre + cyc
    x = value(pre, cyc, E.d, lambda e: Fr(e))      # x_0 = (1-d) sum d^t e_t
    xs = []
    for t in range(len(path)):
        if t + 1 <= len(pre):
            tp, tc = pre[t:], cyc
        else:
            k = (t - len(pre)) % len(cyc)
            tp, tc = [], cyc[k:] + cyc[:k]
        xt = value(tp, tc, E.d, lambda e: Fr(e))
        D = E.D(path[t])
        if D is None or not (D[0] <= xt <= D[1]):
            return False
    return True

def rand_game(n, k=2, lo=-4, hi=6):
    acts = [str(j) for j in range(k)]
    tab = {}
    import itertools
    for a in itertools.product(*[acts] * n):
        tab[a] = tuple(Fr(random.randint(lo * 2, hi * 2), 2) for _ in range(n))
    return Game(n, acts, lambda a: tab[a])

if __name__ == '__main__':
    agree = dis = pos = 0
    cases = []
    games = [(Gn(3), ('C','C','C'), ('C','D','C')), (linear_dilemma(3, Fr(3,2)), ('C','C','C'), ('C','C','D')),
             (pd(1, Fr(1,2)), ('C','C'), ('D','C'))]
    import itertools
    for _ in range(25):
        n = random.choice([2, 3])
        G = rand_game(n)
        profs = list(itertools.product(*[G.actions] * n))
        A, B = random.sample(profs, 2)
        games.append((G, A, B))
    for G, A, B in games:
        for _ in range(40):
            d = Fr(random.randint(30, 97), 100)
            E = Edge(G, A, B, d)
            pre = [random.randint(0, 1) for _ in range(random.randint(0, 4))]
            cyc = [random.randint(0, 1) for _ in range(random.randint(1, 6))]
            a1, a2 = direct_ok(E, pre, cyc), map_ok(E, pre, cyc)
            if a1 == a2: agree += 1
            else: dis += 1
            pos += a1
    print('paths compared', agree + dis, 'agree', agree, 'disagree', dis, 'SPE paths among them', pos)
