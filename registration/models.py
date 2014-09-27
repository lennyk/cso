from django.db import models
from cso.models import CSOUser


class Registration(models.Model):
    user = models.OneToOneField(CSOUser)
    PARTNER_TYPE_CHOICES = (
        ('LD', 'Lead'),
        ('FW', 'Follow'),
    )
    partner_type = models.CharField(max_length=2, choices=PARTNER_TYPE_CHOICES)

    def __str__(self):
        return self.user.get_full_name()
