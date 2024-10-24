from django.urls import path

from userprofile.views import ServiceUserProfileView

urlpatterns = [
    path('', ServiceUserProfileView.as_view())
]