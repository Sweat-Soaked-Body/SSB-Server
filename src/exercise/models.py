from django.db import models

from user.models import ServiceUser


class Category(models.Model):
    name = models.CharField(max_length=13)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=13)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='exercises')
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='exercises')


    class Meta:
        db_table = 'exercise'

    def __str__(self):
        return self.name


class ExerciseLike(models.Model):
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='exercise_like')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_like')