# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.db import models
#
#
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#
# class User(AbstractBaseUser):
#     class Type(models.TextChoices):
#         FREE = "free", "無料ユーザ"  # NOTE: 管理サイトにアクセス不可
#         PRO = "pro", "Proユーザ"  # NOTE: 管理サイトにアクセス可能
#
#     id = models.BigAutoField(primary_key=True)
#     email_enc = models.BinaryField(max_length=1000)
#     password_enc = models.BinaryField(max_length=1000)
#     name_enc = models.BinaryField(max_length=1000)
#     type = models.CharField(choices=Type.choices, max_length=10)
#
#     USERNAME_FIELD = "email_enc"
#     EMAIL_FIELD = "email_enc"
#     # USERNAME_FIELD = "email"
#     # EMAIL_FIELD = "email"
#
#     objects = UserManager()
#
#     class Meta:
#         db_table = "users"
#         verbose_name = verbose_name_plural = "利用者ユーザ"
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
#     def check_password(self, raw_password):
#         # TODO: 動確
#         return True
#
#     def __str__(self):
#         return self.name
#
#     @classmethod
#     def create_test_data(cls):
#         cls.objects.create(
#             email_enc=b"pro@example.com",
#             password_enc=b"pass",
#             name_enc="PRO太郎".encode(),
#             type=cls.Type.PRO.value,
#         )
#         cls.objects.create(
#             email_enc=b"free@example.com",
#             password_enc=b"pass",
#             name_enc="FREE太郎".encode(),
#             type=cls.Type.FREE.value,
#         )


from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from user.models import DemoUser
from user.models.demo_user import AbstractChildUserMixin


class UserManager(BaseUserManager):
    use_in_migrations = True


class User(AbstractChildUserMixin, DemoUser):
    class Type(models.TextChoices):
        FREE = "free", "無料ユーザ"  # NOTE: 管理サイトにアクセス不可
        PRO = "pro", "Proユーザ"  # NOTE: 管理サイトにアクセス可能

    # NOTE: 親モデルの "id" と命名が競合してエラーとなるため、"child_id" とする
    child_id = models.BigAutoField(primary_key=True, db_column="id")
    demo_user_ptr = models.OneToOneField(
        DemoUser,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=False,
        related_name="user",
        # NOTE: PRO 以外の type のユーザは NULL になる
        null=True,
    )
    email_enc = models.BinaryField(max_length=1000)
    password_enc = models.BinaryField(max_length=1000)
    name_enc = models.BinaryField(max_length=1000)
    type = models.CharField(choices=Type.choices, max_length=10)

    USERNAME_FIELD = "email_enc"
    EMAIL_FIELD = "email_enc"
    # USERNAME_FIELD = "email"
    # EMAIL_FIELD = "email"

    class Meta:
        db_table = "users"
        verbose_name = verbose_name_plural = "利用者ユーザ"

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
