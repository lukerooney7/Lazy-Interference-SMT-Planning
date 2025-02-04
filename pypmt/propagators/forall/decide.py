import z3


def split_action(action):
    actions = str(action).split('_')
    return int(actions[-1]), '_'.join(actions[:-1])


class ForallDecidePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.name = "forall-decide"
        self.mutexes = 0
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.add_decide(lambda t, idx, phase: self._decide(t, idx))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]  # Use a set instead of a NetworkX graph
        self.trail = []  # Trail to record changes
        self.levels = []
        self.consistent = True
        self.neighbours = {}

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

    def _decide(self, t, idx):
        step, action_name = split_action(t)
        if step >= len(self.current) or not self.current[step]:
            # A new step or empty step will never cause interference
            self.next_split(t=t, idx=idx, phase=1)
            return
        # Caching neighbours
        if action_name not in self.neighbours:
            self.neighbours[action_name] = set(self.graph.successors(action_name)) | set(
                self.graph.predecessors(action_name))
        # Checking if this action has an edge to any that are already True via set-intersect
        if self.neighbours[action_name] & self.current[step]:
            self.next_split(t=t, idx=idx, phase=-1) # False if will cause interference
        else:
            self.next_split(t=t, idx=idx, phase=1) # True otherwise

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
                self.mutexes += 1
            # Checking and adding in nodes using set intersection
            for source in self.current[step] & set(self.graph.predecessors(action_name)):
                literals.add(self.encoder.get_action_var(source, step))
                self.consistent = False
                self.mutexes += 1
            # Check if anything has caused interference
            if literals:
                literals.add(action)  # New action itself is only added once
                self.conflict(deps=list(literals), eqs=[])
