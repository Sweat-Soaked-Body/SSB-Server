from django.db.transaction import atomic
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from userprofile.models import ServiceUserProfile
from userprofile.serializers import ServiceUserProfileSerializer


class ServiceUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request: Request) -> Response:
        profile = ServiceUserProfile.objects.filter(service_user=request.user).first()
        serializer = ServiceUserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
