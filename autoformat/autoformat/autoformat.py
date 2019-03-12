from pyreto import suppress

from .parser import parse
from .scope import Scope


def autoformat(string, depth=0, **kwargs):
    scope = Scope(depth+1, **kwargs)
    output = []
    for token, evaluate in parse(string):
        if evaluate:
            with suppress():
                token = scope.evaluate(token[1:-1])
        output.append(token)
    return ''.join(output)
