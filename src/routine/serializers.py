from rest_framework import serializers

from routine.models import Routine, Set


class SetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'

        extra_kwargs = {
            'routine' : {'read_only': True},
        }


class PatchSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('status',)


class RoutineSerializer(serializers.ModelSerializer):
    sets = SetsSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'read_only': True},
        }
