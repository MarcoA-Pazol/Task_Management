from django.db import models

# Create your models here.
class Task(models.Models):
    title = models.CharField(max_length=200)
    
