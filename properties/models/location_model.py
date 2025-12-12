from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import BaseModel


class Location(BaseModel):
    """ Location model for properties """
    class LocationType(models.TextChoices):
        COUNTRY = "country", _("Country")
        CITY = "city", _("City")
        DISTRICT = "district", _("District")
        NEIGHBORHOOD = "neighborhood", _("Neighborhood")

    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )


    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]
        unique_together = ("name", "location_type",)

    def __str__(self):
        return f"{self.name} ({self.location_type})"
