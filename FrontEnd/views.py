from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_list_or_404, redirect
from BackEnd.models import Task #Loading models from Task_Manager/BackEnd/models.py
from django.http import JsonResponse

# Create your views here.
def home(request):
    title = 'P-S Inc'
    return render(request, 'home.html', {'title':title})

@login_required
def tasks(request):
    return render(request, 'tasks.html')

@login_required
def team(request):
    return render(request, 'team.html')

def help(request):
    return render(request, 'help.html')

#Session views
def login(request):
    pass

def register(request):
    pass


def logout(request):
    pass