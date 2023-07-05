from z3 import *

class z3model:
    def __init__(self,m):
        self.m = m

    def getReal(self, x):
        v = self.m[x]
        if is_int_value(v):
            return float(v)
        if is_rational_value(v):
            n = v.numerator_as_long()
            d = v.denominator_as_long()
            return float(n) / float(d)
        if is_algebraic_value(v):
            r = v.approx(2)
            n = r.numerator_as_long()
            d = r.denominator_as_long()
            return float(n) / float(d)
        
        return self.m[x].__repr__

    def keys(self):
        for d in self.m:
            print(f"key: {d}")