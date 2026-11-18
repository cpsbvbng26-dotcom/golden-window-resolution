# Target 5: numerics for the beta-transformation with a hole (0,t) (Allaart-Kong setting).
# Independent of the symbolic formulas: count n-cylinders of T_beta that meet the n-step survivor set
# {x in [t,1): T^j x in [t,1), j<n}, by a dynamic programme over cylinder images with multiplicities.
import sys
from mpmath import mp, mpf, log, findroot
mp.dps = 90

def counts(beta, t, n):
    beta = mpf(beta); t = mpf(t); c = 1/beta
    key = lambda l, r: (mp.nstr(l, 40), mp.nstr(r, 40))
    states = {key(t, mpf(1)): (t, mpf(1), 1)}
    N = [1]
    for _ in range(n):
        new = {}
        for (l, r, m) in states.values():
            pieces = []
            if l < c:
                pieces.append((beta*l, beta*min(r, c)))
            if r > c:
                pieces.append((beta*max(l, c) - 1, beta*r - 1))
            for (l2, r2) in pieces:
                l2 = max(l2, t)
                if l2 < r2:
                    k = key(l2, r2)
                    if k in new:
                        new[k] = (new[k][0], new[k][1], new[k][2] + m)
                    else:
                        new[k] = (l2, r2, m)
        states = new
        N.append(sum(v[2] for v in states.values()))
    return N, len(states)

def dim_est(beta, t, n=160, m=60):
    N, ns = counts(beta, t, n)
    if N[-1] == 0 or N[-1-m] == 0:
        return mpf(0), ns, N[-1]
    h = (log(N[-1]) - log(N[-1-m]))/m
    return h/log(mpf(beta)), ns, N[-1]

if __name__ == '__main__':
    # sanity: t -> 0 gives dim -> 1; compare a fixed point with the 'alpha - t' generating function where it applies
    for (bb, tt) in [('1.8', '0.001'), ('1.8', '0.2'), ('1.9', '0.3')]:
        s, ns, NN = dim_est(bb, tt)
        print("sanity beta", bb, "t", tt, "dim est", mp.nstr(s, 8), "states", ns)
    # Allaart-Kong discontinuity point of tau: S = 01, beta_r with alpha(beta_r) = 11(01)^inf
    f = lambda B: 1/B + 1/B**2 + 1/(B**2*(B**2-1)) - 1
    br = findroot(f, 1.8)
    tl, tr = 1/br**2, 1/(br**2-1)
    t0 = (tl+tr)/2
    print("beta_r =", mp.nstr(br, 15), " tau(beta_r) =", mp.nstr(tl, 12), " tau(beta_r+) =", mp.nstr(tr, 12), " t0 =", mp.nstr(t0, 12))
    print("dim at (beta_r, t0):", mp.nstr(dim_est(br, t0)[0], 8))
    print(" k   horizontal (br+e, t0)   vertical-ish (br+e, t0-e)   diagonal (br+e, t0+e)")
    for k in range(2, 10):
        e = mpf(10)**(-k)
        h1 = dim_est(br+e, t0)[0]; h2 = dim_est(br+e, t0-e)[0]; h3 = dim_est(br+e, t0+e)[0]
        print(f"{k:2d}   {mp.nstr(h1, 8):>14s}   {mp.nstr(h2, 8):>14s}   {mp.nstr(h3, 8):>14s}")
        sys.stdout.flush()
