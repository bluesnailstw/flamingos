from users.models import User
from django.contrib.auth.models import Group
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'gitlab',)
        read_only_fields = ('date_joined', 'last_login', 'name', 'email')


class UserGroupSerializer(serializers.ModelSerializer):
    user_set = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.all())

    class Meta:
        model = Group
        fields = '__all__'
