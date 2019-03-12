import contextlib
import os

from pyreto import export


@export
@contextlib.contextmanager
def in_directory(path):
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_path)
