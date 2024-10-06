import z3
from networkx.utils import UnionFind
from pip._internal.req import constructors


class BaseUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None):
        # Need to understand what all of this does!
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.trail = []
        self.lim = []
        # self.add_fixed(lambda x, v: self._fixed(x, v))
        # self.add_final(lambda: self._final())
        # self.add_eq(lambda x, y: self._eq(x, y))
        # self.add_created(lambda t: self._created(t))
        self.first = True

    # def push(self):
    #     print("push")
    #
    # def pop(self, n):
        # print("pop")

    # def _fixed(self, x, v):
        # print("fixed: ", x, " := ", v)

    # def _fixed_trail(selfs):
        # print("fixed trail")

    # def _created(self, t):
        # print("Created", t)

    # def _eq(self, x, y):
        # print(x, " = ", y)

    # def _final(self):
        # print("Final")
