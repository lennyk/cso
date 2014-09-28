from django.contrib import admin
from events.models import Date, College, CollegeURL, CollegeCSOParticipation


class DateAdmin(admin.ModelAdmin):
    class Meta:
        model = Date


class CollegeAdmin(admin.ModelAdmin):
    class Meta:
        model = College


class CollegeURLAdmin(admin.ModelAdmin):
    class Meta:
        model = CollegeURL


class CollegeCSOParticipationAdmin(admin.ModelAdmin):
    class Meta:
        model = CollegeCSOParticipation


admin.site.register(Date, DateAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(CollegeURL, CollegeURLAdmin)
admin.site.register(CollegeCSOParticipation, CollegeCSOParticipationAdmin)
