import networkx
import networkx as nx
import z3
# from matplotlib import pyplot as plt
import copy

from pypmt.utilities import log


class LazyUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None, e=None):
        # Need to understand what all of this does!
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.trail = []  # Tracks variables/states as they are fixed, maintains state of the solution
        self.lim = []  # Stores limit values, helps backtracking when Z3 undoes changes (conflicts/backtracking)
        self.add_final(lambda: self._final())
        # self.add_eq(lambda x, y: self._eq(x, y))
        # self.add_created(lambda t: self._created(t))
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.first = True
        self.encoder = e
        self.graph = self.encoder.modifier.graph
        self.current = [nx.DiGraph()]
        self.stack = []

    def push(self):
        # log("Push", 5)
        # print("push")
        self.stack.append(copy.deepcopy(self.current))

    def pop(self, n):
        # log(f'pop {n} times', 3)
        for _ in range(n):
            self.current = self.stack.pop()

    def _final(self):
        # plt.figure(figsize=(20, 20))
        # nx.draw(self.current, node_size=1500, font_size=10, with_labels=True)
        # plt.show()
        log("Final", 5)

    def _fixed(self, action, value):
        # log(f'fixed: {action} :=  {value}', 3)
        if value:
            step = int(str(action).split('_')[-1])
            action_name = '_'.join(str(action).split('_')[:-1])
            while step >= len(self.current):
                self.current.append(nx.DiGraph())
            literals = []
            self.current[step].add_node(action_name)
            for e in self.graph.edges(action_name):
                a1, a2 = e
                if a2 in self.current[step] and a1 in self.current[step]:
                    self.current[step].add_edge(a1, a2)
                    literals.append(self.encoder.get_action_var(a1, step))
                    literals.append(self.encoder.get_action_var(a2, step))
            # plt.figure(figsize=(20, 20))
            # for i in self.current:
            #     if i:
            #         nx.draw(i, node_size=1500, font_size=10, with_labels=True)
            #         plt.show()
            if literals:
                literals.append(action)
                self.conflict(deps=literals, eqs=[])
            # else:
            #     plt.figure(figsize=(20, 20))
            #     nx.draw(self.current, node_size=1500, font_size=10, with_labels=True)
