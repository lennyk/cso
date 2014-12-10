from django.shortcuts import render
from events.models import CollegeCSOParticipation
from events.models import Date


def dates_page(request):
    active_dates = Date.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/dates.html', {'active_dates': active_dates})


def colleges_page(request):
    participations = CollegeCSOParticipation.objects.filter(cso_year='2015', attending=True)
    participations = sorted(participations, key=lambda p: p.college.college_name.lower())
    return render(request, 'events/colleges.html', {'participations': participations})
