from rest_framework import serializers

from user.models import AdminUser, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "name", "type")


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ("id", "email", "password", "name", "type")
