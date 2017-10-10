from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'labels', views.LabelViewSet)
router.register(r'organisations', views.OrganisationViewSet)
router.register(r'sites', views.SiteViewSet)
router.register(r'jobs', views.JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # YOLO clients who do not care about versioning:
    url(r'', include(router.urls)),

    # Explicit version for the more discerning clients:
    url(r'^/(?P<version>v[0-9+].[0-9]+.[0-9]+)?/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
