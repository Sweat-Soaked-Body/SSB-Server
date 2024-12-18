from django.urls import path

from .views import ExerciseView, ExerciseLikeView
from .views import CategoryView

urlpatterns = [
    path('', ExerciseView.as_view()),
    path('/<int:pk>', ExerciseView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/like', ExerciseLikeView.as_view()),
]