from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.exceptions import MessageException
from chat.models import Message
from chat.serializers import MessageSerializer
from core.authentications import CsrfExemptSessionAuthentication


class MessageView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.GET.get('user')
        message = Message.objects.filter(
            Q(service_user=request.user) &
            (
                Q(room__friend__to_user__profile__name=user) |
                Q(room__friend__from_user__profile__name=user)
            )
        ).order_by('-timestamp').first()
        if not message:
            raise MessageException.MessageNotFoundError
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
