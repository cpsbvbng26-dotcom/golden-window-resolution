import numpy as np, itertools
def P23(d):
    e=1-d; V=[(1,1,1),(0,0,0)]
    base=[(e,1,1),(d,1,e),(1-e*e,d*e,d),(d*d+e,d*d+e/2,e/2)]
    for b in base:
        for p in itertools.permutations(range(3)):
            V.append(tuple(b[p[k]] for k in range(3)))
    return np.unique(np.round(np.array(V,float),12),axis=0)
