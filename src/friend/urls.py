from django.urls import path

from friend.views import FriendView


urlpatterns = [
    path('', FriendView.as_view()),
    path('/<int:pk>', FriendView.as_view()),
]