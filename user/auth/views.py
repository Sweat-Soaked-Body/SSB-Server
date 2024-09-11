from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.auth.serializers import UserModelSerializer, SigninSerializer
from user.models import User


# Create your views here.
class SigninView(APIView):
    authentication_classes = []

    def post(self, request: object) -> Response:
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response(
                {"detail": "Invalid ID or Password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignupView(APIView):
    authentication_classes = []

    def post(self, request: object) -> Response:
        serializer = UserModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response(status=status.HTTP_200_OK)
