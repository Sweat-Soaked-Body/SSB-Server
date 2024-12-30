from django.urls import path

from chat.views import MessageView


urlpatterns = [
    path('', MessageView.as_view())
]