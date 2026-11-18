import numpy as np, sys
from aps_vert import solve
from scipy.optimize import linprog
Minv=lambda phi: (np.sum(phi)-np.array(phi))/2.0
tests={'(2,3,3)':(0,1,1),'(2,2.5,2.5)':(0,.5,.5),'(2,2.2,2.2)':(0,.2,.2),'(2,3.5,2.5)':(0,1.5,.5),'(2,2.1,2.9)':(0,.1,.9),'(2.1,2.1,2.1)':(.1,.1,.1),'(2,2.05,2.05)':(0,.05,.05)}
def inside(V,x):
    n=len(V); r=linprog(np.zeros(n),A_eq=np.vstack([V.T,np.ones(n)]),b_eq=np.r_[x,1],bounds=[(0,None)]*n,method='highs')
    return r.status==0
if __name__=="__main__":
  for d in map(float,sys.argv[1:]):
    V,it=solve(d)
    print("delta",d,"nvert",len(V), {k:inside(V,Minv(v)) for k,v in tests.items()},flush=True)
