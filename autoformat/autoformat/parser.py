def parse(string):
    index = 0
    while index < len(string):
        char = string[index]
        if char not in '{}':
            yield char, False
            index += 1
        elif char == '{':
            if string[index:index+2] == '{{':
                yield '{', False
                index += 2
            else:
                start = index
                index = skip_expression(index, string)
                yield string[start:index], True
        else: # }
            if string[index:index+2] == '}}':
                yield '}', False
                index += 2
            else:
                raise ValueError("unmatched '}'")


def skip_expression(index, string):
    index += 1
    depth = 1
    while index < len(string):
        char = string[index]
        if char not in '{}\'"':
            index += 1
        elif char == '{':
            depth += 1
            index += 1
        elif char == '}':
            depth -= 1
            if not depth:
                break
            index += 1
        else: # '"
            index = skip_string(index, string)
    else:
        raise ValueError("unmatched '{'")
    return index + 1


def skip_string(index, string):
    quote = string[index]
    if string[index:index+3] == 3*quote:
        end = lambda char: char == quote and string[index:index+3] == 3*quote
        inc = lambda index: index + 3
    else:
        end = lambda char: char == quote
        inc = lambda index: index + 1
    index = inc(index)
    while index < len(string):
        char = string[index]
        if end(char):
            index = inc(index)
            break
        if char == '\\':
            index += 2
        else:
            index += 1
    return index
