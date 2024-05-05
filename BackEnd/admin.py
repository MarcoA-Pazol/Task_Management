from django.contrib import admin
from .models import Employee, Help_Question, Team_Task, Team, Personal_Task
# Register your models here.
admin.site.register(Employee)
admin.site.register(Help_Question)
admin.site.register(Team_Task)
admin.site.register(Personal_Task)
admin.site.register(Team)
