from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

#List for choiceable values
OCCUPATION_CHOICES = [
    # BackEnd
    ['Back-End Developer', 'Back-End Developer'],
    ['Servers Engineer', 'Server Engineer'],
    # FrontEnd
    ['Front-End Developer', 'Front-End Developer'],
    # DevOps
    ['DevOps Developer', 'DevOps Developer'],
    ['Prompt Engineer', 'Prompt Engineer'],
    
    # Design
    ['Product Designer', 'Product Designer'],
    ['Graphic Designer', 'Graphic Designer'],
    ['UX Designer', 'UX Designer'],
    ['UI Designer', 'UI Designer'],
    ['UI/UX Designer', 'UI/UX Designer'],
    ['Web Designer', 'Web Designer'],
    
    # Project Management
    ['Project Manager', 'Project Manager'],
    ['SCRUM Master', 'SCRUM Master'],
    ['Agile Coach', 'Agile Coach'],
    
    # Quality Assurance (QA)
    ['Manual Tester', 'Manual Tester'],
    ['Automated Tester', 'Automated Tester'],
    ['Performance Tester', 'Performance Tester'],
    
    # Information Technology (IT)
    ['IT Support Specialist', 'IT Support Specialist'],
    ['Network Administrator', 'Network Administrator'],
    ['System Administrator', 'System Administrator'],
    ['Cybersecurity Specialist', 'Cybersecurity Specialist'],
    
    # Sales and Marketing
    ['Sales Specialist', 'Sales Specialist'],
    ['Marketing Specialist', 'Marketing Specialist'],
    ['Digital Marketer', 'Digital Marketer'],
    ['Content Marketer', 'Content Marketer'],
    ['SEO/SEM Specialist', 'SEO/SEM Specialist'],
    
    # Customer Support/Service
    ['Customer Support Specialist', 'Customer Support Specialist'],
    ['Technical Support Specialist', 'Technical Support Specialist'],
    ['Client Relations Specialist', 'Client Relations Specialist'],
    
    # Consultancy
    ['Business Consultant', 'Business Consultant'],
    ['IT Consultant', 'IT Consultant'],
    ['Strategy Consultant', 'Strategy Consultant'],
    ['Process Improvement Specialist', 'Process Improvement Specialist'],
    
    # Product Management
    ['Product Manager', 'Product Manager'],
    ['Product Strateist', 'Product Strategist'],
    ['Product Marketer', 'Product Marketer'],
    
    # Data
    ['Data Scientist', 'Data Scientist'],
    ['Data Engineer', 'Data Engineer'],
    ['Data Analyst', 'Data Analyst'],
    ['Database Manager', 'Database Manager'],
    ['Business Intelligence Analyst', 'Business Intelligence Analyst'],
    
    # Finance
    ['Accountant', 'Accountant'],
    ['Financial Planning Analyst', 'Financial Planning Analyst'],
    ['Billing Specialist', 'Billing Specialist'],
    
    # Operations
    ['Operations Manager', 'Operations Manager'],
    ['Supply Chain Manager', 'Supply Chain Manager'],
    ['Facilities Manager', 'Facilities Manager'],
    
    # Legal
    ['Legal Counsel', 'Legal Counsel'],
    ['Compliance Officer', 'Compliance Officer'],
    ['Contract Manager', 'Contract Manager'],
    
    # Research and Development (R&D)
    ['Innovation Specialist', 'Innovation Specialist'],
    ['Prototyping Specialist', 'Prototyping Specialist'],
    ['Researcher', 'Researcher'],
    
    # Training and Development
    ['Employee Training Specialist', 'Employee Training Specialist'],
    ['Leadership Development Specialist', 'Leadership Development Specialist'],
    ['Professional Development Specialist', 'Professional Development Specialist'],
    
    # Administration
    ['Office Administrator', 'Office Administrator'],
    ['Executive Assistant', 'Executive Assistant'],
    ['Receptionist', 'Receptionist'],
    
    # Vendor Management
    ['Supplier Relations Specialist', 'Supplier Relations Specialist'],
    ['Contract Negotiation Specialist', 'Contract Negotiation Specialist'],
    
    # Corporate Strategy
    ['Business Strategist', 'Business Strategist'],
    ['Market Research Analyst', 'Market Research Analyst'],
    ['Competitive Analyst', 'Competitive Analyst'],
    
    # Communications
    ['Internal Communications Specialist', 'Internal Communications Specialist'],
    ['Public Relations Specialist', 'Public Relations Specialist'],
    ['Corporate Communications Specialist', 'Corporate Communications Specialist'],
]


#List of questions to be displayed on 'Help' page for user. 
HELP_QUESTIONS = [
    #Account
    ['How to change my username?', 'Go to your profile > account > Change username > then fill the formulary, with your new username and password.', 'Account'],
    ['How to delete my account?', 'Go to help (this page), then send a request on bottom help formulary with the reason "Delete account". Then wait for 1 - 3 habilited days to get your account deleted.', 'Account'],
    ['I Forgot my username', 'Send an E-Mail to ptsolutions@pt.org.en with the "username" reason. You must send this E-mail via your related account E-Mail. Then in a maximum 1 hour you will get your username via E-Mail.', 'Account'],
    ['I Forgot my password', 'In Login formulary on the bottom is there a "I forgot my password" link, click on them, then follow instructions using your email and username to reset or restablish your password.', 'Account'],
    #Team
    ['How to be owner of a team?', 'Create an account > Go to Team on top bar > Create Team > Fill formulary > See your Team on Team page. Your own Team will be displayed on a gold border and leader name color.', 'Team'],
    ['How to join on a Team', 'Log with your account > Go to Team on top bar > Join Team > Fill formulary > See Teams you are member on Team page.', 'Team'],
    ['How to Kick Out members for my own Team?', 'You can Kick Out members for your Team clicking on your Team overview on Teams page, then a Kick Off button will be displayed fron of members, except for your name.', 'Team'],
    ['How to get members for my Team?', 'You can Invite members for your same working area on a send invitation button in front of every company user that is on your same area, but be carefull because if ou invite all members you saw, you can not get a well controll over your team workflow, whatever, you can kick off members later.', 'Team'],
    ['How to Add Tasks to myself?', 'You can assign yourself tasks on Tasks > Personal Tasks > Assign Task, you can stablish delivery date to manage controll over your times and reminders.', 'Task'],
    ['How to get an evaluation for Task?', 'Go to Send Evaluation > Send the file, image, evidence, etc. to be evaluated. > Get Response on your notifications center included in your profile page where you can find notification like this "Evaluation: Your task has been evaluated succesfully. Task state: Completed".', 'Task'],
    ['How to assign same Task for more than one member for my own Team?', 'In Task assignation formulary, in "Asigned to" click on "Group". then on down displayed list assign task to every member you want.', 'Task'] 
]

def save_initial_help_questions():
    for question in HELP_QUESTIONS:
        question_text, answer_text, category = question
        if not Help_Question.objects.filter(question=question_text).exists():
            Help_Question.objects.create(question=question_text, answer=answer_text, category=category)
            

"""All team management relationed models"""
class Employee(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    birthday = models.DateField(default="2024-01-01")
    occupation = models.CharField(max_length=50, default="Worker")
    department = models.CharField(max_length=50, default="Production")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    

class Team(models.Model):
    owner = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="team_owner")
    name = models.CharField(max_length=30)
    description = models.TextField()
    department = models.CharField(max_length=50)
    members = models.ManyToManyField(Employee, related_name='team_members')
    created_at = models.DateTimeField(auto_now_add=True)
    access_key = models.CharField(max_length=8, primary_key=True)
    
    def __str__(self):
        return self.name
    
    
class Team_Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=50)
    status = models.BooleanField(default="Uncompleted")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='assigned_team')
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_employee')
    
    def __str__(self):
        return self.title
    

#Personal Tasks Relationed Models
class Personal_Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=50)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='owner')
    #Now, we need to tell the model how the posts should be ordered, and displayed on the web page. The logic for this will be added to a nested inner Meta class. The Meta class generally contains other important model logic that isn’t related to database field definition.
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.title
    

#Questions model for help section 
class Help_Question(models.Model):
    question = models.CharField(max_length=150)
    answer = models.TextField()
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.question


#This class is for a sugested model, the comments that I suggest to the client to add this part because it can be useful and interesting to add this part on a every task if the Employee have a sugestion, comment, complaint or doubt.
class Comment(models.Model):
    comment_owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='comment_owner')
    content = models.TextField()
    task = models.ForeignKey(Team_Task, on_delete=models.CASCADE, related_name='comment_task')
    comment_date = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    reason = models.CharField(max_length=150)
    message = models.TextField()
    destinatary = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    
    