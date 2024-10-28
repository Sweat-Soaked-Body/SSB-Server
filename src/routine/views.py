from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.transaction import atomic
from rest_framework import status

from routine.exception import RoutineException, SetsException
from routine.models import Routine, Set
from routine.serializers import RoutineSerializer, SetsSerializer, PatchSetsSerializer
from user.authentication import CookieBasedJWTAuthentication


class RoutineView(APIView):
    authentication_classes = [CookieBasedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        routine = Routine.objects.filter(service_user=request.user)\
            .prefetch_related('sets')
        serializer = RoutineSerializer(routine, many=True)
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
    authentication_classes = [CookieBasedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @atomic
    def post(self, request: Request, pk: int) -> Response:
        if not (routine:=Routine.objects.filter(pk=pk, service_user=request.user).first()):
            raise RoutineException.RoutineNotFound
        serializer = SetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(routine=routine)
        return Response(status=status.HTTP_201_CREATED)

    @atomic
    def patch(self, request: Request, routine_pk: int, sets_pk: int) -> Response:
        if not (sets:=Set.objects.filter(pk=sets_pk, routine__service_user=request.user, routine_id=routine_pk).first()):
            raise SetsException.SetsNotFound
        serializer = PatchSetsSerializer(sets, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @atomic
    def delete(self, request: Request, routine_pk: int, sets_pk: int) -> Response:
        if not (sets:=Set.objects.filter(pk=sets_pk, routine__service_user=request.user, routine_id=routine_pk).first()):
            raise SetsException.SetsNotFound
        sets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)