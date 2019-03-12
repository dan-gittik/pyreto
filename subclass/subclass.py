import collections


class Subclassable(type):
    
    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super(Subclassable, mcs).__new__(mcs, name, bases, attrs, **kwargs)
        for superclass in get_superclasses(cls):
            if 'on_subclass' in vars(superclass):
                superclass.on_subclass(cls)
        return cls


def get_subclasses(cls):
    for subclass in _bfs(cls, lambda cls: cls.__subclasses__()):
        yield subclass


def get_superclasses(cls):
    for superclass in _bfs(cls, lambda cls: cls.__bases__):
        yield superclass


def _bfs(parent, get_children):
    visited = set()
    items = collections.deque(get_children(parent))
    while items:
        item = items.popleft()
        if item in visited:
            continue
        yield item
        visited.add(item)
        items.extend(get_children(item))
