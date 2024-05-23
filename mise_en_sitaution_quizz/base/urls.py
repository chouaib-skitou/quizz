from django.urls import path, include
from .views import home, authView, create_quiz, QuizDetailView, QuizList, delete_quiz, update_quiz, save_quiz, get_quiz_json, update_quiz_form, get_quiz_details, submit_quiz, take_quiz, PlayerView

app_name = 'base'  # Add this line to define the namespace for your app

#Les url du serveur. On définit leur chemin et ce à qui ils accèdent
urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_quiz/", create_quiz, name="create_quiz"),
    path('get_quiz_json/<int:id>/', get_quiz_json, name='get-quiz-json'),
    path('update_quiz_form/<int:id>/', update_quiz_form, name='update-quiz-form'),
    path("save_quiz/", save_quiz, name="save_quiz"),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/', QuizList, name='quiz_list'),
    path('quiz/<int:pk>/delete/', delete_quiz, name='delete_quiz'),
    path('quiz/<int:pk>/update/', update_quiz, name='update_quiz'),
    path('get_quiz_details/<int:quiz_id>/', get_quiz_details, name='get-quiz-details'),
    path('submit_quiz/<int:quiz_id>/', submit_quiz, name='submit-quiz'),
    path('take_quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path("classement/", PlayerView, name="classement"), 
    #Nouvelle page de test. Accès au dossier dans classement,
    #PlayerView : 
]
