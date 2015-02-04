from django.shortcuts import render
from events.models import CollegeCSOParticipation, Date
from datetime import datetime


def home_page(request):
    participations = CollegeCSOParticipation.objects.filter(cso_year='2015', attending=True)
    participations = sorted(participations, key=lambda p: p.college.college_name.lower())
    active_dates = Date.objects.filter(is_active=True).order_by('date')

    now = datetime.now()
    ticket_college_presale = {
        'date': datetime(2015, 2, 16, 10, 0, 0),
    }
    ticket_college_presale['days_until'] = (ticket_college_presale.get('date').date() - now.date()).days

    ticket_public_sale = {
        'date': datetime(2015, 3, 1, 10, 0, 0),
    }
    ticket_public_sale['days_until'] = (ticket_public_sale.get('date').date() - now.date()).days

    return render(request, 'cso/home.html', {'user': request.user,
                                             'participations': participations,
                                             'active_dates': active_dates,
                                             'ticket_college_presale': ticket_college_presale,
                                             'ticket_public_sale': ticket_public_sale,
                                             'now': now
                                             })


def constitution_page(request):
    return render(request, 'cso/constitution.html')
