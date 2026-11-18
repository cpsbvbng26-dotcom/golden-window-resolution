# Prop 2/7 rotation threshold: delta_n(r) root of g = m d - r + (1+r) h(d), h = d^(n-1)(1-d)/(1-d^n), m=n-2.
# Claim A: delta_n(r) = r/m - (1+r)(m-r) r^(n-1) / m^(n+1) * (1+O(n (r/m)^(n-1)))... checked numerically.
from mpmath import mp, mpf, findroot
import math
mp.dps=200
def thr(n,r):
    m=n-2; h=lambda d: d**(n-1)*(1-d)/(1-d**n)
    g=lambda d: m*d-r+(1+r)*h(d)
    lo,hi=mpf(0),mpf(1)
    for _ in range(700):
        mid=(lo+hi)/2
        if g(mid)>=0: hi=mid
        else: lo=mid
    return hi
# direct simulation check (independent of g): value of the cooperator furthest from defection, by discounted sum
def thr_sim(n,r,T=3000):
    import numpy as np
    b,c=1.0,r
    def ok(d):
        # phase k=0: defector; player at phase j defects when (t+j)%n==0
        # value of player whose defection is n-1 periods away
        j=n-1; v=0.0; w=1.0
        for t in range(T):
            pay = b*(n-1) if (t-j)%n==0 else b*(n-2)-c
            v+=w*pay; w*=d
        v*=(1-d)
        dev=(1-d)*(b*(n-2))+d*0.0   # deviate: save c this period, then minmax 0
        return v>=dev
    lo,hi=0.0,1.0
    for _ in range(60):
        mid=(lo+hi)/2
        if ok(mid): hi=mid
        else: lo=mid
    return hi
print(" n   r     delta_n(r)              approx               rel.err of correction   sim(float)")
for r in (mpf(1),mpf('0.5'),mpf('1.5')):
    for n in (4,5,6,8,10,14,20,30):
        m=n-2
        if r>=m: continue
        d=thr(n,r); corr=(1+r)*(m-r)*r**(n-1)/m**(n+1)
        approx=r/m-corr
        err=abs((r/m-d)-corr)/corr
        s=thr_sim(n,float(r)) if n<=10 else float('nan')
        print("%3d %4s  %.18f  %.18f  %.3e   %.9f"%(n,mp.nstr(r,3),float(d),float(approx),float(err),s))
