class Dictionary(dict):

    def __init__(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def __setitem__(self, key, value):
        value = self._propagate(value)
        super(Dictionary, self).__setitem__(key, value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

    def _propagate(self, value):
        if isinstance(value, dict):
            return type(self)(value)
        elif isinstance(value, (tuple, list, set, frozenset)):
            return type(value)(self._normalize(item) for item in value)
        return value
