import networkx as nx
import z3
from pypmt.utilities import log


class LazyUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        # Need to understand what all of this does!
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.trail = []  # Tracks variables/states as they are fixed, maintains state of the solution
        self.lim = []  # Stores limit values, helps backtracking when Z3 undoes changes (conflicts/backtracking)
        # self.add_fixed(lambda x, v: self._fixed(x, v))
        self.add_final(lambda: self._final())
        # self.add_eq(lambda x, y: self._eq(x, y))
        # self.add_created(lambda t: self._created(t))
        self.add_fixed(self._fixed)
        self.first = True
        self.encoder = e  # Do we need this apart from the graph???
        self.graph = self.encoder.modifier.graph
        self.current = nx.DiGraph()
        self.stack = []

    def push(self):
        log("Push", 5)
        self.stack.append(self.current.copy())

    def pop(self, n):
        log("Pop", 5)
        self.current = self.stack.pop()

    def _final(self):
        log("Final", 5)

    def check_forAll(self):
        for edge in self.current.edges():
            a1, a2 = edge
            self.solver.add(z3.Not(z3.And(a1, a2)))
        return False

    def check_exists(self):
        components = nx.strongly_connected_components(self.current)
        for c in components:
            numbers = {}
            for i, a in enumerate(c):
                numbers[a] = i
            subgraph = self.current.subgraph(c)
            for edge in subgraph.edges():
                a1, a2 = edge
                if numbers[a1] < numbers[a2]:
                    self.solver.add(z3.Not(z3.And(a1, a2)))

    def _fixed(self, action, value):
        for e in self.graph.out_edges(action):
            a1, a2 = e
            self.current.add_edge(a1, a2)
        self.check_forAll()
