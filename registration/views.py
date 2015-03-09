from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView
import stripe

from allauth.account.adapter import get_adapter

from .forms import RegistrationForm
from .models import Registration, SavedCustomer, Ticket
from .forms import StripeForm


@login_required
def registration_update(request):
    existing_registration = Registration.objects.get(user=request.user)
    next_page = request.GET.get('next', None)

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=existing_registration)
        if form.is_valid():
            form.save()
            # send an email to verify edu email
            if request.user.registration.college_verified_by_email() and not request.user.registration.college_verified():
                request.user.registration.edu_email().send_confirmation(request)
                get_adapter().add_message(
                    request,
                    messages.INFO,
                    'account/messages/'
                    'email_confirmation_sent.txt',
                    {'email': request.user.registration.edu_email().email}
                )
            return redirect(next_page or 'registration_home')
    else:
        verification_message = None
        # if existing_registration:
        # reg_dict = model_to_dict(existing_registration)
        # if reg_dict['college_verification_type'] == 'email':
        #         # TODO: handle this somehow
        #         pass
        #     if reg_dict['college_verification_type'] == 'message':
        #         verification_message = CollegeVerificationMessage.objects.get(registration=existing_registration).message
        form = RegistrationForm(instance=existing_registration, verification_message=verification_message)
    return render(request, 'registration/update.html', {'form': form})


@login_required
def registration_home(request):
    request.user.registration.notify_user_of_needed_registration_action(request)
    return render(request, 'registration/home.html', {'registration': request.user.registration})


def get_customer(user):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if hasattr(user, 'savedcustomer'):
        try:
            return stripe.Customer.get(user.savedcustomer)
        except:
            user.savedcustomer.delete()
    customer = stripe.Customer.create(description=user, email=user.email)
    customer.save()
    savedcustomer = SavedCustomer(user=user, stripe_id=customer.id)
    savedcustomer.save()
    return customer


class StripeMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class PurchaseTicketView(StripeMixin, FormView):
    template_name = 'registration/purchase_ticket.html'
    form_class = StripeForm
    success_url = reverse_lazy('registration_home')

    def form_valid(self, form):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        customer = get_customer(self.request.user)
        customer.sources.create(source=form.cleaned_data['stripe_token'])

        charge = stripe.Charge.create(
            amount=2500,
            currency='usd',
            customer=customer,
            description='Collegiate Salsa Open 2015 full pass for {}'.format(self.request.user),
            statement_descriptor='Collegiate Salsa Open',
            # receipt_email=True,
        )
        ticket = Ticket(registration=self.request.user.registration, charge_id=charge.id)
        ticket.save()

        messages.add_message(
            self.request, messages.SUCCESS,
            'Success! You\'ve purchased your ticket, let\'s dance!'
        )

        return super(PurchaseTicketView, self).form_valid(form)


class RefundTicketView(TemplateView):
    template_name = 'registration/refund_ticket.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        registration = request.user.registration
        if registration.can_refund_ticket():
            registration.refund_ticket()
            messages.add_message(request, messages.INFO, 'Your ticket has been refunded. We\'re sorry you couldn\'t make it!')
        return redirect('registration_home')
