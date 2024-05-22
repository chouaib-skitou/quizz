from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import ControllerForm
from .models import Controller

from django.http import JsonResponse
from .models import Device, Player
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

#Create and display players
def PlayerView(request):
  allPlayer = Player.objects.order_by("score").reverse()

<<<<<<< HEAD
  return render(request, "classement/classement.html", {"p1": p1,"p2": p2,"p3": p3 })
  #method to send object to a file
=======
  return render(request, "classement/classement.html", {"allPlayer" : allPlayer })

>>>>>>> 538cda73c198ac3b0f9a83e0590c6880707fe806

