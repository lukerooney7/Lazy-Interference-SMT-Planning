import networkx as nx
import z3


class ForallPropIdPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []
        self.propagated = set()
        self.propagatedStack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.propagatedStack.append(self.propagated.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.propagated = self.propagatedStack.pop()

    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = set()
            self.current[step].add_node(action_name)
            # Check out edges
            for _, dest in self.graph.edges(action_name):
                if dest in self.current[step]:
                    literals.add(self.encoder.get_action_var(dest, step))
                elif (dest, action_name) not in self.propagated:
                    # Neighbouring actions must be false
                    self.propagate(
                        e=z3.Not(self.encoder.get_action_var(dest, step)),
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated.add((dest, action_name))
                    self.propagated.add((action_name, dest))
            # Check in edges
            for source, _ in self.graph.in_edges(action_name):
                if source in self.current[step]:
                    literals.add(self.encoder.get_action_var(source, step))
                elif (source, action_name) not in self.propagated:
                    # Neighbouring actions must be false
                    self.propagate(
                        e=z3.Not(self.encoder.get_action_var(source, step)),
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated.add((source, action_name))
                    self.propagated.add((action_name, source))
            # Check if anything has caused interference
            if literals:
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
