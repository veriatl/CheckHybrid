import os
import subprocess
import datetime 

class dReal:

    def __init__(self):
        self.prog = "/opt/dreal/4.21.06.2/bin/dreal"
        self.file = ""

    def getSMT2(self, body):
        s = self.header()
        s += body
        s += self.footer()
        return s

    def header(self):
        return "(set-logic QF_NRA)\n"
    
    def footer(self):
        return "(check-sat)\n(get-model)\n(exit)"

    def exe(self):
        r = subprocess.run([self.prog, self.file])
        return r.stdout

    def save(self, text):
        # prepare path
        __location__ = os.path.realpath(
                        os.path.join(os.getcwd(), 
                                     os.path.dirname(__file__)))

        file = datetime.date.today().strftime("test-%m-%d-%y.smt2")                             
        file_loc = os.path.join(__location__, file)

        # store file path
        self.file = file_loc

        # write to file
        with open(file_loc, "w") as text_file:
            text_file.write(text)
        