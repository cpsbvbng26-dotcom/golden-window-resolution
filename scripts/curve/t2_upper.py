# Target 2: 1 - dim(delta) as delta -> 2/3 from below.
from fractions import Fraction as F
from mpmath import mp, mpf, log
from gw import X_of, path, zroot, G
mp.dps = 250

# A* at delta = 2/3 exactly (rational arithmetic): positions n with s_{n-1} >= 1 = delta X
def Astar(K):
    s = F(3, 2); b = F(3, 2); A = []
    for k in range(K):
        assert s != 1 and s != 0
        if s >= 1:
            A.append(k+1); s = b*(s-1)
        else:
            s = b*s
    return A
As = Astar(400)
print("A* first terms:", As[:20])
# check: sum_{A*} (2/3)^n = delta*X = 1 (to truncation)
tw = mpf(2)/3
print("sum (2/3)^n over A* =", mp.nstr(sum(tw**n for n in As), 30))
M1 = sum(n*tw**n for n in As)
C = 9/(log(mpf(3)/2)*M1)
print("M1 = sum n (2/3)^n =", mp.nstr(M1, 30))
print("C  = 9/(log(3/2) M1) =", mp.nstr(C, 30))

# exact escape identity  1 - G_d(d) = (1/X) sum_{n in A} d^{n-1} |H cap [0, s_{n-1}]|
for dd in ['0.62', '0.6345', '0.65', '0.66', '0.6666']:
    d = mpf(dd); X = X_of(d)
    A, S, stop, _ = path(d, 900)
    lhs = 1 - G(A, d)
    rhs = 0
    for n in A:
        s = S[n-1]
        rhs += d**(n-1)*(max(0, min(s, 1) - d*X))
    rhs /= X
    print(f"delta={dd}: 1-G(delta)={mp.nstr(lhs, 20)}  escape sum={mp.nstr(rhs, 20)}  diff={mp.nstr(lhs-rhs, 3)}")

print("\n k   1-dim                 (1-dim)/eps           ratio to C        kappa/(9 eps)")
for k in range(2, 31):
    eps = mpf(10)**(-k)
    d = mpf(2)/3 - eps
    A, S, stop, _ = path(d, 1200)
    z = zroot(A, it=900)
    s = log(z)/log(d)
    kappa = 1 - G(A, d)
    print(f"{k:2d} {mp.nstr(1-s, 15):>22s} {mp.nstr((1-s)/eps, 15):>20s} {mp.nstr((1-s)/eps/C, 12):>16s} {mp.nstr(kappa/(9*eps), 12):>16s}")
