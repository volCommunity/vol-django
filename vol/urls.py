from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico',
                                               permanent=False), name='favicon'),
    url('about', views.about, name='about'),
    url(r'^results/(?P<location>[\w\s+]+)/(?P<interests>[\w\s+]+)', views.results, name='results'),
    url(r'^job/(?P<id>[\d]+)', views.job, name='job')  # TODO: should this be a nice name (SEO etc)
]
