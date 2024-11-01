import networkx as nx
import z3
from networkx import NetworkXNoCycle

from pypmt.utilities import log


class ExistsBasicUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e
        self.add_final(lambda : self._final())
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []
        # self.numbers = {a: i for i, a in enumerate(self.graph)}

    def push(self):
        log("push",1)
        new = []
        for graph in self.current:
            new.append(graph.copy())
            if len(graph.nodes) == 2 and len(graph.edges) == 2:
                print("H")
        self.stack.append(new)

    def pop(self, n):
        log("pop", 1)
        for _ in range(n):
            self.current = self.stack.pop()

    def _final(self):
        for graph in self.current:
            if len(list(nx.simple_cycles(graph))) > 0:
                print("FINISHED WITH CYCLE")
        for s in self.stack:
            for graph in s:
                if len(list(nx.simple_cycles(graph))) > 0:
                    print("FINISHED WITH CYCLE")

    def _fixed(self, action, value):

        if value:
            log("fixed start", 1)
            actions = str(action).split('_')
            step = int(actions[-1])

            action_name = '_'.join(actions[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            cycles = list(nx.simple_cycles(self.current[step]))
            if len(cycles) > 0:
                print(f"{len(cycles)} cycles found early")
            literals = set()
            self.current[step].add_node(action_name)
            edges = list(self.graph.in_edges(action_name)) + list(self.graph.edges(action_name))

            for a1, a2 in edges:
                if a2 in self.current[step] and a1 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
            try:
                cycle = nx.find_cycle(G=self.current[step], source=action_name)
                if cycle:
                    for a, b in cycle:

                        # if numbers[a] > numbers[b]:
                        literals.add(self.encoder.get_action_var(a, step))
                        literals.add(self.encoder.get_action_var(b, step))
                            # self.current[step].remove_node(a)
                print("here")
            except NetworkXNoCycle:
                if len(list(nx.simple_cycles(self.current[step]))) > 0:
                    print("HERE")
                pass
            if literals:
                log("fixed invalid", 1)
                self.conflict(deps=list(literals), eqs=[])
                # self.current[step].remove_node(action_name)
                cycles = list(nx.simple_cycles(self.current[step]))
                if len(cycles) > 0:
                    print(f"{len(cycles)} cycles found before leaving invalid")
            else:
                log("fixed valid", 1)
                cycles = list(nx.simple_cycles(self.current[step]))
                if len(cycles) > 0:
                    print(f"{len(cycles)} cycles found before leaving valid")
