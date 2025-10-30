from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from base.models import DeepDeleteMixin
from properties.models.location_model import Location


class PropertyTag(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Amenity(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class PropertyBasicInformation(DeepDeleteMixin, models.Model):
    class UnitTypeChoices(models.TextChoices):
        APARTMENT = "apartment", _("Apartment")
        VILLA = "villa", _("Villa")
        TOWNHOUSE = "townhouse", _("Townhouse")
        PENTHOUSE = "penthouse", _("Penthouse")
        DUPLEX = "duplex", _("Duplex")
        HOTEL_ROOM = "hotel_room", _("Hotel Room")
        HOME_OFFICE = "home_office", _("Home Office")
        OFFICE = "office", _("Office")
        STUDIO = "studio", _("Studio")

    class AreaUnit(models.TextChoices):
        SQUARE_FEET = "sqft", "Square Feet"
        SQUARE_METERS = "sqm", "Square Meters"
        ACRES = "acres", "Acres"
        HECTARES = "hectares", "Hectares"

    class ProjectStatusChoices(models.TextChoices):
        CONSTRUCTION = "construction", _("Under Construction")
        COMPLETED = "completed", _("Completed")
        PLANNED = "planned", _("Planned")

    class PropertyBedroomChoices(models.TextChoices):
        ONE_BEDROOM = "1_bedroom", _("1 Bedroom")
        TWO_BEDROOM = "2_bedroom", _("2 Bedrooms")
        THREE_BEDROOM = "3_bedroom", _("3 Bedrooms")
        FOUR_BEDROOM = "4_bedroom", _("4 Bedrooms")
        FIVE_PLUS_BEDROOM = "5_plus_bedroom", _("5+ Bedrooms")
        PENTHOUSE = "penthouse", _("Penthouse")
        STUDIO = "studio", _("Studio")
        DUPLEX = "duplex", _("Duplex")

    class PropertyBathroomChoices(models.TextChoices):
        ONE_BATHROOM = "1_bathroom", _("1 Bathroom")
        TWO_BATHROOM = "1.5_bathroom", _("1.5 Bathrooms")
        THREE_BATHROOM = "bathroom", _("2 Bathrooms")
        THREE_PLUS_BATHROOM = "2.5_bathroom", _("2.5 Bathrooms")

    property_name = models.CharField(max_length=150, unique=True)
    tag = models.ForeignKey(
        PropertyTag, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=ProjectStatusChoices.choices,
        default=ProjectStatusChoices.CONSTRUCTION,
    )
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"location_type": "city"},
        related_name="city_properties",
    )
    country = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"location_type": "country"},
        related_name="country_properties",
    )
    neighborhood = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"location_type": "neighborhood"},
        related_name="neighborhood_properties",
    )

    unit_type = models.CharField(
        max_length=50,
        choices=UnitTypeChoices.choices,
        default=UnitTypeChoices.APARTMENT,
    )

    bedrooms = models.CharField(
        max_length=50,
        choices=PropertyBedroomChoices.choices,
        default=PropertyBedroomChoices.ONE_BEDROOM,
    )
    bathrooms = models.CharField(
        max_length=50,
        choices=PropertyBathroomChoices.choices,
        default=PropertyBathroomChoices.ONE_BATHROOM,
    )

    max_guests = models.CharField(max_length=50, null=True, blank=True)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="amenities")
    view_count = models.PositiveIntegerField(default=0)

    build_year = models.PositiveIntegerField(null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)

    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.property_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.property_name
