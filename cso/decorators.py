from django.contrib.auth.decorators import user_passes_test, login_required


# TODO: check if the user has a Registration instead of is_active
# TODO: change login_url to the Registration form
registration_required = user_passes_test(lambda u: u.is_active, login_url='/profile/not_active')


def registration_and_login_required(function):
    return login_required(registration_required(function))
