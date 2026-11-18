import numpy as np
P=np.array([[0,0,1],[1,0,0],[0,1,0]],float); a=0.6; p=np.array([1,0,0.])
print("Series I T* =",np.round(np.linalg.solve(np.eye(3)-a*P,(1-a)*p),6),"printed (0.510204, 0.306122, 0.183673)")
# grim threshold: VC=3/(1-d) >= VD=4+2d/(1-d)
import sympy as sp; d=sp.symbols('d'); print("Series I grim threshold:",sp.solve(sp.Eq(3/(1-d),4+2*d/(1-d)),d))
# Series III: P_n^2 = I only for n=2
for n in range(2,9):
    Pn=np.roll(np.eye(n),1,axis=0); print(n, np.allclose(Pn@Pn,np.eye(n)), np.abs(Pn@Pn.T-np.eye(n)).max())
