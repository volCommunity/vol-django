from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico',
                                               permanent=False), name='favicon'),
    url('about', views.about, name='about'),
    url(r'^results/(?P<location>[\w\s+]+)/(?P<interests>[\w\s+]+)', views.results, name='results'),
    url(r'^jobs/(?P<slug>[\d\w-]+)', views.job, name='job'),  # TODO: should this be a nice name (SEO etc)

    url(r'^login/?$', auth_views.login, name='login'),
    url(r'^logout/?$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    url(r'^settings/?$', views.settings, name='settings'),
    url(r'^settings/password/?$', views.password, name='password'),
]
