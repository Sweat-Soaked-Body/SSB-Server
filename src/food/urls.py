from django.urls import path

from food.views import FoodView, FoodAnalView, FoodSerchView

urlpatterns = [
    path('', FoodView.as_view(), name='food'),
    path('/<int:pk>', FoodView.as_view()),

    path('/anal', FoodAnalView.as_view()),
    path('/serch', FoodSerchView.as_view()),
]