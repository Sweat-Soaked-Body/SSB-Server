from django.db.transaction import atomic
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from django.conf import settings
from datetime import datetime

from user.serializers import ServiceUserSerializer, SigninSerializer


class SigninView(APIView):
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.signin()
        response = Response(status=status.HTTP_200_OK)
        exp = datetime.now()+settings.JWT_ACCESS_EXP
        response.set_cookie('access', str(token.access_token), expires=exp, httponly=True, secure=True)
        return response


class SignupView(APIView):
    authentication_classes = []

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
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        return response