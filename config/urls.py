from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from login.views import (
    LoginView,
    LogoutView,
    SessionView,
)
from user.views import AdminUserViewSet, ContractorViewSet, ProUserViewSet

router = DefaultRouter()
router.register("pro-users", ProUserViewSet, basename="user")
router.register("admin-users", AdminUserViewSet, basename="admin-user")
router.register("contractors", ContractorViewSet, basename="contractor")

urlpatterns = [
    *router.urls,
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("session/", SessionView.as_view(), name="session"),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
