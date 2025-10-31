from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
        }

    def validate(self, attrs):
        username = attrs.get("username")

        # Password match check
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Email or phone check
        if "@" in username:
            # It is email
            if User.objects.filter(email=username).exists():
                raise serializers.ValidationError(
                    {"username": "User with this email already exists."}
                )
        else:
            # It is phone number
            if User.objects.filter(phone_number=username).exists():
                raise serializers.ValidationError(
                    {"username": "User with this phone number already exists."}
                )

        return attrs

    def create(self, validated_data):
        # Remove password2
        validated_data.pop("password2")
        username = validated_data.pop("username")
        password = validated_data.pop("password")

        # Use your custom create_user() logic (handles email/phone automatically)
        user = User.objects.create_user(
            username=username, password=password, **validated_data
        )

        # Create related profile if needed
        Profile.objects.create(user=user)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile_completion_percentage = serializers.ReadOnlyField(
        source="profile.profile_completion_percentage"
    )
    is_profile_complete = serializers.ReadOnlyField(
        source="profile.is_profile_complete"
    )
    full_name = serializers.ReadOnlyField(source="get_full_name")
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "profile_picture",
            "profile_completion_percentage",
            "is_profile_complete",
            "role",
            "is_active",
            "is_verified",
            "date_joined",
            "last_login",
        )
        read_only_fields = (
            "id",
            "email",
            "profile_completion_percentage",
            "is_profile_complete",
        )

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        user = User.objects.create_user(**validated_data)
        # Auto-create profile
        Profile.objects.create(user=user, **(profile_data or {}))
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "profile_completion_percentage",
            "is_profile_complete",
        )

    def update(self, instance, validated_data):
        request = self.context.get("request")
        profile_data = validated_data.pop("profile", None)

        # Store old values for comparison
        old_email = instance.email
        old_phone = instance.phone_number
        old_username = instance.username
        old_role = instance.role

        # Apply normal update
        user = super().update(instance, validated_data)

        # --- Admin user logic ---
        if request and request.user.is_staff:
            new_email = validated_data.get("email", old_email)
            new_phone = validated_data.get("phone_number", old_phone)

            # If username equals old email/phone, update it too
            if old_username == old_email and new_email != old_email:
                user.username = new_email
            elif old_username == old_phone and new_phone != old_phone:
                user.username = new_phone
            user.save()

        # --- Non-admin logic ---
        else:
            new_email = validated_data.get("email", old_email)
            new_phone = validated_data.get("phone_number", old_phone)
            new_role = validated_data.get("role", old_role)

            if old_username in [old_email, old_phone]:
                if new_email != old_email or new_phone != old_phone:
                    raise serializers.ValidationError(
                        "You cannot change your email or phone number because it matches your username."
                    )
            if old_role != new_role:
                raise serializers.ValidationError("Role Can change by admin only")

        # --- Profile sync ---
        if profile_data:
            Profile.objects.update_or_create(user=user, defaults=profile_data)

        # --- Recalculate completion percentage ---
        if hasattr(user.profile, "calculate_completion_percentage"):
            user.profile.calculate_completion_percentage()

        return user


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserDropDownSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="username")
    value = serializers.IntegerField(source="id")

    class Meta:
        model = User
        fields = ["label", "value"]


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for Permission model"""

    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "content_type"]


class PermissionDropDownSerializer(serializers.ModelSerializer):
    """Serializer for Permission model"""

    label = serializers.CharField(source="name")
    value = serializers.IntegerField(source="id")

    class Meta:
        model = Permission
        fields = ["label", "value"]


class SetUserRoleSerializer(serializers.Serializer):
    """Assign a role to multiple users"""

    user_ids = serializers.ListField(child=serializers.CharField(), write_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=True
    )

    def create(self, validated_data):
        user_ids = validated_data.get("user_ids", [])
        group = validated_data.get("group")

        updated_users = []

        for uid in user_ids:
            try:
                user = User.objects.get(id=uid)
                user.groups.set([group])
                user.save()
                updated_users.append(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"user_id": f"User with id {uid} not found"}
                )

        return updated_users


class SetUserPermissionsSerializer(serializers.Serializer):
    """This serializer represent to add permission into a user"""

    user_id = serializers.IntegerField()
    permissions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate_user_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return value

    def validate_permissions(self, value):
        perms = Permission.objects.filter(id__in=value)
        if len(perms) != len(value):
            raise serializers.ValidationError("Some permissions are invalid")
        return value

    def save(self):
        user = User.objects.get(id=self.validated_data["user_id"])
        permissions = Permission.objects.filter(
            id__in=self.validated_data["permissions"]
        )

        # clear old permissions and assign new ones
        user.user_permissions.set(permissions)
        user.save()
        return user


class GroupDropDownSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""

    label = serializers.CharField(source="name")
    value = serializers.IntegerField(source="id")

    class Meta:
        model = Group
        fields = ["label", "value"]


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model with permissions"""

    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        group = Group.objects.create(**validated_data)
        group.permissions.set(permissions)
        return group

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if permissions is not None:
            instance.permissions.set(permissions)
        return instance


class UserGroupSerializer(serializers.ModelSerializer):
    """Serializer for User model with groups"""

    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "phone_number", "email", "groups", "permissions"]

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_permissions(self, obj):
        permissions = set()
        for group in obj.groups.all():
            for perm in group.permissions.all():
                permissions.add(perm.codename)
        return list(permissions)
