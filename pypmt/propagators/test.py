from collections import defaultdict
import z3


class TestPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
        self.stack = []
        self.nots = defaultdict(dict)
        self.consistent = True

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
        self.consistent = True
    def _fixed(self, action, value):
        if value and self.consistent:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            literals = set()
            new_mutexes = set()
            for source, dest in list(self.graph.edges(action_name)):
                if not self.consistent:
                    break
                if dest in self.current[step]:

                    literals.add(self.encoder.get_action_var(dest, step))
                    self.consistent = False
                    for i in range(0, len(self.current)):
                        new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                      self.encoder.get_action_var(dest, i))))
                    break
                else:
                    if dest not in self.nots[step]:
                        self.nots[step][dest] = z3.Not(self.encoder.get_action_var(dest, step))
                    self.propagate(
                        e=self.nots[step][dest],
                        ids=[action],
                        eqs=[(action, self.encoder.get_action_var(dest, step))]
                    )
            if not literals:
                for source, dest in list(self.graph.in_edges(action_name)):
                    if not self.consistent:
                        break
                    if source in self.current[step]:
                        literals.add(self.encoder.get_action_var(source, step))
                        self.consistent = False
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                          self.encoder.get_action_var(dest, i))))
                        break
                    else:
                        if source not in self.nots[step]:
                            self.nots[step][source] = z3.Not(self.encoder.get_action_var(source, step))
                        self.propagate(
                            e=self.nots[step][source],
                            ids=[action],
                            eqs=[(action, self.encoder.get_action_var(source, step))]
                        )
            if literals:
                self.solver.add(new_mutexes)
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
            else:
                self.current[step].add(action_name)