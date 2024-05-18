from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
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
    elif occupation == "Worker":
        department = "Production"
    else:
        department = "None" 
    
    return department


# Create your views here.
def home(request):
    return render(request, 'home.html')



#TASK views
@login_required
def tasks(request):
    return render(request, 'tasks.html')



#TEAM views
@login_required
def team(request):    
    #Retireve all teams you are joined
    teams = Team.objects.filter(members=request.user)
    #Context
    context = {'teams': teams}
    return render(request, 'team/team.html', context)

@login_required
def join_team(request):
    if request.method == "POST":
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            access_key_join = form.cleaned_data['access_key']
            try:
                team = Team.objects.get(access_key=access_key_join)
                team.members.add(request.user)
                team.save()
                return redirect('/team/')
            except Team.DoesNotExist:
                form.add_error('access_key', 'Invalid access key.')
    else:
        form = JoinTeamForm()
        
    context = {'form':form}
    return render(request, 'team/join_team.html', context)

def create_team(request):
    #Obtain team if the owner has one
    try:
        owner = request.user
        if Team.objects.get(owner=owner) is not None:
            have_team = True
        else:
            have_team = False
    except:
        have_team = False
        
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
                #Cleane data for object creation(Team)
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                access_key_create = form.cleaned_data['access_key']
                #Get the current user(owner)
                owner = request.user
                #Get current user´s department
                department = owner.department
                
                if Team.objects.filter(access_key=access_key_create).exists():
                    form.add_error('access_key', 'The access key you have provided already is in use, please try with another.')
                    print("⚠ Access key already exists ⚠")
                else: 
                    try:
                        team = Team.objects.create(owner=owner, name=name, description=description, department=department, access_key=access_key_create)
                        team.members.add(owner)
                        team.save()
                        return redirect('/')
                    except IntegrityError:
                        form.add_error('name', 'You are already owner of a team. You can not create another one.')
                        print(IntegrityError)
                        return redirect('/team/create/')
                    except Exception as e:
                        print(e)
    else:
        form = CreateTeamForm()
    
    context = {'form':form, 'have_team':have_team}
    return render(request, 'team/create_team.html', context)




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
            # Guardar los datos del formulario y crear el usuario
            try:
                user = form.save(commit=False)
                # Define el departamento basado en la ocupación
                user.department = get_department(occupation=form.cleaned_data['occupation'])
                user.save()
                # Autenticar y redirigir al usuario
                auth.login(request, user)
                return redirect('/')
            except IntegrityError:
                form.add_error('username', 'This username already exists, try another one.')
                print(IntegrityError)
            except Exception as e:
                form.add_error(None, e)
                print(e)
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