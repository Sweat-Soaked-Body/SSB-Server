from django.db import models

from user.models import ServiceUser


class Food(models.Model):
    name = models.CharField(max_length=20)
    weight = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'food'