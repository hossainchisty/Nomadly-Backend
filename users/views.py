from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    GroupDropDownSerializer,
    GroupSerializer,
    PermissionDropDownSerializer,
    PermissionSerializer,
    SetUserPermissionsSerializer,
    SetUserRoleSerializer,
    UserCreateSerializer,
    UserDeleteSerializer,
    UserDropDownSerializer,
    UserGroupSerializer,
    UserListSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT login view using username field,
    where username contains either email or phone number.
    """

    @extend_schema(
        summary="Obtain Token Pair",
        description="Takes a set of user credentials and returns an access and refresh JSON web token pair.",
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get(
            "username"
        )  # email or phone_number (saved in 'username' field)
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Authenticate directly (Django will check against USERNAME_FIELD)
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ✅ Generate token via SimpleJWT
        serializer = self.get_serializer(
            data={"username": username, "password": password}
        )
        serializer.is_valid(raise_exception=True)

        # ✅ Build response
        response_data = serializer.validated_data
        response_data["user"] = UserProfileSerializer(user).data

        # ✅ Update last login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return Response(response_data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Register User",
        description="Register a new user with email/phone and password.",
        request=UserRegistrationSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        """Handle registration"""
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                # Send verification email
                # self.send_verification_email(user)

                return Response(
                    {
                        "message": "Registration successful.",
                        "user_id": user.id,
                        "username": user.email or user.phone_number,
                        "full_name": user.get_full_name(),
                    },
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                return Response(
                    {"error": f"Registration failed. Please try again. {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def send_verification_email(self, user):
    #     """Send email verification using django-allauth"""
    #     try:
    #         email_address = EmailAddress.objects.create(
    #             user=user, email=user.email, primary=True, verified=False
    #         )

    #         # Create confirmation and get key
    #         confirmation = EmailConfirmationHMAC(email_address)

    #         # Build activation URL
    #         activation_url = "{}/verify-email/{}".format(
    #             getattr(settings, "FRONTEND_URL", "http://localhost:3000"),
    #             confirmation.key,
    #         )

    #         # if settings.DEBUG:
    #         #     print(f"=== EMAIL VERIFICATION URL ===")
    #         #     print(f"User: {user.email}")
    #         #     print(f"Verification URL: {activation_url}")
    #         #     print(f"================================")
    #         #     return

    #         # Send email

    #         subject = "Verify your account"
    #         message = render_to_string(
    #             "email_verification.html",
    #             {
    #                 "user": user,
    #                 "activation_url": activation_url,
    #                 "expiry_days": getattr(
    #                     settings, "EMAIL_CONFIRMATION_EXPIRE_DAYS", 1
    #                 ),
    #             },
    #         )

    #         email = EmailMessage(subject, message, to=[user.email])
    #         email.content_subtype = "html"
    #         email.send()

    #     except Exception as e:
    #         # Log the error but don't fail registration
    #         print(f"Failed to send verification email: {e}")
    #         import traceback

    #         traceback.print_exc()


class UserModelViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get("role")
        if role:
            queryset = queryset.filter(role=role)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.query_params.get("dropdown") == "true":
                return UserDropDownSerializer
            return UserListSerializer
        elif self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "destroy":
            return UserDeleteSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action in ["list", "update", "partial_update", "me"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["create", "destroy"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [p() for p in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="role",
                description="Filter users by role",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="dropdown",
                description="Return dropdown format if true",
                required=False,
                type=OpenApiTypes.BOOL,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Get Current User Profile", responses=UserProfileSerializer)
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "codename"]

    def get_queryset(self):
        qs = Permission.objects.all()
        search = self.request.query_params.get("search", None)
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(
                codename__icontains=search
            )
        return qs

    def get_serializer_class(self):
        dropdown = self.request.query_params.get("dropdown", None)
        if dropdown and dropdown.lower() == "true":
            return PermissionDropDownSerializer
        return super().get_serializer_class()

    # Assign group/role to user
    @extend_schema(
        summary="Set Users Role",
        description="Assign a role to a user",
        request=SetUserRoleSerializer,
    )
    @action(detail=False, methods=["POST"], url_path="set-user")
    def set_users_role(self, request):
        serializer = SetUserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Roles assigned successfully"})

    # Assign individual permissions to user
    @extend_schema(
        summary="Set User Permissions",
        description="Assign specific permissions to a user",
        request=SetUserPermissionsSerializer,
    )
    @action(detail=False, methods=["POST"], url_path="set-user-permissions")
    def set_user_permissions(self, request):
        serializer = SetUserPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Permissions assigned successfully"})

    # Get all permissions grouped by app and model
    @extend_schema(
        summary="Permission List",
        description="Get all permissions grouped by app and model",
    )
    @action(detail=False, methods=["GET"], url_path="permission-list")
    def permission_list(self, request):
        permissions = Permission.objects.all().select_related("content_type")
        formatted = {}
        for perm in permissions:
            app_label = perm.content_type.app_label
            model = perm.content_type.model
            key = f"{app_label}.{model}"
            if key not in formatted:
                formatted[key] = []
            formatted[key].append(
                {
                    "id": perm.id,
                    "name": perm.name,
                    "codename": perm.codename,
                }
            )
        return Response(formatted)

    # Get user permissions
    @extend_schema(
        summary="User Permissions",
        description="Get all permissions for a specific user",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="ID of the user to fetch permissions for",
                required=True,
                type=OpenApiTypes.INT,
            )
        ],
    )
    @action(detail=False, methods=["GET"], url_path="user-permissions")
    def user_permissions(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        user = get_object_or_404(User, id=user_id)

        user_perms = user.user_permissions.all().values("id", "name", "codename")
        group_perms = Permission.objects.filter(group__user=user).values(
            "id", "name", "codename"
        )

        return Response(
            {"user_id": user.id, "permissions": list(user_perms.union(group_perms))}
        )

    # Create a custom permission
    @extend_schema(
        summary="Add Custom Permission",
        description="Create a new custom permission",
        request=OpenApiTypes.OBJECT,
    )
    @action(detail=False, methods=["POST"], url_path="add-custom")
    def add_custom_permission(self, request):
        name = request.data.get("name")
        codename = request.data.get("codename")
        app_label = request.data.get("app_label", "user")
        model = request.data.get("model", "user")

        if not name or not codename:
            return Response(
                {"error": "Both 'name' and 'codename' are required."},
                status=400,
            )

        # Get the content type
        content_type = ContentType.objects.filter(
            app_label=app_label, model=model
        ).first()
        if not content_type:
            return Response(
                {"error": f"Invalid app_label/model: {app_label}.{model}"},
                status=400,
            )

        # Check duplicate codename
        if Permission.objects.filter(
            codename=codename, content_type=content_type
        ).exists():
            return Response(
                {"error": "Permission with this codename already exists."},
                status=400,
            )

        # Create new permission
        permission = Permission.objects.create(
            name=name,
            codename=codename,
            content_type=content_type,
        )
        return Response(
            {
                "id": permission.id,
                "name": permission.name,
                "codename": permission.codename,
                "content_type": f"{app_label}.{model}",
            },
            status=201,
        )


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Group.objects.all()

    def get_serializer_class(self):
        dropdown = self.request.query_params.get("dropdown", None)
        if dropdown and dropdown.lower() == "true":
            return GroupDropDownSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="dropdown",
                description="Return dropdown format if true",
                required=False,
                type=OpenApiTypes.BOOL,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserGroupViewSet(ModelViewSet):
    """Group and permission to access a user into system"""

    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserGroupSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(summary="Get Current User Group Info")
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user = request.user
        serializer = UserGroupSerializer(user)
        return Response(serializer.data)
