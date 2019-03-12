import functools
import sys

from pyreto import export
from pyreto.call import Call
from pyreto.dictionary import Dictionary


@export
def parametrized_decorator(**defaults):
    defaults = Dictionary(defaults)
    def decorator_wrapper(decorator):
        @functools.wraps(decorator)
        def wrapped_decorator(*args, **kwargs):
            if len(args) == 1 and callable(args[0]):
                return decorator(args[0], **defaults)
            def deferred_decorator(function):
                call = Call(decorator, **defaults)
                call.amend(function, *args, **kwargs)
                return call()
            return deferred_decorator
        wrapped_decorator.defaults = defaults
        return wrapped_decorator
    return decorator_wrapper
