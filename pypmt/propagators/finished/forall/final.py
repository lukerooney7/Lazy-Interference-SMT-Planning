import networkx as nx
import z3


class ForallFinalPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.add_final(lambda : self._final())
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []
        self.mutexes = 0
        self.name = "forall-final"

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()

    def _final(self):
        for i, step in enumerate(self.current):
            for source, dest in step.edges:
                self.conflict(deps=[self.encoder.get_action_var(source, i), self.encoder.get_action_var(dest, i)], eqs=[])

    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            self.current[step].add_node(action_name)
            # Checking and adding out edges
            for source, dest in list(self.graph.edges(action_name)):
                if dest in self.current[step]:
                    self.current[step].add_edge(source, dest)            # Checking and adding in edges
            for source, dest in list(self.graph.in_edges(action_name)):
                if source in self.current[step]:
                    self.current[step].add_edge(source, dest)