from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from expTracker import models
from .models import Accounts, Expense
from django.views.generic import TemplateView
from django.views.generic import ListView
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.


def home(request):
    return render(request, 'home/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # <-- add ()
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    # Always return a response
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form  = AuthenticationForm(request, data = request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user  = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
       
        