import networkx as nx
import z3


class ExistsIncrementalCyclePropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [set()]
        self.ancestors = {}
        self.descendants = {}
        self.stackA = []
        self.stackD = []
        self.stack = []
        self.consistent = True

    def push(self):
        new = []
        for graph in self.current:
            new.append(graph.copy())
        self.stack.append(new)
        self.stackA.append(self.ancestors.copy())
        self.stackD.append(self.descendants.copy())

    def pop(self, n):
        for _ in range(n):
            self.current = self.stack.pop()
            self.ancestors = self.stackA.pop()
            self.descendants = self.stackD.pop()
        self.consistent = True


    def incremental_cycle(self, source, dest, step):
        to_explore = [dest] # Initially only check the connected node (this will be updated)
        # Search connected nodes for cycles
        while len(to_explore) > 0:
            node = to_explore.pop()
            # Check if node connects back to existing path (makes cycle)
            if source == node or node in self.ancestors[source]:
                self.consistent = False
                # Throw conflict on edge if cycle found
                self.conflict(deps=[self.encoder.get_action_var(source, step),
                                    self.encoder.get_action_var(dest, step)], eqs=[])
            elif source in self.ancestors[node]:
                pass
            # Check if S*-equivalent
            elif (not len(self.ancestors[source]) == len(self.ancestors[node])
                  and not len(self.descendants[source]) == len(self.descendants[node])):
                pass
            else:
                self.ancestors[node].add(source)
                self.descendants[source].add(node)
                for neighbour in self.graph.neighbors(node):
                    if neighbour in self.current[step]:
                        to_explore.append(neighbour)

    def _fixed(self, action, value):
        if value and self.consistent:
            # Parse action name and step
            actions = str(action).split('_')
            step = int(actions[-1])
            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(set())
            self.current[step].add(action_name)
            if action_name not in self.ancestors:
                # Initialise ancestors/descendants if new node
                self.ancestors[action_name] = set()
                self.descendants[action_name] = set()
            # Incremental Cycle Detection for Inwards edges
            for source, _ in self.graph.in_edges(action_name):
                if not self.consistent:
                    return
                if source in self.current[step]:
                    self.incremental_cycle(source, action_name, step)
            # Incremental Cycle Detection for outwards edges
            for _, dest in set(self.graph.edges(action_name)):
                if not self.consistent:
                    return
                if dest in self.current[step]:
                    self.incremental_cycle(action_name, dest, step)
