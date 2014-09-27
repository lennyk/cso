from django.shortcuts import render
from cso.decorators import registration_and_login_required


def registration_register(request):
    return render(request, 'registration/register.html')


@registration_and_login_required
def registration_home(request):
    return render(request, 'registration/dashboard.html')
