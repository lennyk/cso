from datetime import datetime

from django.shortcuts import render
from django.contrib import messages

from events.models import CollegeCSOParticipation, Date, TicketSales


def home_page(request):
    ticket_sale_delay_message = (
        'We apologize for the delay in opening ticket sales. '
        'We\'re working hard to have it ready for you and we appreciate your enthusiasm! '
        'Student ticket sales will go up on <strong>{}</strong>.'
    )

    participations = CollegeCSOParticipation.objects.filter(cso_year='2015', attending=True)
    participations = sorted(participations, key=lambda p: p.college.college_name.lower())
    active_dates = Date.objects.filter(is_active=True).order_by('date')

    ticket_college_presale = {
        'date': TicketSales.student_ticket_sale_datetime(),
        'days_until': TicketSales.days_until_student_ticket_sale()
    }

    ticket_public_sale = {
        'date': TicketSales.public_ticket_sale_datetime(),
        'days_until': TicketSales.days_until_public_ticket_sale()
    }

    ticket_sales_are_open = TicketSales.public_ticket_sale_is_open() or TicketSales.student_ticket_sale_is_open()

    if not ticket_sales_are_open:
        messages.add_message(request, messages.WARNING, ticket_sale_delay_message.format(TicketSales.student_ticket_sale_datetime_human()))
    return render(request, 'cso/home.html', {
        'user': request.user,
        'participations': participations,
        'active_dates': active_dates,
        'ticket_college_presale': ticket_college_presale,
        'ticket_public_sale': ticket_public_sale,
        'ticket_sales_are_open': ticket_sales_are_open,
        'now': datetime.now()
    })


def constitution_page(request):
    return render(request, 'cso/constitution.html')
