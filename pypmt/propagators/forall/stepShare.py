import networkx as nx
import z3


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
            # Checking and adding in edges
            for source, dest in list(self.graph.edges(action_name)):
                if dest in graph:
                    graph.add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(dest, step))
                    if (source, dest) not in self.mutexes and (dest, source) not in self.mutexes:
                        new_mutexes = set()
                        # Add mutexes for this interference for all seen steps
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                          self.encoder.get_action_var(dest, step))))
                        self.solver.add(new_mutexes)
                        self.mutexes.add((source, dest))
            # Checking and adding out edges
            for source, dest in list(self.graph.in_edges(action_name)):
                if source in graph:
                    graph.add_edge(source, dest)
                    literals.add(self.encoder.get_action_var(source, step))
                    if (source, dest) not in self.mutexes and (dest, source) not in self.mutexes:
                        new_mutexes = set()
                        # Add mutexes for this interference for all seen steps
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                          self.encoder.get_action_var(dest, step))))
                        self.solver.add(new_mutexes)
                        self.mutexes.add((source, dest))
            # Check if anything has caused interference
            if literals:
                literals.add(action)  # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])
