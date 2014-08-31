from django.shortcuts import render
from pages.models import Date


def home_page(request):
    return render(request, 'home.html')


def thecso_page(request):
    return render(request, 'thecso.html')


def constitution_page(request):
    return render(request, 'constitution.html')


def dates_page(request):
    active_dates = Date.objects.filter(is_active=True)
    return render(request, 'dates.html', {'active_dates': active_dates})


def colleges_page(request):
    return render(request, 'colleges.html')
