from pyreto import export

import sys


@export
class ordered(object):

    standard_names = None

    def __init__(self, cls=None):
        if cls is not None:
            raise SyntaxError("ordered wasn't invoked (did you forget the parenthesis in '@ordered()'?)")
        self.old = sys.gettrace()
        sys.settrace(self.tracer)

    def __call__(self, cls):
        cls._order = self.order
        return cls

    def tracer(self, frame, event, arg):
        names = frame.f_code.co_names
        if self.standard_names is None:
            type(self).standard_names = names
        self.order = tuple(name for name in names if name not in self.standard_names)
        sys.settrace(self.old)


# Invoke ordered on an empty class to get an initial reading on any standard names.
@ordered()
class _(object):
    pass
