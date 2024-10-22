import networkx as nx
import z3
from pypmt.utilities import log


class ForallNoGraphUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
        self.stack = []

    def push(self):
        self.stack.append([graph.copy() for graph in self.current])

    def pop(self, n):
        if n > 0:
            self.current = self.stack[-n]  # Update `self.current` to the nth-to-last element
            del self.stack[-n:]

    def _fixed(self, action, value):
        if value:
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            literals = set()
            self.current[step].add(action_name)
            edges = list(self.graph.edges(action_name)) + list(self.graph.in_edges(action_name))
            current_step = self.current[step]
            for a1, a2 in edges:
                if a2 in current_step and a1 in current_step:
                    literals.add(self.encoder.get_action_var(a1, step))
                    literals.add(self.encoder.get_action_var(a2, step))

            if literals:
                self.conflict(deps=list(literals), eqs=[])