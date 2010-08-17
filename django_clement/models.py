def cache_m2m(name):
    cname = '_'+name
    def fget(self):
        if not hasattr(self, cname):
            setattr(self, cname, getattr(self, name).all())
        return getattr(self, cname)
    def fset(self, value):
        setattr(self, cname, value)
    return property(fget, fset)
