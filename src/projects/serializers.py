from projects.models import Project, Line
from rest_framework import serializers
from users.models import User
from django.contrib.auth.models import Group
from asset.models import Host, HostGroup


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    user_group = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Group.objects.all())
    host_group = serializers.PrimaryKeyRelatedField(read_only=False, queryset=HostGroup.objects.all())
    line = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Line.objects.all())

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('date_created', 'date_updated')
