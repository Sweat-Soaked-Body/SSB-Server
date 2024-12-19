from django.db import models

from user.models import ServiceUser


class Friend(models.Model):
    from_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='to_user')

    class Meta:
        db_table = 'friend'

        unique_together = (('from_user', 'to_user'),)