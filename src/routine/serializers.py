from rest_framework import serializers

from .models import Routine, Set


class PatchSetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('status',)


class SetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ('id', 'routine', 'weight', 'count', 'time', 'status')

        extra_kwargs = {
            'routine' : {'required': False},
            'status' : {'required': False},
        }


class RoutineSerializer(serializers.ModelSerializer):
    sets = SetsSerializer(many=True)
    date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Routine
        fields = ('id', 'service_user', 'exercise', 'sets', 'date')

        extra_kwargs = {
            'service_user': {'required': False},
        }

    def create(self, validated_data):
        exercise = validated_data.pop('exercise')
        date = validated_data.pop('date')
        user = validated_data.pop('service_user')
        routine = Routine.objects.create(exercise=exercise, date=date, service_user=user)

        set_objs = []
        sets = validated_data.pop('sets')
        for s in sets:
            set_objs.append(Set(routine=routine, **s))

        Set.objects.bulk_create(set_objs)
        return validated_data