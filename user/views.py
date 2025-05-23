from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from common.authentication import DemoSessionAuthentication
from common.permissions import (
    IsAdminUser,
    IsContractor,
    IsProUser,
)
from common.view_mixin import BaseViewMixin
from user.models import AdminUser, User
from user.serializers import AdminUserSerializer, UserSerializer


class ProUserViewSet(BaseViewMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (DemoSessionAuthentication,)
    permission_classes = (IsAuthenticated & IsProUser,)

    lookup_field = "id"
    lockup_value_converter = "int"
    queryset = User.objects.filter(type=User.Type.PRO)
    serializer_class = UserSerializer

    # def list(self, request, *args, **kwargs):
    #     print("headers===========")
    #     print(request.headers)
    #     print("sessions===========")
    #     print(request.session.items())
    #     return super().list(request, *args, **kwargs)


class AdminUserViewSet(BaseViewMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (DemoSessionAuthentication,)
    permission_classes = (IsAuthenticated & IsAdminUser,)

    lookup_field = "id"
    lockup_value_converter = "int"
    queryset = AdminUser.objects.filter(type=AdminUser.Type.ADMIN)
    serializer_class = AdminUserSerializer


class ContractorViewSet(BaseViewMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (DemoSessionAuthentication,)
    permission_classes = (IsAuthenticated & IsContractor,)

    lookup_field = "id"
    lockup_value_converter = "int"
    queryset = AdminUser.objects.filter(type=AdminUser.Type.CONTRACTOR)
    serializer_class = AdminUserSerializer
