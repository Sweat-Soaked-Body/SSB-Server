from rest_framework import serializers
from food.models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'required': False},
        }
