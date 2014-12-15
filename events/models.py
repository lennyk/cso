from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse


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
