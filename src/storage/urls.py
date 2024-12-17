from django.urls import path

from storage.views import S3UploadView


urlpatterns = [
    path('', S3UploadView.as_view())
]