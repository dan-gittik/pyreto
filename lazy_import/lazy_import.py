import importlib
import types

from pyreto import export


@export
def lazy_import(name):
    return LazyModule(name)


class LazyModule(types.ModuleType):
    
    def __init__(self, name):
        super(LazyModule, self).__init__(name)
        self.__module = None
    
    def __getattr__(self, key):
        if self.__module is None:
            self.__module = importlib.import_module(self.__name__)
        return getattr(self.__module, key)
