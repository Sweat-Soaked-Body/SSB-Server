from django.contrib.auth.hashers import check_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.exception import UserException
from user.models import ServiceUser


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def signin(self):
        user = ServiceUser.objects.filter(username=self.data.get('username')).first()
        if user is None:
            raise UserException.UserNotFoundError

        if not check_password(self.data.get('password'), user.password):
            raise UserException.UserNotFoundError

        token = TokenObtainPairSerializer.get_token(user)
        return token


class ServiceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUser
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if len(validated_data['password']) <= 4:
            return Response({"error": "Password too short"}, status=status.HTTP_400_BAD_REQUEST)

        ServiceUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return validated_data
