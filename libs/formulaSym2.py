from z3 import *
import libs.config as cfg

### Symbolic Static Checker

# simplification of formulaSym.py, 
# * eliminate quantifier on array and
# * eliminate uninterpreted function
# * rename free variables


class Formula:

    def __init__(self, zeta, omega_n):
        self.predicate__init__()
        self.exp = cfg.E
        self.pi = cfg.PI
        self.sigma = cfg.SIGMA
        self.zeta = zeta
        self.omega_n = omega_n
        self.y = Array('y', RealSort(), RealSort()) 
        self.t = Real('t')
  
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

    def Edc(self, num_last=1, den_last=1):
        return self.dc == (num_last / den_last) 

    def EMp_2(self):
        zeta = self.zeta
        cond = zeta >= 1
        oversht = self.overshoot == 0
        return Implies(cond, oversht)


    def EMp_1(self):
        zeta = self.zeta
        pre = And(zeta < 1.0, zeta>=0.0) 
        temp = Real('temp')
        
        temp_prop = (temp * temp == (1-zeta*zeta))
        power = (- self.pi * zeta) / temp
        Mp = self.exp ** power

        post = And(temp_prop, self.overshoot == Mp)
        return Implies(pre, post)

    def Etp(self):
        zeta = self.zeta
        omega_n = self.omega_n
        pre = And(zeta < 1, zeta>=0) 
        
        temp = Real('temp')
        temp_prop = (temp * temp == (1-zeta*zeta))
        omega_d = omega_n * temp

        post = And(temp_prop, self.peak == self.pi / omega_d, self.peak >= 0)

        return Implies(pre, post)

    def Ets(self):
        f = And(self.settle >= 0,self.settle == 4.60 / (self.zeta * self.omega_n))
        return f

    def Etr(self):
        f = And(self.settle >= 0, self.rise == (2.16 * self.zeta + 0.60) / self.omega_n)
        return f

    # Lemmas
    def EMp_3(self):
        zeta = self.zeta
        pre = And(zeta < 1.0, zeta>=0.0) 
        return Implies(pre, And(self.overshoot > 0, self.overshoot <= 1))

    def Lmin(self):
        cond = And(self.zeta >=0, self.zeta<1)
        return Implies(cond, self.y[self.t] >= 0)

    def mono_inc(self, f, t1, t2):
        return Implies(t1>=t2, f[t1] >= f[t2])

    def Lmono(self):
        zeta = self.zeta
        cond = zeta == 1
        t3 = Real('t3')
        mono_inc = self.mono_inc(self.y, self.t, t3)
        return Implies(cond, mono_inc)

