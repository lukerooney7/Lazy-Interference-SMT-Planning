import networkx as nx
import z3
from networkx import NetworkXNoCycle


class ExistsBasicUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
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
            edges = list(self.graph.in_edges(action_name)) + list(self.graph.edges(action_name))
            for a1, a2 in edges:
                if a2 in self.current[step] and a1 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
            try:
                cycle = nx.find_cycle(G=self.current[step], source=action_name)
                if cycle:
                    for a, b in cycle:
                        literals.add(self.encoder.get_action_var(a, step))
                        literals.add(self.encoder.get_action_var(b, step))
            except NetworkXNoCycle:
                pass
            if literals:
                self.conflict(deps=list(literals), eqs=[])