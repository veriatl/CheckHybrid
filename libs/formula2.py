from z3 import *
import libs.metrics as metrics
import libs.config as cfg


### Numerical Static Checker

# Simplify Formula.py
# * eliminate quantifier on array and
# * eliminate uninterpreted function
# * rename free variables

class Formula:

    def __init__(self,zeta,omega_n):      
        self.m = metrics.Metrics(zeta,omega_n)
        self.predicate__init__()
        self.exp = cfg.E
        self.pi = cfg.PI
        self.sigma = cfg.SIGMA
        self.t = Real('ft')      
        self.y = Array('y', RealSort(), RealSort()) 
        self.zeta = zeta
        self.omega_n = omega_n

    def predicate__init__(self):    
        self.input = Real('input')
        self.dc = Real('dc')
        self.steady = Real('steady')
        self.overshoot = Real('overshoot')
        self.peak = Real('peak')
        self.rise = Real('rise')
        self.settle = Real('settle')


    def Pdc(self):
        return self.steady == self.input * self.dc 

    def PMp(self):
        return self.y[self.peak] == self.steady * self.overshoot + self.steady

    def Ptp_1(self):
        return self.max(self.y, self.t, self.peak)

    def max(self, y, t, tp):
        return y[t] <= y[tp]

    def Ptp_2(self):
        return self.first(self.y, self.t, self.peak)

    def first(self, y, t, tx):
        return Implies(y[t] == y[tx], t>=tx)

    def Ptr(self):
        y = self.y
        t = self.t
        t2 = Real('t2')
        return And(y[t2] == 0.1*self.input, y[t2+self.rise]==0.9*self.input,
                    self.first(y, t, t2), self.first(y, t, t2+self.rise))

    def Pts(self):
        y = self.y
        ts = self.settle 
        sigma = self.sigma
        v = self.steady
        t = self.t

        abs = And(y[t] - v >= -sigma*v, y[t] - v <= sigma*v)
        return Implies(t >= ts, abs)

    def Pin(self, r):
        return self.input == r

    def Edc(self, a, b):
        return self.dc == self.m.dc(a,b)

    def EMp(self):
        return self.overshoot == self.m.overshoot()

    def Etp(self):
        if self.m.peak() != None:
            return self.peak == self.m.peak()
        else:
            return 1 == 1

    def Etr(self):
        return self.rise == self.m.rise()

    def Ets(self):
        return self.settle == self.m.settle(self.sigma)

    # Lemmas

    def Lmono(self):
        t3 = Real('t3')
        return Implies(self.zeta == 1, self.mono_inc(self.y, self.t, t3))
    
    def mono_inc(self, f, t1, t2):
        return Implies(t1>=t2, f[t1] >= f[t2])

    def Lmin(self):
        cond = And(self.zeta >=0, self.zeta<1)
        return Implies(cond, self.y[self.t] >= 0)


