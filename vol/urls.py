from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('about', views.about, name='about'),
    url(r'^results/(?P<subject>[a-zA-Z0-9+]+)/(?P<location>[a-zA-Z+]+)/(?P<interests>[a-zA-Z+]+)', views.results,
        name='results'),
    url(r'^job/(?P<job_id>[0-9]+)', views.job, name='job'),
    url(r'^organisation/(?P<organisation_id>[0-9]+)', views.organisation, name='organisation'),
    url(r'^site/(?P<site_id>[0-9]+)', views.site, name='site'),
    url(r'^label/(?P<label_id>[0-9]+)', views.label, name='label'),
]
