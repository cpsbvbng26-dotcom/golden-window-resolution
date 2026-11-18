# Exact rational version of the maximality certificate: rationalise the LP duals and verify
# dual feasibility and the bound in exact arithmetic; then the Perron-root step: e_k <= delta*sum_j M_kj e_j.
import numpy as np, itertools, sys
from fractions import Fraction as Fr
from scipy.optimize import linprog
from p23_facets import P23, facets
PhiF=[[-1,1,1],[1,-1,1],[1,1,-1]]
def run(dfr):
    d=dfr; eps=(1-d)/d
    F=facets(P23(d)); rows=[];known=[]
    for (n,hh),on in F.items():
        rows.append((list(n),hh))
        isIR=any(list(n)==[-t for t in PhiF[i]] for i in range(3)) and hh==0
        iscube=sorted(n)==[0,0,1] and hh==1
        isdiff=sorted(n)==[-1,0,1] and hh==d
        known.append(isIR or iscube or isdiff)
    base=rows+[([1 if j==i else 0 for j in range(3)],Fr(1)) for i in range(3)]+[([-1 if j==i else 0 for j in range(3)],Fr(0)) for i in range(3)]
    U=[k for k in range(len(rows)) if not known[k]]
    M=[[Fr(0)]*len(U) for _ in U]; ok=True
    for ki,k in enumerate(U):
        lam=rows[k][0]; hk=rows[k][1]
        for a in itertools.product([0,1],repeat=3):
            idx=[i for i in range(3) if a[i]==1]
            cons=base+[([-t for t in PhiF[i]],-eps) for i in idx]
            A=np.array([[float(t) for t in c[0]] for c in cons]); b=np.array([float(c[1]) for c in cons])
            r=linprog(-np.array([float(t) for t in lam]),A_ub=A,b_ub=b,bounds=[(None,None)]*3,method='highs')
            if r.status==2:  # infeasible: no constraint from this profile (needs exact infeasibility proof; checked below)
                continue
            mu=[Fr(-m).limit_denominator(10**7) for m in r.ineqlin.marginals]
            mu=[m if m>0 else Fr(0) for m in mu]
            # exact dual feasibility: sum mu_c * A_c = lam
            for t in range(3):
                if sum(mu[c]*cons[c][0][t] for c in range(len(cons)))!=lam[t]: ok=False
            bound=sum(mu[c]*cons[c][1] for c in range(len(cons)))
            val=(1-d)*sum(lam[t]*a[t] for t in range(3))+d*bound
            if val>hk: ok=False
            for ji,j in enumerate(U): M[ki][ji]=max(M[ki][ji],mu[j])
    rowsum=max(sum(r) for r in M)
    return ok,rowsum
for s in sys.argv[1:]:
    ok,rs=run(Fr(s))
    print("delta %-8s exact dual feasibility and bounds: %s ; max row sum of multipliers on unknown facets = %s ; delta*rowsum = %s"%(s,ok,rs,Fr(s)*rs))
