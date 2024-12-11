from django.db import models


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

    class Meta:
        db_table = 'exercise'

    def __str__(self):
        return self.name
