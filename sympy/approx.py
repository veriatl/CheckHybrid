from sympy import diff, sin, exp 
import sympy 

d1 = sympy.var('d1')
d2 = sympy.var('d2')
s = sympy.var('s')
Ms = 1 + d1*s + d2*s*s
Ms_1 = diff(Ms, s)
Ms_2 = diff(Ms_1, s)
Ms_3 = diff(Ms_2, s)
print (Ms_3)