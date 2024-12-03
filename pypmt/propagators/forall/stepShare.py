import networkx as nx
import z3


class ForallStepSharePropagator(z3.UserPropagateBase):
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

    def step_share(self, source, dest):
        if (source, dest) in self.mutexes or (dest, source) in self.mutexes:
            return
        for i in range(0, len(self.current)-1):
            self.propagate(
                z3.Or(z3.Not(self.encoder.get_action_var(dest, i)),
                    z3.Not(self.encoder.get_action_var(source, i))),
            [])
        self.mutexes.add((source, dest))

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
            # Checking and adding in edges
            for source, dest in list(self.graph.edges(action_name)):
                if dest in graph:
                    graph.add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(dest, step))
                    self.step_share(source, dest)
            # Checking and adding out edges
            for source, dest in list(self.graph.in_edges(action_name)):
                if source in graph:
                    graph.add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(source, step))
                    self.step_share(source, dest)
            # Check if anything has caused interference
            if literals:
                literals.add(action)  # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])
