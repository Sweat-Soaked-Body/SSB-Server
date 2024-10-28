from django.urls import path

from exercise.views import ExerciseView
from exercise.views import CategoryView

urlpatterns = [
    path('', ExerciseView.as_view()),
    path('category/', CategoryView.as_view()),
]