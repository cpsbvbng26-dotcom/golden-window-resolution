# Joint continuity at a point where BOTH alpha(beta) and b(t,beta) jump: beta0 = golden ratio
# (greedy expansion of 1 is 110^inf, finite), t0 = 1/beta0^3 (greedy expansion 0010^inf, finite).
import sys
from mpmath import mp, mpf, sqrt
from t5_hole0 import dim_est
mp.dps = 90
b0 = (1+sqrt(5))/2
for t0name, t0 in [('1/phi^3', 1/b0**3), ('1/phi^2+1/phi^5', 1/b0**2 + 1/b0**5)]:
    print("point beta0 = phi, t0 =", t0name, "=", mp.nstr(t0, 12), " dim there:", mp.nstr(dim_est(b0, t0, 200, 80)[0], 8))
    print(" k    (+e,+e)     (+e,-e)     (-e,+e)     (-e,-e)     (+e,0)      (0,-e)")
    for k in range(3, 10, 2):
        e = mpf(10)**(-k)
        vals = [dim_est(b0+sb*e, t0+st*e, 200, 80)[0] for sb, st in [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,-1)]]
        print(f"{k:2d}  " + "  ".join(f"{float(v):.6f}" for v in vals)); sys.stdout.flush()
