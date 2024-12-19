from django.db import models

from user.models import ServiceUser


class UserSex(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    UNLABELED = 'unlabeled'


class ServiceUserProfile(models.Model):
    service_user = models.OneToOneField(ServiceUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=8, unique=True)
    sex = models.CharField(choices=UserSex)
    age = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField(null=True)
    daily_calorie = models.PositiveSmallIntegerField(null=True, blank=False, default=2500)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.name
