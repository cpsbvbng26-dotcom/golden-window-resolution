# Independent check of targets 1-3: brute counting of cylinders of the greedy map T_beta(y) = beta*y mod 1
# that meet the n-step survivor set of the hole (t,1), t = delta*X (lit-check reduction), no first-return formula used.
import sys
from mpmath import mp, mpf, log, sqrt
from gw import X_of, path, zroot
mp.dps = 120

def counts_right(beta, t, n):
    c = 1/beta
    key = lambda l, r: (mp.nstr(l, 50), mp.nstr(r, 50))
    states = {key(mpf(0), t): (mpf(0), t, 1)}
    N = [1]
    for _ in range(n):
        new = {}
        for (l, r, m) in states.values():
            pieces = []
            if l < c: pieces.append((beta*l, beta*min(r, c)))
            if r >= c: pieces.append((beta*max(l, c) - 1, beta*r - 1))
            for (l2, r2) in pieces:
                r2 = min(r2, t)
                if l2 <= r2:
                    k = key(l2, r2)
                    new[k] = (l2, r2, (new[k][2] if k in new else 0) + m)
        states = new
        N.append(sum(v[2] for v in states.values()))
    return N

def compare(d, n=220, m=80):
    d = mpf(d); beta = 1/d; t = d*X_of(d)
    N = counts_right(beta, t, n)
    h_count = (log(N[-1]) - log(N[-1-m]))/m
    A, S, stop, _ = path(d, 1500)
    h_formula = -log(zroot(A, it=600))
    return h_count/log(beta), h_formula/log(beta)

if __name__ == "__main__":
    for dd in ['0.62', '0.6425', '0.65', '0.66', str(mpf(2)/3 - mpf('1e-2')), str(mpf(2)/3 - mpf('1e-3'))]:
      a, b = compare(mpf(dd))
      print(f"delta={mp.nstr(mpf(dd), 10):>12s}  dim by counting={mp.nstr(a, 10)}  dim by first-return formula={mp.nstr(b, 10)}  1-dim(count)={mp.nstr(1-a, 6)}")
      sys.stdout.flush()
