from django.urls import path

from routine.views import RoutineView, SetView

urlpatterns = [
    path('', RoutineView.as_view()),
    path('<int:pk>/', RoutineView.as_view()),
    path('<int:pk>/set/', SetView.as_view()),
    path('<int:routine_pk>/set/<int:sets_pk>/', SetView.as_view()),
]