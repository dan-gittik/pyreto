import datetime
import sqlalchemy


try:
    long, unicode
except NameError:
    long, unicode = int, str

supported_types = [
    bool,
    int,
    long,
    float,
    bytes,
    str,
    unicode,
    datetime.date,
    datetime.time,
    datetime.datetime,
    sqlalchemy.sql.elements.ColumnElement,
]

supported_attributes = [
    '_expression',
    '_table',
]


def to_raw(expression):
    if expression is None or isinstance(expression, supported_types):
        return expression
    for attribute in supported_attributes:
        if hasattr(expression, attribute):
            return getattr(expression, attribute)
    raise ValueError('unsupported expression: {expression!r}'.format(expression=expression))


def to_string(database, expression):
    compiled = expression.compile(dialect=database._engine.dialect)
    string = compiled.string
    for name in compiled.positiontup:
        string = string.replace(compiled.bindparam_string(name), str(compiled.params[name]), 1)
    return string
