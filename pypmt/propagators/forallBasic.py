import networkx as nx
import z3

class ForallBasicUserPropagator(z3.UserPropagateBase):
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

    def _final(self):
        for graph in self.current:
            if len(list(nx.simple_cycles(graph))) > 0:
                print("FINISHED WITH edges")
        for s in self.stack:
            for graph in s:
                if len(list(nx.simple_cycles(graph))) > 0:
                    print("FINISHED WITH edges")

    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            if len(self.current[step].edges) > 0:
                print(f'{len(self.current[step].edges)} edges found at start')
            self.current[step].add_node(action_name)
            for a1, a2 in list(self.graph.edges(action_name)):
                action_2 = self.encoder.get_action_var(a2, step)
                if a2 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
                    literals.add(action_2)
                    # self.conflict(deps=[action_2, action], eqs=[])
            for a1, a2 in list(self.graph.in_edges(action_name)):
                action_1 = self.encoder.get_action_var(a1, step)
                if a1 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
                    literals.add(action_1)
                    # self.conflict(deps=list([action_1, action]), eqs=[])
            if literals:
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])