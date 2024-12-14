from rest_framework import serializers, status
from rest_framework.response import Response

from .exception import UserException
from .models import ServiceUser


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ServiceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUser
        fields = ('username', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if len(data['password']) <= 4:
            raise UserException.PasswordIsShortError
        return data

    def create(self, validated_data):
        return ServiceUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )