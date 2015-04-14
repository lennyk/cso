from django.contrib import admin

from .models import Registration, CollegeVerificationMessage, SavedCustomer, Ticket


admin.site.register(Registration)
admin.site.register(CollegeVerificationMessage)
admin.site.register(SavedCustomer)
admin.site.register(Ticket)