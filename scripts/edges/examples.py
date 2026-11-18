"""Step 3: examples, computed exactly.  python3 examples.py"""
import math
from fractions import Fraction as Fr
from mpmath import mp, mpf, sqrt
from gen import Edge, GapSystem, Gn, linear_dilemma, renewal_set, renewal_dim, lsz_from_system, count_dim
from edges import edges

mp.dps = 30

def dims(E, check=False):
    kind, data = E.classify()
    if kind == 'interval':
        return kind, mpf(1), None
    if kind != 'gap':
        return kind, mpf(0), None
    A = renewal_set(E)
    s = renewal_dim(A, E.d)
    extra = None
    if check:
        gs = GapSystem(E)
        ls, a, b = lsz_from_system(gs, K=150, look=40)
        cd, _ = count_dim(gs, 120, 0)
        extra = (ls, cd)
    return kind, s, (A[:6], extra)

def M(r):
    return mpf(r.numerator) / r.denominator if isinstance(r, Fr) else mpf(r)

def theta(k, r):
    r = M(r)
    return (sqrt((k - 1) ** 2 + 4 * mpf(r)) - (k - 1)) / 2

def U(k, r):
    r = M(r)
    return max(mpf(1) / 2, (1 + mpf(r)) / (k + 1))

def rotation3(r):
    r = M(r)
    return (sqrt(1 + 4 * mpf(r)) - 1) / 2

def rotation_n(n, r=1):
    # Prop 2/7: g(d) = (n-2)d - r + (1+r) h(d), h = d^(n-1)/(1+...+d^(n-1)); bisection
    def g(d):
        h = d ** (n - 1) / sum(d ** j for j in range(n))
        return (n - 2) * d - r + (1 + r) * h
    lo, hi = mpf(0), mpf(1)
    for _ in range(120):
        m = (lo + hi) / 2
        if g(m) >= 0: hi = m
        else: lo = m
    return hi

def scan_window(game, A, B, lo, hi, N=400):
    """locate, on an exact rational grid, where the classification is gap with positive
    dimension (renewal set has >= 2 elements)"""
    first = last = None
    for i in range(1, N):
        d = Fr(lo) + (Fr(hi) - Fr(lo)) * i / N
        E = Edge(game, A, B, d)
        kind, _ = E.classify()
        if kind == 'gap' and E.I[0][0] == 0 and E.I[1][0] == 0 and len(renewal_set(E)) >= 2:
            if first is None: first = d
            last = d
    return first, last

if __name__ == '__main__':
    print('== Example 1: the note (G_3, edge CCC-CDC)')
    G = Gn(3)
    for dl in ['0.6181', '0.62', '0.63', '0.64', '0.65', '0.66', '0.6666']:
        E = Edge(G, ('C','C','C'), ('C','D','C'), Fr(dl))
        k, s, ex = dims(E, check=True)
        print(f'  delta {dl}: {k}, renewal {float(s):.6f}, LSZ {float(ex[1][0]):.6f}, count(n=110..120) {ex[1][1]:.4f}, A {ex[0]}')
    f, l = scan_window(G, ('C','C','C'), ('C','D','C'), Fr(1, 2), Fr(1), 2000)
    print('  grid window (step 1/4000):', float(f), float(l), ' closed form:', float(theta(2, 1)), float(U(2, 1)))

    print('== Example 2: 3-player linear dilemma, r = c/b')
    G0 = linear_dilemma(3, Fr(1))
    print('  edges exposed by exactly two profiles (r=1):', len(edges(G0)))
    for r in [Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1), Fr(5, 4), Fr(3, 2), Fr(7, 4)]:
        G = linear_dilemma(3, r)
        for (A, B, k) in [(('C','C','C'), ('C','C','D'), 2), (('C','C','D'), ('C','D','D'), 1), (('C','D','D'), ('D','D','D'), 0)]:
            if k <= r:
                f, l = scan_window(G, A, B, Fr(1, 100), Fr(1), 1000)
                print(f'  r={r} edge {"".join(A)}-{"".join(B)} (k={k}): k<=r, grid window: {f}')
                continue
            f, l = scan_window(G, A, B, Fr(1, 100), Fr(1), 1000)
            print(f'  r={r} edge {"".join(A)}-{"".join(B)} (k={k}): grid {float(f):.4f}..{float(l):.4f}'
                  f'  closed form ({float(theta(k, r)):.4f}, {float(U(k, r)):.4f})'
                  + (f'  rotation delta_3(r) = {float(rotation3(r)):.4f}' if k == 2 else ''))
    print('  dim(r, delta) on edge CCC-CCD:')
    for r in [Fr(1, 2), Fr(3, 4), Fr(1), Fr(5, 4), Fr(3, 2)]:
        G = linear_dilemma(3, r)
        th, u = theta(2, r), U(2, r)
        row = []
        for t in [Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(7, 10), Fr(9, 10)]:
            d = Fr(th.__float__()).limit_denominator(10**9) * (1 - t) + Fr(u.__float__()).limit_denominator(10**9) * t
            E = Edge(G, ('C','C','C'), ('C','C','D'), d)
            k, s, ex = dims(E, check=(t == Fr(1, 2)))
            row.append(f'{float(d):.4f}:{float(s):.4f}' + (f'[LSZ {float(ex[1][0]):.4f}, count {ex[1][1]:.4f}]' if ex and ex[1] else ''))
        print(f'   r={r}: ', '  '.join(row))

    print('== Example 3: G_n, main edge C^n - C^(n-1)D, and edges with k other cooperators')
    for n in [2, 3, 4, 5]:
        G = Gn(n)
        A = tuple('C' for _ in range(n)); B = tuple('C' for _ in range(n - 1)) + ('D',)
        if n == 2:
            from edges import edge3
            gg = {a: G.g(a) for a in [('C','C'), ('C','D'), ('D','C'), ('D','D')]}
            print('  n=2: payoffs', {''.join(a): tuple(map(int, v)) for a, v in gg.items()},
                  '-> g(CC) = g(DD); feasible set is a segment; no edge with exactly two profiles')
            continue
        f, l = scan_window(G, A, B, Fr(1, 100), Fr(1), 1000)
        print(f'  n={n}: grid {float(f):.4f}..{float(l):.4f}  closed form ({float(theta(n-1, 1)):.4f}, {float(U(n-1, 1)):.4f})'
              f'  rotation delta_{n} = {float(rotation_n(n)):.6f}')
        for dl in [Fr(1, 2) * (theta(n-1,1) + U(n-1,1)).__float__()]:
            d = Fr(dl).limit_denominator(10**6)
            E = Edge(G, A, B, d)
            k, s, ex = dims(E, check=True)
            print(f'      mid-window delta {float(d):.4f}: dim {float(s):.5f}  LSZ {float(ex[1][0]):.5f} count {ex[1][1]:.4f}')
        for k in range(2, n - 1):
            A2 = tuple('C' for _ in range(k)) + ('C',) + tuple('D' for _ in range(n - k - 1))
            B2 = tuple('C' for _ in range(k)) + ('D',) + tuple('D' for _ in range(n - k - 1))
            f, l = scan_window(G, A2, B2, Fr(1, 100), Fr(1), 1000)
            print(f'     edge with k={k} other cooperators: grid {float(f):.4f}..{float(l):.4f}'
                  f'  closed form ({float(theta(k, 1)):.4f}, {float(U(k, 1)):.4f})')
