# Target 3: plateaus of the entropy h(delta) = -log z*(delta).
import random
from mpmath import mp, mpf, log, sqrt, findroot
from gw import X_of, path, zroot, G
mp.dps = 150
phi = (1+sqrt(5))/2
lo, hi = 1/phi, mpf(2)/3

def stopinfo(d, K=3000):
    A, S, stop, _ = path(d, K)
    return A, S, stop

# (a) fraction of the window (uniform grid) whose forced path has not stopped by step K
random.seed(1)
NS = 20000
pts = [lo + (hi-lo)*mpf(i+0.5)/NS for i in range(NS)]
stops = []
for d in pts:
    A, S, stop = stopinfo(d, 600)
    stops.append(stop if stop is not None else 10**9)
for K in [5, 10, 20, 40, 80, 160, 320, 600]:
    frac = sum(1 for s in stops if s > K)/NS
    sub = [s for d, s in zip(pts, stops) if d < mpf('0.66')]
    frac2 = sum(1 for s in sub if s > K)/len(sub)
    print(f"K={K:4d}: fraction of grid with no stop by step K = {frac:.5f};  K*fraction = {K*frac:.3f};  restricted to delta<0.66: {frac2:.5f}")

# (b) the plateau with A = {1,4}: endpoints solve beta^4 (X-1) = X (left) and beta^3 (X-1) = 1 (right)
fL = lambda d: (1/d)**4*(X_of(d)-1) - X_of(d)
fR = lambda d: (1/d)**3*(X_of(d)-1) - 1
dL = findroot(fL, 0.64); dR = findroot(fR, 0.645)
print("\nplateau A={1,4}: [", mp.nstr(dL, 15), ",", mp.nstr(dR, 15), "]")
z14 = zroot([1, 4])
print("h on it = -log z, z+z^4=1:", mp.nstr(-log(z14), 15))
for d in [dL+mpf('1e-9'), mpf('0.640'), mpf('0.6425'), mpf('0.645'), dR-mpf('1e-9')]:
    A, S, stop = stopinfo(d)
    z = zroot(A)
    print("  delta", mp.nstr(d, 12), "A", A, "h", mp.nstr(-log(z), 12), "dim", mp.nstr(log(z)/log(d), 12))
for d in [dL-mpf('1e-6'), dR+mpf('1e-6')]:
    A, S, stop = stopinfo(d)
    z = zroot(A)
    print("  outside", mp.nstr(d, 12), "A[:8]", A[:8], "h", mp.nstr(-log(z), 12))

# (c) admissibility of u = 1_A (sigma^k u < u lexicographically) and distinct h for distinct A, on the grid
def lexless(u, v):
    for x, y in zip(u, v):
        if x != y:
            return x < y
    return len(u) < len(v)
bad = 0; comps = {}
for d in pts[::5]:
    A, S, stop = stopinfo(d, 600)
    if stop is None:
        continue
    n = A[-1]
    u = [1 if (i+1) in A else 0 for i in range(n)] + [0]*n
    for k in range(1, n):
        if not lexless(u[k:], u[:len(u)-k]):
            bad += 1; break
    comps.setdefault(tuple(A), []).append(d)
print("\nadmissibility violations:", bad, "; distinct finite A seen:", len(comps))
# h strictly increasing across components (sorted by delta)
items = sorted(comps.items(), key=lambda kv: kv[1][0])
hs = [(-log(zroot(list(A))), A) for A, ds in items]
viol = sum(1 for i in range(len(hs)-1) if not hs[i][0] < hs[i+1][0])
print("components in delta order with non-increasing h:", viol, "of", len(hs)-1)

# (d) transversality: ds_k/d delta >= beta^k (1+beta^2) - k beta X, on parameter intervals with fixed digits
worst = mpf(10)
for d in pts[::97]:
    A, S, stop = stopinfo(d, 60)
    kmax = min(len(S), 40)
    h_ = mpf('1e-25')
    A2, S2, stop2, _ = path(d+h_, 60)
    for k in range(1, min(kmax, len(S2))):
        der = (S2[k]-S[k])/h_
        bnd = (1/d)**k*(1+(1/d)**2) - k*(1/d)*X_of(d)
        worst = min(worst, der/bnd)
print("min over sample of (ds_k/d delta)/(beta^k(1+beta^2)-k beta X):", mp.nstr(worst, 8))

# (e) absolutely continuous part of dim: integral of h/(delta log^2 beta) over the window, vs total increase 1
M = 4000
acc = mpf(0)
for i in range(M):
    d = lo + (hi-lo)*(i+mpf(0.5))/M
    A, S, stop = stopinfo(d, 600)
    z = zroot(A, it=200)
    h = -log(z)
    acc += h/(d*log(1/d)**2)
acc *= (hi-lo)/M
print("integral of h/(delta log^2 beta) over the window =", mp.nstr(acc, 8), "(total increase of dim is 1)")
