from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from config.util.exception.CustomException import CustomException
from auth.serializers import SigninSerializer, SignupSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import User

from config.util.authentication.CookieJWTAuthentication import CookieJWTAuthentication


# Create your views here.
class SigninView(APIView):
    authentication_classes = []

    def post(self, request: object) -> Response:
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(username=serializer.data['username']).first()

        if user is None:
            raise CustomException.UserNotFoundError

        if not check_password(serializer.data['password'], user.password):
            raise CustomException.UserNotFoundError

        token = TokenObtainPairSerializer.get_token(user)
        token.set_exp(lifetime=timedelta(days=30))

        response = Response(status=status.HTTP_200_OK)
        response.set_cookie('access', str(token.access_token), httponly=True, secure=True, expires=timedelta(days=30))
        return response


class SignupView(APIView):
    authentication_classes = []

    @transaction.atomic
    def post(self, request: object) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication,]
    permission_classes = [IsAuthenticated]

    def post(self, request: object) -> Response:
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        return response
