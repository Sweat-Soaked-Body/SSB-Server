from rest_framework import serializers
from food.models import Food
from chain.langchain import Langchain


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'required': False},
            'weight': {'required': False},
        }


class FoodAnalSerializer(serializers.Serializer):
    url = serializers.CharField()

    def anal(self):
        return Langchain.analyze_image(image=self.validated_data['url'])