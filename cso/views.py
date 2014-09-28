from django.shortcuts import render


def home_page(request):
    return render(request, 'cso/home.html', {'user': request.user})


def thelda_page(request):
    return render(request, 'cso/thelda.html')


def constitution_page(request):
    return render(request, 'cso/constitution.html')
