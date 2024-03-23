from django.db import models
from django.template.defaultfilters import slugify #For generating slugs from strings
from django.contrib.auth.models import User #For authentication
from django.urls import reverse #To give us greater flexibility with creating URLs

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=100)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)
    
    # Adding functionality for the URL generation and the function for saving the post. This is crucial, because this creates a unique link to match our unique post.
    def get_absolute_url(self):
        return reverse('Task_Manager_Detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Task, self).save(*args, **kwargs)
        
#Now, we need to tell the model how the posts should be ordered, and displayed on the web page. The logic for this will be added to a nested inner Meta class. The Meta class generally contains other important model logic that isn’t related to database field definition.
class Meta:
    ordering = ['created_at']
    
    def __unicode__(self):
        return self.title

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=100)
    age = models.IntegerField()
    adress = models.CharField(max_length=255)
    email = models.EmailField()
    birthday = models.DateField()
    is_active = models.BooleanField()
    

#This class is for a sugested model, the comments that I suggest to the client to add this part because it can be useful and interesting to add this part on a every task if the employees have a sugestion, comment, complaint or doubt.
class Comment(models.Model):
    username = models.ForeignKey(Employee, on_delete=models.CASCADE)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    
    