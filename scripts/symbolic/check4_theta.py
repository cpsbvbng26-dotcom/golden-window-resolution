# Does b = max K~(t) arise from alpha by iterating KLX's Step 3 (theta) over the larger alphabet?
# theta(u) = (u_1 ... u_{m-1} (u_m - 1))^inf with m = min{k >= 1 : sigma^k u < a}; iterate until stable.
from itertools import product
from seqlib import *
from check2_realmap import max_of_X
from check2b_realmap import lyndon_words

def theta_iter(a, u):
    for _ in range(50):
        m = None
        for k in range(1, len(u[0]) + 3 * len(u[1]) + 5):
            if cmp(shift(u, k), a) < 0:
                m = k; break
        if m is None:
            return u
        w = prefix(u, m); w = w[:-1] + (w[-1] - 1,)
        if w[-1] < 0:
            return None
        u = ((), w)
    return None

tot = agree = 0
for alpha in [((), (2, 0)), ((), (2, 1, 0)), ((), (2, 2, 0)), ((), (3, 1)), ((), (2, 0, 1)), ((3,), (0, 2)), ((), (2, 1, 1, 0))]:
    M = max(alpha[0] + alpha[1])
    words = [(d,) for d in range(1, M + 1)] + [w for L in range(2, 6) for w in lyndon_words(M, L)]
    for w in words:
        a = ((), w)
        if not all(cmp(x, alpha) < 0 for x in shifts(a)) or hypothesis(a, alpha):
            continue
        b = max_of_X(a, alpha, M)
        th = theta_iter(a, alpha)
        tot += 1
        ok = (b is None and th is None) or (b is not None and th is not None and cmp(b, th) == 0)
        agree += ok
        if not ok:
            print("differs:", alpha, w, "max:", b, "theta:", th)
print("cases with alpha not in K~(t):", tot, " theta-iteration equals max:", agree)
