from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from properties.models.location_model import Location
from properties.serializers.dropdown_serializers import LocationDropdownSerializer


class LocationDropdownViewSet(viewsets.GenericViewSet):
    """
    Returns different location types for dropdowns.
    """

    @action(detail=False, methods=["get"])
    def countries(self, request):
        queryset = Location.objects.filter(location_type="country")
        serializer = LocationDropdownSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def cities(self, request):
        country_id = request.query_params.get("country_id")
        queryset = Location.objects.filter(location_type="city")
        if country_id:
            queryset = queryset.filter(parent_location_id=country_id)
        serializer = LocationDropdownSerializer(queryset, many=True)
        return Response(serializer.data)
