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

    def create(self, validated_data):
        return Set.objects.create(**validated_data)


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

        extra_kwargs = {
            'service_user': {'required': False},
        }


class RoutineListSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateField(format='%Y-%m-%d')
    exercise = serializers.SerializerMethodField(read_only=True)

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

    def get_exercise(self, obj):
        return obj.exercise.name