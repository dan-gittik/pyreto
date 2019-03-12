import functools

from pyreto import export, undefined
from pyreto.call import Call
from pyreto.dictionary import Dictionary


@export
def defaults(**defaults):
    defaults = Dictionary(defaults)
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            call = Call(function, *args, **kwargs)
            for name, value in call.arguments.items():
                if name in defaults and value is undefined or value is None:
                    call.arguments[name] = defaults[name]
            return call()
        wrapper.defaults = defaults
        return wrapper
    return decorator
