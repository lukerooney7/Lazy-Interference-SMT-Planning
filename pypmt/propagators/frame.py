from collections import defaultdict

import networkx as nx
import z3


class FramePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.mutexes = 0
        self.false = [set()]
        self.clauses = set()
        self.name = "forall-frame"
        self.trail = []
        self.levels = []


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
                    self.false[step].remove(action)


    def _fixed(self, action, value):
        if value:
            return

        action_str = str(action)

        if ':' in action_str:
            variables = action_str.split(':')
            key, step = self.extract_key_step(variables[0])
            or_actions = (
                    self.encoder.frame_add[key] +
                    self.encoder.frame_del[key] +
                    self.encoder.frame_num[key]
            )
            self.ensure_false_size(step)
            if not or_actions:
                self.conflict(deps=[action], eqs=[])
                return
            false = [self.encoder.up_actions_to_z3[a][step] for a in or_actions if a in self.false[step]]

            if len(false) == len(or_actions):
                false.append(action)
                self.conflict(deps=false, eqs=[])
            else:
                false.append(action)
                false.append(action)
                true = [self.encoder.up_actions_to_z3[a][step] for a in or_actions if a not in self.false[step]]
                self.propagate(e=z3.Or(true), ids=false)
            return

        action_name, step = self.extract_key_step(action_str)
        self.ensure_false_size(step)
        self.false[step].add(action_name)
        self.trail.append((step, action_name))

    def extract_key_step(self, action_str):
        parts = action_str.split('_')
        step = int(parts[-1])
        key = '_'.join(parts[:-1])
        return key, step

    def ensure_false_size(self, step):
        while step >= len(self.false):
            self.false.append(set())

