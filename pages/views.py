from django.shortcuts import render

from events.models import Date


def home_page(request):
    return render(request, 'pages/home.html', {'user': request.user})


def thelda_page(request):
    return render(request, 'pages/thelda.html')


def constitution_page(request):
    return render(request, 'pages/constitution.html')


def dates_page(request):
    active_dates = Date.objects.filter(is_active=True).order_by('date')
    return render(request, 'pages/dates.html', {'active_dates': active_dates})


def colleges_page(request):
    return render(request, 'pages/colleges.html')
