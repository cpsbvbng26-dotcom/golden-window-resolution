# Theorem IA numerically: h - h(Y_D) -> 0 (D = 10, 20, 30, 40, 60) for normalized pairs with h > 0.
#
# Y_D = {x in Sigma_{a,b} : neither a|D nor b|D is a factor of x}. h(Y_D) is computed on the unfolded automaton
# of Theorem A (match depths < D, Lemma P) and, independently, as the entropy of the raw automaton of the pair
# (a|D M^inf, b|D 0^inf), whose Sigma differs from Y_D by a countable set. h itself comes from the raw automaton
# of (a, b). Pairs (seed 4407): random eventually periodic pairs, and delicate ones in which the orbit of b
# passes close to a (or of a close to b), or b ends in a (or a in b). Gaps below 1e-11 are printed as "<1e-11".
import random

from lexlib import fmt, fixed, canon, dig, lexcmp, normalized, prefix, raw_H, show, yd

random.seed(4407)
DS = (10, 20, 30, 40, 60)
PER_M = 50


def rnd(M, lo=1, hi=5):
    return canon(tuple(random.randint(0, M) for _ in range(random.randint(0, 3))),
                 tuple(random.randint(0, M) for _ in range(random.randint(lo, hi))))


def delicate(M):
    a, b = rnd(M, 1, 4), rnd(M, 1, 4)
    k = random.randint(6, 14)
    kind = random.choice(['b-orbit near a', 'a-orbit near b', 'b ends in a', 'a ends in b'])
    if kind == 'b-orbit near a':
        b = canon((), (dig(b, 0),) + tuple(random.randint(0, M) for _ in range(random.randint(0, 2))) + prefix(a, k))
    elif kind == 'a-orbit near b':
        a = canon((), (dig(a, 0),) + tuple(random.randint(0, M) for _ in range(random.randint(0, 2))) + prefix(b, k))
    elif kind == 'b ends in a':
        b = canon((dig(b, 0),) + a[0], a[1])
    else:
        a = canon((dig(a, 0),) + b[0], b[1])
    return kind, a, b


rows = []
seen = set()
stats = {}
cross = 0.0
nonmono = 0
for M in (1, 2, 3, 4):
    n = 0
    while n < PER_M:
        if n % 2 == 0:
            kind, (a, b) = 'random', (rnd(M), rnd(M))
        else:
            kind, a, b = delicate(M)
        if (a, b) in seen or lexcmp(a, b) >= 0 or not normalized(a, b):
            continue
        h = raw_H(a, b, M)
        if h < 1e-6:
            continue
        n += 1
        seen.add((a, b))
        hs = []
        for D in DS:
            hD = yd(a, b, D)[0]
            hR = raw_H(canon(prefix(a, D), (M,)), canon(prefix(b, D), (0,)), M)
            cross = max(cross, abs(hD - hR))
            hs.append(hD)
        nonmono += any(hs[i + 1] < hs[i] - 1e-12 for i in range(len(hs) - 1))
        gaps = [max(h - x, 0.0) for x in hs]
        spread = 'spread >= 2' if dig(b, 0) - dig(a, 0) >= 2 else 'spread <= 1'
        s = stats.setdefault((M, spread), [0, 0.0, 0.0])
        s[0] += 1
        s[1] = max(s[1], gaps[3])
        s[2] = max(s[2], gaps[4])
        rows.append((gaps[3], gaps[0], M, kind, a, b, h, gaps))

print('pairs: %d (M = 1..4, %d each; half random, half delicate), all normalized with h > 0' % (len(rows), PER_M))
print('h(Y_D) from the unfolded automaton and from the raw automaton of (a|D M^inf, b|D 0^inf) agree to 1e-12: %s'
      % (cross < 1e-12))
print('pairs where h(Y_D) decreases in D: %d' % nonmono)
print('largest gap h - h(Y_40) and h - h(Y_60):')
for key in sorted(stats):
    print('   M=%d, %s: %3d pairs, max %s and %s' % (key[0], key[1], stats[key][0], fmt(stats[key][1]),
                                                   fmt(stats[key][2])))
print('largest gap over all pairs at D = %s: %s' % (', '.join(map(str, DS)),
                                                  ', '.join(fmt(max(r[7][i] for r in rows)) for i in range(len(DS)))))
# Order by the printed gaps, then by the pair itself: two pairs mirrored into each other have the same gaps up to
# the last bit, and their order must not depend on that bit (2026-11-19, a CI run swapped them).
rows.sort(key=lambda r: (-float(fmt(r[0]).replace('<', '')), -float(fmt(r[1]).replace('<', '')), r[2], r[3], show(r[4]), show(r[5])))
print('slowest four (gaps at D = %s):' % ', '.join(map(str, DS)))
for g40, g10, M, kind, a, b, h, gaps in rows[:4]:
    print('   M=%d %s: a = %s, b = %s, h = %s: %s' % (M, kind, show(a), show(b), fixed(h, 6), ', '.join(fmt(x) for x in gaps)))

print('\nnamed pairs (gaps at D = 10, 20, 30, 40, 60):')
for name, M, a, b in [
        ('orbit of b passes near a', 2, canon((), (0, 1)), canon((), (2,) + (0, 1) * 7)),
        ('slow pair', 2, canon((), (0, 2)), canon((), (2, 1, 0))),
        ('spread 3 (Section 6)', 3, canon((), (0, 1)), canon((), (3, 0))),
        ('double root', 3, canon((0,), (2,)), canon((3,), (1,)))]:
    h = raw_H(a, b, M)
    print('   %-25s a = %s, b = %s, h = %s: %s' % (name, show(a), show(b), fixed(h, 9),
                                                     ', '.join(fmt(max(h - yd(a, b, D)[0], 0.0)) for D in (10, 20, 30, 40, 60))))
