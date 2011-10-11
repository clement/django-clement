try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import curry
import json as json_


def post_only(view):
    return method_only(view, 'POST')

def get_only(view):
    return method_only(view, 'GET')

def method_only(func, method):
    @wraps(func)
    def _wrap(request, *args, **kwargs):
        if request.method != method:
            resp = HttpResponse('Method not allowed: %s' % request.method)
            resp.status_code = 405
            return resp
        return func(request, *args, **kwargs)
    return _wrap


def render_to(func=None, template_name_key='template', mimetype_key='mimetype'):
    def real_decorator(func, template_name_key, mimetype_key):
        def _wrap(request, *args, **kwargs):
            resp = func(request, *args, **kwargs)
            if not isinstance(resp, HttpResponse):
                template_name = resp.pop(template_name_key)
                mimetype = resp.pop(mimetype_key, None)
                return render_to_response(template_name, resp, context_instance=RequestContext(request), mimetype=mimetype)
            else:
                return resp
        return wraps(func)(_wrap)

    curried = curry(real_decorator, template_name_key=template_name_key, mimetype_key=mimetype_key)
    if func:
        return curried(func)
    else:
        return curried

def json(f):
    @wraps(f)
    def _wrap(*args, **kwargs):
        r = f(*args, **kwargs)
        if not isinstance(r, HttpResponse):
            r = HttpResponse(json_.dumps(r), mimetype='application/json')
        return r
    return _wrap

def coerce(*coerce_funs):
    def real_decorator(func):
        def _wrap(request, *args, **kwargs):
            # make sure args is a list
            args = list(args)
            import inspect
            import types
            hop = 1
            # Suspect a method, callable object, class method
            # there's another parameter to remove then
            if not isinstance(func, types.FunctionType):
                hop += 1
            
            for idx, arg_name in enumerate(inspect.getargspec(func)[0][hop:hop+len(coerce_funs)]):
                try:
                    f = coerce_funs[idx]
                    if f:
                        if idx < len(args):
                            args[idx] = f(args[idx])
                        elif arg_name in kwargs:
                            kwargs[arg_name] = f(kwargs[arg_name])
                except IndexError:
                    pass

            return func(request, *args, **kwargs)
        return wraps(func)(_wrap)

    return real_decorator
