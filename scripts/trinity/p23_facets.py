import itertools, sys
from fractions import Fraction as Fr
def P23(d):
    e=1-d; V={(Fr(1),Fr(1),Fr(1)),(Fr(0),Fr(0),Fr(0))}
    for b in [(e,Fr(1),Fr(1)),(d,Fr(1),e),(1-e*e,d*e,d),(d*d+e,d*d+e/2,e/2)]:
        for p in itertools.permutations(range(3)): V.add(tuple(b[p[k]] for k in range(3)))
    return sorted(V)
def cross(u,v): return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def facets(V):
    F={}
    for A,B,C in itertools.combinations(V,3):
        n=cross(tuple(B[i]-A[i] for i in range(3)),tuple(C[i]-A[i] for i in range(3)))
        if n==(0,0,0): continue
        h=sum(n[i]*A[i] for i in range(3))
        s=[sum(n[i]*P[i] for i in range(3))-h for P in V]
        if all(x<=0 for x in s): pass
        elif all(x>=0 for x in s): n=tuple(-t for t in n); h=-h
        else: continue
        # normalise
        k=next(i for i in range(3) if n[i]!=0); m=abs(n[k]); n=tuple(t/m for t in n); h=h/m
        F[(n,h)]=[P for P in V if sum(n[i]*P[i] for i in range(3))==h]
    return F
if __name__=="__main__":
  d=Fr(sys.argv[1]); F=facets(P23(d))
  print("delta",d,"facets",len(F))
  for (n,h),on in sorted(F.items()): print("  %s . x <= %s   (%d vertices)"%(tuple(str(t) for t in n),h,len(on)))
