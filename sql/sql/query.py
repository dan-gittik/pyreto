import collections
import operator
import sys

import sqlalchemy

from pyreto.compat import number_type

from .expression import Expression
from .result import Result
from .utils import to_raw


try:
    reduce
except NameError:
    from functools import reduce

NO_LIMIT = 2**64-1


class Query(object):

    def __init__(self, database, source, query=None):
        if query is None:
            query = sqlalchemy.sql.select()
        self.database = database
        self._source = source
        self._query = query

    def __str__(self):
        return to_string(self.database, self._query)

    def __iter__(self):
        for row in self._execute(self._query):
            yield Result(self, row)

    def __call__(self):
        return list(self)

    def __getitem__(self, key):
        if isinstance(key, number_type):
            query = self._query.offset(key).limit(1)
            return Result(self, self._execute(query).fetchone())
        if isinstance(key, slice):
            query = self._query.offset(slice.start or 0).limit(slice.stop or NO_LIMIT)
            return self._clone(query)
        if isinstance(key, (tuple, list, set, frozenset)):
            query = self._query
            for item in key:
                query = query.column(item)
            return self._clone(query)
        query = self._query.column(to_raw(key))
        return self._clone(query)

    def where(self, clause):
        if clause is None:
            return self
        query = self._query.where(to_raw(clause))
        return self._clone(query)

    def having(self, clause):
        if clause is None:
            return self
        query = self._query.having(to_raw(clause))
        return self._clone(query)

    def group_by(self, *clauses):
        if not clauses:
            return self
        query = self._query.group_by(*[to_raw(clause) for clause in clauses])
        return self._clone(query)

    def order_by(self, *clauses):
        if not clauses:
            return self
        query = self._query.order_by(*[to_raw(clause) for clause in clauses])
        return self._clone(query)

    def join(self, other, on=None, outer=False):
        source = self._source.join(other._source, on, outer)
        return Query(self.database, source, self._query)

    def distinct(self):
        query = self._query.distinct()
        return self._clone(query)

    def count(self):
        query = self._query.column(self.database.function.count(1)._expression)
        return self._execute(query).scalar()

    def exists(self):
        query = sqlalchemy.sql.exists(self._query)
        return self._execute(query).scalar()

    def _clone(self, query):
        return type(self)(self.database, self._source, query)

    def _execute(self, query):
        if not query.columns:
            query = query.column(self._source)
        query = query.select_from(self._source).apply_labels()
        return self.database._execute(query)


class TableQuery(Query):

    def where(self, clause=None, **kwargs):
        clause = self._reduce(clause, kwargs)
        return super(TableQuery, self).where(clause)

    def having(self, clause=None, **kwargs):
        clause = self._reduce(clause, kwargs)
        return super(TableQuery, self).having(clause)

    def update(self, **kwargs):
        query = self._source.update(self._query._whereclause, kwargs or None)
        self.datbase._execute(query)

    def delete(self):
        query = self._source.delete(self._query._whereclause)
        self.database._execute(query)

    def _reduce(self, clause, kwargs):
        clauses = []
        if clause is not None:
            clauses.append(clause)
        for key, value in kwargs.items():
            clauses.append(self._source.columns[key] == value)
        if clauses:
            return reduce(operator.and_, clauses)
        return None
