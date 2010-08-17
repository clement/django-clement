from django.conf import settings

SETTING_PREFIX = 'CLEMENT_'

def setting(name, value):
    globals()[name] = getattr(settings, SETTING_PREFIX+name, value)

setting('GRAVATAR_URL', 'http://www.gravatar.com/avatar/')
setting('GRAVATAR_DEFAULT_S', None)
setting('GRAVATAR_DEFAULT_R', None)
setting('GRAVATAR_DEFAULT_D', 'monsterid')
