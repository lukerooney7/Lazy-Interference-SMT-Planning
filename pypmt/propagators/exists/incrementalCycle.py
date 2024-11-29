import networkx as nx
import z3


class ExistsIncrementalCyclePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
        self.ancestors = {}
        self.descendants = {}
        self.stackA = []
        self.stackD = []
        self.stack = []
        self.consistent = True

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.stackA.append(self.ancestors.copy())
        self.stackD.append(self.descendants.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.stackA.pop()
            self.descendants = self.stackD.pop()
        self.consistent = True

    def _fixed(self, action, value):
        if value and self.consistent:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            self.current[step].add(action_name)
            if action_name not in self.ancestors:
                # Initialise ancestors/descendants if new node
                self.ancestors[action_name] = set()
                self.descendants[action_name] = set()
            # Incremental Cycle Detection
            for source, _ in self.graph.in_edges(action_name):
                if source in self.current[step]:
                    to_explore = [action_name]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.consistent = False
                            self.conflict(deps=[self.encoder.get_action_var(source, step), action], eqs=[])
                            return
                        elif source in self.ancestors[node]:
                            pass
                        elif (not len(self.ancestors[source]) == len(self.ancestors[action_name])
                              and not len(self.descendants[source]) == len(self.descendants[action_name])):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for neighbour, _ in self.graph.in_edges(node):
                                if neighbour in self.current[step]:
                                    to_explore.append(neighbour)
                            for _, neighbour in self.graph.edges(node):
                                if neighbour in self.current[step]:
                                    to_explore.append(neighbour)
            for _, dest in set(self.graph.edges(action_name)):
                if dest in self.current[step]:
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if dest == node or node in self.ancestors[dest]:
                            self.consistent = False
                            self.conflict(deps=[self.encoder.get_action_var(dest, step), action], eqs=[])
                            return
                        elif dest in self.ancestors[node]:
                            pass
                        elif (not len(self.ancestors[dest]) == len(self.ancestors[action_name])
                              and not len(self.descendants[dest]) == len(self.descendants[action_name])):
                            pass
                        else:
                            self.ancestors[node].add(dest)
                            self.descendants[dest].add(node)
                            for neighbour, _ in self.graph.in_edges(node):
                                if neighbour in self.current[step]:
                                    to_explore.append(neighbour)
                            for _, neighbour in self.graph.edges(node):
                                if neighbour in self.current[step]:
                                    to_explore.append(neighbour)