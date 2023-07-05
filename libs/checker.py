from z3 import *
import libs.formula2 as formula_num
import libs.formulaSym2 as formula_sym
import libs.z3model as z3model

class Checker:

    def __init__(self,zeta,omega_n,r=None):     
        
        self.zeta = zeta
        self.omega_n = omega_n
        
        self.solver = Solver()

        if r == None:
            r = Real('r')
        self.amp = r
        
        self.issym = self.isSymbolic()
        self.factory = self.formula_factory()


    def add(self, f):
        self.solver.add(f)

    def formula_factory(self):
        if self.issym:
            return formula_sym.Formula(self.zeta, self.omega_n)
        else:
            return formula_num.Formula(self.zeta, self.omega_n)

    # default automated PO generation 
    def auto_pog(self, safety, context=None):
        wn_square = self.omega_n * self.omega_n
        f = self.factory
        if self.issym:
            Properties = And(f.Pdc(), f.PMp(), f.Ptp_1(), f.Ptp_2(), f.Ptr(), f.Pts(), f.Pin(self.amp))
            Estimations = And(f.Edc(wn_square,wn_square), f.EMp_2(), f.EMp_3(), f.Etp(), f.Ets(), f.Etr()) 
        else:
            Properties = And(f.Pdc(), f.PMp(), f.Ptp_1(), f.Ptp_2(), f.Ptr(), f.Pts(), f.Pin(self.amp))
            Estimations = And(f.Edc(wn_square,wn_square), f.EMp(), f.Etp(), f.Ets(), f.Etr())


        if context != None:
            self.context = context
            self.add(context) 

        self.safety = safety
        self.add(simplify(Estimations))
        self.add(simplify(Properties))
        PO = safety    
        self.add(Not(PO))

    def result(self):
        set_option(rational_to_decimal = True)
        t = Then('simplify', 'qfnra-nlsat')
        s = self.solver
        print(f"static checking result =  {s.check()}")
        if s.check() == sat:
            print(f"static checking model =  {s.model()}")

    def calibrate(self):
        if self.issym:
            z = self.model(self.zeta)
            omg = self.model(self.omega_n)
            c = Checker(z, omg, self.amp)
            c.auto_pog(self.safety)
            print(f"static checking result =  {c.solver.check()}")
            if c.solver.check() == sat:
                print(f"static checking model =  {c.solver.model()}")
            return c
        else:
            return None



    def model(self, key=None):
        s = self.solver
        s.check()
        m = s.model()
        z3helper = z3model.z3model(m)
        return (z3helper.getReal(key))

    def isSymbolic(self):
        if isinstance(self.zeta, z3.z3.ArithRef) or isinstance(self.omega_n, z3.z3.ArithRef):
            return True
        else:
            return False

    def check(self):
        return self.solver.check().__repr__()

