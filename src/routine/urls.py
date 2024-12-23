from django.urls import path

from routine.views import RoutineView, SetView

urlpatterns = [
    path('', RoutineView.as_view()),
    path('/<int:pk>', RoutineView.as_view()),
    path('/set/<int:pk>', SetView.as_view()),
]