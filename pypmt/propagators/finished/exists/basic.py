import networkx as nx
import z3
from networkx import NetworkXNoCycle


class ExistsBasicPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.name = "exists-lazy"
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
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            # Add all in and out edges to graph
            self.current[step].add_node(action_name)
            edges = list(self.graph.in_edges(action_name)) + list(self.graph.edges(action_name))
            for source, dest in edges:
                if source in self.current[step] and dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
            try:
                cycle = nx.find_cycle(G=self.current[step], source=action_name)
                # If a cycle is found, throw conflict for all nodes in cycle
                if cycle:
                    for source, _ in cycle:
                        literals.add(self.encoder.get_action_var(source, step))
            except NetworkXNoCycle:
                pass
            # If interference throw conflict
            if literals:
                self.conflict(deps=list(literals), eqs=[])
