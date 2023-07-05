from tbcontrol.symbolic import routh
import sympy

# simple test
s = sympy.Symbol('s')
K_c = sympy.Symbol('K_c')
den = 10*s**3 + 17*s**2 + 8*s + 1 + K_c
A = routh(sympy.Poly(den, s))
r = sympy.solve([e > 0 for e in A[:, 0]], K_c)

print(r)

# multivars inequal
K = sympy.Symbol('K')
Ki = sympy.Symbol('Ki')
den = s**3 + 3*s**2 + (2+K)*s + Ki
A = routh(sympy.Poly(den, s))
r = sympy.solve([e > 0 for e in A[:, 0]], [K]) 

print(r)

# special case, *not covered*
den = s**5 + 5*s**4 + 11*s**3 + 23*s**2 + 28*s + 12
A = routh(sympy.Poly(den, s))
print(A)

# special case 2, *not covered*
den = s**5 + 3*s**4 + 2*s**3 + 6*s**2 + 6*s + 9
A = routh(sympy.Poly(den, s))
print(A)

