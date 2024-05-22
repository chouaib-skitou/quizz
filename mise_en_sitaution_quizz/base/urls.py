from django.urls import path, include
from .views import home, authView, create_quiz, QuizDetailView, QuizList, delete_quiz, update_quiz

app_name = 'base'  # Add this line to define the namespace for your app

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_quiz/", create_quiz, name="create_quiz"),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/', QuizList, name='quiz_list'),
    path('quiz/<int:pk>/delete/', delete_quiz, name='delete_quiz'),
    path('quiz/<int:pk>/update/', update_quiz, name='update_quiz'),
]
