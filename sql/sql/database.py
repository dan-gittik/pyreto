import threading

import sqlalchemy

from pyreto import cached_property

from .expression import Expression
from .function import Function
from .table import Table


class Database(object):

    def __init__(self, url):
        self._engine = sqlalchemy.create_engine(self.url)
        self._thread = threading.local()
        self.function = Function(self)

    def __str__(self):
        return self.database_url

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exception, error, traceback):
        if exception is None:
            self.commit()
        else:
            self.rollback()

    def __getitem__(self, name):
        return self.tables[name]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    @property
    def database_url(self):
        return str(self._engine.url)

    @property
    def database_driver(self):
        return self._engine.url.drivername

    @property
    def database_username(self):
        return self._engine.url.username

    @property
    def database_password(self):
        return self._engine.url.password

    @property
    def database_host(self):
        return self._engine.url.host

    @property
    def database_port(self):
        return self._engine.url.port

    @property
    def database_name(self):
        return self._engine.url.database

    @property
    def database_query(self):
        return self._engine.url.query

    @cached_property
    def tables(self):
        metadata = sqlalchemy.MetaData(self._engine)
        metadata.reflect()
        tables = {}
        for name, table in metadata.tables.items():
            tables[name] = Table(self, table)
        return tables

    def execute(self, sql, **kwargs):
        for statement in sql.split(';'):
            statement = statement.strip()
            if not statement:
                continue
            self._execute(sqlalchemy.sql.text(statement), **kwargs)

    def scalar(self, expression):
        expression = Expression.normalise(expression)
        return self._execute(sqlalchemy.sql.select([expression])).scalar()

    def begin(self):
        if hasattr(self._thread, 'transaction'):
            raise TypeError('nested transactions are not supported')
        self._thread.transaction = self._engine.connect().begin()

    def commit(self):
        if not hasattr(self._thread, 'transaction'):
            raise RuntimeError('no active transaction')
        self._thread.transaction.commit()
        del self._thread.transaction

    def rollback(self):
        if not hasattr(self._thread, 'transaction'):
            raise RuntimeError('no active transaction')
        self._thread.transaction.rollback()
        del self._thread.transaction

    def _execute(self, *args, **kwargs):
        if hasattr(self._thread, 'transaction'):
            connection = self._thread.transaction.connection
        else:
            connection = self._engine.connect()
        return connection.execute(*args, **kwargs)
