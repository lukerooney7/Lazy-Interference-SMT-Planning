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
        self.false = set()
        self.falseStack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.falseStack.append(self.false.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.false = self.falseStack.pop()

    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            literals = set()
            new_mutexes = set()
            for source, dest in list(self.graph.edges(action_name)):
                if dest in self.current[step]:
                    literals.add(self.encoder.get_action_var(dest, step))
                    for i in range(0, len(self.current)):
                        new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                      self.encoder.get_action_var(dest, i))))
                    break
                else:
                    if dest not in self.nots[step]:
                        self.nots[step][dest] = z3.Not(self.encoder.get_action_var(dest, step))
                    if dest not in self.false:
                        self.propagate(e=self.nots[step][dest], ids=[], eqs=[])
            if not literals:
                for source, dest in list(self.graph.in_edges(action_name)):
                    if source in self.current[step]:
                        literals.add(self.encoder.get_action_var(source, step))
                        for i in range(0, len(self.current)):
                            new_mutexes.add(z3.Not(z3.And(self.encoder.get_action_var(source, i),
                                                          self.encoder.get_action_var(dest, i))))
                        break
                    else:
                        if source not in self.nots[step]:
                            self.nots[step][source] = z3.Not(self.encoder.get_action_var(source, step))
                        if source not in self.false:s
                            self.propagate(e=self.nots[step][source], ids=[], eqs=[])
            if literals:
                self.solver.add(new_mutexes)
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
            else:
                self.current[step].add(action_name)