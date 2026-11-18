from mpmath import mp, mpf, sqrt
from check_count import compare
mp.dps = 120
phi = (1+sqrt(5))/2
for d in [1/phi + mpf('1e-6'), 1/phi + mpf('1e-10'), mpf(2)/3 - mpf('1e-5')]:
    a, b = compare(d, n=400, m=150)
    print(mp.nstr(d, 14), "count:", mp.nstr(a, 10), " formula:", mp.nstr(b, 10))
