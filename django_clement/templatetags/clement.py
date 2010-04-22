"""
Template filters used in `moderation` application
HTML templates. Mainly utility functions.
"""

from django_clement.template import template_function
from django_clement.conf import settings
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.http import QueryDict

# Special object to allow django to recognize this
# module as a template filter and tags module
register = template.Library()

@register.filter
def blank(value):
    """
    Return True if the value is None or
    if it's a string composed only of blank
    characters.

    Undefined behaviour for other datatypes.
    """
    if value is None:
        return True
    return value.strip() == ''

@register.filter
def at(value, key):
    """
    Dictionnary lookup. Useful when it's not possible
    to resolve a dict lookup using the `.` operator
    inside a templates. Example:
    
        {{ stats_dict|at:img.pk }}
    """
    try:
        return value[key]
    except:
        return None
        
@register.filter('in')
def inside(value, sequence):
    """
    `in` operator as a filter.
    Probably a bit deprecated when 1.2 will be out,
    but could still be useful when full python
    expressions are not supported. Example:

        {{ my_value|in:my_list }}

    translate - in python - to 

        my_value in my_list
    """
    try:
        return value in sequence
    except:
        return False


@register.filter
def short_email(email, autoescape=None):
    try:
        idx = email.index('@')
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x : x
        return mark_safe("<abbr title=\"%s\">%s</abbr>" % (esc(email[idx:]), esc(email[:idx]),))
    except ValueError:
        return email
short_email.needs_autoescape = True

def urlp(name, *args, **kwargs):
    """
    Reverse a view name with corresponding arguments
    while being aware of the request urlconf IF
    present in the template context as "request"
    (when using the request context processor for
    example)
    """
    from django.core.urlresolvers import reverse, NoReverseMatch
    from django.conf import settings

    context = kwargs.pop('context')
    try:
        urlconf = context['request'].urlconf
    except:
        urlconf = None


    try:
        return reverse(name, args=args, kwargs=kwargs, urlconf=urlconf, current_app=context.current_app)
    except NoReverseMatch, e:
        if settings.SETTINGS_MODULE:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                return reverse(project_name+'.'+name, args=args, kwargs=kwargs, urlconf=urlconf, current_app=context.current_app)
            except NoReverseMatch:
                raise e
        else:
            raise e
urlp = register.tag(template_function(urlp, send_context=True))

register.tag('eval', template_function(lambda x:x))


@register.filter('gravatar')
def gravatar_filter(email, arg=None):
    """
    filter version of the `gravatar` template tag
    """
    if arg and arg[0] == '?':
        kwargs = {'s': None, 'd': None, 'r': None}
        arg = arg[1:]
    else:
        kwargs = {'s': settings.GRAVATAR_DEFAULT_S,
                  'd': settings.GRAVATAR_DEFAULT_D,
                  'r': settings.GRAVATAR_DEFAULT_R }

    kwargs.update(dict(QueryDict(arg).items()))
    return gravatar_tag(email, **kwargs)

def gravatar_tag(email, **kwargs):
    """
    Generate a gravatar URL for an email adress.

    Allowed parameters are `s`, `d` and `r` as specified
    in (gravatar documentation)[http://en.gravatar.com/site/implement/images/]
    and their default value is controlled by configuration variables
    `GRAVATAR_DEFAULT_*`

    Also, the base gravatar server URL is specified in
    `GRAVATAR_URL`.
    """
    for param in ('s', 'd', 'r',):
        kwargs.setdefault(param, getattr(settings, 'GRAVATAR_DEFAULT_'+param.upper()))

    import hashlib
    url =  settings.GRAVATAR_URL + hashlib.md5(email.lower().strip()).hexdigest()
    
    if any(kwargs):
        url += '?'
        qd = QueryDict('', mutable=True)
        qd.update(dict(filter(lambda (k,v) : v is not None, kwargs.items())))
        url += qd.urlencode()

    return url
register.tag('gravatar', template_function(gravatar_tag))
