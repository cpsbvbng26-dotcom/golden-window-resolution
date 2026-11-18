# C computed a second way: M1 = sum_n n d_n (2/3)^n = sum_{j>=0} (2/3)^j T^j(1), T(y) = (3/2) y mod 1 (greedy), exact rationals.
from fractions import Fraction as F
from mpmath import mp, mpf, log
mp.dps = 40
y = F(1); tot = F(0); w = F(1)
for j in range(300):
    tot += w*y
    w *= F(2, 3)
    y = F(3, 2)*y
    y = y - (1 if y >= 1 else 0)
M1 = mpf(tot.numerator)/tot.denominator
print("M1 via Parry sum =", mp.nstr(M1, 30))
print("C =", mp.nstr(9/(log(mpf(3)/2)*M1), 30))
