from django.contrib.auth.models import AbstractUser


class CSOUser(AbstractUser):

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return super(AbstractUser, self).__str__()
