def compose(*functions):
    functions = list(functions)
    tail = functions.pop()
    if len(functions):
        def composed(*args, **kwargs):
            return reduce(lambda f,g : lambda v: f(g(v)), functions)(tail(*args, **kwargs))
        return composed
    else:
        return tail
