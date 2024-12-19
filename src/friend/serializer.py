from rest_framework import serializers
from friend.models import Friend


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

        extra_kwargs = {
            'from_user': {'required': False},
        }