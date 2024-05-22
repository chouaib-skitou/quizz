from django.urls import path, include
from .views import home, authView, PlayerView

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("classement/", PlayerView,name="classement"),
]
