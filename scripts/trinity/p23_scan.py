import numpy as np, sys
from aps_vert import solve
from p23 import P23
from scipy.spatial import ConvexHull
for d in map(float,sys.argv[1:]):
    V,it=solve(d); V=np.unique(np.round(V,9),axis=0)
    C=P23(d); hc=ConvexHull(C); C=C[hc.vertices]; C=np.unique(np.round(C,9),axis=0)
    same = len(V)==len(C) and np.allclose(V[np.lexsort(V.T)],C[np.lexsort(C.T)],atol=1e-7)
    print("delta %.4f APS vertices %d candidate vertices %d equal %s  vol APS %.10f cand %.10f"%(d,len(V),len(C),same,ConvexHull(V).volume,hc.volume),flush=True)
