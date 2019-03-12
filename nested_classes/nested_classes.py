import sys

from pyreto import export


@export
class nested_classes(object):

    def __init__(self, cls=None):
        if cls is not None:
            raise SyntaxError("nested_classes wasn't invoked (did you forget the parenthesis in '@nested_classes()'?)")
        self.old = sys.gettrace()
        sys.settrace(self.tracer)

    def __call__(self, cls):
        sys.settrace(self.old)
        return cls

    def tracer(self, frame, event, arg):
        if event == 'call':
            for name in frame.f_back.f_locals:
                if name not in frame.f_locals:
                    frame.f_locals[name] = frame.f_back.f_locals[name]
        return self.tracer
