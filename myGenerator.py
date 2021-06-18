import random


class Generator:

  def __init__(self, output_file):
    self.output_file = output_file

  def graph_generate(self, n, model):
    # randomly choose p in [0,1] and randomly generate a graph from G(n,p)
    p = random.random()
    edges = []
    for i in range(n):
      for j in range(i + 1, n):
        if random.random() <= p:
          edges.append((i, j))
    f = open(self.output_file, "w")
    f.write(f"{model}\n")
    f.write(f"{n} {len(edges)}\n")
    for (u, v) in edges:
      f.write(f"{u} {v}\n")
    f.close()

  # n, V denote the number of vertices and the upper bound of value
  def tsp_generate(self, n, V):
    f = open(self.output_file, "w")
    f.write("TSP\n")
    f.write(f"{n}\n")
    for i in range(n):
      for j in range(n):
        if i != j:
          f.write(f"{random.randint(1, V)} ")
        else:
          f.write("0 ")
      f.write("\n")
    f.close()

  # n, W, V denote the number of objects, the capacity and the upper bound of value
  def knaps_generate(self, n, W, V):
    f = open(self.output_file, "w")
    f.write("01-KNAPSACK\n")
    f.write(f"{n} {W}\n")
    for i in range(n):
      f.write(f"{random.randint(0, W)} ")
    f.write("\n")
    for i in range(n):
      f.write(f"{random.randint(1, V)} ")
    f.close()