try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django.http import Http404


def post_only(view):
    return method_only(view, 'POST')

def get_only(view):
    return method_only(view, 'GET')

def method_only(func, method):
    @wraps(func)
    def _wrap(request, *args, **kwargs):
        if request.method != method:
            raise Http404
        return func(request, *args, **kwargs)
    return _wrap
