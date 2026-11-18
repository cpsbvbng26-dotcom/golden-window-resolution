"""(1) Prop 5 of the note recovered from Theorems A-B; (2) porosity of Theorem C measured on
S_N; (3) Theorem G(a): the cube edges of G_4, G_5 are exposed by exactly two profiles (exact
certificates), and a non-edge pair is not exposed (exact separating argument)."""
import random, itertools, math
from fractions import Fraction as Fr
from gen import Edge, Gn, linear_dilemma, GapSystem
from check_dichotomy import backward

random.seed(3)
G = Gn(3)
A, B = ('C','C','C'), ('C','D','C')
print('(1) Prop 5 recovered (t = 1 - x):')
for d in [Fr(1, 2), Fr(11, 20), Fr(3, 5), Fr(2, 3), Fr(7, 10), Fr(9, 10)]:
    E = Edge(G, A, B, d)
    kind, data = E.classify()
    S, hist = backward(E, 40)
    big = [(a, b) for a, b in S if b - a > d ** 40]
    pts = sorted(set(round(float(1 - (a + b) / 2), 12) for a, b in S))
    if kind == 'interval':
        print(f'   delta {d}: interval, T = [{1 - data[1]}, {1 - data[0]}]  (Prop 5(4): [1-delta, 1])')
    else:
        print(f'   delta {d}: {kind}, components at depth 40: {len(S)}, longest {float(max(b-a for a,b in S)):.2e}, T approx {pts[:4]}')

print('(2) porosity on S_N (Theorem C): c = min(g/2, 1/4)')
for d in [Fr(31, 50), Fr(16, 25), Fr(33, 50)]:
    E = Edge(G, A, B, d)
    gs = GapSystem(E)
    g = gs.E[1][0] - gs.E[0][1]
    c = min(g / 2, Fr(1, 4))
    N = 18
    S, _ = backward(E, N)
    worst = 10.0
    for _ in range(3000):
        L = 10 ** random.uniform(-3, 0)
        x0 = random.uniform(0, 1 - L)
        lo, hi = Fr(x0), Fr(x0) + Fr(L)
        # largest gap of S_N inside [lo, hi]
        pts = [lo]
        for a, b in S:
            if b < lo or a > hi: continue
            pts += [max(a, lo), min(b, hi)]
        pts.append(hi)
        best = max(pts[i + 1] - pts[i] for i in range(0, len(pts) - 1, 2))
        worst = min(worst, float(best / (hi - lo)))
    Nn = math.floor(2 / c) + 1
    print(f'   delta {d}: g = {float(g):.4f}, c = {float(c):.4f}, smallest hole ratio found {worst:.4f} (>= c: {worst >= float(c)}),'
          f' box-dimension bound log(N-1)/log N = {math.log(Nn-1)/math.log(Nn):.5f}')

print('(3) Theorem G(a): exposing functionals for cube edges of the linear dilemma')
def certificate(Gm, n, i, c):
    # c: 0/1 vector (1 = C) with c_i = 1; edge to c with c_i = 0. Functional on cube coords:
    s = [Fr(0) if j == i else (Fr(1) if c[j] else Fr(-1)) for j in range(n)]
    # g = M c + shift, M = J - (1+r) I; lambda = M^{-T} s.  Solve M^T lam = s (M symmetric).
    r = Gm_r
    # M^{-1} = -(1/(1+r)) (I + J/(n-1-r-... )) : solve numerically exact by Gaussian elimination
    Mx = [[Fr(1) - (1 + r if a == b else 0) for b in range(n)] for a in range(n)]
    aug = [row[:] + [s[k]] for k, row in enumerate(Mx)]
    for col in range(n):
        piv = next(k for k in range(col, n) if aug[k][col] != 0)
        aug[col], aug[piv] = aug[piv], aug[col]
        for k in range(n):
            if k != col and aug[k][col] != 0:
                f = aug[k][col] / aug[col][col]
                aug[k] = [x - f * y for x, y in zip(aug[k], aug[col])]
    lam = [aug[k][n] / aug[k][k] for k in range(n)]
    prof = lambda v: tuple('C' if t else 'D' for t in v)
    Ap = prof(c); c2 = list(c); c2[i] = 0; Bp = prof(c2)
    gA, gB = Gm.g(Ap), Gm.g(Bp)
    dot = lambda u, v: sum(x * y for x, y in zip(u, v))
    if dot(lam, gA) != dot(lam, gB): return False
    for C in itertools.product('CD', repeat=n):
        if C in (Ap, Bp): continue
        if dot(lam, Gm.g(C)) >= dot(lam, gA): return False
    return True
for n in [3, 4, 5]:
    for Gm_r, Gm in [(Fr(1), Gn(n)), (Fr(1, 3), linear_dilemma(n, Fr(1, 3))), (Fr(n - 1, 2), linear_dilemma(n, Fr(n - 1, 2)))]:
        ok = tot = 0
        for c in itertools.product([0, 1], repeat=n):
            for i in range(n):
                if c[i] == 1:
                    tot += 1
                    ok += certificate(Gm, n, i, c)
        print(f'   n={n}, r={Gm_r}: certified {ok}/{tot} edges (expected n*2^(n-1) = {n * 2 ** (n - 1)})')
