import numpy as np, sys
from aps_vert import solve
from aps_test import inside, Minv
pts=[(1.5,.5),(.15,.05),(.6,.2),(.1,.9),(.01,.09),(1,1),(.3,.3)]
for d in map(float,sys.argv[1:]):
    V,it=solve(d)
    print("delta",d, [(p, round(max(p)/sum(p),4), inside(V,Minv((0,)+p))) for p in pts],flush=True)
