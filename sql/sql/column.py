from pyreto import cached_property

from .expression import Expression


class Column(Expression):

    def __init__(self, table, column):
        super(Column, self).__init__(database=table.database, expression=column)
        self.table = table
        self._column = column

    def __str__(self):
        return '{}.{}'.format(self.table, self.column_name)

    def __pos__(self):
        return self.asecnding

    @property
    def column_name(self):
        return self._column.name

    @property
    def primary_key(self):
        return self._column.primary_key

    @cached_property
    def foreign_key(self):
        if not self._column.foreign_keys:
            return None
        if len(self._column.foreign_keys) > 1:
            raise TypeError('multiple foreign keys are not supported')
        foreign_key, = self._column.foreign_keys
        return self.table.database[foreign_key.column.table.name][foreign_key.column.name]

    @property
    def ascending(self):
        return self._clone(self._column.asc())

    @property
    def descending(self):
        return self._clone(self._column.desc())
