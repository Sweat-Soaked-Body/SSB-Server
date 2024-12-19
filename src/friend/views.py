from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from friend.models import Friend
from friend.serializer import FriendSerializer, FriendListSerializer


class FriendView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    # 내 친구 조회 API
    def get(self, request: Request) -> Response:
        friend = Friend.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user)
        ).prefetch_related('from_user', 'to_user')
        serializer = FriendListSerializer(friend, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 친구 추가 API
    @atomic
    def post(self, request: Request) -> Response:
        serializer = FriendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(from_user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 친구 삭제 API
    @atomic
    def delete(self, request: Request, pk: int) -> Response:
        friend = Friend.objects.filter(
            Q(id=pk) &
            (Q(from_user=request.user) | Q(to_user=request.user))
        )
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)