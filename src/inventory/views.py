from users.views import IsSuperUser
from rest_framework import viewsets
from inventory.models import Inventory
from inventory.serializers import InventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]

    queryset = Inventory.objects.all().order_by('name')
    serializer_class = InventorySerializer
