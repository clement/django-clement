def make_setting_function(prefix, global_dict):
    from django.conf import settings
    def setting(name, value):
        global_dict[name] = getattr(settings, prefix+name, value)
    return setting
