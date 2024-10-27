from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from exercise.models import Exercise, Category
from exercise.serializers import ExerciseSerializer, CategorySerializer
from user.authentication import CookieBasedJWTAuthentication


class ExerciseView(APIView):
    authentication_classes = [CookieBasedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        exercise = Exercise.objects.all()
        serializer = ExerciseSerializer(exercise, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # Todo
        pass


class CategoryView(APIView):
    authentication_classes = [CookieBasedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)