# Target 1: dim(delta) as delta -> 1/phi from above.
from mpmath import mp, mpf, log, sqrt, lambertw, ceil, findroot
from gw import X_of, path, zroot, G
mp.dps = 160
phi = (1+sqrt(5))/2
d0 = 1/phi

def root_bisect(f, lo=mpf('1e-30'), hi=1-mpf('1e-60'), it=500):
    for _ in range(it):
        m = (lo+hi)/2
        if f(m) > 0: hi = m
        else: lo = m
    return (lo+hi)/2

rows = []
for k in list(range(2, 41)) + [60, 80]:
    eps = mpf(10)**(-k)
    d = d0 + eps
    b = 1/d; X = X_of(d)
    # N = least n >= 2 with beta^n (X-1) >= X
    N = int(ceil(log(X/(X-1))/log(b)))
    if N < 2: N = 2
    K = 7*N + 50
    A, S, stop, _ = path(d, K)
    assert A[0] == 1 and A[1] == N, (k, A[:3], N)
    gaps = [A[i+1]-A[i] for i in range(1, len(A)-1)]
    assert all(g >= N-1 for g in gaps), (k, gaps)
    z = zroot(A)
    s = log(z)/log(d)
    zN = root_bisect(lambda z: z + z**N - 1)                       # lower bound on dim
    eN = root_bisect(lambda z: z + z**N/(1 - z**(N-1)) - 1)        # upper bound on dim
    sl = log(zN)/log(d); su = log(eN)/log(d)
    W = lambertw(N).real
    sW = W/(N*log(b))
    L = log(1/eps)
    rows.append((k, N, A[:4], s, sl, su, sW, s*L/log(L), (log(N)-log(log(N)))/(N*log(b))))
    tol = mpf(10)**(-100)
    assert sl - tol <= s <= su + tol, (k, sl, s, su)

print("k  N   A(first)            dim            lower(z+z^N=1)   upper            W(N)/(N log b)   dim*L/logL   (logN-loglogN)/(N log b)")
for r in rows:
    k, N, A4, s, sl, su, sW, ratio, asym = r
    print(f"{k:2d} {N:4d} {str(A4):22s} {float(s):.10f} {float(sl):.10f} {float(su):.10f} {float(sW):.10f} {float(ratio):.6f} {float(asym):.6f}")
# relative errors of W-approximation
print("max rel err W-approx vs dim for k>=10:", max(float(abs(r[6]/r[3]-1)) for r in rows if r[0] >= 10))
print("rel width of bracket at k=40:", [float((r[5]-r[4])/r[3]) for r in rows if r[0] == 40])

# Sharper closed form: dim * L  vs  W(L/log phi), L = log(1/eps)
print("\nk   dim*L        W(L/log phi)   diff        diff*L/(log L)^2")
for r in rows:
    k = r[0]; s = r[3]
    L = k*log(10)
    Wc = lambertw(L/log(phi)).real
    print(f"{k:2d} {float(s*L):.8f} {float(Wc):.8f} {float(s*L-Wc):+.6f} {float((s*L-Wc)*L/log(L)**2):+.4f}")
