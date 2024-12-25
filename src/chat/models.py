from django.db import models

from friend.models import Friend
from user.models import ServiceUser


class Room(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        db_table = 'room'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=False)
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, null=True, blank=False, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    class Meta:
        db_table = 'message'