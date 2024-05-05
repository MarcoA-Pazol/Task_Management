from django.db import models
from django.contrib.auth.models import AbstractUser

"""All team management relationed models"""
class Employee(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    birthday = models.DateField()
    department = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        return self.username

class Team(models.Model):
    owner = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="team_owner")
    name = models.CharField(max_length=200)
    description = models.TextField()
    area = models.CharField(max_length=200)
    members = models.ManyToManyField(Employee, related_name='team_members')
    created_at = models.DateTimeField(auto_now_add=True)
    access_code = models.CharField(max_length=8)
    
    def __str__(self):
        return self.name
    
class Team_Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=100)
    status = models.BooleanField(default="Uncompleted")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='assigned_team')
    assigned_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_employee')
    
    def __str__(self):
        return self.title
    

#Personal Tasks Relationed Models
class Personal_Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=100)
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
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question

    

#This class is for a sugested model, the comments that I suggest to the client to add this part because it can be useful and interesting to add this part on a every task if the Employee have a sugestion, comment, complaint or doubt.
class Comment(models.Model):
    comment_owner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='comment_owner')
    content = models.TextField()
    task = models.ForeignKey(Team_Task, on_delete=models.CASCADE, related_name='comment_task')
    comment_date = models.DateTimeField(auto_now_add=True)
    
    

    
    