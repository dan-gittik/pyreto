import inspect
import sys


if sys.version_info.major >= 3:

    import builtins

    string_type = str
    binary_type = bytes
    number_type = int

    def getargspec(function):
        spec = inspect.getfullargspec(function)
        return spec.args, spec.varargs, spec.varkw, spec.defaults or [], spec.kwonlyargs, spec.kwonlydefaults or {}, spec.annotations

else: # sys.version_info.major < 3

    import __builtins__ as builtins

    string_type = str, unicode
    binary_type = str
    number_type = int, long

    def getargspec(function):
        spec = inspect.getargspec(function)
        return spec.args, spec.varargs, spec.defaults or [], [], {}, {}


def to_binary(value):
    if isinstance(value, string_type):
        return value.encode()
    else:
        return value


def to_string(value):
    if isinstance(value, binary_type):
        return value.decode()
    else:
        return value


if sys.version_info >= (3, 6):
    ordered_dict = dict
else:
    import collections
    ordered_dict = collections.OrderedDict
