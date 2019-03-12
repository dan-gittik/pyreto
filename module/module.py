import os
import sys
import types


def import_module(path):
    with open(path) as reader:
        data = reader.read()
    return evaluate_module(data, path)


def evaluate_module(data, path=None):
    path, directory_path, name = parse_path(path)
    sys_path = sys.path[:]
    try:
        if directory_path:
            sys.path.insert(0, directory_path)
        code = compile(data, path, 'exec')
        module = types.ModuleType(name)
        module.__file__ = path
        module.__name__ = name
        exec(code, vars(module), vars(module))
        return module
    finally:
        sys.path = sys_path


def parse_path(path):
    if not path:
        return '', '', ''
    path = os.path.abspath(path)
    directory_path = os.path.dirname(path)
    basename = os.path.basename(path)
    name, extension = os.path.splitext(basename)
    return path, directory_path, name
