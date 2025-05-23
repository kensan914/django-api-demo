from rest_framework.permissions import BasePermission

from user.models import DemoUser


class IsProUser(BasePermission):
    def has_permission(self, request, _) -> bool:
        if not (demo_user := request.user):
            return False

        return demo_user.child_type == DemoUser.ChildType.PRO


class IsAdminUser(BasePermission):
    def has_permission(self, request, _) -> bool:
        if not (demo_user := request.user):
            return False

        return demo_user.child_type == DemoUser.ChildType.ADMIN


class IsContractor(BasePermission):
    def has_permission(self, request, _) -> bool:
        if not (demo_user := request.user):
            return False

        return demo_user.child_type == DemoUser.ChildType.CONTRACTOR
