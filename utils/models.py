from django.db import models


class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value is not None:
            if len(value) > self.max_length:
                value = value[: self.max_length - 3] + '...'
        return value
