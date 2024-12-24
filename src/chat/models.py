from django.db import models

from friend.models import Friend


class Room(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=False)
