import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bf import brute, in_set
# alpha = (2001)^inf  (beta^4 = 2 beta^3 + 2), t with greedy expansion 1 2 0^inf (Lyndon word 12)
al = ((), (2, 0, 0, 1)); a = ((1, 2), (0,))
lo, hi = 2.0, 3.0
f = lambda x: x**4 - 2*x**3 - 2
for _ in range(200):
    m = (lo + hi) / 2
    lo, hi = (lo, m) if f(m) > 0 else (m, hi)
b = lo; t = 1/b + 2/b**2
print('beta', b, 't', t, 'T t', (b*t) % 1, 'T^2 t', (b*((b*t) % 1)) % 1)
print('alpha self-admissible', all(in_set(al, ((), (0,)), al) for _ in [0]))
print('greedy a in K~:', in_set(a, a, al))
print('brute N_n of K~(t):', brute(a, al, 2, 8, 16))
