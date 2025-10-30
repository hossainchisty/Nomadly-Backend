from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel, DeepDeleteMixin
from users.managers import AccountManager


class UserRole(models.IntegerChoices):
    ADMIN = 0, _("Admin")
    RENTER = 1, _("Renter")
    HOST = 2, _("Host")


class User(AbstractUser, BaseModel):
    """Custom user model that uses username as unique identifier (can store email or phone)."""

    role = models.IntegerField(choices=UserRole.choices, default=UserRole.RENTER)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    profile_picture = CloudinaryField("profile_pictures/", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AccountManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=~models.Q(email=None),
                name="unique_email_not_null",
            ),
            models.UniqueConstraint(
                fields=["phone_number"],
                condition=~models.Q(phone_number=None),
                name="unique_phone_not_null",
            ),
        ]


class Profile(BaseModel, DeepDeleteMixin):
    """Profile model to store additional user information."""

    class GenderChoice(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(
        max_length=10, choices=GenderChoice.choices, null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def calculate_completion_percentage(self):
        """
        Calculate the profile completion percentage based on filled fields.
        """
        fields_to_check = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.user.profile_picture,
            self.linkedin,
            self.website,
        ]
        completed_fields = sum(1 for field in fields_to_check if field)
        total_fields = len(fields_to_check)
        percentage = (completed_fields / total_fields) * 100
        self.profile_completion_percentage = int(percentage)
        self.is_profile_complete = percentage == 100
        self.save()
