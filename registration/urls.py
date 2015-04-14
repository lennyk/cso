from django.conf.urls import patterns, url

from .views import PurchaseTicketView, RefundTicketView


urlpatterns = patterns(
    '',
    url(r'^$', 'registration.views.registration_home', name='registration_home'),
    url(r'^update/$', 'registration.views.registration_update', name='registration_update'),
    url(r'^purchase_ticket/$', PurchaseTicketView.as_view(), name='purchase_ticket'),
    url(r'^refund_ticket/$', RefundTicketView.as_view(), name='refund_ticket'),
)
