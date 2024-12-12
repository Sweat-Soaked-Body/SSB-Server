from django.urls import path

from .views import SigninView, SignupView, LogoutView


urlpatterns = [
    path('/signin', SigninView.as_view()),
    path('/signup', SignupView.as_view()),
    path('/logout', LogoutView.as_view())
]