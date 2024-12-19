from django.urls import path

from friend.views import FriendView


urlpatterns = [
    path('', FriendView.as_view()),
    path('/<str:name>', FriendView.as_view()),
]