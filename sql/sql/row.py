class Row(object):

    def __init__(self, table, **kwargs):
        vars(self).update(
            table = table,
            _values = dict.fromkeys(table.columns),
            _changed = set(),
        )
        for key, value in kwargs.items():
            self[key] = value

    def __repr__(self):
        return '<{cls} #{pk}>'.format(cls=self.table, pk=self.pk)

    def __getitem__(self, name):
        return self._values[name]

    def __setitem__(self, name, value):
        if name in self._values:
            if self._values[name] != value:
                foreign_key = self.table.columns[name].foreign_key
                if foreign_key:
                    value = ForeignKey(foreign_key, value)
                self._values[name] = value
                self._changed.add(name)
        else:
            raise KeyError(name)

    def __delitem__(self, name):
        if name in self._values:
            self._values[name] = None
        else:
            raise KeyError(name)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self._values:
            self[name] = value
        else:
            super(Row, self).__setattr__(name, value)

    def __delitem__(self, name):
        if name in self._values:
            del self[name]
        else:
            super(Row, self).__delattr__(name)

    @property
    def pk(self):
        if self.table.pk is NotImplemented:
            return NotImplemented
        return self._values[self.table.pk.column_name]

    def save(self, force=False):
        if self.pk is NotImplemented:
            self.table.database._execute(self.table._table.insert(self._values))
        else:
            if self.pk is None or self.table.pk.column_name in self._changed:
                cursor = self.table.database._execute(self.table._table.insert(self._values))
                if self.pk is None:
                    self._values[self.table.pk.column_name] = cursor.lastrowid
            elif force or self._changed:
                values = self._values if force else {name: self._values[name] for name in self._changed}
                self.table.database._execute(self.table._table.update(self.table.pk._column == self.pk, values))
            self._changed.clear()

    def delete(self):
        if self.pk is NotImplemented:
            self.table.where(**self._values).delete()
        elif self.pk is not None and self.table.pk.column_name not in self._changed:
            self.table.database._execute(self.table._table.delete(self.table.pk._column == self.pk))
            self._values[self.table.pk.column_name] = None
            self._changed.clear()


class ForeignKey(int):

    def __new__(cls, foreign_key, value):
        if isinstance(value, Row):
            value = value.pk
        instance = super(ForeignKey, cls).__new__(cls, value)
        instance.foreign_key = foreign_key
        return instance

    def __call__(self):
        return self.foreign_key.table.where(self.foreign_key.table.pk == self)[0]
