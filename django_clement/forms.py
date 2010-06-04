from django.forms import *
from django.db import models

class ModelChangeForm(ModelForm):
    def has_changed_instance(self):
        if self.instance.pk is None:
            return True
        else:
            changed = False

            for field_name in self.cleaned_data:
                try:
                    field = self.instance._meta.get_field_by_name(field_name)[0]
                    if isinstance(field, models.FileField):
                        changed = self.cleaned_data[field_name] is not None
                    else:
                        changed = getattr(self.instance, field_name) != self.cleaned_data[field_name]

                    if changed:
                        break
                except models.FieldDoesNotExist:
                    pass

            return changed

