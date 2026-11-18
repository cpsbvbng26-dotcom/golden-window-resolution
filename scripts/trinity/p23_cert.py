# Maximality certificate for E(delta) = P23(delta): weak LP duality + Perron root < 1.
import numpy as np, itertools, sys
from fractions import Fraction as Fr
from scipy.optimize import linprog
from p23_facets import P23, facets
Phi=np.array([[-1,1,1],[1,-1,1],[1,1,-1]],float)
def run(dfr):
    d=float(dfr); eps=(1-d)/d
    F=facets(P23(dfr)); L=[];h=[];known=[]
    for (n,hh),on in F.items():
        n=np.array([float(t) for t in n]); L.append(n); h.append(float(hh))
        # known-valid families: IR (phi_i>=0), cube x_i<=1, difference x_j-x_i<=delta
        nz=np.round(n,12)
        isIR=any(np.allclose(nz,-Phi[i]) for i in range(3)) and abs(float(hh))<1e-14
        iscube=(sorted(np.abs(nz))==[0,0,1]) and nz.max()==1 and abs(float(hh)-1)<1e-14
        isdiff=(sorted(nz)==[-1,0,1]) and abs(float(hh)-d)<1e-14
        known.append(isIR or iscube or isdiff)
    L=np.array(L);h=np.array(h);known=np.array(known)
    U=[k for k in range(len(L)) if not known[k]]
    A0=np.vstack([L,np.eye(3),-np.eye(3)]); b0=np.r_[h,np.ones(3),np.zeros(3)]
    Mmax=np.zeros((len(U),len(U))); worst_gap=-1
    for ki,k in enumerate(U):
        best=-np.inf
        for a in itertools.product([0,1],repeat=3):
            a=np.array(a,float); idx=[i for i in range(3) if a[i]==1]
            A=np.vstack([A0]+([-Phi[idx]] if idx else [])); b=np.r_[b0,-eps*np.ones(len(idx))]
            r=linprog(-L[k],A_ub=A,b_ub=b,bounds=[(None,None)]*3,method='highs')
            if r.status!=0: continue
            mu=-r.ineqlin.marginals   # >=0 duals
            val=(1-d)*L[k]@a+d*(-r.fun)
            best=max(best,val)
            for ji,j in enumerate(U): Mmax[ki,ji]=max(Mmax[ki,ji],mu[j])
        worst_gap=max(worst_gap,best-h[k])
    rho=max(abs(np.linalg.eigvals(d*Mmax)))
    return len(L),len(U),worst_gap,rho
for s in sys.argv[1:]:
    n,u,g,rho=run(Fr(s))
    print("delta %-6s facets %d (unknown %d)  max[B-value - h] = %.2e   Perron root of delta*M = %.4f"%(s,n,u,g,rho))
