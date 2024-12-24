from django.db import models

from friend.models import Friend


class Room(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=False)
