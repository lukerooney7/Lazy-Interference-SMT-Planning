import networkx as nx
import z3


def split_action(action):
    actions = str(action).split('_')
    return int(actions[-1]), '_'.join(actions[:-1])


class ForallDecidePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_decide(lambda t, idx, phase: self._decide(t, idx, phase))
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
        self.stack = []
        self.mutexes = 0
        self.name = "forall-lazy"

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()

    def _decide(self, t, idx, phase):
        if phase != 1:
            return
        step, action_name = split_action(t)
        if step >= len(self.current):
            self.next_split(t=t, idx=idx, phase=1)
            return
        # Checking if this action has an edge to any that are already True
        if set(self.graph.successors(action_name)) | set(self.graph.predecessors(action_name)) & self.current[step]:
            self.next_split(t=t, idx=idx, phase=-1)
        else:
            self.next_split(t=t, idx=idx, phase=1)

    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            step, action_name = split_action(action)
            while step >= len(self.current):
                self.current.append(set())
            self.current[step].add(action_name)
            literals = set()
            for source, dest in list(self.graph.edges(action_name)):
                if dest in self.current[step]:
                    literals.add(self.encoder.get_action_var(dest, step))
                    break
            if not literals:
                for source, dest in list(self.graph.in_edges(action_name)):
                    if source in self.current[step]:
                        literals.add(self.encoder.get_action_var(source, step))
                        break
            if literals:
                literals.add(action)
                self.conflict(deps=list(literals), eqs=[])
