import numpy as np, itertools, sys
from p23 import P23
from scipy.optimize import linprog
Phi=np.array([[-1,1,1],[1,-1,1],[1,1,-1]],float)
def inside(V,x,tol=1e-10):
    n=len(V); r=linprog(np.zeros(n),A_eq=np.vstack([V.T,np.ones(n)]),b_eq=np.r_[x,1],bounds=[(0,None)]*n,method='highs')
    return r.status==0
def gens(d):
    V=P23(d); eps=(1-d)/d; out={}
    for x in V:
        ok=[]
        for a in itertools.product([0,1],repeat=3):
            a=np.array(a); y=(x-(1-d)*a)/d
            if np.any(y<-1e-12) or np.any(y>1+1e-12): continue
            if any(Phi[i]@y<eps-1e-12 for i in range(3) if a[i]==1): continue
            if inside(V,y): ok.append(''.join('CD'[1-k] for k in a))
        out[tuple(np.round(x,4))]=ok
    return out
for d in map(float,sys.argv[1:]):
    g=gens(d); bad=[k for k,v in g.items() if not v]
    print("delta",d,"ungenerated vertices:",bad)
    if d==float(sys.argv[1]):
        for k,v in g.items(): print("   ",k,v)
