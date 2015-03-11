class cached_property(object):
    """property-like descriptor which caches its result in the instance dictionary."""

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        result = vars(instance)[self.func.__name__] = self.func(instance)
        return result
