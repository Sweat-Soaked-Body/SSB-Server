from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.db import transaction
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from config.util.exception.CustomException import CustomException
from src.app.auth.serializers import SigninSerializer, SignupSerializer
from rest_framework.permissions import IsAuthenticated
from src.app.user.models import User

from config.util.authentication.CookieJWTAuthentication import CookieJWTAuthentication


# Create your views here.
@extend_schema_view(
    post=extend_schema(
        summary='Signin API',
        description='access 토큰이 쿠키로 발급 됩니다.',
        request=SigninSerializer
    ))
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


@extend_schema_view(
    post=extend_schema(
        summary='Signup API',
        request=SignupSerializer
    ))
class SignupView(APIView):
    authentication_classes = []

    @transaction.atomic
    def post(self, request: object) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary='Logout API',
    ))
class LogoutView(APIView):
    authentication_classes = [CookieJWTAuthentication,]
    permission_classes = [IsAuthenticated]

    def post(self, request: object) -> Response:
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access')
        return response