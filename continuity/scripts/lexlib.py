# Shared code for the numerics of the continuity paper (continuity/paper/joint-continuity.tex).
#
# A sequence over {0, ..., M} is eventually periodic and is stored as (pre, per): two tuples of ints,
# per non-empty, meaning pre per per per ...  Every function is deterministic.
#
# Three independent ways to get the entropy H(A, B) = h(Sigma_{A,B}) are implemented here:
#   raw_H      a "pending comparison" automaton for ANY pair (no normalization, no Theorem A);
#   thmA_h     Theorem A: -log of the smallest root in (0, 1) of sum (b_n - a_n) z^n = 1, found exactly
#              (integer polynomial, square-free part, real-root isolation); only for normalized pairs;
#   yd         the unfolded interval automaton of Theorem A restricted to match depths < D, which gives
#              h(Y_D) and the exact witnesses p_D = min Y_D, q_D = max Y_D.
import os
import sys
from math import gcd, log

import numpy as np
import sympy
from mpmath import mp, mpf
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

# ---------------------------------------------------------------- printing

AUDIT = os.environ.get('LEXLIB_AUDIT') == '1'


def fmt(g, cut=1e-11):
    """A small non-negative float (a gap) with two significant digits, or '<1e-11' below the cut. With
    LEXLIB_AUDIT=1 a warning goes to stderr when a perturbation of 1e-14 (absolute) or 1e-9 (relative) would
    change the printed text, so that last-bit differences between machines cannot change the output."""
    f = lambda x: '<1e-11' if x < cut else '%.1e' % x
    s = f(g)
    if AUDIT and any(f(x) != s for x in (g - 1e-14, g + 1e-14, g * (1 - 1e-9), g * (1 + 1e-9))):
        print('AUDIT: fragile gap %r -> %s' % (g, s), file=sys.stderr)
    return s


def fixed(x, d):
    """x with d decimals; with LEXLIB_AUDIT=1, a warning when a perturbation of 1e-12 would change the text."""
    s = '%.*f' % (d, x)
    if AUDIT and any('%.*f' % (d, y) != s for y in (x - 1e-12, x + 1e-12)):
        print('AUDIT: fragile value %r -> %s' % (x, s), file=sys.stderr)
    return s


# ---------------------------------------------------------------- sequences


def canon(pre, per):
    """Shortest pre-period and primitive period."""
    pre, per = tuple(pre), tuple(per)
    n = len(per)
    for d in range(1, n + 1):
        if n % d == 0 and per == per[:d] * (n // d):
            per = per[:d]
            break
    while pre and pre[-1] == per[-1]:
        pre, per = pre[:-1], (per[-1],) + per[:-1]
    return (pre, per)


def dig(s, i):
    """i-th digit (0-based)."""
    pre, per = s
    return pre[i] if i < len(pre) else per[(i - len(pre)) % len(per)]


def nxt(s, i):
    """Folded index after i: positions len(pre) + len(per) and len(pre) are identified."""
    pre, per = s
    i += 1
    return len(pre) if i == len(pre) + len(per) else i


def prefix(s, n):
    return tuple(dig(s, i) for i in range(n))


def shift(s, n):
    pre, per = s
    if n <= len(pre):
        return canon(pre[n:], per)
    k = (n - len(pre)) % len(per)
    return canon((), per[k:] + per[:k])


def lexcmp(x, y):
    """Exact lexicographic comparison: -1, 0 or 1."""
    L = max(len(x[0]), len(y[0])) + len(x[1]) * len(y[1]) // gcd(len(x[1]), len(y[1]))
    for i in range(L):
        u, v = dig(x, i), dig(y, i)
        if u != v:
            return -1 if u < v else 1
    return 0


def firstdiff(x, y):
    """Index (1-based) of the first digit where x and y differ, or None if x = y."""
    L = max(len(x[0]), len(y[0])) + len(x[1]) * len(y[1]) // gcd(len(x[1]), len(y[1]))
    for i in range(L):
        if dig(x, i) != dig(y, i):
            return i + 1
    return None


def normalized(a, b):
    """a, b in Sigma_{a,b}, decided exactly (the shifts of an eventually periodic sequence repeat)."""
    if lexcmp(a, b) > 0:
        return False
    for s in (a, b):
        for n in range(len(s[0]) + len(s[1])):
            t = shift(s, n)
            if lexcmp(t, a) < 0 or lexcmp(t, b) > 0:
                return False
    return True


def show(s, n=None):
    pre, per = s
    if n is None:
        return ''.join(map(str, pre)) + '(' + ''.join(map(str, per)) + ')^inf'
    return ''.join(map(str, prefix(s, n)))


# ---------------------------------------------------------------- graphs


def trim(n, edges):
    """States with an infinite future, and the labelled successor lists."""
    succ = [[] for _ in range(n)]
    pred = [[] for _ in range(n)]
    outdeg = [0] * n
    for u, c, v in edges:
        succ[u].append((c, v))
        pred[v].append(u)
        outdeg[u] += 1
    dead = [False] * n
    stack = [u for u in range(n) if outdeg[u] == 0]
    for u in stack:
        dead[u] = True
    while stack:
        v = stack.pop()
        for u in pred[v]:
            if not dead[u]:
                outdeg[u] -= 1
                if outdeg[u] == 0:
                    dead[u] = True
                    stack.append(u)
    alive = [not d for d in dead]
    out = [sorted((c, v) for c, v in succ[u] if alive[v]) for u in range(n)]
    return alive, out


def reachable(out, start=0):
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for _, v in out[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return sorted(seen)


def graph_entropy(n, edges, start=0):
    """log of the spectral radius of the trimmed part reachable from start (0 if empty or < 1)."""
    alive, out = trim(n, edges)
    if not alive[start]:
        return 0.0
    keep = reachable(out, start)
    pos = {u: i for i, u in enumerate(keep)}
    rows, cols = [], []
    for u in keep:
        for _, v in out[u]:
            rows.append(pos[u])
            cols.append(pos[v])
    m = len(keep)
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(m, m))
    _, lab = connected_components(A, directed=True, connection='strong')
    comps = {}
    for i, l in enumerate(lab):
        comps.setdefault(l, []).append(i)
    best = 0.0
    for mem in comps.values():
        sub = A[mem][:, mem].toarray()
        if not sub.any():
            continue
        best = max(best, float(max(abs(np.linalg.eigvals(sub)))))
    return log(best) if best > 1 + 1e-12 else 0.0


def greedy_word(out, pick, start=0):
    """Exact eventually periodic label of the min (pick=min) or max greedy infinite path."""
    seen = {}
    word = []
    v = start
    while v not in seen:
        seen[v] = len(word)
        c, v = pick(out[v])
        word.append(c)
    k = seen[v]
    return canon(word[:k], word[k:])


# ---------------------------------------------------------------- raw automaton (any pair)


def raw_graph(A, B, M, cap=200000):
    """Deterministic automaton for Sigma_{A,B} over {0..M}. A state records, for each earlier tail still
    tied with A (resp. B), the folded index of A (resp. B) it is compared with next. Sigma_{A,B} is the set of
    labels of infinite paths from state 0. No normalization and no Theorem A are used."""
    start = ((), ())
    idx = {start: 0}
    st = [start]
    edges = []
    u = 0
    while u < len(st):
        PA, PB = st[u]
        for c in range(M + 1):
            ok = True
            na = set()
            for i in PA + (0,):
                d = dig(A, i)
                if c < d:
                    ok = False
                    break
                if c == d:
                    na.add(nxt(A, i))
            if not ok:
                continue
            nb = set()
            for i in PB + (0,):
                d = dig(B, i)
                if c > d:
                    ok = False
                    break
                if c == d:
                    nb.add(nxt(B, i))
            if not ok:
                continue
            key = (tuple(sorted(na)), tuple(sorted(nb)))
            v = idx.get(key)
            if v is None:
                v = len(st)
                idx[key] = v
                st.append(key)
                if v > cap:
                    raise RuntimeError('state cap')
            edges.append((u, c, v))
        u += 1
    return len(st), edges


def raw_H(A, B, M):
    n, edges = raw_graph(A, B, M)
    return graph_entropy(n, edges)


def raw_counts(A, B, M, nmax):
    """Exact number of words of length n = 0..nmax of Sigma_{A,B} (paths from the start that stay alive)."""
    n, edges = raw_graph(A, B, M)
    alive, out = trim(n, edges)
    if not alive[0]:
        return [0] * (nmax + 1)
    vec = {0: 1}
    res = [1]
    for _ in range(nmax):
        nv = {}
        for u, k in vec.items():
            for _, v in out[u]:
                nv[v] = nv.get(v, 0) + k
        vec = nv
        res.append(sum(vec.values()))
    return res


def raw_extremes(A, B, M):
    """(min, max) of Sigma_{A,B}, exact, or (None, None) if it is empty."""
    n, edges = raw_graph(A, B, M)
    alive, out = trim(n, edges)
    if not alive[0]:
        return None, None
    return greedy_word(out, min), greedy_word(out, max)


# ---------------------------------------------------------------- Theorem A, exactly

_z = sympy.Symbol('z')


def _gf(s):
    """sum_{n>=1} s_n z^n = P(z) + z^p Q(z) / (1 - z^q), returned as (numerator, denominator)."""
    pre, per = s
    p, q = len(pre), len(per)
    P = sum(sympy.Integer(d) * _z ** (i + 1) for i, d in enumerate(pre))
    Q = sum(sympy.Integer(d) * _z ** (i + 1) for i, d in enumerate(per))
    den = 1 - _z ** q
    return sympy.expand(P * den + _z ** p * Q), den


def series_counts(a, b, nmax):
    """Coefficients N_0..N_nmax of 1/((1 - z)(1 - K(z))), K = sum (b_n - a_n) z^n (exact integers)."""
    c = [0] + [dig(b, i) - dig(a, i) for i in range(nmax)]
    g = [1]
    for n in range(1, nmax + 1):
        g.append(sum(c[k] * g[n - k] for k in range(1, n + 1)))
    out, s = [], 0
    for x in g:
        s += x
        out.append(s)
    return out


def thmA_root(a, b, digits=30):
    """Smallest root in (0, 1) of K(z) = 1, K = sum_{n>=1} (b_n - a_n) z^n, as an mpmath number, or None.
    K - 1 = 0 is cleared of denominators to an integer polynomial. Its square-free part is isolated exactly on
    [0, 1] (so a double root, where K touches 1, is found as well), and the smallest root is refined by
    bisection at 60 significant digits."""
    na, da = _gf(a)
    nb, db = _gf(b)
    N = sympy.Poly(sympy.expand(nb * da - na * db - da * db), _z)
    S = sympy.Poly(sympy.sqf_part(N.as_expr()), _z)
    cands = []
    for (lo, hi), _ in S.intervals(inf=0, sup=1):
        if hi <= 0 or lo >= 1:
            continue
        if lo == hi:
            if 0 < lo < 1:
                cands.append((lo, hi))
            continue
        cands.append((lo, hi))
    if not cands:
        return None
    lo, hi = min(cands)
    coeffs = [int(c) for c in S.all_coeffs()]
    with mp.workdps(60):
        if lo == hi:
            return mpf(lo.p) / lo.q
        f = lambda x: mp.polyval(coeffs, x)
        x0, x1 = mpf(lo.p) / lo.q, mpf(hi.p) / hi.q
        f0 = f(x0)
        for _ in range(200):
            xm = (x0 + x1) / 2
            fm = f(xm)
            if fm == 0:
                return xm
            if (fm > 0) == (f0 > 0):
                x0, f0 = xm, fm
            else:
                x1 = xm
        return (x0 + x1) / 2


def thmA_h(a, b):
    """Theorem A entropy (float); 0 if K = 1 has no root in (0, 1)."""
    r = thmA_root(a, b)
    return 0.0 if r is None else float(-mp.log(r))


# ---------------------------------------------------------------- Y_D: the unfolded automaton of Theorem A


def yd_graph(a, b, D):
    """States (i, j), i, j < D: the current a- and b-match depths (L = sigma^i a, R = sigma^j b). The transitions
    are those of Lemma P: reading c from (L, R), L' = sigma L if c = L_1 and L' = a if c > L_1; likewise for R.
    Requires (a, b) normalized."""
    idx = {(0, 0): 0}
    st = [(0, 0)]
    edges = []
    k = 0
    while k < len(st):
        i, j = st[k]
        l1, r1 = dig(a, i), dig(b, j)
        for c in range(l1, r1 + 1):
            t = (i + 1 if c == l1 else 0, j + 1 if c == r1 else 0)
            if t[0] >= D or t[1] >= D:
                continue
            if t not in idx:
                idx[t] = len(st)
                st.append(t)
            edges.append((k, c, idx[t]))
        k += 1
    return len(st), edges


def yd(a, b, D):
    """h(Y_D), p_D = min Y_D and q_D = max Y_D (exact), or (0.0, None, None) if Y_D is empty."""
    n, edges = yd_graph(a, b, D)
    alive, out = trim(n, edges)
    if not alive[0]:
        return 0.0, None, None
    return graph_entropy(n, edges), greedy_word(out, min), greedy_word(out, max)


# ---------------------------------------------------------------- the folded automaton (for the support lemma)


def folded_graph(a, b):
    """Theorem A's automaton with states (folded index of a, folded index of b)."""
    idx = {(0, 0): 0}
    st = [(0, 0)]
    edges = []
    k = 0
    while k < len(st):
        i, j = st[k]
        l1, r1 = dig(a, i), dig(b, j)
        for c in range(l1, r1 + 1):
            t = (nxt(a, i) if c == l1 else 0, nxt(b, j) if c == r1 else 0)
            if t not in idx:
                idx[t] = len(st)
                st.append(t)
            edges.append((k, c, idx[t]))
        k += 1
    return len(st), edges


def in_positive_scc(a, b, w):
    """Is w the label of an infinite path inside a strongly connected component of radius > 1 of the folded
    automaton of (a, b)? Decided exactly: the pair (state, folded index of w) is eventually periodic."""
    n, edges = folded_graph(a, b)
    rows = [u for u, _, _ in edges]
    cols = [v for _, _, v in edges]
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    _, lab = connected_components(A, directed=True, connection='strong')
    step = {(u, c): v for u, c, v in edges}
    comps = {}
    for i, l in enumerate(lab):
        comps.setdefault(l, []).append(i)
    for mem in comps.values():
        sub = A[mem][:, mem].toarray()
        if not sub.any() or max(abs(np.linalg.eigvals(sub))) <= 1 + 1e-9:
            continue
        C = set(mem)
        for s0 in mem:
            v, i, seen, ok = s0, 0, set(), True
            while (v, i) not in seen:
                seen.add((v, i))
                v = step.get((v, dig(w, i)))
                if v is None or v not in C:
                    ok = False
                    break
                i = nxt(w, i)
            if ok:
                return True
    return False


def agree(x, y):
    """Number of initial digits on which x and y agree (None if equal)."""
    d = firstdiff(x, y)
    return None if d is None else d - 1
