from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from properties.models.basic_info import PropertyBasicInformation
from properties.models.project_image_models import ProjectImage
from properties.models.property_feature import PropertyFeature
from users.models import User


class Property(BaseModel, PropertyBasicInformation):
    class PropertyTypeChoices(models.TextChoices):
        APARTMENT = "apartment", _("Apartment")
        VILLA = "villa", _("Villa")
        TOWNHOUSE = "townhouse", _("Townhouse")
        PENTHOUSE = "penthouse", _("Penthouse")
        DUPLEX = "duplex", _("Duplex")
        HOTEL_ROOM = "hotel_room", _("Hotel Room")
        HOME_OFFICE = "home_office", _("Home Office")
        OFFICE = "office", _("Office")
        STUDIO = "studio", _("Studio")
        WAREHOUSE = "warehouse", _("Warehouse")
        FACTORY = "factory", _("Factory")
        RETAIL = "retail", _("Retail")
        LAND = "land", _("Land")
        FARM = "farm", _("Farm")
        GARAGE = "garage", _("Garage")

    class ApprovalStatusChoices(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")
        IN_REVIEW = "in_review", _("In Review")
        ON_HOLD = "on_hold", _("On Hold")
        NEEDS_REVISION = "needs_revision", _("Needs Revision")
        CANCELLED = "cancelled", _("Cancelled")

    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="" "properties"
    )
    listed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="listed_by"
    )
    property_type = models.CharField(
        max_length=50,
        choices=PropertyTypeChoices.choices,
        default=PropertyTypeChoices.APARTMENT,
    )
    property_features = models.ManyToManyField(
        PropertyFeature, blank=True, related_name="properties"
    )

    approval_status = models.CharField(
        max_length=30,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.DRAFT,
    )

    interior_images = models.ManyToManyField(
        ProjectImage, related_name="interior_projects"
    )

    monthly_rent = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, default=0
    )
    service_fee = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, default=0
    )
    commission_percentage = models.DecimalField(
        max_digits=6, decimal_places=2, default=0
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["approval_status"]),
            models.Index(fields=["property_type"]),
        ]

    def __str__(self):
        return f"{self.property_name} - {self.city}, {self.country}"
