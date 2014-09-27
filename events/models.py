from django.db import models


class Date(models.Model):
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    information = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.date)


class College(models.Model):
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    # TODO: location method combining city, state
    college_name = models.CharField(max_length=60)
    latin_dance_organization_name = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return '%s @ %s' % (self.latin_dance_organization_name, self.college_name)


class CollegeURL(models.Model):
    college = models.ForeignKey(College)
    # TODO: need choices here. Facebook, Website, etc.
    # TODO: url cleanup (remove after &)
    url_type = models.CharField(max_length=255)
    url = models.URLField()


class CollegeCSOAttendance(models.Model):
    # TODO: unique between cso_year and college
    # cso_year = models.IntegerField()
    college = models.ForeignKey(College)
    attending = models.BooleanField(default=False)
    performing = models.BooleanField(default=False)
    competing = models.BooleanField(default=False)
