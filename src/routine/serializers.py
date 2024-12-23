from rest_framework import serializers

from .models import Routine, Set


class SetsSerializer(serializers.ModelSerializer):
    set = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Set
        fields = ('id', 'routine', 'weight', 'count', 'min', 'sec', 'status', 'set')

        extra_kwargs = {
            'routine' : {'required': False},
            'status' : {'required': False},
        }

    def get_set(self, obj):
        all_sets = self.context.get('all_sets')
        return all_sets.index(obj) + 1


class RoutineListSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Routine
        fields = ('id', 'service_user', 'exercise', 'sets', 'date')

        extra_kwargs = {
            'service_user': {'required': False, 'write_only': True},
        }

    def get_sets(self, obj):
        sets = obj.sets.filter().order_by('id')
        context = {'all_sets': list(sets)}
        return SetsSerializer(sets, many=True, context=context).data


class RoutineUploadSerializer(serializers.ModelSerializer):
    sets = SetsSerializer(many=True, write_only=True)

    class Meta:
        model = Routine
        fields = ('id', 'service_user', 'exercise', 'sets', 'date')

        extra_kwargs = {
            'service_user': {'required': False, 'write_only': True},
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