from django.urls import path, include
from .views import home, authView, PlayerView

#Les url du serveur. On définit leur chemin et ce à qui ils accèdent
urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("classement/", PlayerView, name="classement"), 
    #Nouvelle page de test. Accès au dossier dans classement,
    #PlayerView : 

]
