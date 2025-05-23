from abc import ABCMeta, abstractmethod

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class AMCModelMeta(ABCMeta, type(models.Model)):
    """ABCMeta と models.Model をそのまま用いると metaclass conflict エラーとなるため"""


class AbstractChildUserMixin(metaclass=AMCModelMeta):
    """ChildUserモデルごとで異なる振る舞いを定義する Template パターン"""

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def email(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def check_password(self, raw_password: str) -> bool:
        raise NotImplementedError


class DemoUserManager(BaseUserManager):
    use_in_migrations = True


class DemoUser(AbstractBaseUser):
    class ChildType(models.TextChoices):
        PRO = "pro", "Proユーザ"
        ADMIN = "admin", "管理者"
        CONTRACTOR = "contractor", "法人契約者"
        OTHER = "other", "その他"

    id = models.BigAutoField(primary_key=True)
    child_type = models.CharField(choices=ChildType.choices, max_length=10)
    # NOTE: 現状、パスワードは子ユーザモデルで管理しているので、AbstractBaseUser.password を None で上書きする
    password = None

    objects = DemoUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ()  # NOTE: createsuperuser は使用しないため、この項目は特に設定しない

    class Meta:
        db_table = "demo_users"
        verbose_name = verbose_name_plural = "認証用ユーザ"

    # NOTE: AbstractBaseUser.__str__ は、child の email カラムを参照するため、child のフェッチが発生してしまうため、オーバーライド
    def __str__(self):
        return str(self.id)

    @property
    def child(self) -> AbstractChildUserMixin:
        """子ユーザモデルのインスタンスを取得"""
        child_class = self.get_child_class(self.child_type)
        return child_class.objects.get(demo_user_ptr=self)

    @classmethod
    def get_child_class(cls, child_type: ChildType) -> type[AbstractChildUserMixin]:
        """子ユーザモデルのクラスを取得"""
        match child_type:
            case cls.ChildType.PRO:
                from user.models import User

                return User
            case cls.ChildType.ADMIN | cls.ChildType.CONTRACTOR:
                from user.models import AdminUser

                return AdminUser
            case _:
                msg = f"Unexpected child type (:`{child_type}`)"
                raise AssertionError(msg)

    @property
    def name(self) -> str:
        return self.child.name

    # NOTE: USERNAME_FIELD, EMAIL_FIELD によって参照されるため、消さないように注意
    @property
    def email(self) -> str:
        return self.child.email

    # NOTE: Django のパスワード機構は使用せず、独自のパスワード管理をしているため、AbstractBaseUser.set_password をオーバーライド
    def set_password(self, raw_password: str) -> None:
        raise NotImplementedError

    # NOTE: Django のパスワード機構は使用せず、独自のパスワード管理をしているため、AbstractBaseUser.check_password をオーバーライド
    def check_password(self, raw_password: str) -> bool:
        return self.child.check_password(raw_password)
