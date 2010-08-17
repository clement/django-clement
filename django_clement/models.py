def cache_m2m(name, cache_name=None):
    if not cache_name:
        cache_name = '_'+name

    def fget(self):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, getattr(self, name).all())
        return getattr(self, cache_name)
    def fset(self, value):
        setattr(self, cache_name, value)
    return property(fget, fset)
