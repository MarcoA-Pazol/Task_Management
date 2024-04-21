from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required #This is just for testing, it use the Django.admin decorator to login the user through the Django admin login view.
from django.contrib.auth import logout, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from BackEnd.models import Task, Questions #Loading models from Task_Manager/BackEnd/models.py
from BackEnd.forms import RegistrationForm, LoginForm, AskForHelpForm
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
    #Formulary Loading
    if request.method == "POST":
        form = AskForHelpForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            description = form.cleaned_data['description']
    else:
        form = AskForHelpForm()
    
    #Retrieve all questions
    questions = Questions.objects.all()
    
    #Retrieve all categories of questions
    categories = Questions.objects.values_list('category', flat=True).distinct()
    
    #Retrieve all questions grouped by category
    questions_by_category = {}
    for category in categories:
        questions_by_category[category] = Questions.objects.filter(category=category)
    
    #Context will load questions and questions_by_category dicts
    context = {'questions':questions, 'questions_by_category':questions_by_category, 'form':form}
    return render(request, 'help.html', context)

#Session views
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            return redirect('/') #Redirect to home page after succesfully logged in
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
        try:
            #Create new user
            user = User.objects.create_user(username=username, email=email,  password=password)
            #Authenticate and login the new user (optionally)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request)
                return redirect('/') #redirect to home page after user succesfully creation 
        except IntegrityError:
            form.add_error('username', 'This username already exists, try to use another username.')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form':form})
            

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        # Handle GET request (if needed)
        logout(request)
        return redirect('/')