import contextlib
import os
import sys
import traceback
import warnings

from pyreto import export, kwonly


@export
@contextlib.contextmanager
@kwonly(warning_class=Warning, message='', show_traceback=False)
def as_warning(*exceptions, **kwargs):
    if not exceptions:
        exceptions = (Exception,)
    try:
        yield
    except exceptions:
        warn(**kwargs)


def warn(warning_class, message, show_traceback):
    exception, error, tb = sys.exc_info()
    if show_traceback:
        tb = tb.tb_next # Skip current frame.
        lines = traceback.format_exception(exception, error, tb)
    else:
        lines = traceback.format_exception_only(exception, error)
    warning = ''.join(lines)
    if message:
        warning = message + os.linesep + warning
    warnings.warn(warning, warning_class)
