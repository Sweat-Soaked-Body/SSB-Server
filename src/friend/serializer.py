from rest_framework import serializers
from friend.models import Friend


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

        extra_kwargs = {
            'from_user': {
                'required': False,
                'write_only': True,
            },
            'to_user': {
                'write_only': True,
            }
        }


class FriendListSerializer(serializers.Serializer):
    friend = serializers.SerializerMethodField()

    def get_friend(self, obj):
        request = self.context['request']
        return [
            str(i.from_user)
            if i.to_user == request.user
            else str(i.to_user)
            for i in obj
        ]