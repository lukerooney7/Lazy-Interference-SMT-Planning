import networkx as nx
import z3


class ExistsPathUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []

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
            self.current[step].add_node(action_name)
            edges = list(self.graph.out_edges(action_name)) + list(self.graph.in_edges(action_name))
            for source, target in edges:
                if source in self.current[step] and target in self.current[step]:
                    self.current[step].add_edge(source, target)
                    if nx.has_path(self.current[step], target, source):
                        # if not nx.has_path(self.current[step], a2, a1):
                        #     print("missed")
                        literals.add(self.encoder.get_action_var(source, step))
                        literals.add(self.encoder.get_action_var(target, step))
                        self.conflict(deps=list(literals), eqs=[])
                        break
