from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from expTracker import models
from .models import Accounts, Expense
from django.views.generic import TemplateView, FormView
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

def login_view(request):
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
    return render(request, "registration/login.html", {"form": form})

class ExpenseListView(FormView):
    template_name = 'exp_tracker/expense_list.html'
    form_class = ExpenseForm
    success_url = '/'
    
    
    def form_valid(self, form):
        account, _ = Accounts.objects.get_or_create(user=self.request.user)
    
        expense = Expense(
            name = form.cleaned_data['name'],
            amount = form.cleaned_data['amount'],
            interest_rate = form.cleaned_data['interest_rate'],
            date = form.cleaned_data['date'],
            end_date = form.cleaned_data['end_date'],
            long_term = form.cleaned_data['long_term'],
            user = self.request.user
        )
        expense.save()
        account.expense_list.add(expense)
        return super().form_valid(form)

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Accounts.objects.filter( user = user)
        
       
        