import networkx as nx
import z3


class ExistsIterativeCycleUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.A = {}
        self.stackA = []
        self.stack = []
        self.numbers = {a: i for i, a in enumerate(self.graph)}

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.stackA.append(self.A.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.A = self.stackA.pop()


    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            self.current[step].add_node(action_name)
            edges = list(self.graph.in_edges(action_name))
            edges[0:0] = list(self.graph.edges(action_name))

            for n in nx.nodes(self.current[step]):
                if n not in self.A:
                    self.A[n] = set()

            for u, v in edges:
                if u in self.current[step] and v in self.current[step]:
                    self.current[step].add_edge(u, v)
                    to_explore = [v]
                    cycle = False
                    while len(to_explore) > 0:
                        w = to_explore.pop()
                        if u == w:
                            cycle = True
                            break
                        if w in self.A[u]:
                            cycle = True
                            break
                        elif u in self.A[w]:
                            pass
                        elif (not len(nx.ancestors(self.current[step], u)) == len(nx.ancestors(self.current[step], v))
                              and len(nx.descendants(self.current[step], u)) == len(nx.descendants(self.current[step], v))):
                            pass
                        else:
                            self.A[w].add(u)
                            for w, z in self.current[step].edges:
                                to_explore.append(z)
                    if cycle:
                        literals.add(self.encoder.get_action_var(u, step))
                        literals.add(self.encoder.get_action_var(v, step))
                        if not len(list(nx.simple_cycles(self.current[step]))) > 0:
                            print("HERE")

                    # elif len(list(nx.simple_cycles(self.current[step]))) > 0:
                    #     for c in nx.simple_cycles(self.current[step]):
                    #         for n in c:
                    #             literals.add(self.encoder.get_action_var(n, step))
                    #     self.conflict(deps=list(literals), eqs=[])
