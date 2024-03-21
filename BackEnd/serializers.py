from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'status', 'created_at', 'slug')
        read_only_fields = ('created_at', 'slug')