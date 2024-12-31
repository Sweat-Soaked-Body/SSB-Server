from rest_framework import serializers

from diet.models import Diet
from food.models import Food
from food.serializer import FoodSerializer


class DietSerializer(serializers.ModelSerializer):
    food = FoodSerializer(many=True)
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Diet
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }

    def create(self, validated_data):
        date = validated_data.pop('date')
        type = validated_data.pop('type')
        food = validated_data.pop('food')
        image = validated_data.pop('image')
        request = self.context.get('request')

        diet = Diet.objects.create(date=date, type=type, service_user=request.user, image=image)

        foods = []
        for i in food:
            foods.append(Food(diet=diet, service_user=request.user, **i))

        Food.objects.bulk_create(foods)

        return diet

    def update(self, instance, validated_data):
        date = validated_data.pop('date')
        food = validated_data.pop('food')

        instance.date = date
        instance.food.all().delete()

        foods = []
        for food_item in food:
            foods.append(Food(diet=instance, service_user=instance.service_user, **food_item))

        instance.save()
        Food.objects.bulk_create(foods)

        return instance
