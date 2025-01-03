from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.transaction import atomic
from rest_framework import status

from core.authentications import CsrfExemptSessionAuthentication
from routine.exception import RoutineException, SetsException
from routine.models import Routine, Set
from routine.serializers import RoutineListSerializer, SetsSerializer, RoutineSerializer


class RoutineView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        date = request.GET.get('date')
        routine = Routine.objects.filter(service_user=request.user, date=date)\
            .prefetch_related('sets')
        serializer = RoutineListSerializer(routine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: Request) -> Response:
        serializer = RoutineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        if not (routine:=Routine.objects.filter(pk=pk, service_user=request.user).first()):
            raise RoutineException.RoutineNotFound
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SetView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    @atomic
    def post(self, request: Request) -> Response:
        serializer = SetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @atomic
    def put(self, request: Request, pk: int) -> Response:
        sets = Set.objects.filter(id=pk, routine__service_user=request.user).first()
        serializer = SetsSerializer(sets, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        if not (sets:=Set.objects.filter(id=pk, routine__service_user=request.user).first()):
            raise SetsException.SetsNotFound
        sets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)