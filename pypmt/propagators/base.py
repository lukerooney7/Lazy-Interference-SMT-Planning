import z3
from pypmt.utilities import log
from pip._internal.req import constructors


class BaseUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, ctx=None):
        # Need to understand what all of this does!
        z3.UserPropagateBase.__init__(self, s, ctx)
        # self.add_fixed(lambda x, v: self._fixed(x, v))
        # self.add_final(lambda: self._final())
        # self.add_eq(lambda x, y: self._eq(x, y))
        # self.add_created(lambda t: self._created(t))

    # def push(self):
    #     log("Push", 3)
    # #
    # def pop(self, n):
    #     log("Pop", 3)
    # #
    # def _fixed(self, x, v):
    #     log(f'fixed: {x}, := , {v}', 3)
    #
    # def _fixed_trail(selfs):
    #     log("fixed trail", 3)
    #
    # def _created(self, t):
    #     log(f'created: {t}', 3)
    #
    # def _eq(self, x, y):
    #     log(f'{x} = {y}', 3)
    #
    # def _final(self):
    #     log("Final", 3)
