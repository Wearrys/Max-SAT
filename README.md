# Max-SAT Based Solver for NP-complete Problems

This is in requirement of PKU Course : *Algorithm design and analysis*. 

This package includes two parts:

- A sat solver based on the paper RC2.
- A manual reducer for several important NP-complete problems.

## Dependencies

You should install `pysat` before running the code.

```bash
pip3 install pysat
```

## Solver

### Definition

A partial weighted Max-SAT problem is a generalization of the Max-Sat problem. Clauses in a partial CNF formula are characterized as **hard**, meaning that these clauses must be satisfied, or **soft**, meaning that these are to be satisfied, if at all possible.  An integer weight can be associated with each soft clause, and the goal of maximum satisfiability (MaxSAT) is to find an assignment to the propositional variables such that the hard clauses are satisfied, and the sum of the weights of the satisfied soft clauses is maximized. 

### Mechanism

The solver `myRC2.py` is a simplified core-guided Max-SAT solver based on existing RC2 code. It solves the Max-SAT problems of the partial weighted CNF form.

- It uses a **ITotalizer** to create inequalities in SAT.

- It is based on a SAT solver which could returns an unsatisfiable core(a set of clauses can not be satisfied simultaneously). It then create a sat equation which releases the constraints so that at least one of these clauses could be satisfied. 

## Karp Reducer

The code in `myConfigurer.py` converts some NPC problems
to its equivalent form of Max-SAT.

To run it, the input should begin with a line indicates the model(`INDEPENDENT-SET`, `DOMINATING-SET`, `CHROMATIC-NUMBER`, `TSP` or `01-KNAPSACK`), then describe the problem with following format:

- TSP

  Input `n` at first line denote number of nodes
  then input adjacent matrix of size `n*n`

  ```
  TSP
  3
  0 2 2 
  3 0 4 
  2 5 0 
  ```

- IND-SET/DOM-SET/CHROM-NUMBER

  Input `n m` at first line denote number of nodes and edges
  then input one edges at each following line with `u v` denote edge (u, v)

  ```
  INDEPENDENT-SET
  4 5
  0 1
  0 2
  0 3
  1 2
  2 3
  ```

- 01-KNAPSACK

  Input `n W` at first line denote number and capacity of the knapsack
  at the second line input `wei[]` of size `n` denote weights of the objects
  at the third line input `val[]` of size `n` denotes values of the objects
  
  ```
  01-KNAPSACK
  3 5
  1 5 3 
  2 1 3 
  ```

Note that the vertex number in graph **should begin with 0**.

## Bruteforce Solver

The code in `BFSolver.py` contains the brute force code to verify the algorithm's correctness. 

## Data Generator and Correctness Verifier

The code `myGenerator.py` generates small data and `checker.py` runs them in `mySolver.py` and `BFSolver.py`, verifying the correctness by checking the answers.

## Efficiency Tester

The code `myGenerator.py` randomly generates data and `test.py` runs them in `mySolver.py` to test the efficiency of the algorithm in randomly generated data.

## References

Ignatiev, Alexey, Morgado, Antonio, and Marques-Silva, Joaoas. *RC2: An Efficient MaxSAT Solver*. 1 Jan. 2019 : 53 – 64.

Ignatiev, Alexey et al. *PySAT: A Python Toolkit for Prototyping with SAT Oracles.* (2018).
