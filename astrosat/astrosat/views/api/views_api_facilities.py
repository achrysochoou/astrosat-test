from rest_framework import generics, permissions, viewsets
from django_filters import Filter

from astrosat.models import Facility
from astrosat.serializers import FacilitySerializer


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = FacilitySerializer
    queryset = Facility.objects.active()
    # filter_fields = ('status',)
