# Theorem J: JSR{S, S^T} = phi; Euclidean norm extremal; at gamma=1/phi all products have ||.||_2 <= 1;
# x_k -> 0 for every x0 iff the switching word has infinitely many repeated adjacent letters.
import numpy as np, itertools, sympy as sp, random
S=np.array([[1.,1.],[0.,1.]]); T=S.T; phi=(1+5**0.5)/2
# Check 1 (symbolic): singular values of S, rho(S S^T), ||S^2||
s=sp.Matrix([[1,1],[0,1]])
print("Check 1 (sympy): eig(S^T S) =",[sp.nsimplify(e) for e in (s.T*s).eigenvals()],
      " rho(S S^T) =",sp.nsimplify(max((s*s.T).eigenvals(),key=lambda e: float(e))),
      " ||S^2||_2^2 =",sp.nsimplify(max((s**2).T*(s**2)).eigenvals() if False else max(((s**2).T*(s**2)).eigenvals(),key=lambda e: float(e))))
q=np.linalg.norm(S@S,2)/phi**2; print("   q = ||S^2||/phi^2 =",q," exact (1+sqrt2)/phi^2 =",(1+2**0.5)/phi**2)
# Check 2 (brute force over all words up to length 18): max normalised norm and which words attain ~1
best={}
for n in range(1,19):
    mx=0; arg=None
    for w in itertools.product([0,1],repeat=n):
        M=np.eye(2)
        for l in w: M=(S if l==0 else T)@M
        v=np.linalg.norm(M,2)/phi**n
        if v>mx+1e-12: mx,arg=v,w
    best[n]=(mx,arg)
for n in (1,2,3,4,8,12,18):
    print("   n=%2d max ||M_w||/phi^n = %.12f  attained by %s"%(n,best[n][0],''.join('ST'[l] for l in best[n][1])))
# lower bound side: rho(ST)^(1/2) = phi
print("   rho(S T)^(1/2) =",max(abs(np.linalg.eigvals(S@T)))**0.5," phi =",phi)
# Check 3 (simulation): gamma=1/phi; words with repeats -> 0; eventually alternating -> nonzero limit
g=1/phi; rng=random.Random(1)
def run(word,x):
    x=np.array(x,float)
    for l in word: x=g*((S if l==0 else T)@x)
    return np.linalg.norm(x)
x0=[0.3,-1.1]
alt=[k%2 for k in range(4000)]
print("Check 3: alternating word, |x_4000| =",run(alt,x0)," (bounded away from 0)")
# alternating with a repeat inserted every 50 letters
w=[];
for blk in range(80): w+= [k%2 for k in range(50)]+[blk%2]
r=run(w,x0); print("   repeats every ~51 letters (%d repeats): |x| = %.3e, bound q^%d*|x0| = %.3e"%(80,r,80,q**80*np.linalg.norm(x0)))
# i.i.d. random words
print("   i.i.d. fair random words of length 4000:",["%.2e"%run([rng.randrange(2) for _ in range(4000)],x0) for _ in range(5)])
# monotonicity: |x_{k+1}| <= |x_k| along random words
mx=0
for _ in range(200):
    x=np.random.default_rng(_).normal(size=2)
    for k in range(200):
        y=g*((S if rng.randrange(2)==0 else T)@x); mx=max(mx,np.linalg.norm(y)/np.linalg.norm(x)); x=y
assert mx <= 1 + 1e-12, mx  # the claim: no step increases the norm
print("   max one-step ratio over 40000 random steps: %.12f" % mx)
