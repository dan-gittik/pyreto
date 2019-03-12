import contextlib
import os
import shutil
import tempfile


@contextlib.contextmanager
def temporary_file():
    fd, path = tempfile.mkstemp()
    try:
        yield path
    finally:
        os.close(fd)
        os.remove(path)


@contextlib.contextmanager
def temporary_directory():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)
