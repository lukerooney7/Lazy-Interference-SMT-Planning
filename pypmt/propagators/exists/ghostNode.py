import networkx as nx
import z3


class ExistsGhostNodeUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.A = {}
        self.D = {}
        self.stackA = []
        self.stackD = []
        self.stack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
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
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            self.current[step].add_node(action_name)
            if action_name not in self.A:
                self.A[action_name] = set()
                self.D[action_name] = set()
            for u, v in list(self.graph.in_edges(action_name)):
                if u in self.current[step] and v in self.current[step]:
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
                else:
                    clause = set()
                    for node in self.graph.predecessors(u):
                        if node in self.D[v]:
                            clause.add(z3.Not(self.encoder.get_action_var(u, step)))
                            break
                    self.propagate(e=z3.And(clause), ids=[], eqs=[])

            for u, v in list(self.graph.edges(action_name)):
                if u in self.current[step] and v in self.current[step]:
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
                else:
                    clause = set()
                    for node in self.graph.neighbors(v):
                        if node in self.A[u]:
                            clause.add(z3.Not(self.encoder.get_action_var(v, step)))
                            break
                    self.propagate(e=z3.And(clause), ids=[], eqs=[])

