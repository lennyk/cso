from django.shortcuts import render
from events.models import College


def home_page(request):
    return render(request, 'cso/home.html', {'user': request.user, 'colleges': College.objects.all()})


def thelda_page(request):
    return render(request, 'cso/thelda.html')


def constitution_page(request):
    return render(request, 'cso/constitution.html')
