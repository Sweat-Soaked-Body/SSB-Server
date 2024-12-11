from django.urls import path

from .views import ServiceUserProfileView

urlpatterns = [
    path('', ServiceUserProfileView.as_view())
]