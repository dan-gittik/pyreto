import sys

from pyreto import export
from pyreto.compat import number_type


@export
class cenum(object):

    standard_names = None

    def __init__(self, cls=None):
        if cls is not None:
            raise SyntaxError("cenum wasn't invoked (did you forget the parenthesis in '@cenum()'?)")
        self.old = sys.gettrace()
        sys.settrace(self.tracer)

    def __call__(self, cls):
        n = 0
        for name in self.names:
            value = getattr(cls, name)
            if isinstance(value, number_type):
                n = value
            setattr(cls, name, n)
            n += 1
        return cls

    def tracer(self, frame, event, arg):
        names = frame.f_code.co_names
        if self.standard_names is None:
            type(self).standard_names = names
        self.names = [name for name in names if name not in self.standard_names]
        for name in self.names:
            frame.f_locals[name] = None
        sys.settrace(self.old)


# Invoke cenum on an empty class to get an initial reading on any standard names.
@cenum()
class _(object):
    pass
