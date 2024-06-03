from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from BackEnd.models import Team_Task, Help_Question, Team, Employee, Personal_Task #Loading models from Task_Manager/BackEnd/models.py
from BackEnd.forms import RegistrationForm, LoginForm, AskForHelpForm, JoinTeamForm, CreateTeamForm, EditTeamForm

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
    #Get authenticated user
    user = request.user 
    #Retrieve all tasks you have asigned.
    tasks = Team_Task.objects.filter(assigned_employee=user)
    #Context
    context = {'user':user, 'tasks':tasks}
    return render(request, 'tasks/tasks.html', context)


@login_required
def create_personal_task(request):
    return render(request, 'tasks/create_personal_task.html')



#TEAM views
@login_required
def team(request):    
    #Retireve all teams you are joined
    teams = Team.objects.filter(members=request.user)
    #Retrieve authenticated user
    user = request.user
    #Context
    context = {'teams': teams, 'user':user}
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

@login_required
def edit_team(request):
    #Obtain team if the owner has one
    try:
        owner = request.user
        team_name = Team.objects.get(owner=owner)
        if team_name:
            have_team = True
        else:
            have_team = False
    except:
        team_name = 'Team_Name'
        have_team = False
    
    if request.method == "POST":
        form = EditTeamForm(request.POST)
        if form.is_valid():
            #Clean data for their use
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            access_key = form.cleaned_data['access_key']
            
            #Comprobe acces_key is valid and exists
            try:
                team_to_update = Team.objects.filter(access_key=access_key, owner=owner).first()
                
                if team_to_update:
                    if name == "":
                        pass
                    else:
                        team_to_update.name = name
                    if description == "":
                        pass
                    else:
                        team_to_update.description = description
                    team_to_update.save()
                    print(f'Team info updated for access_key: {access_key}, owner: {owner.username}')
                    return redirect('/team/')
                else:
                    if not Team.objects.filter(access_key=access_key).exists():
                        form.add_error('access_key', 'The access key you provided does not exists.')
                    else:
                        form.add_error('access_key', 'It seems access key and owner do not match correctly, please check your access key again.')
                    print(f'Failed to update team: access_key={access_key}, owner={owner.username}')
            except IntegrityError as e:
                print(f'IntegrityError while updating team: {e}')
                return redirect('/team/edit/')
            except Exception as e:
                print(f'Unexpected error while updating team: {e}')
                return redirect('/team/edit/')
    else:
        form = EditTeamForm()
    
    context = {'form':form, 'have_team':have_team, 'team_name':team_name}
    return render(request, 'team/edit_team.html', context)

@login_required
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
                #Cleaned data for object creation(Team)
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

@login_required
def team_overview(request, team_identifier):
    #Get authenticated user
    user = request.user
    
    #Get selected Team to be displayed as an overview info
    try:
        team = Team.objects.get(name=team_identifier)
    except (Team.DoesNotExist, ValueError):
        team = get_object_or_404(Team, id=team_identifier)
    
    if request.method == 'POST':
        
        # Lógica para salir del equipo
        try:
            if user in team.members.all():
                team.members.remove(user)
                team.save()
                messages.success(request, "You have successfully left the team.")
                return redirect('/team/')
            else:
                messages.error(request, "You are not a member of this team.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        
    #Comprobe if Team´s owner is the authenticated user
    if team.owner == user:
        is_owner = True
    else:
        is_owner = False
    
    #Get members list
    members = team.members.all()
        
    context = {'team':team, 'members':members, 'is_owner':is_owner}
        
    return render(request, 'team/team_overview.html', context)

@login_required
def delete_team(request, team_identifier):
    #Obtain team to be deleted
    team = get_object_or_404(Team, name=team_identifier)
    
    #Verify if request method is POST to execute the function
    pass

@login_required
def kick_out_member(request, team_identifier, member_identifier):
    # Obtener el equipo y el miembro a ser expulsado
    team = get_object_or_404(Team, name=team_identifier)
    member = get_object_or_404(Employee, username=member_identifier)

    # Verificar que el usuario autenticado es el propietario del equipo
    if request.user != team.owner:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('team_overview', team_identifier=team_identifier)

    # Manejar la solicitud POST para expulsar al miembro
    if request.method == 'POST':
        if member in team.members.all():
            team.members.remove(member)
            team.save()
            messages.success(request, f"{member.username} has been successfully removed from the team.")
        else:
            messages.error(request, "The user is not a member of this team.")
        return redirect('team_overview', team_identifier=team_identifier)

    # Redirigir a la página de resumen del equipo si no es una solicitud POST
    return redirect('team_overview', team_identifier=team_identifier)




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