from django.shortcuts import render
from events.models import CollegeCSOParticipation, Date


def home_page(request):
    participations = CollegeCSOParticipation.objects.filter(cso_year='2015', attending=True).order_by('college')
    participations = sorted(participations, key=lambda p: p.college.latin_dance_organization_name.lower())
    active_dates = Date.objects.filter(is_active=True).order_by('date')
    return render(request, 'cso/home.html', {'user': request.user,
                                             'participations': participations,
                                             'active_dates': active_dates})


def constitution_page(request):
    return render(request, 'cso/constitution.html')
