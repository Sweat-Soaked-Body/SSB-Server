from django.contrib.auth.models import AbstractUser
from django.db import models


class ServiceUser(AbstractUser):

    class Meta:
        db_table = 'service_user'

    def __str__(self):
        return self.username
