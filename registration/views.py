from django.shortcuts import render, redirect
from cso.decorators import registration_and_login_required, registration_forbidden_and_login_required
from .forms import RegistrationForm
from .models import Registration


# @registration_forbidden_and_login_required
def registration_register(request):
    next_page = request.GET.get('next', None)

    # a workaround because I can't get the annotation to work
    if Registration.objects.filter(user=request.user).exists():
        return redirect(next_page or 'registration_home')

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.save()
            return redirect(next_page or 'registration_home')
    else:
        data_from_user = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = RegistrationForm(initial=data_from_user)

    return render(request, 'registration/register.html', {'form': form})


@registration_and_login_required
def registration_update(request):
    existing_registration = Registration.objects.get(user=request.user)
    next_page = request.GET.get('next', None)
    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=existing_registration)
        if form.is_valid():
            form.save()
            return redirect(next_page or 'registration_home')
    else:
        form = RegistrationForm(instance=existing_registration)
    return render(request, 'registration/update.html', {'form': form})


@registration_and_login_required
def registration_home(request):
    return render(request, 'registration/home.html')
