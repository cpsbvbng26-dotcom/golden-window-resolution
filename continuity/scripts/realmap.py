# Corollary E at a point with beta > 2 where the first digits of min and max of K~ differ by 3, so that neither
# the binary theorem nor the earlier partial extension applies. Both expansions jump there.
#
#   beta0 = (3 + sqrt 13)/2 (beta^2 = 3 beta + 1): greedy expansion of 1 is 310^inf, alpha(beta0) = (30)^inf;
#   t0 = 1/beta0^2: b(t0, beta0) = 010^inf (finite, so b jumps).
#
# Symbolic side: K~ = Sigma_{010^inf, (30)^inf}; its min and max from the raw automaton; Theorem A at that pair.
# Real side, independent of every symbolic formula: a dynamic programme over the images of the n-cylinders of
# T_beta (all branches) restricted to [t, 1), at 80 digits; dim ~ (log N_150 - log N_100) / (50 log beta).
# Estimates at (beta0 + dx e, t0 + dy e) for eight directions and e = 10^-2, 10^-4, 10^-6, 10^-8.
from mpmath import floor, log, mp, mpf, sqrt

from lexlib import fixed, canon, raw_extremes, raw_H, show, thmA_h

mp.dps = 80


def counts(beta, t, n):
    M = int(floor(beta)) if beta != floor(beta) else int(beta) - 1
    key = lambda l, r: (mp.nstr(l, 35), mp.nstr(r, 35))
    states = {key(t, mpf(1)): (t, mpf(1), 1)}
    N = [1]
    for _ in range(n):
        new = {}
        for (l, r, m) in states.values():
            for k in range(M + 1):
                lo, hi = max(l, mpf(k) / beta), min(r, mpf(k + 1) / beta)
                if lo >= hi:
                    continue
                l2, r2 = max(beta * lo - k, t), min(beta * hi - k, mpf(1))
                if l2 < r2:
                    kk = key(l2, r2)
                    if kk in new:
                        new[kk] = (new[kk][0], new[kk][1], new[kk][2] + m)
                    else:
                        new[kk] = (l2, r2, m)
        states = new
        if len(states) > 20000:
            raise RuntimeError('too many interval states')
        N.append(sum(v[2] for v in states.values()))
    return N


def dim_est(beta, t, n=150, m=50):
    N = counts(beta, t, n)
    if N[-1] == 0 or N[-1 - m] == 0:
        return mpf(0)
    return (log(N[-1]) - log(N[-1 - m])) / m / log(beta)


b0 = (3 + sqrt(13)) / 2
t0 = 1 / b0 ** 2
lo, hi = raw_extremes(canon((0, 1), (0,)), canon((), (3, 0)), 3)
print('beta0 = %s, t0 = %s' % (mp.nstr(b0, 12), mp.nstr(t0, 12)))
print('K~ = Sigma_{010^inf, (30)^inf}: min = %s, max = %s; h(raw automaton) = %s; h(Theorem A at (min, max)) = %s'
      % (show(lo), show(hi), fixed(raw_H(canon((0, 1), (0,)), canon((), (3, 0)), 3), 9), fixed(thmA_h(lo, hi), 9)))
print('dimension from Theorem A: log 3 / log beta0 = %s' % mp.nstr(log(3) / log(b0), 10))
print('real-map estimate at the point: %s' % mp.nstr(dim_est(b0, t0), 10))
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
print('  e      ' + '  '.join('%7s' % ('%+d,%+d' % d) for d in dirs))
for k in (2, 4, 6, 8):
    e = mpf(10) ** (-k)
    print('  1e-%d   ' % k + '  '.join('%7.5f' % float(dim_est(b0 + dx * e, t0 + dy * e)) for dx, dy in dirs))
