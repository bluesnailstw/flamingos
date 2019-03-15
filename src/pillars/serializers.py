from rest_framework import serializers
from pillars.models import Configuration, Vars
from inventory.models import Inventory


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
        read_only_fields = ('extra_data', 'date_created', 'date_updated')

    # def create(self, validated_data):
    #     configuration = Configuration.objects.create(**validated_data)
    #     return configuration
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.tags = validated_data.get('tags', instance.tags)
    #     instance.save()
    #     return instance


class VarsSerializer(serializers.ModelSerializer):
    configure = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Configuration.objects.all())
    inventory = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Inventory.objects.all())

    class Meta:
        model = Vars
        fields = '__all__'
        read_only_fields = ('date_created', 'date_updated')
