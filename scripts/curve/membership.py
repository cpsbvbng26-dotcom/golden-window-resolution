# Reduction check (Section 2.2): the game recursion x -> T(x) on [0, X] with the hole (dX, 1)
# against the greedy beta-map criterion T_beta^n(y) <= t(beta), y = d*x, t = dX.
# Exact rationals. Fixed seed. Prints the number of points and of mismatches for each delta.
import random
from fractions import Fraction as F

random.seed(20261118)
DEPTH = 25
POINTS = 50000
DELTAS = [F(62, 100), F(63, 100), F(64, 100), F(65, 100), F(66, 100), F(6666, 10000)]


def game_survives(x, d, X, depth):
    b = 1 / d
    for _ in range(depth):
        if x <= d * X:
            x = b * x
        elif x >= 1:
            x = b * (x - 1)
        else:
            return False
    return True


def greedy_survives(y, d, t, depth):
    b = 1 / d
    for _ in range(depth):
        if y > t:
            return False
        z = b * y
        y = z - (z.numerator // z.denominator)
    return True


for d in DELTAS:
    X = (2 * d - 1) / (d * (1 - d))
    t = d * X
    mism = 0
    surv = 0
    for _ in range(POINTS):
        x = X * F(random.randrange(10**9), 10**9)
        g = game_survives(x, d, X, DEPTH)
        h = greedy_survives(d * x, d, t, DEPTH + 1)
        surv += g
        mism += (g != h)
    print(f"delta {float(d)}: points {POINTS}, depth {DEPTH}, survivors {surv}, mismatches {mism}")
