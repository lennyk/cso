from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, MinLengthValidator
from .models import Registration, CollegeVerificationMessage
from allauth.account.models import EmailAddress


def validate_edu_email(email):
    if not email.endswith(".edu"):
        raise ValidationError('%s is not a .edu email address.' % email)


def validate_unique_email(email):
    if EmailAddress.objects.filter(email=email).exists():
        raise ValidationError('The email address %s is already registered.', email)


class NotBlankValidator(MinLengthValidator):
    message = "This field cannot be blank."

validate_not_blank = NotBlankValidator(1)


class RegistrationForm(forms.ModelForm):
    edu_email = forms.EmailField(label='College email address', required=False)
    verification_message = forms.CharField(label='Verification Message', widget=forms.Textarea, required=False)

    def __init__(self, *args, edu_email=None, verification_message=None, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # overriding here to allow initializing non-model fields
        if edu_email:
            self.fields['edu_email'].initial = edu_email
        if verification_message:
            self.fields['verification_message'].initial = verification_message

    class Meta:
        model = Registration
        fields = [
            'first_name',
            'last_name',
            'partner_type',
            'college_affiliated',
            'college_group',
            'college_verification_type',
            'edu_email',
            'verification_message',
        ]
        widgets = {
            'college_affiliated': forms.RadioSelect,
            'college_verification_type': forms.RadioSelect,
        }

    class Media:
        css = {
            'all': ('registration.css',)
        }
        js = ('registration.js',)

    def save(self, commit=True):
        # save the Registration
        super(RegistrationForm, self).save()

        # add/update/delete data relating to non-Registration models in this form
        if self.instance.college_affiliated:
            if self.instance.college_verification_type == 'email':
                EmailAddress.objects.create(user=self.instance.user, email=self.cleaned_data['edu_email']).save()
                # if message exists for this user, delete it
                CollegeVerificationMessage.objects.filter(registration=self.instance).delete()
            if self.instance.college_verification_type == 'message':
                message, created = CollegeVerificationMessage.objects.get_or_create(registration=self.instance)
                message.message = self.cleaned_data['verification_message']
                message.save()
        else:
            # if message exists for this user, delete it
            CollegeVerificationMessage.objects.filter(registration=self.instance).delete()

    def signup(self, request, user):
        # reg = Registration(user=user)
        # reg.first_name = self.cleaned_data['first_name']
        # reg.last_name = self.cleaned_data['last_name']
        # reg.partner_type = self.cleaned_data['partner_type']
        # reg.college_affiliated = self.cleaned_data['college_affiliated']
        # reg.college_group = self.cleaned_data['college_group']
        # reg.save()
        # TODO: test this - used to signup new user through allauth
        # self.instance.user = user
        # self.cleaned_data['user'] = user
        # RegistrationForm(self).save()
        # RegistrationForm(self).clean()
        super(RegistrationForm, self).save()

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        # cleaned_data = forms.ModelForm(self).clean()
        college_affiliated = cleaned_data.get('college_affiliated')

        # college_affiliated must be set
        if college_affiliated is None:
            self.add_error('college_affiliated', ValidationError('Select a choice.'))

        if not college_affiliated:
            # remove all possibly set values that only apply to college affiliated users
            cleaned_data['college_group'] = None
            cleaned_data['college_verification_type'] = None
            cleaned_data['edu_email'] = None
            cleaned_data['verification_message'] = None
        else:
            # if user has selected college_affiliated, require a college selection
            college_group = cleaned_data.get('college_group')
            if not college_group:
                self.add_error('college_group', ValidationError('Select a College group.'))

            # if user has selected college_affiliated, require a college selection
            college_verification_type = cleaned_data.get('college_verification_type')
            if not college_verification_type:
                self.add_error('college_verification_type', ValidationError('Select a verification method.'))

            if college_verification_type == 'email':
                # validate email, ensure message is empty
                edu_email = cleaned_data.get('edu_email')
                cleaned_data['verification_message'] = None
                try:
                    validate_email(edu_email)
                    validate_edu_email(edu_email)
                    validate_unique_email(edu_email)
                except ValidationError as e:
                    self.add_error('edu_email', e)
            else:
                # ensure email is empty, validate message
                cleaned_data['edu_email'] = None
                verification_message = cleaned_data.get('verification_message')
                try:
                    validate_not_blank(verification_message)
                except ValidationError as e:
                    self.add_error('verification_message', e)

        if self.is_valid():
            return cleaned_data
