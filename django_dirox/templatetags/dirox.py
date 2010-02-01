"""
Template filters used in `moderation` application
HTML templates. Mainly utility functions.
"""

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
    print value, sequence
    try:
        return value in sequence
    except:
        return False
