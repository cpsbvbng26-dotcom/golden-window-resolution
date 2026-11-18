# APS iteration B(W) = co U_a [(1-d)a + d (W cap U_a)] on polytopes given by vertices (outer start).
# x-coordinates (cooperation frequencies). See aps3d.py header.
import numpy as np, itertools, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
Phi=np.array([[-1,1,1],[1,-1,1],[1,1,-1]],float)
def hrep(V):
    h=ConvexHull(V); return h.equations  # rows [A|b]: A x + b <= 0
def intersect(V,extra):  # extra: list of (A_row, rhs) meaning A x <= rhs
    E=hrep(V); A=np.vstack([E[:,:3]]+[e[0][None] for e in extra]); b=np.r_[-E[:,3],[e[1] for e in extra]]
    # chebyshev center
    nrm=np.linalg.norm(A,axis=1)
    r=linprog(np.r_[0,0,0,-1],A_ub=np.c_[A,nrm],b_ub=b,bounds=[(None,None)]*3+[(0,None)],method='highs')
    if r.status!=0: return None
    if r.x[3]<1e-11:
        return 'degenerate'
    hs=HalfspaceIntersection(np.c_[A,-b],r.x[:3]); return hs.intersections
def B(V,d):
    eps=(1-d)/d; pts=[]
    for a in itertools.product([0,1],repeat=3):
        a=np.array(a,float); ex=[(-Phi[i],-eps) for i in range(3) if a[i]==1]
        W=V if not ex else intersect(V,ex)
        if W is None: continue
        if isinstance(W,str): raise RuntimeError('degenerate piece for a=%s'%a)
        pts.append((1-d)*a+d*W)
    P=np.vstack(pts); h=ConvexHull(P); return P[h.vertices]
def start():
    # IR cap cube: vertices by halfspace intersection
    A=np.vstack([np.eye(3),-np.eye(3),-Phi]); b=np.r_[np.ones(3),np.zeros(3),np.zeros(3)]
    hs=HalfspaceIntersection(np.c_[A,-b],np.array([0.6,0.6,0.6])); return hs.intersections
def solve(d,iters=3000,tol=1e-13):
    V=start(); vol=ConvexHull(V).volume
    for it in range(iters):
        V2=B(V,d); v2=ConvexHull(V2).volume
        if abs(v2-vol)<tol: return V2,it
        V,vol=V2,v2
    return V,it
if __name__=="__main__":
    for d in map(float,sys.argv[1:]):
        V,it=solve(d); h=ConvexHull(V)
        V=V[np.lexsort(np.round(V,9).T)]
        print("delta",d,"iterations",it,"volume %.12f"%h.volume,"nvert",len(V))
        for v in V: print("   ",np.round(v,9))
