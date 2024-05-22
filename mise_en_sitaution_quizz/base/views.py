from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests

from django.http import JsonResponse

@login_required
def home(request):
  return render(request, "home.html")
 

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})
