# from django.contrib.auth.base_user import AbstractBaseUser
# from django.db import models
#
#
# class AdminUser(AbstractBaseUser):
#     class Type(models.TextChoices):
#         ADMIN = "admin", "管理者"
#         CONTRACTOR = "contractor", "法人契約者"
#
#     id = models.BigAutoField(primary_key=True)
#     email_enc = models.BinaryField(max_length=1000)
#     password_enc = models.BinaryField(max_length=1000)
#     name_enc = models.BinaryField(max_length=1000)
#     type = models.CharField(choices=Type.choices, max_length=10)
#
#     USERNAME_FIELD = "email"
#     EMAIL_FIELD = "email"
#
#     class Meta:
#         db_table = "admin_users"
#         verbose_name = verbose_name_plural = "管理者ユーザ"
#
#     @property
#     def email(self) -> str:
#         return self.email_enc.decode("utf-8")
#
#     @property
#     def password(self) -> str:
#         return self.password_enc.decode("utf-8")
#
#     @property
#     def name(self) -> str:
#         return self.name_enc.decode("utf-8")
#
#     @classmethod
#     def create_test_data(cls):
#         cls.objects.create(
#             email_enc=b"admin@example.com",
#             password_enc=b"pass",
#             name_enc="ADMIN太郎".encode(),
#             type=cls.Type.ADMIN.value,
#         )
#         cls.objects.create(
#             email_enc=b"contractor@example.com",
#             password_enc=b"pass",
#             name_enc="CONTRACTOR太郎".encode(),
#             type=cls.Type.CONTRACTOR.value,
#         )
#

from django.db import models

from user.models import DemoUser
from user.models.demo_user import AbstractChildUserMixin


class AdminUser(AbstractChildUserMixin, DemoUser):
    class Type(models.TextChoices):
        ADMIN = "admin", "管理者"
        CONTRACTOR = "contractor", "法人契約者"

    # NOTE: 親モデルの "id" と命名が競合してエラーとなるため、"child_id" とする
    child_id = models.BigAutoField(primary_key=True, db_column="id")
    demo_user_ptr = models.OneToOneField(
        DemoUser,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=False,
        related_name="admin_user",
        # NOTE: ADMIN, CONTRACTOR 以外の type のユーザは NULL になる
        null=True,
    )
    email_enc = models.BinaryField(max_length=1000)
    password_enc = models.BinaryField(max_length=1000)
    name_enc = models.BinaryField(max_length=1000)
    type = models.CharField(choices=Type.choices, max_length=10)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        db_table = "admin_users"
        verbose_name = verbose_name_plural = "管理者ユーザ"

    @property
    def email(self) -> str:
        return self.email_enc.decode("utf-8")

    @property
    def password(self) -> str:
        return self.password_enc.decode("utf-8")

    @property
    def name(self) -> str:
        return self.name_enc.decode("utf-8")

    def __str__(self):
        return self.name

    def check_password(self, raw_password):
        return self.password_enc == raw_password.encode("utf-8")
