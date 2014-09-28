from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'registration.views.registration_home', name='registration_home'),
    url(r'^register/$', 'registration.views.registration_register', name='registration_register'),
)
