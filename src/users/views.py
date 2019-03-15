from users.models import User
from users.serializers import UserSerializer, UserGroupSerializer
from rest_framework import permissions
from django.contrib.auth import views
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework import exceptions, status


class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class FLoginView(views.LoginView):

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponse()


class FLogoutView(views.LogoutView):

    def get(self, request, *args, **kwargs):
        return HttpResponse()


class UserGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]

    queryset = Group.objects.all().order_by('name')
    serializer_class = UserGroupSerializer

    def options(self, request, *args, **kwargs):
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        data['ext'] = {
            'users': [{'value': user.id, 'label': user.name} for user in User.objects.filter(is_active=True)]}
        return Response(data, status=status.HTTP_200_OK)
