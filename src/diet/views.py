from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from diet.models import Diet
from diet.serializers import DietSerializer


class DietView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        diet = Diet.objects.filter(service_user=request.user)
        serializer = DietSerializer(diet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: Request) -> Response:
        serializer = DietSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @atomic
    def put(self, request: Request, pk: int) -> Response:
        diet = Diet.objects.filter(id=pk, service_user=request.user).prefetch_related('food').first()
        serializer = DietSerializer(diet, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        diet = Diet.objects.filter(service_user=request.user, id=pk).first()
        diet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DietSearchView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        query = request.GET.get('date')
        food = Diet.objects.filter(date=query)
        serializer = DietSerializer(food, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)