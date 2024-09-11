from django.urls import path

from user.auth.views import SigninView, SignupView

urlpatterns = [
    path('/signin', SigninView.as_view(), name='signin'),
    path('/signup', SignupView.as_view(), name='signup')
]