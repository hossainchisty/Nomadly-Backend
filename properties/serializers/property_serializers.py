from rest_framework import serializers

from properties.models.basic_info import Amenity, PropertyTag
from properties.models.location_model import Location
from properties.models.project_image_models import ProjectImage
from properties.models.property_models import Property, PropertyFeature


class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = "__all__"

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = "__all__"


class PropertyTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTag
        fields = "__all__"


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    tag = PropertyTagSerializer()
    country = LocationSerializer()
    city = LocationSerializer()
    neighborhood = LocationSerializer()
    property_features = PropertyFeatureSerializer(many=True)
    amenities = AmenitySerializer(many=True)
    interior_images = PropertyImageSerializer(many=True)

    class Meta:
        model = Property
        fields = "__all__"


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyRetrieveSerializer(serializers.ModelSerializer):
    tag = PropertyTagSerializer()
    country = LocationSerializer()
    city = LocationSerializer()
    district = LocationSerializer()
    neighborhood = LocationSerializer()
    property_features = PropertyFeatureSerializer(many=True)
    architecture_images = PropertyImageSerializer(many=True)
    interior_images = PropertyImageSerializer(many=True)
    exterior_images = PropertyImageSerializer(many=True)

    class Meta:
        model = Property
        fields = "__all__"


class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "id",
        ]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class AmenityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name", "icon"]


class AmenityRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class AmenityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["name", "icon"]


class AmenityDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id"]


class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = "__all__"


class PropertyFeatureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ["name", "category", "is_premium"]


class PropertyFeatureRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = "__all__"


class PropertyFeatureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ["name", "category", "is_premium"]


class PropertyFeatureDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = ["id"]
