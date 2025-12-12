from django.db import models
from django.utils.translation import gettext_lazy as _


class PropertyReview(models.Model):
    """ Property review model """
    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="property_reviews",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("property", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.user} for {self.property} - Rating: {self.rating}"