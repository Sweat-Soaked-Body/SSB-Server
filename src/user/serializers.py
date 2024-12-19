from rest_framework import serializers, status
from rest_framework.response import Response

from userprofile.models import UserSex, ServiceUserProfile
from .exception import UserException
from .models import ServiceUser


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    sex = serializers.ChoiceField(choices=UserSex.choices)
    age = serializers.IntegerField()
    weight = serializers.IntegerField()
    height = serializers.IntegerField()

    def validate(self, data):
        if len(data['password']) <= 4:
            raise UserException.PasswordIsShortError

        user = ServiceUser.objects.filter(username=data['username']).first()
        if user:
            raise UserException.UserExistsError

        return data

    def create(self, validated_data):
        user = ServiceUser.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
        )
        profile = ServiceUserProfile.objects.create(
            service_user=user,
            name=validated_data.get('name'),
            sex=validated_data.get('sex'),
            age=validated_data.get('age'),
            weight=validated_data.get('weight'),
            height=validated_data.get('height'),
            daily_calorie=validated_data.get('weight') * 35,
        )
        return profile
