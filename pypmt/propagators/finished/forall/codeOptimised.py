import z3


class ForallCodePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]  # Use a set instead of a NetworkX graph
        self.trail = []  # Trail to record changes
        self.levels = []
        self.consistent = True

    def push(self):
        self.levels.append(len(self.trail))

    def pop(self, n):
        for _ in range(n):
            if self.levels:
                # Find the start of the current decision level
                level_start = self.levels.pop()
                # Undo all changes recorded after this level
                while len(self.trail) > level_start:
                    step, action = self.trail.pop()
                    self.current[step].remove(action)
        self.consistent = True
    def _fixed(self, action, value):
        if value and self.consistent:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            if step >= len(self.current):
                while step >= len(self.current):
                    self.current.append(set())
                self.current[step].add(action_name)
                self.trail.append((step, action_name))
                # There cannot be any interference: no other actions in step are True
                return
            literals = set()
            self.trail.append((step, action_name))
            self.current[step].add(action_name)
            for dest in self.current[step] & set(self.graph.neighbors(action_name)):
                literals.add(self.encoder.get_action_var(dest, step))
                self.consistent = False
            # Checking and adding in nodes using set intersection
            for source in self.current[step] & set(self.graph.predecessors(action_name)):
                literals.add(self.encoder.get_action_var(source, step))
                self.consistent = False
            # Check if anything has caused interference
            if literals:
                literals.add(action)  # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])
