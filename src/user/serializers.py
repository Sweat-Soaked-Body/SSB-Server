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

    def create(self, validated_data):
        if len(validated_data['password']) <= 4:
            return Response({"error": "Password too short"}, status=status.HTTP_400_BAD_REQUEST)

        return ServiceUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )