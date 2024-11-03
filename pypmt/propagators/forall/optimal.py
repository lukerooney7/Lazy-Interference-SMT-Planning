import z3


class ForallOptimalUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
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
                self.current.append(set())
            literals = set()
            disallowed_actions = set()
            new_mutexes = set()
            for a1, a2 in list(self.graph.edges(action_name)):
                if a2 in self.current[step]:
                    literals.add(self.encoder.get_action_var(a2, step))
                    for i in range(0, len(self.current)):
                        new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(a1, i),
                                                      self.encoder.get_action_var(a2, i))))
                    break
                else:
                    disallowed_actions.add(self.encoder.get_action_var(a2, step))
            if not literals:
                for a1, a2 in list(self.graph.in_edges(action_name)):
                    if a1 in self.current[step]:
                        literals.add(self.encoder.get_action_var(a1, step))
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(a1, i),
                                                          self.encoder.get_action_var(a2, i))))
                        break
                    else:
                        disallowed_actions.add(self.encoder.get_action_var(a1, step))
            if literals:
                self.solver.add(new_mutexes)
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
            else:
                self.current[step].add(action_name)
                clause = set()
                for a in disallowed_actions:
                    clause.add(z3.Not(a))
                self.propagate(e=z3.And(clause), ids=[], eqs=[])