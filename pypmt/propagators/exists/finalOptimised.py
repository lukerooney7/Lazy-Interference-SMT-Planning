import networkx as nx
import z3


class TestPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.add_final(lambda: self._final())
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.ancestors = {}
        self.descendants = {}
        self.stackA = []
        self.stackD = []
        self.stack = []
        self.stackConflict = []
        self.conflict_edges = [set()]

    def push(self):
        new = []
        new2 = []
        for graph in self.current:
            new.append(graph.copy())
        for step in self.conflict_edges:
            new2.append(step.copy())
        self.stack.append(new)
        self.stackConflict.append(new2)
        self.stackA.append(self.ancestors.copy())
        self.stackD.append(self.descendants.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.stackA.pop()
            self.descendants = self.stackD.pop()
            self.conflict_edges = self.stackConflict.pop()

    def _final(self):
        for step in self.conflict_edges:
            for source, dest in step:
                self.conflict(deps=[source, dest], eqs=[])

    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
                self.conflict_edges.append(set())
            self.current[step].add_node(action_name)
            if action_name not in self.ancestors:
                # Initialise ancestors/descendants if new node
                self.ancestors[action_name] = set()
                self.descendants[action_name] = set()
            # Incremental Cycle Detection
            for source, dest in set(self.graph.in_edges(action_name)) | set(self.graph.edges(action_name)):
                source_var = self.encoder.get_action_var(source, step)
                dest_var = self.encoder.get_action_var(dest, step)
                if source in self.current[step] and dest in self.current[step]:
                    if self.current[step].has_edge(dest, source):
                        self.conflict_edges[step].add((
                            source_var,
                            dest_var
                        ))
                        continue
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    visited = set(dest)
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source] or node in self.descendants[source]:
                            self.conflict_edges[step].add((
                                source_var,
                                dest_var
                            ))
                        elif source in self.ancestors[node]:
                            pass
                        elif (not len(self.ancestors[source]) == len(self.ancestors[dest])
                              and not len(self.descendants[source]) == len(self.descendants[dest])):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for node, neighbour in self.current[step].edges:
                                if neighbour not in visited:
                                    visited.add(neighbour)
                                    to_explore.append(neighbour)
