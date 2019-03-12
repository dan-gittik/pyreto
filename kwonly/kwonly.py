import functools

from pyreto import export, undefined
from pyreto.call import Call
from pyreto.dictionary import Dictionary


@export
def kwonly(**defaults):
    defaults = Dictionary(defaults)
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            call = Call(function, *args, **kwargs)
            names = [name for name, value in call.arguments.items()
                              if name in defaults and value is not undefined and name not in kwargs]
            if names:
                raise TypeError('{name}() requires arguments to be passed by keyword: {args}'.format(
                    name = call.name,
                    args = ', '.join(repr(name) for name in names),
                ))
            for name, value in defaults.items():
                if name not in call.arguments:
                    call.kwargs[name] = value
                elif call.arguments[name] is undefined:
                    call.arguments[name] = value
            return call()
        wrapper.defaults = defaults
        return wrapper
    return decorator
