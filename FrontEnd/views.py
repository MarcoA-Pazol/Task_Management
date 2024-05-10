from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required #This is just for testing, it use the Django.admin decorator to login the user through the Django admin login view.
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from BackEnd.models import Team_Task, Help_Question, Team, Employee #Loading models from Task_Manager/BackEnd/models.py
from BackEnd.forms import RegistrationForm, LoginForm, AskForHelpForm, JoinTeamForm, CreateTeamForm

#Functions
def get_department(occupation):
    if occupation == "Back-End Developer":
        department = "Software Developing"
    elif occupation == "Front-End Developer":
        department = "Software Developing"
    elif occupation == "Full-Stack Developer":
        department = "Software Developing"
    else:
        department = "None" 


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
        join_team_form = JoinTeamForm(request.POST)
        create_team_form = CreateTeamForm(request.POST)
        
        if join_team_form.is_valid():
            access_key = join_team_form.cleaned_data['access_key']
        
        if create_team_form.is_valid():
            #Cleane data for object creation(Team)
            name = create_team_form.cleaned_data['name']
            description = create_team_form.cleaned_data['description']
            access_key = create_team_form.cleaned_data['access_key']
            #Get the current user(owner)
            owner = request.user
            #Get current user´s department
            department = owner.department
            
            try:
                team = Team.objects.create(owner=owner, name=name, description=description, department=department, access_key=access_key)
                team.members.add(owner)
                team.save()
                return redirect('/')
            except IntegrityError:
                create_team_form.add_error('username', 'This username already exists, try another one.')
                print(IntegrityError)
            except Exception as e:
                print(e)
    else:
        join_team_form = JoinTeamForm()
        create_team_form = CreateTeamForm()
    
    #Retireve all teams you are joined
    teams = Team.objects.all()
    
    #Context
    context = {'teams': teams, 'join_team_form': join_team_form, 'create_team_form': create_team_form}
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
            occupation = form.cleaned_data['occupation']
            
            #Get department depending the selected ocupation    #   #   #   #   #
            department = get_department(occupation=occupation)
            
            #Create new Employee
            try:
                user = form.save()
                user = Employee.objects.create(username=username, password=password, email=email, first_name=form.first_name, last_name=form.last_name, address=form.address, birthday=form.birthday, occupation=occupation ,department=department)
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