from django.db.models import Q
from rest_framework import serializers

from chat.models import Room
from friend.exception import FriendException
from friend.models import Friend
from userprofile.models import ServiceUserProfile


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ('id', 'friend')

    def get_friend(self, obj):
        request = self.context['request']

        return \
            str(obj.from_user.profile.name) \
            if obj.to_user == request.user \
            else str(obj.to_user.profile.name)


class AddFriendSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate(self, data):
        to_friend = ServiceUserProfile.objects.filter(name=data.get('name')).first()
        if not to_friend:
            raise FriendException.UserNotFound

        friend = Friend.objects.filter(
            Q(from_user__profile__name=data['name']) | Q(to_user__profile__name=data['name'])
        ).prefetch_related('from_user', 'to_user')
        if friend:
            raise FriendException.FriendAlreadyExists

        return data

    def create(self, validated_data):
        from_user = validated_data.get('from_user')
        to_user = validated_data.get('name')

        friend = Friend.objects.create(
            from_user=from_user,
            to_user=ServiceUserProfile.objects.get(name=to_user).service_user
        )
        Room.objects.create(friend=friend)
        return friend