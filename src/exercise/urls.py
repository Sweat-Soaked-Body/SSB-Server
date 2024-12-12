from django.urls import path

from .views import ExerciseView
from .views import CategoryView

urlpatterns = [
    path('', ExerciseView.as_view()),
    path('/category', CategoryView.as_view()),
]