from rest_framework import serializers

from .models import Exercise, Category, ExerciseLike


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ExerciseLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLike
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }


class ExerciseSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }

    def get_like(self, obj):
        user = self.context.get('request').user  # 받아온 시리얼라이저에서 유저 정보 파싱
        return obj.exercise_like.filter(service_user=user).exists()