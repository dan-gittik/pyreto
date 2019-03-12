import collections
import sys
import weakref

from pyreto import export


refs = collections.defaultdict(list)


if sys.version_info >= (3, 4):

    def on_destroy(instance, function, *args, **kwargs):
        weakref.finalize(instance, function, *args, **kwargs)

else:

    def on_destroy(instance, function, *args, **kwargs):
        # The reference returned by weakref.ref(instance, finalizer) must remain until the object is destroyed in order
        # for the callback to be called; it's therefore kept (by object id) and discarded when the callback is invoked.
        token = id(instance)
        def finalizer(ref):
            refs.pop(token, None)
            function(*args, **kwargs)
        ref = weakref.ref(instance, finalizer)
        refs[token].append(ref)


export(on_destroy)
