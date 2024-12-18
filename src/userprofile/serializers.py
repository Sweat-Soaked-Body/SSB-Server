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
