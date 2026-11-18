# Target 4: why 1/phi twice. Linear dilemma: cooperator pays c, gives b to each co-player; r = c/b.
import sympy as sp
from fractions import Fraction as F

d, b, c = sp.symbols('delta b c', positive=True)
a = b - c            # stage payoff of a cooperator with one cooperating co-player
D = 2*b              # defector with two cooperating co-players (rotation)
Wstar = 2*b - c      # all-C forever
cinc = (1-d)*c/d     # incentive bound on the continuation value (grim trigger, minmax 0)
Q = b*d + b*d**2 - c

# Rotation values (period 3): V0 = defect now, V1 = defect in 1 period, V2 = defect in 2 periods.
V0, V1, V2 = sp.symbols('V0 V1 V2')
sol = sp.solve([sp.Eq(V0, (1-d)*D + d*V2), sp.Eq(V1, (1-d)*a + d*V0), sp.Eq(V2, (1-d)*a + d*V1)], [V0, V1, V2])
# Binding cooperator: the one defecting in 2 periods (value V2). Incentive: V2 >= (1-d)(a+c) + d*0  <=>  V1 >= cinc
rot_slack = sp.simplify(sol[V1] - cinc)
seg_slack = sp.simplify((1-d)*a + d*Wstar - cinc)    # value of (C,D,C) then all-C, minus cinc
print("rotation slack  V1 - cinc            =", sp.factor(rot_slack))
print("segment  slack  (CDC, then CCC) - cinc =", sp.factor(seg_slack))
print("ratio rot/seg =", sp.factor(sp.simplify(rot_slack/seg_slack)))
print("V0 - W*  =", sp.factor(sp.simplify(sol[V0] - Wstar)), "   ; -Q/(1+d+d^2) =", sp.factor(-Q/(1+d+d**2)))
print("check rot = seg + d*(V0-W*):", sp.simplify(rot_slack - (seg_slack + d*(sol[V0]-Wstar))))
# direct incentive check with V2 too
print("V2 - (1-d)(a+c) - d*0 =", sp.factor(sp.simplify(sol[V2] - (1-d)*(a+c))))

# Window in x-coordinates for general r (b = 1): X_r = (2d - r)/(d(1-d)); lower end X_r = 1, upper end d X_r = 1
r = sp.symbols('r', positive=True)
Xr = (2*d - r)/(d*(1-d))
print("X_r - 1 numerator:", sp.factor(sp.numer(sp.together(Xr-1))), " ; 1 - d X_r numerator:", sp.factor(sp.numer(sp.together(1-d*Xr))))
print("width condition: (1+r)/3 - delta3(r) > 0 <=> 4(r-2)^2>0 :", sp.factor(sp.expand((2*r+5)**2 - 9*(1+4*r))))

# Numeric, independent of the algebra: thresholds by bisection on simulated discounted sums.
def disc(stream_fn, dd, T=4000):
    v = 0.0; w = 1.0
    for t in range(T):
        v += w*stream_fn(t); w *= dd
    return (1-dd)*v

def rot_ok(dd, bb, cc):
    # each cooperator phase: continuation from next period must be >= (1-dd)cc/dd
    ok = True
    for phase in range(3):   # phase = periods until own defection
        if phase == 0: continue
        cont = disc(lambda t: (2*bb) if (t - (phase-1)) % 3 == 0 else (bb-cc), dd)
        ok &= cont >= (1-dd)*cc/dd - 1e-13
    return ok

def seg_ok(dd, bb, cc):
    # the lowest admissible continuation c_inc must be reachable by (C,D,C) followed by something <= all-C value
    return (1-dd)*(bb-cc) + dd*(2*bb-cc) >= (1-dd)*cc/dd - 1e-13

def thresh(test, bb, cc):
    lo_, hi_ = 1e-6, 1-1e-9
    for _ in range(60):
        m = (lo_+hi_)/2
        if test(m, bb, cc): hi_ = m
        else: lo_ = m
    return hi_

print("\n r      rotation thr   segment thr    (sqrt(1+4r)-1)/2")
for rr in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.9]:
    t1 = thresh(rot_ok, 1.0, rr); t2 = thresh(seg_ok, 1.0, rr)
    print(f"{rr:5.2f}  {t1:.9f}   {t2:.9f}   {((1+4*rr)**0.5-1)/2:.9f}")
