from django.urls import path, include
from .views import home, authView, gameView

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("question_answer/", gameView , name="gameView" )
]
