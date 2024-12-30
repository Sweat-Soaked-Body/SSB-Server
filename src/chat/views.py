from django.db.models import Q, Subquery, OuterRef
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

        # 서브쿼리 - 각 방 기준으로 메시지 조회
        subquery = Message.objects.filter(
            room=OuterRef('room'),
        ).order_by('-timestamp')

        # 서브쿼리 id[:1]에 맞는 메시지 조회
        message = Message.objects.filter(
            id=Subquery(subquery.values('id')[:1]),
        ).order_by('-timestamp')

        if not message:
            raise MessageException.MessageNotFoundError
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
