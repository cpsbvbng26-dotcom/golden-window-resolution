# Outer approximation (Judd-Yeltekin-Conklin support-function method) of the SPE payoff set
# of the repeated G_3 with public randomization, pure stage actions, perfect monitoring.
# Coordinates: x_i in [0,1] = discounted frequency with which player i cooperates.
# Payoff v_i = 2 + sum_{j!=i} x_j - x_i.  IC for a cooperator i: phi_i(y) >= eps, eps=(1-delta)/delta,
# phi_i(y) = sum_{j!=i} y_j - y_i  (= w_i - 2).  IR: phi_i >= 0.
import numpy as np, itertools, sys
from scipy.optimize import linprog
def fib_dirs(n):
    i=np.arange(n)+0.5; phi=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.c_[np.cos(th)*np.sin(phi),np.sin(th)*np.sin(phi),np.cos(phi)]
Phi=np.array([[-1,1,1],[1,-1,1],[1,1,-1]],float)   # rows: phi_i(y)=Phi[i].y
def aps(delta,ndir=300,iters=400,tol=1e-10,verbose=False):
    eps=(1-delta)/delta
    L=fib_dirs(ndir)
    L=np.vstack([L,np.eye(3),-np.eye(3),Phi,-Phi])
    # start: IR cap cube
    H=np.vstack([np.eye(3),-np.eye(3),-Phi]); h=np.r_[np.ones(3),np.zeros(3),np.zeros(3)]
    prof=[np.array(a,float) for a in itertools.product([0,1],repeat=3)]
    c_old=None
    for it in range(iters):
        c=np.full(len(L),-np.inf)
        for a in prof:
            A=H.copy(); b=h.copy()
            idx=[i for i in range(3) if a[i]==1]
            if idx:
                A=np.vstack([A,-Phi[idx]]); b=np.r_[b,-eps*np.ones(len(idx))]
            for k,l in enumerate(L):
                r=linprog(-l,A_ub=A,b_ub=b,bounds=[(None,None)]*3,method='highs')
                if r.status==0:
                    val=(1-delta)*l@a+delta*(-r.fun)
                    c[k]=max(c[k],val)
        if np.all(~np.isfinite(c)): return None
        # new outer set = intersection of halfspaces l.x <= c(l), plus IR & cube
        H=np.vstack([L,np.eye(3),-np.eye(3),-Phi]); h=np.r_[c,np.ones(3),np.zeros(3),np.zeros(3)]
        if c_old is not None and np.max(np.abs(c-c_old))<tol: break
        c_old=c
    return L,c,it
if __name__=="__main__":
    for d in map(float,sys.argv[1:]):
        out=aps(d)
        if out is None: print(d,"empty"); continue
        L,c,it=out
        print("delta",d,"iters",it)
        # report support in a few directions
        names={'x1':[1,0,0],'-x1':[-1,0,0],'x1+x2+x3':[1,1,1],'-(x1+x2+x3)':[-1,-1,-1]}
        for k in range(len(L)-12,len(L)): print("  dir",np.round(L[k],3),"h=%.9f"%c[k])
