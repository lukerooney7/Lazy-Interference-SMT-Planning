import networkx as nx
import z3

class ExistsGhost2Propagator(z3.UserPropagateBase):
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
        self.propagated = set()
        self.propagatedStack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.ancestorsStack.append(self.ancestors.copy())
        self.descendantsStack.append(self.descendants.copy())
        self.propagatedStack.append(self.propagated.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.ancestorsStack.pop()
            self.descendants = self.descendantsStack.pop()
            self.propagated = self.propagatedStack.pop()

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
            for source, dest in self.graph.in_edges(action_name):
                if source in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.conflict(deps=[self.encoder.get_action_var(source, step),
                                                action], eqs=[])
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif not len(self.ancestors[source]) == len(self.ancestors[dest]) and not len(self.descendants[source]) == len(self.descendants[dest]):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for neighbour in self.current[step].neighbors(node):
                                to_explore.append(neighbour)
                elif (set(self.graph.predecessors(source)) & (self.descendants[dest] | {dest})
                    and (source, dest) not in self.propagated):
                    self.propagate(
                        e=z3.Not(self.encoder.get_action_var(source, step)),
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated.add((source, dest))
                    self.propagated.add((dest, source))
                else:
                    s = set()
                    for node in self.graph.predecessors(source):
                        s |= set(self.graph.predecessors(node))
                    for n in s & (self.descendants[dest] | {dest}):
                        self.propagate(e=z3.Or(
                            z3.Not(self.encoder.get_action_var(source, step)),
                            z3.Not(self.encoder.get_action_var(n, step)),
                            z3.Not(action)
                        ), ids=[], eqs=[])
                        self.propagated.add((n, source))
                        self.propagated.add((source, n))
            # Incremental cycle detection for out edges
            for source, dest in self.graph.edges(action_name):
                if dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.conflict(deps=[action,
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif not len(self.ancestors[source]) == len(self.ancestors[dest]) and not len(self.descendants[source]) == len(self.descendants[dest]):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            for neighbour in self.current[step].neighbors(node):
                                to_explore.append(neighbour)
                elif (set(self.graph.neighbors(dest)) & (self.ancestors[source] | {source})
                      and (source, dest) not in self.propagated):
                    self.propagate(
                        e=z3.Not(self.encoder.get_action_var(dest, step)),
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated.add((source, dest))
                    self.propagated.add((dest, source))
                else:
                    s = set(dest)
                    for node in self.graph.neighbors(dest):
                        s |= set(self.graph.neighbors(node))
                    for n in s & (self.ancestors[source] | {source}):
                        self.propagate(e=z3.Or(
                            z3.Not(self.encoder.get_action_var(dest, step)),
                            z3.Not(self.encoder.get_action_var(n, step)),
                            z3.Not(action)
                        ), ids=[], eqs=[])
                        self.propagated.add((n, dest))
                        self.propagated.add((dest, n))
