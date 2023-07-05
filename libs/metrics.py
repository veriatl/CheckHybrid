import numpy
from control import *

class Metrics:

    # @tf a standard 2nd transfer function
    def __init__(self, zeta, omega_n):
        self.zeta = zeta
        self.omega_n = omega_n
        
    # dc gain
    def dc(self, a, b):
        const_num = a
        const_den = b

        return (const_num / const_den)

    # peak time
    def peak(self):
        if 0<= self.zeta and self.zeta< 1:
            omega_d = self.omega_n * numpy.sqrt(1-self.zeta**2)
            return numpy.pi / omega_d
        else:
            return None
    
    # overshoot
    def overshoot(self):
        if 0<= self.zeta and self.zeta< 1:
            pow = (- numpy.pi * self.zeta) / (numpy.sqrt(1-self.zeta**2))
            return numpy.exp(pow)
        elif self.zeta >= 1:
            return 0
        else:
            return None
    
    # rise time
    def rise(self):
        return (2.16 * self.zeta + 0.6) / self.omega_n

    # settling time
    def settle(self, e):
        return -numpy.log(e) / (self.zeta * self.omega_n)


# # print(s.model())
