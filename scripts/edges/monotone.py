"""dim along the edge CCC-CCD of the 3-player linear dilemma, on a fine grid of each window;
counts decreases (monotonicity is proved for r <= 1 = k-1; for r > 1 it is only tested here),
and reports the values next to the window ends (limits 0 and 1)."""
from fractions import Fraction as Fr
from mpmath import mpf
from gen import Edge, linear_dilemma, Gn, renewal_set, renewal_dim, renewal_set_kappa
from mpmath import mp
from examples import theta, U

def run(G, A, B, k, r, N=600):
    th, u = float(theta(k, r)), float(U(k, r))
    vals = []
    for i in range(1, N):
        d = Fr(th + (u - th) * i / N).limit_denominator(10**6)
        E = Edge(G, A, B, d)
        kind, _ = E.classify()
        assert kind == 'gap', (kind, d)
        assert E.I[0] == E.I[1] and E.I[0][0] == 0
        kap = E.I[0][1]
        Am = renewal_set_kappa(mpf(d.numerator) / d.denominator, mpf(kap.numerator) / kap.denominator)
        if i % 100 == 0:          # spot check against the exact path
            assert renewal_set(E, 60) == [n for n in Am if n <= 60]
        s = renewal_dim(Am, d)
        vals.append((float(d), float(s)))
    dec = sum(1 for i in range(len(vals) - 1) if vals[i + 1][1] < vals[i][1] - 1e-12)
    return dec, vals

if __name__ == '__main__':
    for r in [Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1), Fr(5, 4), Fr(3, 2), Fr(7, 4), Fr(19, 10)]:
        dec, v = run(linear_dilemma(3, r), ('C','C','C'), ('C','C','D'), 2, r)
        print(f'r={r}: decreases {dec}/{len(v)-1}; first {v[0][0]:.6f}:{v[0][1]:.4f}  last {v[-1][0]:.6f}:{v[-1][1]:.4f}')
    for n in [4, 5]:
        A = tuple('C' for _ in range(n)); B = tuple('C' for _ in range(n - 1)) + ('D',)
        dec, v = run(Gn(n), A, B, n - 1, 1)
        print(f'G_{n} main edge: decreases {dec}/{len(v)-1}; first {v[0][0]:.6f}:{v[0][1]:.4f}  last {v[-1][0]:.6f}:{v[-1][1]:.4f}')
