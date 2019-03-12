class Object(object):
    
    def __init__(self, **kwargs):
        vars(self).update(kwargs)

    def __str__(self):
        return '{' + ', '.join('{}: {!r}'.format(key, value) for key, value in vars(self).items()) + '}'
