from django.urls import path

from diet.views import DietView


urlpatterns = [
    path('', DietView.as_view()),
    path('/<int:pk>', DietView.as_view()),
]