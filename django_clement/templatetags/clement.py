"""
Template filters used in `moderation` application
HTML templates. Mainly utility functions.
"""

from django_clement.template import template_function
from django import template

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
