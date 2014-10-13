from django.db import models
from cso.models import CSOUser
from events.models import College
from allauth.account.models import EmailAddress
from .utils import email_is_academic


class Registration(models.Model):
    user = models.OneToOneField(CSOUser)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(
        max_length=30,
        help_text="We will sign you in at the event with your driver's license or other ID card so enter your first " +
                  "and last name exactly as it appears on your ID card."
    )

    COLLEGE_AFFILIATED_CHOICES = (
        (False, 'I do not belong to a college dance club or team.'),
        (True, 'I am an active member of a college dance club or team.'),
    )

    college_affiliated = models.BooleanField(default=False,
                                             choices=COLLEGE_AFFILIATED_CHOICES)

    college_group = models.ForeignKey(College, default=None, null=True, blank=True)

    COLLEGE_VERIFICATION_TYPE_CHOICES = (
        ('email', 'Verify by using a .edu email address.'),
        ('message', 'Verify by providing a written message.'),
    )
    college_verification_type = models.CharField(choices=COLLEGE_VERIFICATION_TYPE_CHOICES,
                                                 help_text='If you have a .edu email address, please use the email ' +
                                                           'address verification option. If you do not have a .edu ' +
                                                           'email address but are an active member of a college ' +
                                                           'dance club or team (coach, alumni, etc.) please choose ' +
                                                           'the message option and provide a brief explanation.',
                                                 max_length=12, default='email', null=True, blank=True)

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

    def registration_boolean_details(self):
        return [
            ('College Verified', self.college_verified()),
        ]

    def emails(self):
        emails = EmailAddress.objects.filter(user=self.user)
        for email in emails:
            email.is_academic = email_is_academic(email.email)
        return emails

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.user.get_full_name()

    def college_verified_email(self):
        for email in self.emails():
            if email.verified and email_is_academic(email.email):
                return True
        return False

    def college_verified_message(self):
        return False

    def college_verified(self):
        return self.college_verified_email() or self.college_verified_message()


class CollegeVerificationMessage(models.Model):
    registration = models.OneToOneField(Registration)
    message = models.TextField(null=False, blank=False)
