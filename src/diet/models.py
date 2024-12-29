from django.db import models

from user.models import ServiceUser


class DietType(models.TextChoices):
    BREAKFAST = "BREAKFAST", "아침"
    BRUNCH = "BRUNCH", "아점"
    LUNCH = "LUNCH", "점심"
    DINNER_LITE = "DINNER_LITE", "점저"
    DINNER = "DINNER", "저녁"
    MIDNIGHT_SNACK = "MIDNIGHT_SNACK", "야식"
    SNACK = "SNACK", "간식"


class Diet(models.Model):
    service_user = models.ForeignKey(ServiceUser, on_delete=models.CASCADE, related_name='diets')
    date = models.DateField()
    type = models.CharField(max_length=20, choices=DietType.choices, null=True, blank=False)

    class Meta:
        db_table = 'diet'
