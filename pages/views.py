from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')


def thecso_page(request):
    return render(request, 'thecso.html')


def constitution_page(request):
    return render(request, 'constitution.html')


def dates_page(request):
    return render(request, 'dates.html')


def colleges_page(request):
    return render(request, 'colleges.html')
