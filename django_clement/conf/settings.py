from django_clement.conf import make_setting_function

_setting = make_setting_function('CLEMENT_', globals())

_setting('GRAVATAR_URL', 'http://www.gravatar.com/avatar/')
_setting('GRAVATAR_DEFAULT_S', None)
_setting('GRAVATAR_DEFAULT_R', None)
_setting('GRAVATAR_DEFAULT_D', 'monsterid')
