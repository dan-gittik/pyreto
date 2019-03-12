import importlib
import os
import sys
import types


def install_collection(collection_path):
    collection_importer = CollectionImporter(collection_path)
    collection_importer.install()


class CollectionImporter(object):

    def __init__(self, collection_path):
        self.path = collection_path
        self.name = os.path.basename(self.path)
        self.package = types.ModuleType(self.name)
        self.package.__path__ = self.path
        self.package.__package__ = self.name

    def install(self):
        sys.meta_path.insert(0, self)
        sys.modules[self.name] = self.package

    def find_module(self, module_name, path=None):
        if module_name == self.name or module_name.startswith(self.name + '.'):
            return self

    def load_module(self, module_name):
        if module_name == self.name:
            return self.package
        _, module_name = module_name.split('.', 1)
        module_directory = os.path.join(self.path, module_name)
        if not os.path.exists(module_directory):
            raise ImportError('cannot import name {!r}'.format(module_name))
        path = sys.path[:]
        try:
            sys.path.insert(0, module_directory)
            module = importlib.import_module(module_name)
            setattr(self.package, module_name, module)
            sys.modules[self.name + '.' + module_name] = module
            return module
        finally:
            sys.path = path
