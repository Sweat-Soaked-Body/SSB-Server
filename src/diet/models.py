from django.db import models

from user.models import ServiceUser


class Diet(models.Model):
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='diets')
    date = models.DateField()

    class Meta:
        db_table = 'diet'
        unique_together = (('service_user', 'date'),)
