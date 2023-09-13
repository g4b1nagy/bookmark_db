from django.db import models

from utils.models import TruncatingCharField


class Bookmark(models.Model):
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    icon = models.FileField(blank=True)
    name = TruncatingCharField(max_length=256)
    url = models.URLField(max_length=2048, unique=True)
    labels = models.ManyToManyField('Label', blank=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    name = TruncatingCharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
