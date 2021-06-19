from pysat.examples.rc2 import RC2
from myConfigurer import Configurer


class Solver:
  def __init__(self, oracle, config):
    self.model = config[0]
    self.solver = oracle(config[1], solver='g3') #, adapt=True, exhaust=True, incr=True, minz=True)
    self.transform = config[2]

  def solve(self):
    self.solver.compute()
    return self.transform(self.solver.cost)


if __name__ == '__main__':
  Config = Configurer('./input.txt')
  MySolver = Solver(RC2, Config.config())
  print (MySolver.solve())
