from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from users.views import GroupViewSet, PermissionViewSet, UserGroupViewSet, UserModelViewset
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r"user", UserModelViewset, basename="user")
routers.register(r"system-permissions", PermissionViewSet, basename="system-permissions")
routers.register(r"system-groups", GroupViewSet, basename="groups")
routers.register(r"system-access", UserGroupViewSet, basename="user-groups")


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += routers.urls
