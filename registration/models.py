from django.db import models
from cso.models import CSOUser
from events.models import College


class Registration(models.Model):
    user = models.OneToOneField(CSOUser)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    college_affiliated = models.BooleanField(default=False)

    college_group = models.ForeignKey(College, default=None, null=True, blank=True)

    PARTNER_TYPE_CHOICES = (
        ('LD', 'Lead'),
        ('FW', 'Follow'),
    )
    partner_type = models.CharField('dance orientation', max_length=2, choices=PARTNER_TYPE_CHOICES)

    def registration_details(self):
        return [
            ('Full Name', self.get_full_name()),
            (self._meta.get_field_by_name('partner_type')[0].verbose_name.title(), self.get_partner_type_display()),
            ('School Affiliation', self.college_group if self.college_affiliated and self.college_group else 'None'),
        ]

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.user.get_full_name()
