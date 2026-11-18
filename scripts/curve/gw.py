# Common routines for the golden window (deepen round, 2026-11-18).
# Notation: delta in (1/phi, 2/3), beta = 1/delta, X = (2delta-1)/(delta(1-delta)) = 1/(1-delta) - 1/delta.
from mpmath import mp, mpf, log, sqrt

def X_of(d):
    return (2*d-1)/(d*(1-d))

def path(d, K):
    """Forced path s_0..; returns (A, states, stop_index or None, dead_flag).
    A = {k+1 : s_k >= dX} along the path; stop when s_k in [dX,1)."""
    X = X_of(d); b = 1/d; s = X; A = []; S = []
    for k in range(K):
        S.append(s)
        if s >= d*X:
            A.append(k+1)
        if s >= 1:
            s = b*(s-1)
        elif s < d*X:
            s = b*s
        else:
            return A, S, k, False
    return A, S, None, False

def G(A, z):
    return sum(z**n for n in A)

def zroot(A, lo=None, hi=None, it=400):
    """root z* in (0,1) of sum_{n in A} z^n = 1 (bisection)."""
    lo = mpf(0) if lo is None else lo
    hi = mpf(1) if hi is None else hi
    for _ in range(it):
        m = (lo+hi)/2
        if G(A, m) > 1: hi = m
        else: lo = m
    return (lo+hi)/2

def dim(d, K=None):
    d = mpf(d)
    if K is None:
        K = 800
    A, S, stop, _ = path(d, K)
    z = zroot(A)
    return log(z)/log(d), A, z
