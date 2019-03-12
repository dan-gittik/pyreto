import collections

import sqlalchemy

from pyreto.dictionary import Dictionary


def get_table_names(source):
    if isinstance(source, sqlalchemy.sql.expression.Join):
        return get_table_names(source.left) + get_table_names(source.right)
    else:
        return [source.name]


def Result(query, row):
    tables = get_table_names(query._source)
    values = collections.defaultdict(dict)
    others = {}
    for key, value in row.items():
        for table in tables:
            if key.startswith(table):
                key = key[len(table)+1:]
                values[table][key] = value
                break
        else:
            others[key] = value
    if len(values) == 1:
        table, row = values.popitem()
        others.update(row)
        return query.database.tables[table](**others)
    else:
        for table, row in values.items():
            others[table] = query.database.tables[table](**row)
        return Dictionary(**others)
