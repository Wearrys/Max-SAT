from myRC2 import RC2
from myGenerator import Generator
from myConfigurer import Configurer
from mySolver import Solver
import BFSolver

import random

if __name__ == '__main__':
  g = Generator("input.txt")
  c = Configurer("input.txt")
  
  TIME = 0
  TYPE = ["DOMINATING-SET", "CHROMATIC-NUMBER", "INDEPENDENT-SET"]

  while True:
    op = random.randint(1, 3)
    if (op == 1):
      g.graph_generate(8, TYPE[random.randint(0, 2)])
    elif (op == 2):
      g.knaps_generate(5, 100, 10000)
    else:
      g.tsp_generate(10, 100)

    s = Solver(RC2, c.config())
    b = BFSolver.bruteforceSolver()

    assert(s.solve() == b.solve("input.txt"))

    TIME += 1
    print ("OK", TIME)