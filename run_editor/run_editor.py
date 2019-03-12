import os

from pyreto import defaults, export
from pyreto.compat import to_binary
from pyreto.temporary import temporary_file


@export
@defaults(data=b'', editor='vim')
def run_editor(data, editor):
    data = to_binary(data)
    with temporary_file() as path:
        with open(path, 'wb') as writer:
            writer.write(data)
        os.system('{} {}'.format(editor, path))
        with open(path, 'rb') as reader:
            data = reader.read()
        return data
