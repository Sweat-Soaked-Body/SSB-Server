from django.db import models
from exercise.models import Exercise
from user.models import ServiceUser


class Routine(models.Model):
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='routines')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='routines')
    date = models.DateField(null=True, blank=False)

    class Meta:
        db_table = 'routines'

    def __str__(self):
        return self.service_user.profile.name


class SetStatus(models.TextChoices):
    UNFINISHED = 'unfinished'
    FINISHED = 'finished'


class Set(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='sets')

    weight = models.PositiveSmallIntegerField()

    count = models.PositiveSmallIntegerField(null=True, blank=True)
    time = models.PositiveSmallIntegerField(null=True, blank=True)

    status = models.CharField(choices=SetStatus.choices, default=SetStatus.UNFINISHED)

    class Meta:
        db_table = 'sets'

    def __str__(self):
        return self.routine.service_user.profile.name
