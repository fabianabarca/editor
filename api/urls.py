from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"provider", views.ProviderViewSet)
router.register(r"feed", views.FeedViewSet)
router.register(r"gtfs/agency", views.AgencyViewSet)
router.register(r"gtfs/stops", views.StopViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
