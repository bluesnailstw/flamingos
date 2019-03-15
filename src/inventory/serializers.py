from rest_framework import serializers
from inventory.models import Inventory
from users.models import User
from django.contrib.auth.models import Group


class InventorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())
    user_group = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Group.objects.all())

    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ('reserved', 'date_created', 'date_updated')
