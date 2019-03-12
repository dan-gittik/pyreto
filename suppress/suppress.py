import contextlib

from pyreto import export


@export
@contextlib.contextmanager
def suppress(*exceptions):
    if not exceptions:
        exceptions = (Exception,)
    try:
        yield
    except exceptions:
        pass
