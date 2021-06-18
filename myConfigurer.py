import math
from pysat.formula import WCNFPlus


class Configurer:
  def __init__(self, file):
    self.file = file
    self.num_var = 0

  def new_var(self):
    self.num_var += 1
    return self.num_var

  def reduce(self, model, data):

    self.num_var = 0
    wcnf = WCNFPlus()

    def _not(a):
      if (a == 'zero'):
        return 'one'
      elif (a == 'one'):
        return 'zero'
      else:
        return -a

    def _and(a, b):
      if (a == 'zero' or b == 'zero'):
        return 'zero'
      elif (a == 'one' or b == 'one'):
        if (a == 'one'):
          return b
        return a
      else:
        c = self.new_var()
        wcnf.append([-c, a])
        wcnf.append([-c, b])
        wcnf.append([-a, -b, c])
        return c

    def _or(a, b):
      return _not(_and(_not(a), _not(b)))

    def _xor(a, b):
      return _or(_and(_not(a), b), _and(a, _not(b)))

    if (model == 'INDEPENDENT-SET'):
      n, m = map(int, data[1].split(' '))
      x = [self.new_var() for i in range(n)]

      for i in range(n):
        wcnf.append([x[i]], weight=1)
      for i in range(m):
        u, v = map(int, data[i + 2].split(' '))
        wcnf.append([-x[u], -x[v]])
      return wcnf, lambda x: n - x

    elif (model == 'DOMINATING-SET'):
      n, m = map(int, data[1].split(' '))
      x = [self.new_var() for i in range(n)]
      adj = [set([x[i]]) for i in range(n)]

      for i in range(n):
        wcnf.append([-x[i]], weight=1)
      for i in range(m):
        u, v = map(int, data[i + 2].split(' '))
        adj[u].add(x[v])
        adj[v].add(x[u])
      for i in range(n):
        wcnf.append(list(adj[i]))
      return wcnf, lambda x: x

    elif (model == 'CHROMATIC-NUMBER'):
      n, m = map(int, data[1].split(' '))
      c = [self.new_var() for i in range(n)]
      x = [[self.new_var() for i in range(n)] for j in range(n)]

      for i in range(n):
        wcnf.append([-c[i]], weight=1)
        wcnf.append([x[i][j] for j in range(n)])  # at least one color
        for j in range(n):
          wcnf.append([-x[i][j], c[j]])
          for k in range(j + 1, n):
            wcnf.append([-x[i][j], -x[i][k]])  # at most one color

      for i in range(m):
        u, v = map(int, data[i + 2].split(' '))
        for j in range(n):
          wcnf.append([-x[u][j], -x[v][j]])
      
      return wcnf, lambda x: x

    elif (model == 'TSP'):
      n = int(data[1])
      x = [[self.new_var() if not (i == j) else None for i in range(n)] for j in range(n)]
      f = [[self.new_var() if (i > 0) else 'one' for i in range(n)] for j in range(n)]

      for i in range(n):
        d = list(map(int, data[i+2].split(' ')))
        for j in range(n):
          if not (i == j):
            wcnf.append([-x[i][j]], weight=d[j])
            for k in range(j+1, n):
              if not (k == i):
                wcnf.append([-x[i][j], -x[i][k]])  # outdegree(i) <= 1
                # wcnf.append([-x[j][i], -x[k][i]])  # indegree(i) <= 1
        wcnf.append(list(filter(lambda x: x != None, [x[j][i] for j in range(n)])))  # indegree(i) >= 1
        wcnf.append(list(filter(lambda x: x != None, [x[i][j] for j in range(n)])))  # outdegree(i) >= 1

      for i in range(1, n):
        wcnf.append([-f[0][i]])

      for i in range(1, n):
        for j in range(1, n):
          a = f[i][j]
          b = f[i-1][j]
          for k in range(n):
            if not (k == j):
              b = _or(b, _and(f[i-1][k], x[k][j]))
          print (i, j, a, b)
          wcnf.append([-a, b])
          wcnf.append([-b, a])

      for i in range(1, n):
        wcnf.append([f[n-1][i]])
      return wcnf, lambda x: x

    elif (model == '01-KNAPSACK'):
      n, W = map(int, data[1].split(' '))
      wei = list(map(int, data[2].split(' ')))
      val = list(map(int, data[3].split(' ')))
      x = [self.new_var() for i in range(n)]

      B = max(W, sum(wei))
      B = math.ceil(math.log2(B)) + 1
      S = ['zero' for i in range(B)]

      def add(X, Y):
        C = 'zero'
        Z = [0 for i in range(B)]
        for i in range(B):
          t0 = _xor(X[i], Y[i])
          t1 = _and(X[i], Y[i])
          Z[i], C = _xor(t0, C), _or(t1, _and(t0, C))
        return Z

      for i in range(n):
        wcnf.append([x[i]], weight=val[i])
        T = [(x[i]) if (wei[i] >> j & 1) else 'zero' for j in range(B)]
        S = add(S, T)

      EQ = 'one'
      LT = 'zero'
      for i in range(B-1, -1, -1):
        W_i = 'one' if (W >> i & 1) else 'zero'
        LT = _or(LT, _and(EQ, _and(_not(S[i]), W_i)))
        EQ = _and(EQ, _not(_xor(S[i], W_i)))

      if(_or(LT, EQ) not in ['zero', 'one']):
        wcnf.append([_or(LT, EQ)])

      return wcnf, lambda x: sum(val) - x

  def config(self):
    data = [line.strip() for line in open(self.file, 'r')]
    model = data[0]
    formula, transform = self.reduce(model, data)
    return model, formula, transform
