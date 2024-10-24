from django.db.transaction import atomic
from django.http import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import CookieBasedJWTAuthentication
from userprofile.models import ServiceUserProfile
from userprofile.serializers import ServiceUserProfileSerializer


class ServiceUserProfileView(APIView):
    authentication_classes = [CookieBasedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        profile = ServiceUserProfile.objects.filter(service_user=request.user).first()
        serializer = ServiceUserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request: HttpRequest) -> Response:
        serializer = ServiceUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(service_user=request.user)
        return Response(status=status.HTTP_201_CREATED)
