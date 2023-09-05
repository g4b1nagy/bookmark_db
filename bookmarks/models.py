from django.db import models


class Label(models.Model):
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    icon = models.FileField(blank=True)
    name = models.CharField(max_length=256)
    url = models.URLField(max_length=2048, unique=True)
    labels = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        return self.name
