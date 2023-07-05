import path
import libs.checker as checker
from z3 import *
import unittest
import numpy

class Table():

    def test_ex_ap0506():
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
        expect = "sat"
        
        org = "$\\frac{K K_m}{s^2 + (K_m K_b+0.01) s + K K_m}$"
        approx = "-"
        req = "TD"
        method = "S"

        return org, approx, req, method, res, expect

    def test_ex_ap0509():
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
        expect = "sat"

        org = "$\\frac{K_p s + K_i}{s^4+40s^3+375s^2+K_p s + K_i}$"
        approx = "$\\frac{\omega_n^2}{(s^2+\sqrt{2}\omega_n s + \omega_n^2)}$"
        req = "TD"
        method = "S"

        return org, approx, req, method, res, expect


    def test_ex_car():
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
        expect = "sat"

        org = "$\\frac{K_d s + K_p}{s^2+K_d s + K_p}$"
        approx = "$\\frac{K_p}{s^2+K_d s + K_p}$"
        req = "SF"
        method = "N"

        return org, approx, req, method, res, expect


    def test_ex_car2():
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
        expect = "unsat"

        org = "$\\frac{K_d s + K_p}{s^2+K_d s + K_p}$"
        approx = "$\\frac{K_p}{s^2+K_d s + K_p}$"
        req = "SF"
        method = "N"

        return org, approx, req, method, res, expect

    def test_ex_car3():
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
        expect = "sat"

        org = "$\\frac{K_d s + K_p}{s^2+K_d s + K_p}$"
        approx = "$\\frac{K_p}{s^2+K_d s + K_p}$"
        req = "SF"
        method = "S"

        return org, approx, req, method, res, expect


    def test_ex_dp0503():
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
        expect = "sat"
        
        org = "$\\frac{K}{s^2 + q s + K}$"
        approx = "-"
        req = "TD"
        method = "S"

        return org, approx, req, method, res, expect

    def test_ex_dp0504():
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
        expect = "sat"

        org = "$\\frac{10K}{(s+3)(s+7)(s+70)+10K}$"
        approx = "$\\frac{K/7}{21+K/7}\\frac{21+K/7}{(s+3)(s+7)+K/7}$"
        req = "TD"
        method = "N"

        return org, approx, req, method, res, expect

    def test_ex_dp0506():
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
        expect = "unsat"

        org = "$\\frac{K_1}{s^2+(K_1 K_2+1)s+K_1}$"
        approx = "-"
        req = "TD"
        method = "N"

        return org, approx, req, method, res, expect

    def test_ex_nmp():
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
        expect = "sat"

        org = "$\\frac{-0.5s + 1}{s^2+3s+1}$"
        approx = "$\\frac{1}{s^2+3s+1}$"
        req = "SF"
        method = "N"

        return org, approx, req, method, res, expect

    def test_ex_plane():
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
        expect = "sat"

        org = "$\\frac{114K_p}{ s^3 + 11.4s+14s+114K_p}$"
        approx = "$\\frac{11.29 K_p}{ s^2 + \sqrt{1.92-2.91 K_p}s+11.29 K_p}$"
        req = "TD"
        method = "S"

        return org, approx, req, method, res, expect

import sys

if __name__ == '__main__':

    if len(sys.argv) < 2:
        mode = "simple"
    else:
        mode = sys.argv[1]
        tests = ['ex_nmp', 'ex_dp0503', 'ex_dp0504', 'ex_dp0506', 'ex_plane',
                    'ex_car', 'ex_car2', 'ex_car3', 'ex_ap0506', 'ex_ap0509']

        with open('table.md', 'w') as the_file:
            # write title
            the_file.write("**Reproducing: Table.1 Evaluation results for static checking of hybrid system designs**\n\n")

            the_file.write("| id | org. | approx. | req. | method | actual res. | expect res. |\n")
            the_file.write("| ----------- | ----------- | ----------- | ----------- | ----------- |----------- |----------- |\n")

            # write content
            for test in tests:
                test_name = 'test_' + test
                org, approx, req, method, res, expect = getattr(Table, test_name)()

                if mode == "full":
                    the_file.write( f"| {test} | {org} | {approx} | {req} | {method} | {res} | {expect} | \n")
                else:
                    the_file.write( f"| {test} | omit | omit | {req} | {method} | {res} | {expect} | \n")

