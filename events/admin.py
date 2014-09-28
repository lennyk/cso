from django.contrib import admin
from events.models import Date


class DateAdmin(admin.ModelAdmin):
    class Meta:
        model = Date


admin.site.register(Date, DateAdmin)
