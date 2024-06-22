from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from BackEnd.models import Team_Task, Help_Question, Team, Employee, Personal_Task, save_initial_help_questions, Notification
from BackEnd.forms import RegistrationForm, LoginForm, AskForHelpForm, JoinTeamForm, CreateTeamForm, EditTeamForm

#Functions
def get_department(occupation):
        #Software Developing
        if occupation == 'Back-End Developer' or occupation == 'Server Engineer' or occupation == 'Front-End Developer':
            department = 'Software Developing'
        
        # DevOps
        elif occupation == 'DevOps Developer'  or occupation == 'Prompt Engineer':
            department = 'DevOps'
        
        # Design
        elif occupation == 'Product Designer' or occupation == 'Graphic Designer' or occupation == 'UX Designer' or occupation == 'UI Designer' or occupation == 'UI/UX Designer' or occupation == 'Web Designer':
            department = 'Design'
        
        # Project Management
        elif occupation == 'Project Manager' or occupation == 'SCRUM Master' or occupation == 'Agile Coach':
            department = 'Project Management'
        
        # Quality Assurance (QA)
        elif occupation == 'Manual Tester' or occupation == 'Automated Tester' or occupation == 'Performance Tester': 
            department = 'Quality Assurance'
        
        # Information Technology (IT)
        elif occupation == 'IT Support Specialist' or occupation == 'Network Administrator' or occupation == 'System Administrator' or occupation == 'Cybersecurity Specialist':
            department = 'Information Technology'
        
        # Sales and Marketing
        elif occupation == 'Sales Specialist' or occupation == 'Marketing Specialist' or occupation == 'Digital Marketer' or occupation == 'Content Marketer' or occupation == 'SEO/SEM Specialist':
            department = 'Sales and Marketing'
        
        # Customer Support/Service
        elif occupation == 'Customer Support Specialist' or occupation == 'Technical Support Specialist' or occupation == 'Client Relations Specialist':
            department = 'Customer Support/Service'
        
        # Consultancy
        elif occupation == 'Business Consultant' or occupation == 'IT Consultant' or occupation == 'Strategy Consultant' or occupation == 'Process Improvement Specialist':
            department = 'Consultancy'
        
        # Product Management
        elif occupation == 'Product Manager' or occupation == 'Product Strategist' or occupation == 'Product Marketer':
            department = 'Product Management'
        
        # Data
        elif occupation == 'Data Scientist' or occupation == 'Data Engineer' or occupation == 'Data Analyst' or occupation == 'Business Intelligence Analyst' or occupation == 'Database Manager': 
            department = 'Data'
        
        # Finance
        elif occupation == 'Accountant' or occupation == 'Financial Analyst' or occupation == 'Billing Specialist':
            department = 'Finance'
        
        # Operations
        elif occupation == 'Operations Manager' or occupation == 'Supply Chain Manager' or occupation == 'Facilities Manager':
            department = 'Operations'
        
        # Legal
        elif occupation == 'Legal Counsel' or occupation == 'Compliance Officer' or occupation == 'Contract Manager':
            department = 'Legal'
        
        # Research and Development (R&D)
        elif occupation == 'Innovation Specialist' or occupation == 'Prototyping Specialist' or occupation == 'Researcher':
            department = 'Research and Development (R&D)'
        
        # Training and Development
        elif occupation == 'Training Specialist' or occupation == 'Leadership Development Specialist' or occupation == 'Professional Development Specialist':
            department = 'Training and Development'
        
        # Administration
        elif occupation == 'Office Administrator occupation' or occupation == 'Executive Assistant' or occupation == 'Receptionist':
            department = 'Administration'
        
        # Vendor occupation Management
        elif occupation == 'Supplier Relations Specialist' or occupation == 'Contract Negotiation Specialist': 
            department = 'Vendor Management'
        
        # Corporate Strategy
        elif occupation == 'Business Strategist' or occupation == 'Market Research Analyst' or occupation == 'Competitive Analyst': 
            department = 'Corporate Strategy'
        
        # Communications
        elif occupation == 'Internal Communications Specialist' or occupation == 'Public Relations Specialist' or occupation == 'Corporate Communications Specialist':
            department = 'Communications'
        
        # Production
        elif occupation == 'Worker':
            department = 'Production'
        
        else:
            department = 'Production'
    
        return department

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
                if request.user in team.members.all():
                    print(f'{request.user} is already in "{team.name}" Team')
                    return redirect('join_team')
                else:
                    team.members.add(request.user)
                    team.save()
                    team_members = team.members.all()
                    for member in team_members:
                        if member != team.owner:
                            notification_to_team_members = Notification.objects.create(reason="New Member Joined", message=f"'{request.user}' has joined to {team.name} Team where you are member.", destinatary=member, is_read=False)
                    notification_to_team_owner = Notification.objects.create(reason='New Member Joined', message=f"'{request.user}' has joined to your Team.", destinatary=team.owner, is_read=False)
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
                notification_to_team_owner = Notification.objects.create(reason=f"Member leave {team.name} Team", message=f"'{user}' has leave your Team.", destinatary=team.owner, is_read=False)
                team_destinataries = team.members.all()
                for member in team_destinataries:
                    if member != team.owner:
                        notification_to_team_members = Notification.objects.create(reason=f"Member leave {team.name} Team", message=f"'{user}' has leave {team.name} Team where you are member.", destinatary=member, is_read=False)
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
    
    #Get members to invite list
    members_to_invite = Employee.objects.filter(department=user.department).exclude(username=user.username)
        
    context = {'team':team, 'members':members, 'is_owner':is_owner, 'members_to_invite':members_to_invite}
        
    return render(request, 'team/team_overview.html', context)

@login_required
def delete_team(request, team_identifier):
    #Obtain team to be deleted
    try:
        team = get_object_or_404(Team, name=team_identifier)
    except:
        team = Team.objects.filter(name=team_identifier).get()
    
    if request.method == "POST":
        try:
            Team.objects.filter(name=team).delete()
            messages.success(request, f'{team.name} Team has been deleted succesfully!')
        except:    
            messages.error(request, "The Team could not be removed succesfully.")
        return redirect('/team/')
    
    return redirect('/team/')

@login_required
def invite_member(request, team_identifier, member_identifier):
    #Obtain Team and Member to be invited
    team = get_object_or_404(Team, name=team_identifier)
    member = get_object_or_404(Employee, username=member_identifier)
    
    #Verify authenticated user is Team 
    if request.user != team.owner:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('team_overview', team_identifier=team_identifier)
    
    #Manage POST request to invite member to your Team
    if request.method == 'POST':
        if member in team.members.all():
            messages.warning(request, f"{member.username} is already on your Team")
        else:
            #FUTURE FUNCTIONALITY IMPLEMENTATION: send_invitation(member, team)
            #For now
            team.members.add(member)
            team.save()
            messages.success(request, f"{member.username} has been succesfully invited to your Team")
        return redirect('team_overview', team_identifier=team_identifier)
            
    return redirect('team_overview', team_identifier=team_identifier)
    

@login_required
def kick_out_member(request, team_identifier, member_identifier):
    #Obtain Team and Member to be invited
    team = get_object_or_404(Team, name=team_identifier)
    member = get_object_or_404(Employee, username=member_identifier)

    #Verify authenticated user is Team owner
    if request.user != team.owner:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('team_overview', team_identifier=team_identifier)

    #Manage POST request to remove member for Team
    if request.method == 'POST':
        if member in team.members.all():
            team.members.remove(member)
            team.save()
            messages.success(request, f"{member.username} has been successfully removed from the team.")
        else:
            messages.error(request, "The user is not a member of this team.")
        return redirect('team_overview', team_identifier=team_identifier)

    return redirect('team_overview', team_identifier=team_identifier)




def help(request):
    #Formulary Loading
    save_initial_help_questions()
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
    
    
#Notifications Views
@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(destinatary=user, is_read=False)
    read_notifications = Notification.objects.filter(destinatary=user, is_read=True)
    
    context = {'notifications':notifications, 'read_notifications':read_notifications}
    return render(request, 'notifications/notifications.html', context)
        
@login_required
def mark_as_read_notification(request, notification_identifier):
    notification = get_object_or_404(Notification, id=notification_identifier)
    
    if request.method == "POST":
        try:
            notification.is_read = True
            notification.save()
            print("Notification has stablished to is_read=True state")
        except Exception as e:
            print(f'Failed to mark Notification as read: {e}')
    
    return redirect('notifications')