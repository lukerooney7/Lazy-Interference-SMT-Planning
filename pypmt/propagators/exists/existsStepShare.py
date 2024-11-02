import networkx as nx
import z3
from pypmt.utilities import log


class ExistsBasicUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []
        self.mutexes = set()
        self.numbers = {a: i for i, a in enumerate(self.graph)}

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
            self.current[step].add_node(action_name)
            edges = list(self.graph.edges(action_name)) + list(self.graph.in_edges(action_name))
            for a1, a2 in edges:
                if a2 in self.current[step] and a1 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
            for a1, a2 in self.current[step].edges():
                if self.numbers[a1] <= self.numbers[a2]:
                    literals.add(self.encoder.get_action_var(a1, step))
                    literals.add(self.encoder.get_action_var(a2, step))
                    # if (a1, a2) not in self.mutexes and (a2, a1) not in self.mutexes:
                        # new_mutexes = set()
                    for i in range(0, len(self.current)):
                        literals.add(self.encoder.get_action_var(a1, i))
                        literals.add(self.encoder.get_action_var(a2, i))
                        #     new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(a1, i),
                        #                                   self.encoder.get_action_var(a2, step))))
                        # self.solver.add(new_mutexes)
                        # self.mutexes.add((a1, a2))
                    break

            if literals:
                # literals.add(action)
                self.conflict(deps=list(literals), eqs=[])