from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils.dateformat import DateFormat


class TicketSales(object):

    @classmethod
    def student_ticket_sale_datetime(cls):
        return datetime.combine(Date.objects.get(id=1).date, Date.objects.get(id=1).time)

    @classmethod
    def public_ticket_sale_datetime(cls):
        return datetime.combine(Date.objects.get(id=2).date, Date.objects.get(id=2).time)

    @classmethod
    def ticket_refunds_close(cls):
        return Date.objects.get(id=4).date

    @classmethod
    def student_ticket_sale_datetime_human(cls):
        date = DateFormat(cls.student_ticket_sale_datetime())
        return date.format('l, F jS') + ' at ' + date.format('g:i A')

    @classmethod
    def public_ticket_sale_datetime_human(cls):
        date = DateFormat(cls.public_ticket_sale_datetime())
        return date.format('l, F jS') + ' at ' + date.format('g:i A')

    @classmethod
    def student_ticket_sale_is_open(cls):
        return cls.student_ticket_sale_datetime() < datetime.now()

    @classmethod
    def public_ticket_sale_is_open(cls):
        return cls.public_ticket_sale_datetime() < datetime.now()

    @classmethod
    def days_until_student_ticket_sale(cls):
        if cls.student_ticket_sale_is_open():
            return 0
        return (cls.student_ticket_sale_datetime().date() - datetime.now().date()).days

    @classmethod
    def days_until_public_ticket_sale(cls):
        if cls.public_ticket_sale_is_open():
            return 0
        return (cls.public_ticket_sale_datetime().date() - datetime.now().date()).days


class Date(models.Model):
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.date)


class College(models.Model):
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2, default='CA')
    college_name = models.CharField(max_length=80)
    latin_dance_organization_name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s @ %s' % (self.latin_dance_organization_name, self.college_name)

    def location(self):
        return '%s, %s' % (self.city, self.state)

    def listing_url(self):
        return reverse('home') + "#" + slugify(self.__str__())


class CollegeURL(models.Model):
    college = models.ForeignKey(College)
    URL_TYPE_CHOICES = (
        ("facebook", "Facebook"),
        ("website", "Website"),
        ("youtube", "YouTube"),
    )
    # TODO: url cleanup (remove after &)
    url_type = models.CharField(choices=URL_TYPE_CHOICES, max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.url

    class Meta:
        unique_together = (
            ("college", "url_type"),
        )
        ordering = ['url_type']


class CollegeCSOParticipation(models.Model):
    CSO_YEAR_CHOICES = (
        (2015, '2015'),
    )
    cso_year = models.IntegerField(choices=CSO_YEAR_CHOICES, default=CSO_YEAR_CHOICES[0][1])  # default='2015'
    college = models.ForeignKey(College)
    attending = models.BooleanField(default=False)
    performing = models.BooleanField(default=False)
    competing = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s Participation' % (self.college, self.cso_year)

    class Meta:
        unique_together = (
            ("college", "cso_year"),
        )
