from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect ,HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import ControllerForm
from .models import Controller

from django.http import JsonResponse
from .models import Device
from django.contrib import messages



@login_required
def home(request):
  return render(request, "home.html")
#   return render(request, "home.html", {})
 

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})

@login_required
def gameView(request):
    # Définir le total de questions quelque part, pourrait être stocké de manière plus dynamique
    total_questions = 10

    if request.method == 'POST':
        if 'post_request_count' not in request.session:
            request.session['post_request_count'] = 1  # Commencer à 1 pour la première question
        else:
            request.session['post_request_count'] += 1

        answer = request.POST.get('answer')

        current_question = request.session['post_request_count']
        is_last_question = current_question >= total_questions

        if is_last_question:
            request.session['post_request_count'] = 0  # Réinitialiser pour une nouvelle session de quiz

        context = {
            "multiple_answers": False,
            "is_last_question": is_last_question
        }

        return render(request, "question_answer/main.html", context)

    else:
        # Réinitialiser le compteur lorsque l'utilisateur commence un nouveau quiz
        request.session['post_request_count'] = 0
        return render(request, "question_answer/main.html", {"multiple_answers": False, "is_last_question": False})

 
 #"qt","","q":"test question", "a1":"answer1","a1":"answer3","a1":"answer2"