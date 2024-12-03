import z3


class ForallCodePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]  # Use a set instead of a NetworkX graph
        self.stack = []
        self.consistent = True

    def push(self):
        self.stack.append([graph.copy() for graph in self.current])

    def pop(self, n):
        if n > 0:
            self.current = self.stack[-n]
            del self.stack[-n:]
        self.consistent = True
    def _fixed(self, action, value):
        if value and self.consistent:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            literals = set()
            self.current[step].add(action_name)
            # Checking and adding out nodes
            for dest in self.current[step] & set(self.graph.neighbors(action_name)):
                literals.add(self.encoder.get_action_var(dest, step))
                self.consistent = False
            # Checking and adding in nodes
            for source in self.current[step] & set(self.graph.predecessors(action_name)):
                literals.add(self.encoder.get_action_var(source, step))
                self.consistent = False
            # Check if anything has caused interference
            if literals:
                literals.add(action)  # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])
