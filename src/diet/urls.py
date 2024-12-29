from django.urls import path

from diet.views import DietView, DietSearchView

urlpatterns = [
    path('', DietView.as_view()),
    path('/<int:pk>', DietView.as_view()),

    path('/search', DietSearchView.as_view()),
]