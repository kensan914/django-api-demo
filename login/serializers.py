from rest_framework import serializers

from user.models import DemoUser


class DemoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoUser
        fields = ("name", "child_type")


class SessionSerializer(serializers.Serializer):
    user = DemoUserSerializer()
    csrf_token = serializers.CharField()
