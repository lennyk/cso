# based on:
# * https://github.com/pennersr/django-allauth/issues/215#issuecomment-25511647
# * http://stackoverflow.com/a/24358708
# although I think my changes make the solution more elegant :)

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.conf import settings


class CSOSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email_address = sociallogin.account.extra_data['email']
        user_model = get_user_model()
        users = user_model.objects.filter(email=email_address)
        if users:
            perform_login(request, users[0], email_verification=settings.ACCOUNT_EMAIL_VERIFICATION)
            raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))
