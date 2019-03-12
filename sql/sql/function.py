import sqlalchemy

from .expression import Expression


class Function(object):

    def __init__(self, database):
        self.database = database

    def __getitem__(self, name):
        def function(*args):
            func = getattr(sqlalchemy.sql.func, name)
            args = [Expression.normalise(arg) for arg in args]
            return Expression(self.database, func(*args))
        function.__name__ = name
        return function

    def __getattr__(self, name):
        return self[name]
