from asset.models import Host, HostGroup
from rest_framework import serializers
from inventory.models import Inventory


class HostSerializer(serializers.ModelSerializer):
    status_h = serializers.CharField(source='get_status_display')
    idle_h = serializers.CharField(source='get_idle_display')
    inventory = serializers.PrimaryKeyRelatedField(allow_null=True,
                                                   queryset=Inventory.objects.all())
    inventory_h = serializers.StringRelatedField(source='inventory')

    class Meta:
        model = Host
        exclude = ('salt_raw',)
        read_only_fields = ('minion',
                            'date_created',
                            'date_updated',
                            'host_name',
                            'machine_id',
                            'manufacturer',
                            'serialnumber',
                            'oscodename',
                            'osrelease',
                            'cpu_model',
                            'disks',
                            'mem_total',
                            'swap_total',
                            'num_cpus',
                            'virtual',
                            'virtual_subtype',
                            'ip4_interfaces')


class HostGroupSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(required=False, read_only=False,
                                                queryset=HostGroup.objects.all())
    children = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    hosts = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Host.objects.all())

    class Meta:
        model = HostGroup
        fields = '__all__'
        read_only_fields = ('date_created', 'date_updated')
