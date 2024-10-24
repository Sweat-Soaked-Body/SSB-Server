from rest_framework import serializers

from userprofile.models import ServiceUserProfile


class ServiceUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUserProfile
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }
