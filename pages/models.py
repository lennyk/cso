from django.db import models


class Date(models.Model):
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    information = models.TextField()
    is_active = models.BooleanField(default=True)
