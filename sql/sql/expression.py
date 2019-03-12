import sqlalchemy

from .utils import to_raw, to_string


class Expression(object):

    def __init__(self, database, expression):
        self.database = database
        self._expression = expression

    def __str__(self):
        return to_string(self.database, self._expression)

    def __eq__(self, other):
        return self._clone(self._expression == to_raw(other))

    def __ne__(self, other):
        return self._clone(self._expression != to_raw(other))

    def __gt__(self, other):
        return self._clone(self._expression > to_raw(other))

    def __lt__(self, other):
        return self._clone(self._expression < to_raw(other))

    def __ge__(self, other):
        return self._clone(self._expression >= to_raw(other))

    def __le__(self, other):
        return self._clone(self._expression <= to_raw(other))

    def __add__(self, other):
        return self._clone(self._expression + to_raw(other))

    def __sub__(self, other):
        return self._clone(self._expression - to_raw(other))

    def __mul__(self, other):
        return self._clone(self._expression * to_raw(other))

    def __div__(self, other):
        return self._clone(self._expression / to_raw(other))

    def __mod__(self, other):
        return self._clone(self._expression % to_raw(other))

    def __radd__(self, other):
        return self._clone(to_raw(other) + self._expression)

    def __rsub__(self, other):
        return self._clone(to_raw(other) - self._expression)

    def __rmul__(self, other):
        return self._clone(to_raw(other) * self._expression)

    def __rdiv__(self, other):
        return self._clone(to_raw(other) / self._expression)

    def __rmod__(self, other):
        return self._clone(to_raw(other) % self._expression)

    def __invert__(self):
        return self._clone(~self._expression)

    def __or__ (self, other):
        return self._clone(self._expression | to_raw(other))

    def __and__(self, other):
        return self._clone(self._expression & to_raw(other))

    def is_(self, other):
        return self._clone(self._expression.is_(to_raw(other)))

    def is_not(self, other):
        return self._clone(self._expression.isnot(to_raw(other)))

    def in_(self, collection):
        collection = [to_raw(item) for item in collection]
        return self._clone(self._expression.in_(collection))

    def not_in(self, collection):
        collection = [to_raw(item) for item in collection]
        return self._clone(self._expression.notin(collection))

    def like(self, pattern):
        return self._clone(self._expression.like(to_raw(pattern)))

    def startswith(self, pattern):
        return self.like(pattern + '%')

    def endswith(self, pattern):
        return self.like('%' + pattern)

    def contains(self, pattern):
        return self.like('%' + pattern + '%')

    def unary(self, operator, after=False):
        if after:
            kwargs = {'modifier': operator}
        else:
            kwargs = {'operator': operator}
        return self._clone(sqlalchemy.sql.UnaryExpression(self._expression, **kwargs))

    def binary(self, operator):
        def operation(operand1, operand2):
            operand1 = to_raw(operand1)
            operand2 = to_raw(operand2)
            return self._clone(operand1.op(operator)(operand2))
        operation.__name__ = operator
        return operation

    def as_(self, name):
        return self._clone(self._expression.label(name))

    def _clone(self, expression):
        return Expression(self.database, expression)
