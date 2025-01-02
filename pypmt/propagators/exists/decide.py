import networkx as nx
import z3
from networkx import NetworkXNoCycle


def split_action(action):
    actions = str(action).split('_')
    return int(actions[-1]), '_'.join(actions[:-1])


class ExistsDecidePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.add_decide(lambda t, idx, phase: self._decide(t, idx, phase))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.ancestors = [{}]
        self.descendants = [{}]
        self.stackA = []
        self.stackD = []
        self.stack = []

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        new2 = []
        for step in self.ancestors:
            new2.append(step)
        self.stackA.append(new2)
        new3 = []
        for step in self.descendants:
            new3.append(step)
        self.stackD.append(new3)

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.stackA.pop()
            self.descendants = self.stackD.pop()

    def _decide(self, t, idx, phase):
        if phase != 1:
            return
        step, action_name = split_action(t)
        if step >= len(self.current):
            self.next_split(t=t, idx=idx, phase=1)
            return
        for a in set(self.graph.predecessors(action_name)) & set(self.current[step].nodes):
            if self.ancestors[step][a] & (set(self.graph.successors(action_name)) & set(self.current[step].nodes)):
                self.next_split(t=t, idx=idx, phase=-1)
                return
        for a in set(self.graph.successors(action_name)) & set(self.current[step].nodes):
            if self.descendants[step][a] & (set(self.graph.predecessors(action_name)) & set(self.current[step].nodes)):
                self.next_split(t=t, idx=idx, phase=-1)
                return
        self.next_split(t=t, idx=idx, phase=0)


    def _fixed(self, action, value):
        if value:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
                self.descendants.append({})
                self.ancestors.append({})
            self.current[step].add_node(action_name)
            edges = list(self.graph.in_edges(action_name)) + list(self.graph.edges(action_name))
            if action_name not in self.ancestors[step]:
                # Initialise ancestors/descendants if new node
                self.ancestors[step][action_name] = set()
                self.descendants[step][action_name] = set()
            # Incremental Cycle Detection
            for source, dest in edges:
                if source in self.current[step] and dest in self.current[step]:
                    self.current[step].add_edge(source, dest)
                    self.ancestors[step][dest].add(source)
                    self.descendants[step][source].add(dest)
                    to_explore = [dest]
                    while len(to_explore) > 0:
                        node = to_explore.pop()
                        if source == node or node in self.ancestors[step][source]:
                            self.conflict(deps=[self.encoder.get_action_var(source, step),
                                                self.encoder.get_action_var(dest, step)], eqs=[])
                            break
                        elif source in self.ancestors[step][node]:
                            pass
                        else:
                            self.ancestors[step][node].add(source)
                            self.descendants[step][source].add(node)
                            for src, dest in self.current[step].edges:
                                if src == node:
                                    to_explore.append(dest)
