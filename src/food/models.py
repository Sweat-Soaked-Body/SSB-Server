from django.db import models

from user.models import ServiceUser
from diet.models import Diet


class Food(models.Model):
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='food', null=True, blank=False)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='diets', null=True, blank=False)
    name = models.CharField(max_length=20)
    weight = models.PositiveIntegerField(default=100, blank=True)
    calories = models.PositiveIntegerField()
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'food'