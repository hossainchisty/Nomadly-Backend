from django.contrib import admin

from properties.models.basic_info import PropertyTag
from properties.models.location_model import Location
from properties.models.project_image_models import ProjectImage
from properties.models.property_feature import PropertyFeature
from properties.models.property_models import Property
from properties.models.property_review import PropertyReview


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "property_name",
        "property_type",
        "created_at",
    )
    list_filter = ("property_type", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "location_type")
    list_filter = ("location_type",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(PropertyTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("image",)


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(PropertyReview)
class PropertyReviewAdmin(admin.ModelAdmin):
    list_display = ("property", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("property__property_name", "user__username")
    ordering = ("-created_at",)
