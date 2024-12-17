from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from storage.serializer import FileSerializer


class S3UploadView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.upload()
        return Response({'url': url}, status=status.HTTP_201_CREATED)
