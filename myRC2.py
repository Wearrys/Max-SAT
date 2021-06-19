import re
import os
import six
import sys
import getopt
import itertools
import collections

from math import copysign
from pysat.formula import CNFPlus, WCNFPlus
from pysat.card import ITotalizer
from pysat.solvers import Solver, SolverNames


class RC2:
    def __init__(self, formula, solver='g3', verbose=0):
        self.verbose = verbose
        self.solver = solver
        self.wght = {}
        self.sels = []
        self.sums = []
        self.bnds = {}
        self.smap = {}
        self.sels_set = {}
        self.topv = formula.nv
        self.tobj = {}
        self.cost = 0
        VariableMap = collections.namedtuple('VariableMap', ['e2i', 'i2e'])
        self.vmap = VariableMap(e2i={}, i2e={})
        self.init(formula)
        print('RC2 is initialized.\n')

    def init(self, formula):
        self.oracle = Solver(
            name=self.solver, bootstrap_with=formula.hard, use_timer=True)
        for i, cl in enumerate(formula.soft):
            selv = cl[0]  # if (cl = v) selector_variable = v
            if len(cl) > 1:
                self.vcnt += 1
                selv = self.topv
                self.s2cl[selv] = cl[:]
                cl.append(-self.topv)
                self.oracle.add_clause(cl)
            if selv not in self.wght:
                self.sels.append(selv)
                self.wght[selv] = formula.wght[i]
                self.smap[selv] = i
            else:
                self.wght[selv] += formula.wght[i]
        self.sels_set = set(self.sels)
        self.sall = self.sels[:]

        for v in range(1, formula.nv + 1):
            self.vmap.e2i[v] = v
            self.vmap.i2e[v] = v

        if self.verbose:
            print('c formula: {0} vars, {1} hard, {2} soft'.format(
                formula.nv, len(formula.hard), len(formula.soft)))

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.delete()

    def delete(self):
        if self.oracle:
            self.oracle.delete()
            self.oracle = None

    def compute(self):
        res = self.__compute()
        if res:
            self.model = self.oracle.get_model()
            if self.verbose:
                print("Total model:{}".format(self.model))

            # The model is empty
            if self.model is None and self.topv == 0:
                self.model = []
            self.model = filter(lambda l: abs(l) in self.vmap.i2e, self.model)
            self.model = map(lambda l: int(
                copysign(self.vmap.i2e[abs(l)], l)), self.model)
            self.model = sorted(self.model, key=lambda l: abs(l))

            return self.model

    def __compute(self):
        while not self.oracle.solve(assumptions=self.sels + self.sums):
            self.get_core()

            if not self.core:
                return False

            self.process_core()

            if self.verbose:
                print("iteration round, cost : {}, core size : {}, soft size : {}, core : {}".format(self.cost,
                                                                                                     len(self.core), len(self.sels) + len(self.sums), self.core))
        return True

    def get_core(self):
        self.core = self.oracle.get_core()

        if self.core:
            if not self.core:
                return
            self.minw = min(map(lambda l: self.wght[l], self.core))

            iter1, iter2 = itertools.tee(self.core)
            self.core_sels = list(l for l in iter1 if l in self.sels_set)
            self.core_sums = list(l for l in iter2 if l not in self.sels_set)

    def process_core(self):
        self.cost += self.minw
        self.garbage = set()
        if len(self.core_sels) != 1 or len(self.core_sums) > 0:
            self.process_sels()
            self.process_sums()

            if len(self.rels) > 1:
                t = self.create_sum()
                self.set_bound(t, 1)
        else:
            self.oracle.add_clause([-self.core_sels[0]])
            self.garbage.add(self.core_sels[0])
        self.filter_assumps()

    def process_sels(self):
        self.rels = []

        for l in self.core_sels:
            if self.wght[l] == self.minw:
                self.garbage.add(l)
                self.rels.append(-l)
            else:
                self.wght[l] -= self.minw
                self.topv += 1
                self.oracle.add_clause([l, self.topv])
                self.rels.append(self.topv)

    def process_sums(self):
        for l in self.core_sums:
            if self.wght[l] == self.minw:
                self.garbage.add(l)
            else:
                self.wght[l] -= self.minw

            t, b = self.update_sum(l)
            if b < len(t.rhs):
                lnew = -t.rhs[b]
                if lnew not in self.wght:
                    self.set_bound(t, b)
                else:
                    self.wght[lnew] += self.minw
            self.rels.append(-l)

    def update_sum(self, assump):
        t = self.tobj[assump]
        b = self.bnds[assump] + 1
        t.increase(ubound=b, top_id=self.topv)
        self.topv = t.top_id
        if t.nof_new:
            for cl in t.cnf.clauses[-t.nof_new:]:
                self.oracle.add_clause(cl)
        return t, b

    def set_bound(self, tobj, rhs):
        self.tobj[-tobj.rhs[rhs]] = tobj
        self.bnds[-tobj.rhs[rhs]] = rhs
        self.wght[-tobj.rhs[rhs]] = self.minw
        self.sums.append(-tobj.rhs[rhs])

    def create_sum(self, bound=1):
        t = ITotalizer(lits=self.rels, ubound=bound, top_id=self.topv)
        self.topv = t.top_id
        for cl in t.cnf.clauses:
            self.oracle.add_clause(cl)
        return t

    def filter_assumps(self):
        self.sels = list(filter(lambda x: x not in self.garbage, self.sels))
        self.sums = list(filter(lambda x: x not in self.garbage, self.sums))
        self.bnds = {l: b for l, b in six.iteritems(
            self.bnds) if l not in self.garbage}
        self.wght = {l: w for l, w in six.iteritems(
            self.wght) if l not in self.garbage}
        self.sels_set.difference_update(set(self.garbage))
        self.garbage.clear()


def usage():
    '''
    Print usage message
    '''
    print('Usage:', os.path.basename(sys.argv[0]), '[options] file')
    print('Options:')
    print('\t-h,--help : Show this messag')


def parse_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhs:', [
                                   'verbose', 'help', 'solver='])
    except getopt.GetoptError as err:
        sys.stderr.write(str(err).capitalize() + '\n')
        usage()
        sys.exit(1)
    verbose = 0
    solver = 'g3'

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-s', '--solver'):
            print("arg = {}".format(arg))
            solver = str(arg)
        elif opt in ('-v', '--verbose'):
            verbose = 1
        else:
            assert False, 'Unhandled option :{} {}'.format(opt, arg)

    if len(args) != 1:
        assert False, 'No input file or too many.'

    return verbose, solver, args[0]


if __name__ == '__main__':
    verbose, solver, file = parse_options()
    if re.search('\.wcnf[p|+]?(\.(gz|bz2|lzma|xz))?$', file):
        formula = WCNFPlus(from_file=file)
    else:
        formula = CNFPlus(from_file=file).wghted()
    with RC2(formula, solver=solver, verbose=verbose) as rc2:
        model = rc2.compute()
        if model != None:
            print("model = {}".format(model))
            print('cost = {}'.format(rc2.cost))
        else:
            print("s UNSATISFIABLE")
