from pyreto import cached_property

from .column import Column
from .row import Row
from .query import TableQuery


class Table(object):

    pk = NotImplemented

    def __init__(self, database, table):
        self.database = database
        self._table = table

    def __str__(self):
        return self.table_name

    def __call__(self, **kwargs):
        return Row(self, **kwargs)

    def __getitem__(self, name):
        return self.columns[name]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    @property
    def table_name(self):
        return self._table.name

    @cached_property
    def columns(self):
        columns = {}
        for name, column in self._table.columns.items():
            columns[name] = Column(self, column)
        return columns

    @cached_property
    def pk(self):
        pk = NotImplemented
        for column in self.columns.values():
            if column.primary_key and pk is not NotImplemented:
                raise TypeError('multiple primary keys are not supported')
            pk = column
        return pk

    @property
    def select(self):
        return TableQuery(self.database, self._table)

    @property
    def where(self):
        return self.select.where

    @property
    def join(self):
        return self.select.join

    def alias(self, name):
        self.database.tables[name] = table = Table(self.database, self._table.alias(name))
        return table

    def insert(self, rows):
        rows = [{name: row.get(name) for name in self.columns} for row in rows]
        self.database._execute(self._table.insert(rows))
