from django.shortcuts import render
from events.models import College, CollegeCSOParticipation, CollegeURL, Date

def home_page(request):
    # TODO: intelligently filter the colleges
    colleges = []
    for college in College.objects.all():
        colleges.append({
            'college': college,
            'participation': CollegeCSOParticipation.objects.get(college=college),
            'URLs': CollegeURL.objects.filter(college=college),
        })
    active_dates = Date.objects.filter(is_active=True).order_by('date')
    return render(request, 'cso/home.html', {'user': request.user,
                                             'colleges': colleges,
                                             'active_dates': active_dates})


def constitution_page(request):
    return render(request, 'cso/constitution.html')
