from users.views import IsSuperUser
from pillars.models import Configuration, Vars
from pillars.serializers import ConfigurationSerializer, VarsSerializer
from rest_framework import viewsets


class ConfigurationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]

    queryset = Configuration.objects.all().order_by('name')
    serializer_class = ConfigurationSerializer


class VarsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Vars.objects.all().order_by('configure')
    serializer_class = VarsSerializer
