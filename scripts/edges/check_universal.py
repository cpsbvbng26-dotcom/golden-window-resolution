"""Theorem H (the universal window for I_A = I_B = [0, kappa]):
  kappa < 1-delta: S = {0, 1-delta};  kappa = 1-delta: countable;
  1-delta < kappa < (1-delta)/delta: 0 < dim < 1;  kappa >= (1-delta)/delta: S = [0, 1-delta+delta*kappa].
Checked on random rational (delta, kappa): classification and backward S_N; dimension by
renewal and by LSZ (independent formulas); monotonicity in kappa on a grid."""
import random
from fractions import Fraction as Fr
from gen import Edge, GapSystem, renewal_set, renewal_dim, lsz_from_system
from check_dichotomy import backward

class Synth(Edge):
    def __init__(self, d, kap):
        self.d = Fr(d); self.I = {0: (Fr(0), Fr(kap)), 1: (Fr(0), Fr(kap))}

random.seed(5)
tally = {}
maxdiff = 0
for _ in range(300):
    d = Fr(random.randint(20, 95), 100); kap = Fr(random.randint(0, 100), 100)
    E = Synth(d, kap)
    kind, data = E.classify()
    if kap < 1 - d: pred = 'two points'
    elif kap == 1 - d: pred = 'countable'
    elif kap < (1 - d) / d: pred = 'fractal'
    else: pred = 'interval'
    N = 30
    S, hist = backward(E, N)
    if S is None:
        N = 12
        S, hist = backward(E, N)
    if pred == 'interval':
        ok = kind == 'interval' and S == [(Fr(0), 1 - d + d * kap)]
    elif pred == 'two points':
        ok = kind == 'gap' and len(S) == 2 and max(b - a for a, b in S) <= d ** N and S[0][0] == 0 and S[1][0] <= 1 - d <= S[1][1]
    else:
        ok = kind == 'gap' and max(b - a for a, b in S) <= d ** N
        if pred == 'fractal' and ok:
            s1 = renewal_dim(renewal_set(E, 400), E.d)
            s2, a, b = lsz_from_system(GapSystem(E), K=120, look=35)
            ok = 0 < s1 < 1
            maxdiff = max(maxdiff, abs(float(s1) - float(s2)))
    tally[(pred, ok)] = tally.get((pred, ok), 0) + 1
print(tally, 'max |renewal - LSZ| over fractal cases:', maxdiff)

# monotone in kappa at fixed delta
for d in [Fr(55, 100), Fr(62, 100), Fr(7, 10), Fr(8, 10)]:
    lo, hi = 1 - d, min(Fr(1), (1 - d) / d)
    vals = []
    for i in range(1, 200):
        kap = lo + (hi - lo) * Fr(i, 200)
        vals.append(float(renewal_dim(renewal_set(Synth(d, kap), 400), d)))
    dec = sum(1 for i in range(len(vals) - 1) if vals[i + 1] < vals[i] - 1e-12)
    flat = sum(1 for i in range(len(vals) - 1) if abs(vals[i + 1] - vals[i]) <= 1e-12)
    print(f'delta {d}: dim over kappa in W: {vals[0]:.4f} .. {vals[-1]:.4f}, decreases {dec}, equal neighbours {flat}')
