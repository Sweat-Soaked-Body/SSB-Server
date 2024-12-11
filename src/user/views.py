from django.contrib.auth import authenticate, login, logout
from django.db.transaction import atomic
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status

from core.authentications import CsrfExemptSessionAuthentication
from user.exception import UserException
from user.serializers import ServiceUserSerializer, SigninSerializer


class SigninView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not (user := authenticate(request, **serializer.validated_data)):
            raise UserException.UserNotFoundError
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class SignupView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    @atomic
    def post(self, request: Request) -> Response:
        serializer = ServiceUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)