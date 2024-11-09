import networkx as nx
import z3


class ForallBasicUserPropagator(z3.UserPropagateBase):
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
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            self.current[step].add_node(action_name)
            # Checking and adding out edges
            for source, dest in list(self.graph.edges(action_name)):
                if dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(dest, step))
            # Checking and adding in edges
            for source, dest in list(self.graph.in_edges(action_name)):
                if source in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(source, step))
            # Check if anything has caused interference
            if literals:
                literals.add(action) # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])