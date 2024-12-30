from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from exercise.models import Exercise, Category, ExerciseLike
from exercise.serializers import ExerciseSerializer, CategorySerializer, ExerciseLikeSerializer


class ExerciseView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        exercise = Exercise.objects.filter(service_user=request.user).prefetch_related('exercise_like')
        serializer = ExerciseSerializer(exercise, many=True, context={'request': request})  # 콘텍스트를 시리얼라이저에 전달
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: Request) -> Response:
        serializer = ExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @atomic
    def put(self, request: Request, pk: int) -> Response:
        exercise = Exercise.objects.filter(id=pk, service_user=request.user).first()
        serializer = ExerciseSerializer(exercise, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        exercise = Exercise.objects.filter(id=pk, service_user=request.user)
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExerciseLikeView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        like = ExerciseLike.objects.filter(service_user=request.user).prefetch_related('exercise')
        serializer = ExerciseLikeSerializer(like, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: Request) -> Response:
        serializer = ExerciseLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        like = ExerciseLike.objects.filter(id=pk, service_user=request.user).first()
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)