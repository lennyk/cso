from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def registration_login(request):
    if request.user.is_authenticated():
        return redirect('registration_home')
    return render(request, 'login.html')


@login_required
def registration_home(request):
    return render(request, 'registration.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
