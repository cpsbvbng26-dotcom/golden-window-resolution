# Checks of Theorem F (the face "player 1 always cooperates" of the Series II example).
# P(d) = {x1=1, x2>=1-d, x3>=1-d, x2+x3>=1}, d>=1/2.
import numpy as np, itertools
from fractions import Fraction as Fr
import random
from aps_vert import solve
from scipy.spatial import ConvexHull
# Check 2: APS outer iteration (no use of the formula); slice x1=1 vs pentagon
print("Check 2: APS slice x1 = 1 versus the pentagon")
for d in [0.505,0.52,0.55,0.6,2/3,0.7,0.75,0.8,0.9]:
    V,it=solve(d)
    F=V[np.abs(V[:,0]-1)<1e-9][:,1:]
    F=np.unique(np.round(F,9),axis=0)
    pent=np.array([[1,1],[1,1-d],[d,1-d],[1-d,d],[1-d,1]])
    pent=np.unique(np.round(pent,9),axis=0)
    ok=len(F)==len(pent) and np.allclose(np.sort(F,axis=0),np.sort(pent,axis=0),atol=1e-7)
    print("  delta=%.4f  slice vertices=%d  pentagon vertices=%d  equal=%s"%(d,len(F),len(pent),ok))
V,it=solve(0.49); print("  delta=0.49: any vertex with x1=1?", bool(np.any(np.abs(V[:,0]-1)<1e-9)))
# Check 3: exact rational self-generation of P(d) with explicit decompositions, plus IC on simulated paths
print("Check 3: exact decomposition of the five vertices, rational delta")
def in_P(y,d): return y[0]<=1 and y[1]<=1 and y[0]>=1-d and y[1]>=1-d and y[0]+y[1]>=1
def in_Tp(y,d):  # continuation set for player 1's IC: y2+y3 >= 1+eps
    eps=(1-d)/d; return y[0]<=1 and y[1]<=1 and y[0]+y[1]>=1+eps
bad=0
for d in [Fr(1,2),Fr(11,20),Fr(3,5),Fr(2,3),Fr(7,10),Fr(4,5),Fr(9,10),Fr(99,100)]:
    eps=(1-d)/d
    verts={(1,1):((1,1),(Fr(1),Fr(1))),(1,1-d):((1,0),(Fr(1),eps)),(d,1-d):((0,0),(Fr(1),eps)),
           (1-d,d):((0,0),(eps,Fr(1))),(1-d,1):((0,1),(eps,Fr(1)))}
    for v,(a,y) in verts.items():
        x=tuple((1-d)*a[k]+d*y[k] for k in range(2))
        if x!=tuple(Fr(t) for t in v) or not in_Tp(y,d) or not in_P(y,d): bad+=1
print("  failures:",bad)
# path simulation: Markov strategy on continuation x in P: write x as lottery over the 4 images, play, move on
def decompose(x,d):
    # find lottery over vertices of P(d) (barycentric via LP-free fan triangulation from (1,1)),
    # then map each vertex to (action, continuation) as above.
    eps=(1-d)/d
    V=[(1,1),(1,1-d),(d,1-d),(1-d,d),(1-d,1)]
    act={0:((1,1),(1,1)),1:((1,0),(1,eps)),2:((0,0),(1,eps)),3:((0,0),(eps,1)),4:((0,1),(eps,1))}
    for k in range(1,4):
        A=np.array([[V[0][0],V[k][0],V[k+1][0]],[V[0][1],V[k][1],V[k+1][1]],[1,1,1]],float)
        try: lam=np.linalg.solve(A,[x[0],x[1],1])
        except np.linalg.LinAlgError: continue
        if lam.min()>=-1e-12: return [(lam[0],act[0]),(lam[1],act[k]),(lam[2],act[k+1])]
    return None
rng=random.Random(20261118); worst=1e9; nfail=0
for trial in range(300):
    d=rng.uniform(0.5,0.98)
    while True:
        x=(rng.uniform(1-d,1),rng.uniform(1-d,1))
        if x[0]+x[1]>=1: break
    # check: payoff of player 1 from realized path equals 2 + x2+x3-1 in expectation is not needed;
    # check IC at every realized period: continuation of player 1 (= 1 + y2 + y3) >= c = 1+1/d.
    cur=x
    for t in range(200):
        L=decompose(cur,d)
        if L is None: nfail+=1; break
        r=rng.random(); acc=0
        for lam,(a,y) in L:
            acc+=lam
            if r<=acc+1e-15: break
        w1=1+y[0]+y[1]; c=1+1/d
        worst=min(worst,w1-c)
        if not in_P(y,d): nfail+=1
        cur=y
print("  300 random starts, 200 periods each: decomposition failures=%d, min slack of player 1's IC=%.3e"%(nfail,worst))
