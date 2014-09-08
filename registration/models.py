from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class Date(models.Model):
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    information = models.TextField()
    is_active = models.BooleanField(default=True)


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class RegistrantAvatar(models.Model):
    image = models.ImageField(storage=OverwriteStorage(), upload_to='registrant/avatar', blank=True, null=True)


class Registrant(models.Model):
    user = models.OneToOneField(User)
    avatar = RegistrantAvatar()
    # Not sure if this implicitly already happens because of the OneToOneField
    # ordering = ['user.first_name', 'user.last_name']
