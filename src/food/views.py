from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from food.models import Food
from food.serializer import FoodSerializer, FoodAnalSerializer


class FoodView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        food = Food.objects.all()
        serializer = FoodSerializer(food, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: Request) -> Response:
        serializer = FoodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    @atomic
    def put(self, request: Request, pk: int) -> Response:
        food = Food.objects.filter(id=pk, service_user=request.user).first()
        serializer = FoodSerializer(food, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(status=status.HTTP_200_OK)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        food = Food.objects.filter(id=pk, service_user=request.user).first()
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FoodAnalView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = FoodAnalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anal = serializer.anal()
        return Response(anal, status=status.HTTP_200_OK)
