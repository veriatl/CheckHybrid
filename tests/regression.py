import path
import libs.checker as checker
from z3 import *
import unittest
import numpy

class RegressionTest(unittest.TestCase):

    def test_ex_ap0506(self):
        # Constants

        Km = Real('Km')
        Kb = Real('Kb')
        K = Real('K')
        omega = Real('omega')
        zeta = Real('zeta')

        # Setup
        f1 = omega * omega == K * Km
        f2 = Km*Kb+0.01 == 2 * zeta * omega
        safety = (Km*Kb+0.01) / (K * Km) == 1

        f3 = And(f1,f2,safety) # we want solve satisfication problem instead of validity problem here

        c = checker.Checker(zeta,omega)
        c.add(f3)
        res = c.check()
        self.assertTrue(res == 'sat')

    def test_ex_ap0509(self):
        # Constants
        Kp = Real('Kp')
        Ki = Real('Ki')
        omega = Real('omega')
        a, b = Reals('a b')
        zeta = 0.707

        # Setup
        f1 = omega * omega * a * b == Ki
        f2 = (a+b)*omega*omega+1.414*omega*a*b == Kp
        f3 = 1.414*omega*(a+b)+a*b == 375
        f4 = 1.414*omega + a + b == 40
        f5 = And(a > 10 * 0.707*omega, b > 10*0.707*omega)
        f6 = omega > 0
        f7 = (-numpy.log(0.02) / (0.707 * omega)) < 5

        f8 = And(f1,f2,f3,f4,f5,f6,f7) # we want solve satisfication problem instead of validity problem here
        # Setup
        c = checker.Checker(zeta,omega)
        c.add(f8)

        res = c.check()
        self.assertTrue(res == 'sat')

        zeta = zeta
        omega_n = c.model(omega)
        c2 = checker.Checker(zeta,omega_n)

        f = c2.factory
        f.sigma = 0.02
        safety = f.settle < 5
        c2.auto_pog(safety)
        res = c2.check()
        self.assertTrue(res == 'unsat')


    def test_ex_car(self):
       # Constants
        Kp = 2
        Kd = 0.14
        r = 1

        # Approximated Design
        n = [Kp]
        d = [1, Kd, Kp]

        # Chars calculation
        wn_square = d[-1]
        two_zeta_wn = d[-2]

        omega_n = math.sqrt(wn_square)
        zeta = two_zeta_wn/(2*omega_n)

        # Setup
        c = checker.Checker(zeta,omega_n)

        p = c.factory.y
        t = c.factory.t
        c.amp = 1       
        r = c.amp
        safety = p[t] <= r

        c.auto_pog(safety)
        res = c.check()
        self.assertTrue(res == 'sat')

    def test_ex_car2(self):
        # Constants
        Kp = 2
        Kd = 0.14
        r = 1

        # Approximated Design
        n = [Kp]
        d = [1, Kd, Kp]

        # Chars calculation
        wn_square = d[-1]
        two_zeta_wn = d[-2]

        omega_n = math.sqrt(wn_square)
        zeta = two_zeta_wn/(2*omega_n)

        # Setup
        c = checker.Checker(zeta,omega_n)

        p = c.factory.y
        t = c.factory.t
        c.amp = 1       
        r = c.amp
        safety = p[t] <= 2*r

        c.auto_pog(safety)
        res = c.check()
        self.assertTrue(res == 'unsat')

    def test_ex_car3(self):
        # Constants
        Kp = Real('Kp')
        Kd = Real('Kd')
        r = Real('r')
        zeta =  Real('zeta')
        omega_n = Real('omega_n')

        # Approximated Design
        f1 = Kp == omega_n * omega_n
        f2 = Kd == (2*omega_n*zeta)
        f3 = zeta >= 0
        f4 = Kp <= 2
        f5 = omega_n > 0
        f6 = Kd > 0
        f7 = 5 * Kd < Kp
        context = And(f1,f2,f3,f4,f5,f6, f7)

        # Setup
        c = checker.Checker(zeta,omega_n, 1)

        p = c.factory.y
        t = c.factory.t
        r = c.amp
        safety = p[t] <= r

        c.auto_pog(safety, context)

        res = c.check()
        self.assertTrue(res == 'sat')

    def test_ex_dp0503(self):
        # Define Constants Symbolically
        K = Real('K')
        zeta =  Real('zeta')
        omega_n = Real('omega_n')
        r = Real('r')
        q = 17
        wn_square = omega_n * omega_n

        f0 = omega_n * omega_n == K
        f1 = q == 2 * zeta * omega_n
        context = And(f0,f1)

        # Setup
        c = checker.Checker(zeta,omega_n)

        # Safety
        f = c.factory
        safety = f.settle < 0.5

        # PO generation
        c.auto_pog(safety, context)

        res = c.check()
        self.assertTrue(res == 'sat')

    def test_ex_dp0504(self):
        K = 500
        r = 1
        # Approximated transfer function
        Hs_hat_num = [K/7]
        Hs_hat_den = [1, 10, 21+K/7]

        # Chars calculation
        wn_square = Hs_hat_den[-1]
        two_zeta_wn = Hs_hat_den[-2]

        omega_n = math.sqrt(wn_square)
        zeta = two_zeta_wn/(2*omega_n)

        # Setup
        c = checker.Checker(zeta,omega_n,1)

        # Safety
        f = c.factory
        factor = K / (K + 147) 
        steady = f.steady * factor
        safety = And(steady-r <= 0.12, steady-r>=-0.12)

        # PO Generation
        c.auto_pog(safety)

        res = c.check()
        self.assertTrue(res == 'sat')

    def test_ex_dp0506(self):
        # Constants
        K1 = 121
        K2 = 0.14
        r = 1

        # Original Transfer function
        Hs_num = [K1]
        Hs_den = [1, K1*K2+1, K1]

        # Chars calculation
        wn_square = Hs_den[-1]
        two_zeta_wn = Hs_den[-2]

        omega_n = math.sqrt(wn_square)
        zeta = two_zeta_wn/(2*omega_n)

        # Setup
        c = checker.Checker(zeta,omega_n)

        # Safety
        f = c.factory
        t = c.factory.t
        safety = And(f.overshoot <= 0.02, f.peak <= 0.5)

        # PO Generation
        c.auto_pog(safety)

        res = c.check()
        self.assertTrue(res == 'unsat')

    def test_ex_nmp(self):
        # Approximated transfer function
        Hs_hat_num = [1]
        Hs_hat_den = [1, 1.9, 1]

        wn_square = Hs_hat_den[-1]
        two_zeta_wn = Hs_hat_den[-2]

        omega_n = math.sqrt(wn_square)
        zeta = two_zeta_wn/(2*omega_n)

        c = checker.Checker(zeta,omega_n)

        y = c.factory.y
        t = c.factory.t
        c.amp = 1
        r = c.amp
        safety = y[t] >= 0

        c.auto_pog(safety, c.factory.Lmin())

        res = c.check()
        self.assertTrue(res == 'unsat')

    def test_ex_plane(self):
        # Define Constants Symbolically
        Kp = Real('Kp')
        zeta =  Real('zeta')
        omega_n = Real('omega_n')
        r = Real('r')
        wn_square = omega_n * omega_n

        f0 = And(Kp > 0, Kp < 0.65, r==1.0)
        f1 = zeta * zeta == 0.043 / Kp - 0.065
        f2 = omega_n * omega_n == 11.29 * Kp
        f3 = zeta >= 0
        f4 = omega_n >= 0
        f5 = And(f0,f1,f2,f3,f4)

        # Setup
        c = checker.Checker(zeta,omega_n)

        f = c.factory
        safety = f.overshoot == 0

        c.add(f5)
        c.auto_pog(safety)
        res = c.check()
        self.assertTrue(res == 'sat')


if __name__ == '__main__':
    unittest.main()


