"""Edges of the feasible set exposed by exactly two pure profiles (any number of players):
pair (A,B) qualifies iff some lambda has lambda.(g(A)-g(B)) = 0 and lambda.(g(A)-g(C)) > 0
for every other profile C.  Search: random lambda in the subspace plus a local improvement,
then an exact certificate with Fractions.  (A failed search is not a proof of non-edge; for
3 players we also run an exact 2-D test.)"""
import itertools, random
from fractions import Fraction as Fr

def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def dot(u, v): return sum(a * b for a, b in zip(u, v))
def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])

def certify(G, A, B, lam):
    gA, gB = G.g(A), G.g(B)
    if dot(lam, sub(gA, gB)) != 0: return False
    M = dot(lam, gA)
    for C in itertools.product(*[G.actions] * G.n):
        if C in (A, B): continue
        if dot(lam, G.g(C)) >= M: return False
    return True

def edge3(G, A, B):
    """exact test for 3 players: the plane lambda.w0 = 0 is 2-D; open half-plane intersection"""
    gA, gB = G.g(A), G.g(B)
    w0 = sub(gA, gB)
    if w0 == (0, 0, 0): return None
    e = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    u = next(cross(w0, x) for x in e if cross(w0, x) != (0, 0, 0))
    v = cross(w0, u)
    ns = []
    for C in itertools.product(*[G.actions] * G.n):
        if C in (A, B): continue
        w = sub(gA, G.g(C))
        ns.append((dot(u, w), dot(v, w)))
    cands = []
    eta = Fr(1, 10**6)
    for (p, q) in ns:
        cands += [(p, q), (-q + eta * p, p + eta * q), (q + eta * p, -p + eta * q)]
    for (p, q) in ns:
        for (p2, q2) in ns:
            cands.append((p + p2, q + q2))
    for (s, t) in cands:
        if all(s * p + t * q > 0 for (p, q) in ns):
            lam = tuple(s * a + t * b for a, b in zip(u, v))
            assert certify(G, A, B, lam)
            return lam
    return None

def edges(G):
    profs = list(itertools.product(*[G.actions] * G.n))
    out = []
    for A, B in itertools.combinations(profs, 2):
        lam = edge3(G, A, B)
        if lam is not None:
            out.append((A, B, lam))
    return out
