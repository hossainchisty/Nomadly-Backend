from django.urls import include, path
from rest_framework import routers

from properties.views.location_viewset import LocationDropdownViewSet
from properties.views.property_viewset import AmenityViewSet, PropertyDropdownViewSet, PropertyFeatureViewSet, PropertyViewSet

router = routers.DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"amenities", AmenityViewSet, basename="amenities")
router.register(r"features", PropertyFeatureViewSet, basename="features")
router.register(
    r"dropdowns/locations", LocationDropdownViewSet, basename="location-dropdowns"
)
router.register(r"dropdowns", PropertyDropdownViewSet, basename="dropdowns")


urlpatterns = [
    path("", include(router.urls)),
]
