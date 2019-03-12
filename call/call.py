import inspect

from pyreto import undefined
from pyreto.compat import getargspec, ordered_dict


class Call(object):
    
    def __init__(self, callable, *args, **kwargs):
        self._callable = callable
        if inspect.isclass(self._callable):
            function = self._callable.__init__
        else:
            function = self._callable
        self._names, self._args, self._kwargs, self._defaults, _, self._kwonly, _ = getargspec(function)
        self.name = self._callable.__name__
        self.arguments = self._infer_arguments()
        if args or kwargs:
            self.amend(*args, **kwargs)
        
    def __str__(self):
        return '{name}({args})'.format(
            name = self.name,
            args = ', '.join('{}={!r}'.format(name, value) for name, value in self.arguments.items()),
        )

    def __bool__(self):
        return self.callable
    __nonzero__ = __bool__

    def __iter__(self):
        return iter(self.unpack())

    def __call__(self):
        return self.invoke()

    @property
    def callable(self):
        return undefined not in self.arguments.values()

    @property
    def args(self):
        if not self._args:
            return None
        return self.arguments[self._args]

    @property
    def kwargs(self):
        if not self._kwargs:
            return None
        return self.arguments[self._kwargs]

    def amend(self, *args, **kwargs):
        for name, value in zip(self._names, args):
            self.arguments[name] = value
        args = args[len(self._names):]
        if args:
            if not self._args:
                raise TypeError('{name}() takes {takes} positional arguments but {given} were given'.format(
                    name = self.name,
                    takes = len(self._names),
                    given = len(self._names) + len(args),
                ))
            else:
                self.arguments[self._args] = args
        for name in list(kwargs):
            if name in self._names or name in self._kwonly:
                self.arguments[name] = kwargs.pop(name)
        if kwargs:
            if not self._kwargs:
                raise TypeError('{name}() got unexpected keyword arguments: {args}'.format(
                    name = self.name,
                    args = ', '.join(repr(name) for name in kwargs),
                ))
            else:
                self.arguments[self._kwargs] = kwargs
        return self

    def inject(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.arguments:
                self.arguments[name] = value
        return self

    def reset(self):
        self.arguments = self._infer_arguments()
        return self

    def unpack(self):
        if not self.callable:
            names = [name for name, value in self.arguments.items() if value is undefined]
            raise TypeError('{name}() missing {num} required positional arguments: {args}'.format(
                name = self.name,
                num = len(names),
                args = ', '.join(repr(name) for name in names),
            ))
        args = [self.arguments[name] for name in self._names]
        if self._args:
            args.extend(self.arguments[self._args])
        kwargs = {name: self.arguments[name] for name in self._kwonly}
        if self._kwargs:
            kwargs.update(self.arguments[self._kwargs])
        return args, kwargs

    def invoke(self):
        args, kwargs = self.unpack()
        return self._callable(*args, **kwargs)

    def _infer_arguments(self):
        arguments = ordered_dict.fromkeys(self._names, undefined)
        for name, value in zip(reversed(self._names), reversed(self._defaults)):
            arguments[name] = value
        if self._args:
            arguments[self._args] = []
        arguments.update(self._kwonly)
        if self._kwargs:
            arguments[self._kwargs] = {}
        return arguments
