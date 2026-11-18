# Re-check every number printed in Series II (revised), independently.
import numpy as np, itertools
from scipy.spatial import ConvexHull
rng = np.random.default_rng(20261118)
# 3.1 anisotropic operator: sigma(T) = (T3,T1,T2)
Q = np.array([[0,0,1],[1,0,0],[0,1,0]],float)
a = np.array([0.5,0.7,0.3]); p = np.array([1,0,0.5]); D = np.diag(a)
f = lambda x: D@Q@x + (np.eye(3)-D)@p
Ts = np.linalg.solve(np.eye(3)-D@Q, (np.eye(3)-D)@p)
print("T* =", np.round(Ts,6), " printed (0.754190, 0.527933, 0.508380)")
dev=0
for _ in range(6):
    x=rng.random(3)
    for k in range(400): x=f(x)
    dev=max(dev,np.abs(x-Ts).max())
print("max deviation after 400 steps", dev)
X=rng.random((20000,3));Y=rng.random((20000,3))
r=np.linalg.norm((X-Y)@(D@Q).T,axis=1)/np.linalg.norm(X-Y,axis=1)
print("sup ratio over 20000 pairs", r.max(), " printed 0.699973; ||DQ||_2 =", np.linalg.norm(D@Q,2))
for k in range(1,7):
    M=np.linalg.matrix_power(D@Q,k)
    cyc=max(np.prod([a[(i-j)%3] for j in range(k)]) for i in range(3))
    print(" k=%d ||(DQ)^k||_2=%.6f  max cyclic product=%.6f"%(k,np.linalg.norm(M,2),cyc))
print("(DQ)^3 =", np.round(np.linalg.matrix_power(D@Q,3),12).tolist(), "prod a =", a.prod())
print("rho(DQ) =", max(abs(np.linalg.eigvals(D@Q))), " (prod a)^(1/3) =", a.prod()**(1/3))
# 4. game
def g(prof):
    nC=[sum(1 for j in range(3) if j!=i and prof[j]=='C') for i in range(3)]
    return tuple(nC[i]+1 if prof[i]=='C' else nC[i]+2 for i in range(3))
profs=[''.join(t) for t in itertools.product('CD',repeat=3)]
P=np.array([g(s) for s in profs],float)
for s in profs: print(s,g(s))
H=ConvexHull(P); print("hull volume",H.volume," vertices",len(H.vertices),"of 8")
# facets
eq=np.unique(np.round(H.equations/np.abs(H.equations[:,:3]).max(axis=1)[:,None],9),axis=0)
for e in eq: print(" facet: %s . v <= %s"%(np.round(e[:3],4), np.round(-e[3],4)))
# minmax
mm=min(max(g(''.join(x))[0] for x in [(ai,)+o] ) for o in itertools.product('CD',repeat=2) for ai in 'C')
print("pure minmax player1 =", min(max(g(ai+o[0]+o[1])[0] for ai in 'CD') for o in itertools.product('CD',repeat=2)))
# 6. spring network
K=np.array([[2,-1,-1],[-1,2,-1],[-1,-1,2]],float); al=0.25
print("eig K", np.round(np.linalg.eigvalsh(K),12), "rho(aK)=",max(abs(np.linalg.eigvals(al*K))))
S=np.zeros((3,3));T=K.copy()
for k in range(200): S+=T; T=al*K@T
C=K@np.linalg.inv(np.eye(3)-al*K)
print("K_inf closed form", np.round(C,12).tolist(), " partial-sum diff", np.abs(S-C).max())
