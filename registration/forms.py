from django.forms import ModelForm
from .models import Registration


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'partner_type', 'college_affiliated', 'college_group']
