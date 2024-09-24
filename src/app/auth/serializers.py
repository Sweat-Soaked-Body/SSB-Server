from rest_framework import serializers, status
from rest_framework.response import Response

from src.app.user.models import User


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if len(validated_data['password']) <= 4:
            return Response({"error": "Password too short"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return validated_data
