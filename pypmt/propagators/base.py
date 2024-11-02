import z3
from pypmt.utilities import log
from pip._internal.req import constructors


class BaseUserPropagator(z3.UserPropagateBase):
    def __init__(self, s, e, ctx=None):
        z3.UserPropagateBase.__init__(self, s, ctx)
        self.add_fixed(lambda x, v: self._fixed(x, v))
        self.encoder = e

    def push(self):
        pass

    def pop(self, n):
        pass

    def _fixed(self, x, v):
        pass
