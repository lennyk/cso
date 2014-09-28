from django.shortcuts import render, redirect
from cso.decorators import registration_and_login_required, registration_forbidden_and_login_required
from .forms import RegistrationForm


# @registration_forbidden_and_login_required
def registration_register(request):
    form = RegistrationForm(request.POST or None)
    next_page = request.GET.get('next', None)

    if form.is_valid():
        registration = form.save(commit=False)
        registration.user = request.user
        registration.save()
        return redirect(next_page or 'registration_home')

    return render(request, 'registration/register.html', {'form': form})


@registration_and_login_required
def registration_update(request):
    pass


@registration_and_login_required
def registration_home(request):
    return render(request, 'registration/home.html')
