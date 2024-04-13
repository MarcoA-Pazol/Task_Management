from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_list_or_404, redirect
from BackEnd.models import Task, Questions #Loading models from Task_Manager/BackEnd/models.py
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    return render(request, 'tasks.html')

@login_required
def team(request):
    return render(request, 'team.html')

def help(request):
    #Retrieve all questions
    questions = Questions.objects.all()
    
    #Retrieve all categories of questions
    categories = Questions.objects.values_list('category', flat=True).distinct()
    
    #Retrieve all questions grouped by category
    questions_by_category = {}
    for category in categories:
        questions_by_category[category] = Questions.objects.filter(category=category)
    
    #Context will load questions and questions_by_category dicts
    context = {'questions':questions, 'questions_by_category':questions_by_category}

    return render(request, 'help.html', context)

#Session views
def login(request):
    pass

def register(request):
    pass


def logout(request):
    pass