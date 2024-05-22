from django.urls import path, include
from .views import home, authView, create_quiz

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_quiz/", create_quiz, name="authView"),
]
