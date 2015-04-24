from datetime import datetime

from django.db import models
from django.contrib import messages
import stripe
from django.conf import settings
from allauth.account.models import EmailAddress

from cso.models import CSOUser
from events.models import College, TicketSales
from .utils import email_is_academic


class SavedCustomer(models.Model):
    user = models.OneToOneField(CSOUser, blank=False, null=False)
    stripe_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.user.email, self.stripe_id)


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

    def college_email_is_verified(self):
        for email in self.emails():
            if email.verified and email_is_academic(email.email):
                return True
        return False

    def college_message_is_verified(self):
        # since we have no human validation process in place consider everyone that's provided a message to be verified
        return self.college_verified_by_message()

    def college_verified_by_message(self):
        return self.college_verification_type == 'message'

    def college_verified_by_email(self):
        return self.college_verification_type == 'email'

    def college_verification_message(self):
        # message = CollegeVerificationMessage.objects.get(registration=self)
        # return message.message if message else None
        if CollegeVerificationMessage.objects.filter(registration=self).exists():
            return CollegeVerificationMessage.objects.get(registration=self).message
        else:
            return None

    def has_edu_email(self):
        return self.edu_email() is not None

    def edu_email(self):
        for email in self.emails():
            if email and email_is_academic(email.email):
                return email
        return None

    def has_ticket(self):
        return Ticket.objects.filter(registration=self).exists()

    def college_verified(self):
        if self.college_affiliated:
            if self.college_verified_by_email():
                return self.college_email_is_verified()
            if self.college_verified_by_message():
                return self.college_message_is_verified()
        return False

    def can_buy_ticket(self):
        if TicketSales.public_ticket_sale_is_open() and not self.has_ticket():
            return True
        if self.college_affiliated and self.college_verified() and TicketSales.student_ticket_sale_is_open() and not self.has_ticket():
            return True
        return False

    def can_refund_ticket(self):
        return self.has_ticket() and datetime.today().date() < TicketSales.ticket_refunds_close()

    def refund_ticket(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.retrieve(self.ticket.charge_id)
        charge.refunds.create()
        self.ticket.delete()

    @staticmethod
    def __send_notification_message(request, message, level=messages.INFO):
        messages.add_message(request, level, message)

    def notify_user_of_needed_registration_action(self, request):

        if self.has_ticket():
            return

        if self.college_affiliated:

            if self.college_verified_by_email() and not self.college_email_is_verified():
                self.__send_notification_message(request,
                                                 'Before you can buy your ticket you need to verify your academic email address. '
                                                 'Check your academic email inbox for the confirmation link.')
                return
            if self.college_verified_by_message() and not self.college_message_is_verified():
                self.__send_notification_message(request,
                                                 'Before you can buy your ticket we need to verify your academic approval message. '
                                                 'Please be patient as this is a manual process. '
                                                 'You will receive an email when you can come back and purchase your ticket.')
                return
            if not TicketSales.student_ticket_sale_is_open():
                self.__send_notification_message(request,
                                                 'Student ticket sales are not open yet. They will open on {}. '
                                                 'See you then!'.format(TicketSales.student_ticket_sale_datetime_human()))
                return
            if not TicketSales.public_ticket_sale_is_open():
                self.__send_notification_message(request,
                                                 'Student ticket sales are open! '
                                                 'Purchase your ticket by clicking Purchase Ticket below.',
                                                 messages.SUCCESS)
                return

        else:

            if not TicketSales.public_ticket_sale_is_open():
                self.__send_notification_message(request,
                                                 'Public ticket sales are not open yet. They will open on {}. '
                                                 'See you then!'.format(TicketSales.public_ticket_sale_datetime_human()))
                return

        self.__send_notification_message(request,
                                         'Public ticket sales are open! '
                                         'Purchase your ticket by clicking Purchase Ticket below.',
                                         messages.SUCCESS)


class Ticket(models.Model):
    registration = models.OneToOneField(Registration, blank=False, null=False)
    charge_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.registration.user.email, self.registration.user.get_full_name())


class CollegeVerificationMessage(models.Model):
    registration = models.OneToOneField(Registration)
    message = models.TextField(null=False, blank=False)
