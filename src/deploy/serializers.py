from django.contrib.auth.models import Group
from deploy.models import Task, History
from projects.models import Project
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Project.objects.all())
    target = serializers.PrimaryKeyRelatedField(read_only=True)
    operator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('status', 'occupy', 'operator', 'date_created', 'date_updated')
