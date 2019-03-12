import inspect

from pyreto.compat import builtins


class Scope(object):
    
    def __init__(self, depth=0, **namespace):
        frame = inspect.currentframe()
        for _ in range(depth+1):
            frame = frame.f_back
        self.frame = frame
        self.namespace = namespace

    def __getitem__(self, key):
        if key in self.namespace:
            return self.namespace[key]
        frame = self.frame
        while frame:
            if key in frame.f_locals:
                return frame.f_locals[key]
            frame = frame.f_back
        if key in self.frame.f_globals:
            return self.frame.f_globals[key]
        if hasattr(builtins, key):
            return getattr(builtins, key)
        raise KeyError(key)

    def evaluate(self, token):
        try:
            return str(eval(token, {}, self))
        except SyntaxError as error:
            index = error.offset - 1
        if token[index] in ':!':
            token, formatting = token[:index], '{' + token[index:] + '}'
            return formatting.format(eval(token, {}, self))
