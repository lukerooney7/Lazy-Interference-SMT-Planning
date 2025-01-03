import networkx as nx
import z3
from collections import defaultdict

class TestUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = defaultdict(nx.DiGraph)
        self.ancestors = {}
        self.descendants = {}
        self.ancestorsStack = []
        self.descendantsStack = []
        self.stack = []
        self.nots = defaultdict(dict)

    def push(self):
        new = defaultdict(nx.DiGraph)
        for k, v in self.current.items():
            new[k] = v.copy()
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
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif (len(self.ancestors[source]) != len(self.ancestors[dest])
                              and len(self.descendants[source]) != len(self.descendants[dest])):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            to_explore.extend(neighbour for _, neighbour in self.current[step].edges)
                elif (set(self.graph.predecessors(source)) & self.descendants[dest]
                      or source in set(self.graph.neighbors(dest))):
                    if source in self.nots[step]:
                        n = self.nots[step][source]
                    else:
                        n = z3.Not(self.encoder.get_action_var(source, step))
                        self.nots[step][source] = n
                    self.propagate(e=n, ids=[], eqs=[])
            # Incremental cycle detection for out edges
            for source, dest in self.graph.edges(action_name):
                if dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[source]:
                            self.conflict(deps=[self.encoder.get_action_var(source, step),
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            break
                        elif source in self.ancestors[node]:
                            pass
                        elif (len(self.ancestors[source]) != len(self.ancestors[dest])
                              and len(self.descendants[source]) != len(self.descendants[dest])):
                            pass
                        else:
                            self.ancestors[node].add(source)
                            self.descendants[source].add(node)
                            to_explore.extend(neighbour for _, neighbour in self.current[step].edges)
                elif (set(self.graph.neighbors(dest)) & self.ancestors[source]
                      or source in set(self.graph.neighbors(dest))):
                    if dest in self.nots[step]:
                        n = self.nots[step][dest]
                    else:
                        n = z3.Not(self.encoder.get_action_var(dest, step))
                        self.nots[step][dest] = n
                    self.propagate(e=n, ids=[], eqs=[])
