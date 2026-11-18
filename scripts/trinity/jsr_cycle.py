# Theorem K: JSR{D Q_n, D Q_n^T} = max_i sqrt(a_i a_{i+1}) (n>=3, cyclic indices).
import numpy as np, itertools
rng=np.random.default_rng(7)
def Qn(n):
    Q=np.zeros((n,n))
    for i in range(n): Q[i,(i-1)%n]=1
    return Q
def brute(a,L):
    n=len(a);D=np.diag(a);F=D@Qn(n);B=D@Qn(n).T
    lo=0;hi=0
    for k in range(1,L+1):
        best=0
        for w in itertools.product([0,1],repeat=k):
            M=np.eye(n)
            for l in w: M=(F if l==0 else B)@M
            best=max(best,max(abs(np.linalg.eigvals(M)))**(1/k))
            hi_k=None
        lo=max(lo,best)
    # upper bound: max over words of length L of ||M||_inf^(1/L) (monomial => exact max entry)
    ub=0
    for w in itertools.product([0,1],repeat=L):
        M=np.eye(n)
        for l in w: M=(F if l==0 else B)@M
        ub=max(ub,np.abs(M).max()**(1/L))
    return lo,ub
worst=0
for trial in range(12):
    n=int(rng.integers(3,7)); a=rng.uniform(0.05,0.99,n); L=12
    pred=max(np.sqrt(a[i]*a[(i+1)%n]) for i in range(n))
    lo,ub=brute(a,L)
    worst=max(worst,abs(lo-pred))
    print("n=%d a=%s pred=%.9f  lower(rho,len<=%d)=%.9f  upper(maxentry,len %d)=%.9f"%(n,np.round(a,3),pred,L,lo,L,ub))
print("max |lower - pred| =",worst)
a=np.array([0.5,0.7,0.3]); print("Series II a=(0.5,0.7,0.3): pred",max(np.sqrt(a[i]*a[(i+1)%3]) for i in range(3)), brute(a,12))
