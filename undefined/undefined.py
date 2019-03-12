from pyreto import export


class Undefined(object):

    def __repr__(self):
        return '<undefined>'
    
    def __bool__(self):
        return False
    __nonzero__ = __bool__


undefined = Undefined()
export(undefined)
