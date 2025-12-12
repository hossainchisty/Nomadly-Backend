from rest_framework import serializers

from properties.models.basic_info import Amenity, PropertyTag
from properties.models.location_model import Location
from properties.models.property_feature import PropertyFeature


class PropertyFeatureDropdownSerializer(serializers.ModelSerializer):
    """ Property feature dropdown serializer """
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = PropertyFeature
        fields = ["label", "value"]
        
class AmenityDropdownSerializer(serializers.ModelSerializer):
    """ Amenity dropdown serializer """
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = Amenity
        fields = ["label", "value"]


class PropertyTagDropdownSerializer(serializers.ModelSerializer):
    """ Property tag dropdown serializer """
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = PropertyTag
        fields = ["label", "value"]


class LocationDropdownSerializer(serializers.ModelSerializer):
    """ Location dropdown serializer """
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="id")

    class Meta:
        model = Location
        fields = ["label", "value"]
