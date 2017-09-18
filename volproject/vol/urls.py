from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('about', views.about, name='about'),
    url(r'^job/(?P<job_id>[0-9]+)', views.job, name='job'),
    url(r'^organisation/(?P<organisation_id>[0-9]+)', views.organisation, name='organisation'),
    url(r'^site/(?P<site_id>[0-9]+)', views.site, name='site'),
    url(r'^label/(?P<label_id>[0-9]+)', views.label, name='label'),
]
