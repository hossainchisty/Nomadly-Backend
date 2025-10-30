from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for user_management instead of usernames.
    """

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have either an email or phone number")

        email = None

        # Detect if it's an email or phone number
        if "@" in username:
            email = self.normalize_email(username)
            user = self.model(email=email, username=username, **extra_fields)

        else:
            user = self.model(phone_number=username, username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)
