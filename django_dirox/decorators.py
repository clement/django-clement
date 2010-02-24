try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import curry


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


def render_to(func=None, template_name_key='template', mimetype_key='mimetype'):
    def real_decorator(func, template_name_key, mimetype_key):
        def _wrap(request, *args, **kwargs):
            resp = func(request, *args, **kwargs)
            template_name = resp.pop(template_name_key)
            mimetype = resp.pop(mimetype_key, None)
            return render_to_response(template_name, resp, context_instance=RequestContext(request), mimetype=mimetype)
        return wraps(func)(_wrap)

    curried = curry(real_decorator, template_name_key=template_name_key, mimetype_key=mimetype_key)
    if func:
        return curried(func)
    else:
        return curried
