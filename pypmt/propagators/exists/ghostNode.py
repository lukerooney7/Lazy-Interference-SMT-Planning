import networkx as nx
import z3

class GhostNodeUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.ancestors = {}
        self.descendants = {}
        self.ancestorsStack = []
        self.descendantsStack = []
        self.stack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.ancestorsStack.append(self.ancestors.copy())
        self.descendantsStack.append(self.descendants.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.ancestorsStack.pop()
            self.descendants = self.descendantsStack.pop()

    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            self.current[step].add_node(action_name)
            # Initialise ancestors/descendants if new node
            if action_name not in self.ancestors:
                self.ancestors[action_name] = set()
                self.descendants[action_name] = set()
            # Incremental cycle detection for in edges
            for source, dest in list(self.graph.in_edges(action_name)):
                if source in self.current[step] and dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.conflict(deps=[self.encoder.get_action_var(source, step),
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            self.consistent = True
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif not len(self.ancestors[source]) == len(self.ancestors[dest]) and not len(self.descendants[source]) == len(self.descendants[dest]):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for node, neighbour in self.current[step].edges:
                                to_explore.append(neighbour)
                else:
                    clause = set()
                    for node in self.graph.predecessors(source):
                        if node in self.descendants[dest]:
                            clause.add(z3.Not(self.encoder.get_action_var(source, step)))
                            break
                    self.propagate(e=z3.And(clause), ids=[], eqs=[])
            # Incremental cycle detection for out edges
            for source, dest in list(self.graph.edges(action_name)):
                if source in self.current[step] and dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.conflict(deps=[self.encoder.get_action_var(source, step),
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            self.consistent = False
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif not len(self.ancestors[source]) == len(self.ancestors[dest]) and not len(self.descendants[source]) == len(self.descendants[dest]):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for node, neighbour in self.current[step].edges:
                                to_explore.append(neighbour)
                else:
                    for node in self.graph.neighbors(dest):
                        if node in self.ancestors[source]:
                            self.propagate(e=z3.Not(self.encoder.get_action_var(dest, step)), ids=[], eqs=[])
                            break
