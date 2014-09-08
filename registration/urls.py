from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'registration.views.registration_home', name='registration_home'),
                       url(r'^login/$', 'registration.views.registration_login', name='registration_login'),
                       url(r'^logout/$', 'registration.views.logout', name='logout'),
)