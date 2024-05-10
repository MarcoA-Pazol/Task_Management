from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

#Lists for choiceable values
OCCUPATION_CHOICES = [
        ['Back-End', 'Back-End Developer'],
        ['Graphic Design', 'Graphic Desinger'],
        ['User Experience Design', 'UX Designer']
    ]

"""All team management relationed models"""
class Employee(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    birthday = models.DateField()
    occupation = models.CharField(max_length=50, choices=OCCUPATION_CHOICES, default=None)
    department = models.CharField(max_length=50)
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
    access_key = models.CharField(max_length=8)
    
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
    question = models.CharField(max_length=50)
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
    
    

    
    