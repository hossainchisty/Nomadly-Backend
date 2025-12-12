
from django.db import models


class PropertyFeature(models.Model):
    """ Property feature model """

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, null=True, blank=True, choices=[
        ("indoor", "Indoor"),
        ("outdoor", "Outdoor"),
        ("safety", "Safety"),
        ("amenities", "Amenities"),
        ("parking", "Parking"),
        ("fitness", "Fitness"),
        ("pets", "Pets"),
        ("firesafety", "Fire Safety"),
        ("other", "Other"),
    ])
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name