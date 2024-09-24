from django.urls import path

from src.app.auth.views import SignupView, SigninView, LogoutView

urlpatterns = [
    path('/signin', SigninView.as_view(), name='signin'),
    path('/signup', SignupView.as_view(), name='signup'),
    path('/logout', LogoutView.as_view(), name='logout')
]
