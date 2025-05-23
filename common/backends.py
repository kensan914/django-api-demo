from django.contrib.auth.backends import BaseBackend

from user.models import AdminUser, DemoUser, User


class DemoBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None

        if (
            pro_user := User.objects.filter(
                email_enc=email.encode("utf-8"), type=User.Type.PRO.value
            ).first()
        ) and pro_user.check_password(password):
            return pro_user.demo_user_ptr

        if (
            admin_user := AdminUser.objects.filter(
                email_enc=email.encode("utf-8"), type=AdminUser.Type.ADMIN.value
            ).first()
        ) and admin_user.check_password(password):
            return admin_user.demo_user_ptr

        return None

    def get_user(self, user_id):
        try:
            demo_user = DemoUser.objects.get(pk=user_id)
        except DemoUser.DoesNotExist:
            return None
        return demo_user
