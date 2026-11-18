import numpy as np, itertools, sys
from fractions import Fraction as Fr
from scipy.optimize import linprog
from p23_facets import P23, facets
PhiF=[[-1,1,1],[1,-1,1],[1,1,-1]]
for s in sys.argv[1:]:
    d=Fr(s); eps=(1-d)/d; F=facets(P23(d))
    base=[(list(n),hh) for (n,hh) in F]+[([1 if j==i else 0 for j in range(3)],Fr(1)) for i in range(3)]+[([-1 if j==i else 0 for j in range(3)],Fr(0)) for i in range(3)]
    out=[]
    for a in itertools.product([0,1],repeat=3):
        idx=[i for i in range(3) if a[i]==1]
        cons=base+[([-t for t in PhiF[i]],-eps) for i in idx]
        A=np.array([[float(t) for t in c[0]] for c in cons]); b=np.array([float(c[1]) for c in cons])
        r=linprog(np.r_[0,0,0,1],A_ub=np.c_[A,-np.ones(len(A))],b_ub=b,bounds=[(None,None)]*3+[(None,None)],method='highs')
        out.append((''.join('DC'[t] for t in a),round(r.x[3],6)))
    print(s,"min violation t* per profile (t*>0 means infeasible):",out)
