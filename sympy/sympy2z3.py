from z3 import *
from sympy.core import Mul, Add, Pow, Symbol, Number
from sympy import And, Or, Not
from sympy.core.relational import Lt, Le

def sympy_to_z3(sympy_var_list, sympy_exp):
    'convert a sympy expression to a z3 expression. This returns (z3_vars, z3_expression)'

    z3_vars = []
    z3_var_map = {}

    for var in sympy_var_list:
        name = var.name
        z3_var = Real(name)
        z3_var_map[name] = z3_var
        z3_vars.append(z3_var)

    result_exp = _sympy_to_z3_rec(z3_var_map, sympy_exp)

    return z3_vars, result_exp

def _sympy_to_z3_rec(var_map, e):
    'recursive call for sympy_to_z3()'
    rv = None



    if isinstance(e, Symbol):
        rv = var_map.get(e.name)

        if rv == None:
            raise RuntimeError("No var was corresponds to symbol '" + str(e) + "'")

    elif isinstance(e, Number):
        rv = float(e)
    elif isinstance(e, Mul):
        rv = _sympy_to_z3_rec(var_map, e.args[0])

        for child in e.args[1:]:
            rv *= _sympy_to_z3_rec(var_map, child)
    elif isinstance(e, Add):
        rv = _sympy_to_z3_rec(var_map, e.args[0])

        for child in e.args[1:]:
            rv += _sympy_to_z3_rec(var_map, child)
    elif isinstance(e, Pow):
        term = _sympy_to_z3_rec(var_map, e.args[0])
        exponent = _sympy_to_z3_rec(var_map, e.args[1])

        if exponent == 0.5:
            # sqrt
            rv = Sqrt(term)
        else:
            rv = term**exponent
    elif isinstance(e, sympy.And):
        rv = _sympy_to_z3_rec(var_map, e.args[0])

        for child in e.args[1:]:
            rv = z3.And(rv, _sympy_to_z3_rec(var_map, child))
    elif isinstance(e, sympy.Or):
        rv = _sympy_to_z3_rec(var_map, e.args[0])

        for child in e.args[1:]:
            rv = z3.Or(rv, _sympy_to_z3_rec(var_map, child))

    elif isinstance(e, sympy.Not):
        rv = _sympy_to_z3_rec(var_map, e.args[0])

        rv = z3.Not(rv)

    elif isinstance(e, Lt):
        rv1 = _sympy_to_z3_rec(var_map, e.args[0])
        rv2 = _sympy_to_z3_rec(var_map, e.args[1])
        rv = rv1 < rv2
    elif isinstance(e, Le):
        rv1 = _sympy_to_z3_rec(var_map, e.args[0])
        rv2 = _sympy_to_z3_rec(var_map, e.args[1])
        rv = rv1 <= rv2

    if rv == None:
        raise RuntimeError("Type '" + str(type(e)) + "' is not yet implemented for convertion to a z3 expresion. " + \
                            "Subexpression was '" + str(e) + "'.")

    return rv

from tbcontrol.symbolic import routh
import sympy
from z3 import Solver, sat

s = sympy.Symbol('s')
K_c = sympy.Symbol('K_c')
den = 10*s**3 + 17*s**2 + 8*s + 1 + K_c
A = routh(sympy.Poly(den, s))
r = sympy.solve([e > 0 for e in A[:, 0]], K_c)

var_list = [K_c]
sympy_exp = r
z3_vars, z3_exp = sympy_to_z3(var_list, sympy_exp)

print(z3_vars, z3_exp)

s = Solver()
s.add(z3_exp) 
result = s.check()
print(s.model())

