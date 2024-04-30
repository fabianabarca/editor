from gtfs.models import Provider, Feed, Agency, Stop
from rest_framework import permissions, viewsets

from .serializers import *


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows on board equipment to be viewed or edited.
    """

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows on board equipment to be viewed or edited.
    """

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows on board equipment to be viewed or edited.
    """

    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class StopViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows on board equipment to be viewed or edited.
    """

    queryset = Stop.objects.all()
    serializer_class = StopSerializer
