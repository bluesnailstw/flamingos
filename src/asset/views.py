from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from asset.models import Host, HostGroup, SERVER_STATUS, USE_STATUS
from asset.serializers import HostSerializer, HostGroupSerializer
from users.views import IsSuperUser
from rest_framework import exceptions, status
from inventory.models import Inventory
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django_filters import FilterSet, NumberFilter, BooleanFilter, CharFilter


class HostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Host.objects.all().order_by('host_name')
    serializer_class = HostSerializer

    def options(self, request, *args, **kwargs):
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        data['ext'] = {
            'inventories': [{'value': env.id, 'label': env.name} for env in Inventory.objects.all()],
        }
        data['ext']['inventories'].append({'value': None, 'label': '未定义'})
        return Response(data, status=status.HTTP_200_OK)


class HostGroupFilter(FilterSet):
    is_root = BooleanFilter(field_name='parent', lookup_expr='isnull')

    class Meta:
        model = HostGroup
        fields = ['name', 'parent', 'is_root']


class HostGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]

    queryset = HostGroup.objects.all().order_by('name')
    serializer_class = HostGroupSerializer
    filterset_class = HostGroupFilter


class HostGroupContentView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, format=None):
        data = {}
        host_group_id = request.query_params.get('id')
        try:
            host_group = HostGroup.objects.get(id=host_group_id)
        except ObjectDoesNotExist or MultipleObjectsReturned:
            pass
        else:
            data['host'] = [{'id': host.id,
                             'host_name': host.host_name} for host in host_group.hosts.all()]
        return Response(data)
