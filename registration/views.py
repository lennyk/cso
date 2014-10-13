from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .forms import RegistrationForm
from .models import Registration, CollegeVerificationMessage


@login_required
def registration_update(request):
    existing_registration = Registration.objects.get(user=request.user)
    next_page = request.GET.get('next', None)

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=existing_registration)
        if form.is_valid():
            form.save()
            return redirect(next_page or 'registration_home')
    else:
        verification_message = None
        # if existing_registration:
        #     reg_dict = model_to_dict(existing_registration)
        #     if reg_dict['college_verification_type'] == 'email':
        #         # TODO: handle this somehow
        #         pass
        #     if reg_dict['college_verification_type'] == 'message':
        #         verification_message = CollegeVerificationMessage.objects.get(registration=existing_registration).message
        form = RegistrationForm(instance=existing_registration, verification_message=verification_message)
    return render(request, 'registration/update.html', {'form': form})


@login_required
def registration_home(request):
    return render(request, 'registration/home.html')
