from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.metadata import BaseMetadata
from users.models import User
import requests
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings
from collections import OrderedDict


class TemplateViewWithCsrf(TemplateView):

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FBackend:
    def authenticate(self, request, username=None, password=None):

        def get_dummy_token():
            data = {'access_token': 'token_test'
                    }
            return data

        def get_token():
            payload = {
                'grant_type': 'password',
                'username': username,
                'password': password
            }
            r = requests.post('%s/oauth/token' % settings.GITLAB_HOST, data=payload)
            return r.json()

        gitlab_auth = get_dummy_token()
        token = gitlab_auth.get('access_token', '')

        if token:
            def get_dummy_user_info():
                return username, None

            def get_user_info():
                r = requests.get('%s/api/v3/user?access_token=%s' % (settings.GITLAB_HOST, token))
                data = r.json()
                return data.get('name'), data.get('avatar_url')

            real_name, avatar_url = get_dummy_user_info()
            user, created = User.objects.update_or_create(email=username,
                                                          defaults={
                                                              'name': real_name,
                                                              'gitlab': gitlab_auth,
                                                              'avatar': avatar_url
                                                          })
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('results', data)
        ]))


class FMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """

    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description()
        }
