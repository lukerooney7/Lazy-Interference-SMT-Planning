import networkx as nx
import z3
from collections import defaultdict

class ExistsOptimalUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = defaultdict(nx.DiGraph)
        self.A = {}
        self.D = {}
        self.stackA = []
        self.stackD = []
        self.stack = []

    def push(self):
        new = defaultdict(nx.DiGraph)
        for k, v in self.current.items():
            new[k] = v.copy()
        self.stack.append(new)
        self.stackA.append(self.A.copy())
        self.stackD.append(self.D.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.A = self.stackA.pop()
            self.D = self.stackD.pop()

    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            self.current[step].add_node(action_name)
            if action_name not in self.A:
                self.A[action_name] = set()
                self.D[action_name] = set()
            for u, v in self.graph.in_edges(action_name):
                if u in self.current[step]:
                    self.current[step].add_edge(u, v)
                    to_explore = [v]
                    while len(to_explore) > 0:
                        w = to_explore.pop()
                        if u == w or w in self.A[u]:
                            self.conflict(deps=[self.encoder.get_action_var(u, step),
                                                self.encoder.get_action_var(v, step)], eqs=[])
                            break
                        elif u in self.A[w]:
                            pass
                        elif not len(self.A[u]) == len(self.A[v]) and not len(self.D[u]) == len(self.D[v]):
                            pass
                        else:
                            self.A[w].add(u)
                            self.D[u].add(w)
                            for w, z in self.current[step].edges:
                                to_explore.append(z)
                elif set(self.graph.predecessors(u)) & self.D[v]:
                    self.propagate(e=z3.Not(self.encoder.get_action_var(u, step)), ids=[], eqs=[])

            for u, v in self.graph.edges(action_name):
                if v in self.current[step]:
                    self.current[step].add_edge(u, v)
                    to_explore = [v]
                    while len(to_explore) > 0:
                        w = to_explore.pop()
                        if u == w or w in self.A[u]:
                            self.conflict(deps=[self.encoder.get_action_var(u, step),
                                                self.encoder.get_action_var(v, step)], eqs=[])
                            break
                        elif u in self.A[w]:
                            pass
                        elif not len(self.A[u]) == len(self.A[v]) and not len(self.D[u]) == len(self.D[v]):
                            pass
                        else:
                            self.A[w].add(u)
                            self.D[u].add(w)
                            for w, z in self.current[step].edges:
                                to_explore.append(z)
                elif set(self.graph.neighbors(v)) & self.A[u]:
                    self.propagate(e=z3.Not(self.encoder.get_action_var(v, step)), ids=[], eqs=[])
