from rest_framework import serializers

from .models import ServiceUserProfile
from .exception import UserProfileException


class ServiceUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUserProfile
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }

    def create(self, validated_data):
        profile = ServiceUserProfile.objects.filter(service_user=validated_data['service_user']).first()
        if profile:
            raise UserProfileException.ProfileAlreadyExists

        return ServiceUserProfile.objects.create(**validated_data)