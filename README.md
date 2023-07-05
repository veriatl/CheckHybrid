# A Static Checker for Hybrid System Designs via the Laplace Transformation
 
**Abstract:** We propose a static checker, based on Laplace transform, for checking hybrid system designs against their time-domain and safety requirements. It aims to filter out designs that have obvious requirement violations. This is to prevent users from performing expensive design evaluation tasks (e.g. simulation, model checking, or theorem proving) until those violations are reviewed or fixed. In the process, our checker depends on domain knowledge of the Laplace transformation to transform and approximate a hybrid system design for a linear time-invariant system into a mathematical model, namely the transfer function. Then, it derives time-domain metrics based on the approximation, and provides an interpretation of time-domain metrics in first-order formulas over real numbers to coarsely quantify the reachable states. This allows it to formulate a proof obligation for checking requirement violations of the approximation in the Z3 SMT solver. Our checker can be applied to hybrid system designs that are parameterized by either numerical or symbolic values. We evaluated our approach on 10 hybrid system designs from the literature and textbooks. This repository/artifact contains the source code of our static checker and evaluation that we conduct and conclude in our paper. 

**Table of Contents** 
  - [Organization of the repository](#organization-of-the-repository)
  - [Requirements](#requirements)
  - [Offline installation (Ubuntu)](#offline-installation-ubuntu)
  - [How to use](#how-to-use)
  - [Experiments](#experiments)
  - [License](#license)
  - [Issues](#issues)
  - [Acknowledgement](#acknowledgement)
  
## Organization of the repository 

* Folder [libs](https://github.com/veriatl/CheckHybrid/tree/main/libs) - contains the source code for our static checker.
* Folder [notebooks](https://github.com/veriatl/CheckHybrid/tree/main/notebooks) - contains the python notebooks for the experiment in the paper.
* Folder [tests](https://github.com/veriatl/CheckHybrid/tree/main/tests) - contains scripts for regression tests and reproducing experiment.
* Folder [sympy](https://github.com/veriatl/CheckHybrid/tree/main/sympy) - contains experimental features such as automatic transfer function approximation, and routh array for stability.
* Folder [offline](https://github.com/veriatl/CheckHybrid/tree/main/offline) - for achieved Python dependencies used in this repository.


## Requirements 

Basics:

* Python 3.8
  * Pip (21.1.3) 
  * Jupyter (1.0.0) Notebook (6.4.6)

SMT Solver in Python:

* z3-solver (4.8.10.0)

Control, Statistics, and Plotting in Python:

* control (0.9.0)
* scipy (1.7.1)
* numpy (1.21.2)
* matplotlib (3.4.3)
* sympy (1.8)

## Offline installation (Ubuntu)

**Assume Python and Pip are installed, and this repository is downloaded as an archive file named `CheckHybrid-main.zip`**

 0. Navigate to the folder that contains the archive, and unzip it to a folder we hereafter refer as `CheckHybrid-main`:
```
unzip CheckHybrid-main.zip
```

 1. Navigate to `CheckHybrid-main/offline/`, installing python dependencies via pip using provided packages (a reboot is needed after this step):
```
cd CheckHybrid-main/offline
pip3 install -r requirements.txt -U --no-index --find-links .
sudo reboot
```

## How to use
 0. Import our static checker, z3 solver into your python project
 ```
 import libs.checker as checker
 from z3 import *
 ```

 1. It receives the damping ratio **zeta**, and un-damped natural frequency **omega_n** for the transfer function of a given hybrid system design (approximated by the user if it is not in standard 2nd-order form): 
 ```
 omega_n = Real('omega_n')  
 zeta = Real('zeta')
 c = checker.Checker(zeta,omega_n)
 ```

 2. Add additional user-specified constraints if there are any:
 ```
 f1 = And(zeta>=0, zeta < 1)
 c.add(f1)
 ```

 3. Add desired safety or time-domain requirements:
 ```
 p = c.factory.y
 t = c.factory.t
 r = c.amp
 safety = p[t] <= r
 c.auto_pog(safety)
 ```

 4. Obtain the checking result. The checker returns **sat** and a counterexample when requirements are violated by the design according to our checker, or **unsat** if our checker does not find requirement violations, or **unknown** if the checker cannot solve:
 ```
 c.result()
 # to obtain more accurate counterexample for symbolic static checking:
 # new_checker = c.calibrate()    
 ```

 5. Counterexample extraction:
 ```
 v_z = c.model(zeta)
 ```

## Experiments

**To reproduce Table.1 in the paper**. Assuming you are in the root folder `CheckHybrid-main/`. simply run the following from the command line:

```
cd tests
python3 table.py simple
```

It generates a file `tests/table.md` that can be opened in a text editor (transfer functions are omitted for display).

The following command can generate a markdown file `tests/table.md` with the transfer functions:
```
cd tests
python3 table.py full
``` 


**To walkthrough of provided examples**. Assuming you are in the root folder `CheckHybrid-main/`. 

 0. first run the following from the command line to start the `jupyter notebook` in your browser:
```
cd notebooks
jupyter notebook
```

 1. You will then see this interface, choose an example of your interest:

<img src="imgs/entry.PNG" alt="jupyter entry" width="400"/>

 2. Then you can execute each code block (cell) by clicking the `Run` button from the menu:

<img src="imgs/execute.PNG" alt="jupyter entry" width="400"/>

 3. The result of the executed block will appear (if there are any):

<img src="imgs/result.PNG" alt="jupyter entry" width="400"/>

> Note that `jupyter notebook` is an interpreter. This means that cells have dependencies. So, you will need to step through each block to get to the bottom. Alternatively, you can click `Cell -> Run All` to execute all blocks at once.



## License

This project is licensed under Eclipse Public License (v2). See LICENSE.md in the root directory for details. Third party libraries are under independent licenses, see their source files for details.

## Issues

If you experience issues installing or using our static checker, you can submit an issue on github or contact us at:

> Zheng Cheng: zheng.cheng@inria.fr

> Dominique Méry: dominique.mery@loria.fr

## Acknowledgement

This work is supported by the grant ANR-17-CE25-0005 (The [DISCONT](http://discont.loria.fr) Project) from the Agence Nationale de la Recherche (ANR).
