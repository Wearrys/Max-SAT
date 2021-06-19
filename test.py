from myRC2 import RC2
# from pysat.examples.rc2 import RC2
from tools.myGenerator import Generator
from myConfigurer import Configurer
from mySolver import Solver
import time
import tools.BFSolver

import random

if __name__ == '__main__':
  g = Generator("input.txt")
  c = Configurer("input.txt")
  
  TIME = 0
  TYPE = ["DOMINATING-SET", "CHROMATIC-NUMBER", "INDEPENDENT-SET"]

  f = open("result.txt", "w")
  # run 20 times for each n
  T = 10
  # ns = [5, 8, 10, 12, 15, 18, 20, 22, 25, 28, 30, 100]
  ns = [[20, 5]]
  ty = 2

  f.write(f"TSP\n")
  for n, V in ns:
    total_time = 0.0
    for i in range(T):
      # g.graph_generate(n, TYPE[ty])
      g.tsp_generate(n, V)
      start_time = time.time()
      print("start")
      s = Solver(RC2, c.config())
      res = s.solve()
      print(f"i = {i}, res = {res}")
      end_time = time.time()
      total_time += end_time - start_time
    total_time /= T
    f.write(f"n = {n}, V = {V}, average running time = {total_time} seconds\n")
  f.close()