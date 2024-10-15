import networkx as nx
import z3
# from matplotlib import pyplot as plt
import copy

from pypmt.utilities import log


class LazyUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        # Need to understand what all of this does!
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.trail = []  # Tracks variables/states as they are fixed, maintains state of the solution
        self.lim = []  # Stores limit values, helps backtracking when Z3 undoes changes (conflicts/backtracking)
        self.add_final(lambda: self._final())
        # self.add_eq(lambda x, y: self._eq(x, y))
        # self.add_created(lambda t: self._created(t))
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.first = True
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)

    def pop(self, n):
        # log(f'pop {n} times', 3)
        for _ in range(n):
            self.current = self.stack.pop()

    def _final(self):
        log("Final", 5)

    def _fixed(self, action, value):
        if value:
            step = int(str(action).split('_')[-1])
            action_name = '_'.join(str(action).split('_')[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = []
            self.current[step].add_node(action_name)
            edges = list(self.graph.edges(action_name)) + list(self.graph.in_edges(action_name))
            if self.encoder.modifier.forall:
                for e in edges:
                    a1, a2 = e
                    if a2 in self.current[step] and a1 in self.current[step]:
                        self.current[step].add_edge(a1, a2)
                        literals.append(self.encoder.get_action_var(a1, step))
                        literals.append(self.encoder.get_action_var(a2, step))
            else:
                for e in edges:
                    a1, a2 = e
                    if a2 in self.current[step] and a1 in self.current[step]:
                        self.current[step].add_edge(a1, a2)
                        if sum(1 for _ in nx.strongly_connected_components(self.graph)) > 0:
                            literals.append(self.encoder.get_action_var(a1, step))
                            literals.append(self.encoder.get_action_var(a2, step))
                            break
            if literals:
                literals.append(action)
                literals = list(dict.fromkeys(literals))
                self.conflict(deps=literals, eqs=[])
