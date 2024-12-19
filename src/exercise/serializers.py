from rest_framework import serializers

from .models import Exercise, Category, ExerciseLike


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'required': False},
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExerciseLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLike
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'required': False},
        }