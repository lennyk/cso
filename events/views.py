from django.shortcuts import render
from events.models import College, CollegeCSOParticipation, CollegeURL
from events.models import Date


def dates_page(request):
    active_dates = Date.objects.filter(is_active=True).order_by('date')
    return render(request, 'events/dates.html', {'active_dates': active_dates})


def colleges_page(request):
    # TODO: intelligently filter the colleges
    colleges = []
    for college in College.objects.all():
        colleges.append({
            'college': college,
            'participation': CollegeCSOParticipation.objects.get(college=college),
            'URLs': CollegeURL.objects.filter(college=college),
        })
    return render(request, 'events/colleges.html', {'colleges': colleges})
