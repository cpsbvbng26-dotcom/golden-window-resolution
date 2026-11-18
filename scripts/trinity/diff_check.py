import numpy as np, sys
from aps_vert import solve
for d in map(float,sys.argv[1:]):
    V,it=solve(d)
    m=max(abs(v[i]-v[j]) for v in V for i in range(3) for j in range(3))
    print("delta %.3f  max |x_i - x_j| over APS vertices = %.10f   (bound delta)  vertices %d"%(d,m,len(np.unique(np.round(V,9),axis=0))),flush=True)
