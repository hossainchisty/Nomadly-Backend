from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from properties.models.basic_info import Amenity, PropertyTag
from properties.models.location_model import Location
from properties.models.property_feature import PropertyFeature
from properties.models.property_models import Property
from properties.serializers.dropdown_serializers import (
    AmenityDropdownSerializer,
    LocationDropdownSerializer,
    PropertyFeatureDropdownSerializer,
    PropertyTagDropdownSerializer,
)
from properties.serializers.property_serializers import (
    AmenityCreateSerializer,
    AmenityDeleteSerializer,
    AmenityRetrieveSerializer,
    AmenitySerializer,
    AmenityUpdateSerializer,
    PropertyCreateSerializer,
    PropertyDeleteSerializer,
    PropertyFeatureCreateSerializer,
    PropertyFeatureDeleteSerializer,
    PropertyFeatureRetrieveSerializer,
    PropertyFeatureSerializer,
    PropertyFeatureUpdateSerializer,
    PropertyRetrieveSerializer,
    PropertySerializer,
    PropertyUpdateSerializer,
)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "name",
    ]

    serializer_action_map = {
        "list": PropertySerializer,
        "create": PropertyCreateSerializer,
        "retrieve": PropertyRetrieveSerializer,
        "update": PropertyUpdateSerializer,
        "partial_update": PropertyUpdateSerializer,
        "delete": PropertyDeleteSerializer,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]

    serializer_action_map = {
        "list": AmenitySerializer,
        "create": AmenityCreateSerializer,
        "retrieve": AmenityRetrieveSerializer,
        "update": AmenityUpdateSerializer,
        "partial_update": AmenityUpdateSerializer,
        "delete": AmenityDeleteSerializer,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)


class PropertyFeatureViewSet(viewsets.ModelViewSet):
    queryset = PropertyFeature.objects.all()
    serializer_class = PropertyFeatureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "category"]

    serializer_action_map = {
        "list": PropertyFeatureSerializer,
        "create": PropertyFeatureCreateSerializer,
        "retrieve": PropertyFeatureRetrieveSerializer,
        "update": PropertyFeatureUpdateSerializer,
        "partial_update": PropertyFeatureUpdateSerializer,
        "delete": PropertyFeatureDeleteSerializer,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_serializer_class(self):
        return self.serializer_action_map.get(self.action, self.serializer_class)


class PropertyDropdownViewSet(viewsets.ViewSet):
    """ViewSet to return dropdown lists for property-related models."""

    @action(detail=False, methods=["get"])
    def features(self, request):
        """
        GET api/v1/properties/dropdowns/features/
        Returns all property features for dropdown
        """
        features = PropertyFeature.objects.all()
        serializer = PropertyFeatureDropdownSerializer(features, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def aminities(self, request):
        """
        GET api/v1/properties/dropdowns/aminities/
        Returns all property features for dropdown
        """
        features = Amenity.objects.all()
        serializer = AmenityDropdownSerializer(features, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def tags(self, request):
        """
        GET api/v1/properties/dropdowns/tags/
        Returns all property tags for dropdown
        """
        tags = PropertyTag.objects.all()
        serializer = PropertyTagDropdownSerializer(tags, many=True)
        return Response(serializer.data)
