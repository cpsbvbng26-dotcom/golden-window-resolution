"""Check of Theorem C (four constraints; the dimension depends on the end constraints only
through a and b) on gap systems where the end constraints are active
(alpha_A > 0 or omega_B < 1, so l != 0^inf or r != 1^inf).
Two numbers per case:
  LSZ  : maximal s with pi_{beta^s}(a) = pi_{beta^s}(b), a/b = extreme surviving A/B words
  count: growth of the exact word counts N_n of the survivor subshift (DP over states)
and a direct lexicographic test of Sigma_S = {sigma^n e in [l,a] u [b,r]} on random words."""
import random, itertools, math
from fractions import Fraction as Fr
from mpmath import mpf
from gen import Edge, GapSystem, lsz_dim, count_dim
from check_reduction import rand_game

random.seed(11)

def lex_le(u, v):
    """finite-prefix lexicographic u <= v on the common length"""
    for x, y in zip(u, v):
        if x != y:
            return x < y
    return True

def lex_ok(w, l, a, b, r):
    for j in range(len(w)):
        t = w[j:]
        if t[0] == 0 and not (lex_le(l, t) and lex_le(t, a)):
            return False
        if t[0] == 1 and not (lex_le(b, t) and lex_le(t, r)):
            return False
    return True

found = 0
rows = []
tries = 0
while found < 8 and tries < 5000:
    tries += 1
    n = random.choice([2, 3])
    G = rand_game(n)
    profs = list(itertools.product(*[G.actions] * n))
    A, B = random.sample(profs, 2)
    vlow = [G.pure_minmax(i) - Fr(random.randint(0, 6), 2) for i in range(n)]
    d = Fr(random.randint(52, 90), 100)
    E = Edge(G, A, B, d, vlow=vlow)
    kind, data = E.classify()
    if kind != 'gap' or data[0] is None or data[1] is None:
        continue
    if E.I[0][0] == 0 and E.I[1][1] == 1:
        continue          # want an active end constraint
    gs = GapSystem(E)
    try:
        cd, c = count_dim(gs, 70, 25)
    except ZeroDivisionError:
        continue
    if cd < 0.15:
        continue
    beta = mpf(d.denominator) / d.numerator
    a = gs.extreme_word(0, True, 120, 30); b = gs.extreme_word(1, False, 120, 30)
    l = gs.extreme_word(0, False, 120, 30); r = gs.extreme_word(1, True, 120, 30)
    s = lsz_dim(a, b, beta)
    if abs(float(s) - cd) > 5e-4:          # slow convergence: recount deeper
        cd, c = count_dim(gs, 400, 40)
    # lexicographic test on random words of length 14 against the dynamic language
    agree = dis = 0
    for _ in range(400):
        w = [random.randint(0, 1) for _ in range(14)]
        st = (gs.u, gs.v)
        for e in w:
            st = gs.step(st, e)
            if st is None: break
        dyn = st is not None and gs.alive(st, 30)
        lx = lex_ok(w, l, a, b, r)
        if dyn == lx: agree += 1
        else: dis += 1
    rows.append((float(d), E.I[0], E.I[1], float(s), round(cd, 4), agree, dis,
                 ''.join(map(str, l[:16])), ''.join(map(str, a[:16])), ''.join(map(str, b[:16])), ''.join(map(str, r[:16]))))
    found += 1
for row in rows:
    print('delta', row[0], 'I_A', tuple(map(float, row[1])), 'I_B', tuple(map(float, row[2])))
    print('   LSZ', round(row[3], 5), ' count', row[4], ' lex-test agree/disagree', row[5], row[6])
    print('   l', row[7], 'a', row[8], 'b', row[9], 'r', row[10])
