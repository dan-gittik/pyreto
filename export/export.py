import inspect
import sys


def export(value):
    name = inspect.currentframe().f_back.f_globals.get('__name__')
    if name is None:
        raise RuntimeError('unable to determine module name')
    # In Python 2, the only reference to the module is by sys.modules, so when we replace it, it's garbage collected
    # and we lose access to its global scope. To avoid this, we save a reference to the module, and so keep it alive.
    if sys.version_info.major <= 2:
        value.__module = sys.modules[name]
    sys.modules[name] = value


export(export)
