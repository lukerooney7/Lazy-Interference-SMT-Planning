from collections import defaultdict

import networkx as nx
import z3


class ExistsPropPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.ancestors = [{}]
        self.descendants = [{}]
        self.trail_current = []
        self.trail_ancestors = []
        self.trail_descendants = []
        self.levels = []
        self.consistent = True
        self.propagated = defaultdict(set)
        self.nots = defaultdict(dict)

    def push(self):
        self.levels.append((len(self.trail_current), len(self.trail_ancestors), len(self.trail_descendants)))

    def pop(self, n):
        self.consistent = True
        for _ in range(n):
            if self.levels:
                cur_idx, anc_idx, des_idx = self.levels.pop()
                # Undo changes for `current`
                while len(self.trail_current) > cur_idx:
                    step, action = self.trail_current.pop()
                    self.current[step].remove_node(action)
                # Undo changes for `ancestors`
                while len(self.trail_ancestors) > anc_idx:
                    step, action, ancestor = self.trail_ancestors.pop()
                    self.ancestors[step][action].discard(ancestor)
                while len(self.trail_descendants) > anc_idx:
                    step, action, descendant = self.trail_descendants.pop()
                    self.ancestors[step][action].discard(descendant)

    def incremental_cycle(self, step, source, dest):
        self.current[step].add_edge(source, dest)
        to_explore = [dest]
        while len(to_explore) > 0:
            node = to_explore.pop()
            if source == node or node in self.ancestors[step][source]:
                self.conflict(deps=[self.encoder.get_action_var(source, step),
                                    self.encoder.get_action_var(dest, step)], eqs=[])
                self.consistent = False
                break
            elif source in self.ancestors[step][node]:
                pass
            else:
                self.ancestors[step][node].add(source)
                self.trail_ancestors.append((step, node, source))
                self.descendants[step][source].add(node)
                self.trail_descendants.append((step, source, node))
                for node, neighbour in self.current[step].edges:
                    to_explore.append(neighbour)

    def _fixed(self, action, value):
        if value and self.consistent:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            if step >= len(self.current):
                while step >= len(self.current):
                    self.current.append(nx.DiGraph())
                    self.ancestors.append({})
                    self.descendants.append({})
                self.current[step].add_node(action_name)
                if action_name not in self.ancestors[step]:
                    # Initialise ancestors/descendants if new node
                    self.ancestors[step][action_name] = set()
                    self.descendants[step][action_name] = set()
                self.trail_current.append((step, action_name))
                return
            self.current[step].add_node(action_name)
            self.trail_current.append((step, action_name))
            if action_name not in self.ancestors[step]:
                # Initialise ancestors/descendants if new node
                self.ancestors[step][action_name] = set()
                self.descendants[step][action_name] = set()
            # Incremental Cycle Detection
            for source, _ in self.graph.in_edges(action_name):
                if source in self.current[step]:
                    self.incremental_cycle(step, source, action_name)
                elif (set(self.graph.predecessors(source)) & (self.descendants[step][action_name] | {action_name})
                    and (source, action_name) not in self.propagated[step]):
                    if source not in self.nots[step]:
                        self.nots[step][source] = z3.Not(self.encoder.get_action_var(source, step))
                    self.propagate(
                        e=self.nots[step][source],
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated[step].add((source, action_name))

            for _, dest in self.graph.edges(action_name):
                if dest in self.current[step]:
                    self.incremental_cycle(step, action_name, dest)
                elif (set(self.graph.neighbors(dest)) & (self.ancestors[step][action_name] | {action_name})
                      and (action_name, dest) not in self.propagated[step]):
                    if dest not in self.nots[step]:
                        self.nots[step][dest] = z3.Not(self.encoder.get_action_var(dest, step))
                    self.propagate(
                        e=self.nots[step][dest],
                        ids=[action, action],
                        eqs=[]
                    )
                    self.propagated[step].add((action_name, dest))
