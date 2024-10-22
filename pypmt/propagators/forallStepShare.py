import networkx as nx
import z3
from pypmt.utilities import log


class ForallStepShareUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []
        self.mutexes = set()
        self.edge_map = {}

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()

    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            graph = self.current[step]
            graph.add_node(action_name)
            if action_name in self.edge_map:
                edges = self.edge_map[action_name]
            else:
                edges = list(self.graph.edges(action_name)) + list(self.graph.in_edges(action_name))
                self.edge_map[action_name] = edges
            for a1, a2 in edges:
                if a2 in graph and a1 in graph:
                    graph.add_edge(a1, a2)
                    literals.add(self.encoder.get_action_var(a1, step))
                    literals.add(self.encoder.get_action_var(a2, step))
                    if (a1, a2) not in self.mutexes and (a2, a1) not in self.mutexes:
                        new_mutexes = set()
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(a1, i),
                                                          self.encoder.get_action_var(a2, step))))
                        self.solver.add(new_mutexes)
                        self.mutexes.add((a1, a2))
            if literals:
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
