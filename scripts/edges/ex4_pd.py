"""Example 4: two-player PD, CC=(1,1), DD=(0,0), DC=(1+g,-l), CD=(-l,1+g) (the usual
normalisation, recalled), edge [CC, DC]. With public randomization the equilibrium set on the
edge is p([0, v*]), v* = 1 - delta + delta*kappa_B (short argument in note.md section 9).  Question (Mailath,
Obara and Sekiguchi 2002, abstract only): is the maximum p(v*) a pure-strategy SPE payoff?
v* in S  <=>  F_B(v*) = kappa_B in S.  In the gap case the branch is unique, so membership is
decided by one orbit: exit -> no (certain); orbit reaches 0 or repeats -> yes (certain)."""
from fractions import Fraction as Fr
import math
from gen import Edge, pd

def decide(E, x, N=400):
    kind, data = E.classify()
    if kind == 'interval':
        return 'yes'
    EA, EB = data
    seen = set()
    for t in range(N):
        if x in seen or x == 0:
            return 'yes'
        seen.add(x)
        if EA and EA[0] <= x <= EA[1]:
            x = E.F(0, x)
        elif EB and EB[0] <= x <= EB[1]:
            x = E.F(1, x)
        else:
            return 'no'
    return 'undecided'

def decide_float(d, kA, kB, x, N=60):
    qA, rB, vB = d * kA, 1 - d, 1 - d + d * kB
    for t in range(N):
        if 0 <= x <= qA: x = x / d
        elif rB <= x <= vB: x = (x - 1 + d) / d
        else: return t
    return N

if __name__ == '__main__':
    for (g, l) in [(Fr(1), Fr(1)), (Fr(1, 2), Fr(1)), (Fr(3, 2), Fr(1)), (Fr(1), Fr(1, 2))]:
        G = pd(g, l)
        A, B = ('C', 'C'), ('D', 'C')
        # thresholds on an exact grid
        lo = max(g / (1 + g), l / (1 + l))
        N = 4000
        first_interval = None
        tally = {'yes': 0, 'no': 0, 'undecided': 0}
        gapgrid = []
        for i in range(1, N):
            d = lo + (1 - lo) * Fr(i, N)
            E = Edge(G, A, B, d)
            kind, data = E.classify()
            if kind == 'interval':
                if first_interval is None: first_interval = d
                continue
            if kind != 'gap':
                continue
            kB = E.I[1][1]
            res = decide(E, kB)
            tally[res] += 1
            gapgrid.append((d, res))
        yes = [float(d) for d, r in gapgrid if r == 'yes']
        print(f'g={g} l={l}: IC nonempty from delta={float(lo):.4f}; first interval-case grid delta '
              f'{float(first_interval):.4f}; gap-case grid points {len(gapgrid)}: {tally}')
        print(f'   gap-case grid points where the maximum IS a pure SPE payoff: {yes[:12]}{" ..." if len(yes) > 12 else ""}')
        # float scan of the set Y_n = {delta : orbit of kappa_B survives n steps}
        M = 200000
        d0, d1 = float(lo), float(first_interval)
        surv = {n: 0 for n in (5, 10, 20, 40)}
        comps = {n: 0 for n in surv}
        prev = {n: False for n in surv}
        for j in range(1, M):
            d = d0 + (d1 - d0) * j / M
            rho = (1 - d) / d
            kA = min(1.0, (1 - float(g) * rho) / (1 + float(l)))
            kB = min(1.0, (1 - float(l) * rho) / (1 + float(l)))
            t = decide_float(d, kA, kB, kB, 41)
            for n in surv:
                ok = t >= n
                surv[n] += ok
                if ok and not prev[n]: comps[n] += 1
                prev[n] = ok
        print('   share of the gap range where the orbit of kappa_B survives n steps:',
              {n: round(surv[n] / M, 4) for n in surv}, ' runs of survivors:', comps)
