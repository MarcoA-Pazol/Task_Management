from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required #This is just for testing, it use the Django.admin decorator to login the user through the Django admin login view.
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from BackEnd.models import Team_Task, Help_Question, Team, Employee #Loading models from Task_Manager/BackEnd/models.py
from BackEnd.forms import RegistrationForm, LoginForm, AskForHelpForm, JoinTeamForm
# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    return render(request, 'tasks.html')

@login_required
def team(request):
    #Formulary loading
    if request.method == "POST":    
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            access_code = form.cleaned_data['access_code']
    else:
        form = JoinTeamForm()
    
    #Retireve all teams you are joined
    teams = Team.objects.all()
    
    #Context
    context = {'teams': teams, 'form': form}
    return render(request, 'team.html', context)

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
    questions = Help_Question.objects.all()
    
    #Retrieve all categories of questions
    categories = Help_Question.objects.values_list('category', flat=True).distinct()
    
    #Retrieve all questions grouped by category
    questions_by_category = {}
    for category in categories:
        questions_by_category[category] = Help_Question.objects.filter(category=category)
    
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
            print("The values are correct")
            #Get cleaned data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #Create new Employee
            try:
                user = form.save()
                user = Employee.objects.create(username=username, password=password, email=email, first_name=form.first_name, last_name=form.last_name, address=form.address, birthday=form.birthday, department=form.department)
            except IntegrityError:
                form.add_error('username', 'This username already exists, try another one.')
                print(IntegrityError)
            except Exception as e:
                form.add_error(None, e)
                print(e)
            #Authenticate and login the new user(optionally)
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            
            print(form.cleaned_data)
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        # Handle GET request (if needed)
        logout(request)
        return redirect('/')