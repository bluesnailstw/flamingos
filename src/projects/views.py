from users.views import IsSuperUser
from projects.models import Project
from projects.serializers import ProjectSerializer
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Project.objects.all().order_by('name')
    serializer_class = ProjectSerializer
