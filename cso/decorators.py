from django.contrib.auth.decorators import user_passes_test, login_required


registration_required = user_passes_test(lambda u: hasattr(u, 'registration'), login_url='registration_register')
registration_forbidden = user_passes_test(lambda u: not hasattr(u, 'registration'), login_url='registration_home')


def registration_and_login_required(function):
    return login_required(registration_required(function))


def registration_forbidden_and_login_required(function):
    return registration_forbidden(registration_required(function))
