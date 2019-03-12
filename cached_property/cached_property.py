import threading

from pyreto import export, on_destroy, parametrized_decorator


@export
@parametrized_decorator(threadsafe=False)
class cached_property(object):

    def __init__(self, function, threadsafe):
        self.function = function
        self.threadsafe = threadsafe
        self.values = {}
        if self.threadsafe:
            self.lock = threading.Lock()

    def __get__(self, instance, cls):
        if instance is None:
            return self
        token = id(instance)
        if self.threadsafe and token not in self.values:
            with self.lock:
                if token not in self.values:
                    self.add_value(token, instance)
        elif token not in self.values:
            self.add_value(token, instance)
        return self.values[token]

    def add_value(self, token, instance):
        self.values[token] = self.function(instance)
        on_destroy(instance, self.remove_value, token)

    def remove_value(self, token):
        self.values.pop(token, None)
