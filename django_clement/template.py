try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.
from django import template
import re


class template_function(object):
    """
    Decorate a function so it can be registered directly as a template
    tag and be called with a full argument list (both positional and
    keywords), understands filters on variable, and an optionnal "as variable"
    feature.

    This is thus more powerful than django's `simple_tag` decorator.
    Use it like that :
    >>> from django import template
    >>> register = template.Library()
    >>> register.tag("my_tag_name", template_function(my_function))

    or, the decorator way

    >>> @register.tag
    >>> @template_function
    >>> def my_tag_name(a, b, c=None):
    >>>     return a + b + c


    In the template, you can then call your function like :

    >>> {% my_tag_name var|lower "b" c="ccc" %}

    to print it directly, or

    >>> {% my_tag_name var|lower "b" c="ccc" as new_var %}

    to assign the result in a new variable
    """
    def __init__(self, function, send_context=False):
        self.send_context = send_context
        update_wrapper(self, function)
        self.function = function

    def __call__(self, parser, token):
        # Reset the state of the node
        args = []
        kwargs = {}
        assign = None

        contents = token.split_contents()
        tag_name = contents.pop(0)

        try:
            if contents[-2] == 'as':
                assign = contents[-1]
                contents = contents[:-2]
        except IndexError:
            pass

        # Separate positionnal from keywords
        for symbol in contents:
            match = re.match("^(([a-zA-Z_][a-zA-Z0-9_]*)=)", symbol)
            key = match and str(match.groups()[1])
            value = parser.compile_filter((match and symbol[len(match.groups()[0]):]) or symbol)

            if key:
                kwargs[key] = value
            else:
                args.append(value)

        return TemplateFunction(self.function, args, kwargs, assign, self.send_context)


class TemplateFunction(template.Node):
    def __init__(self, function, args=[], kwargs={}, assign=None, send_context=False):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.assign = assign
        self.send_context = send_context

    def render(self, context):
        f = lambda v: v.resolve(context)
        args = map(f, self.args)
        kwargs = {}
        for name, arg in self.kwargs.items():
            kwargs[name] = arg.resolve(context)

        if self.send_context:
            kwargs['context'] = context

        result = self.function(*args, **kwargs)
        if self.assign:
            context[self.assign] = result
            return ""
        else:
            return result
