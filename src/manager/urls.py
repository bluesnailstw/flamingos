"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from rest_framework import routers
from users.views import UserViewSet, FLoginView, FLogoutView, UserDetailView
from users.views import UserGroupViewSet
from asset.views import HostViewSet
from asset.views import HostGroupViewSet, HostGroupContentView
from projects.views import ProjectViewSet
from deploy.views import TaskViewSet
from inventory.views import InventoryViewSet
from pillars.views import VarsViewSet, ConfigurationViewSet
from manager.utils import TemplateViewWithCsrf
from manager.views import debug, test
from deploy.views import do_deploy

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'host_groups', HostGroupViewSet)
router.register(r'user_groups', UserGroupViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'configurations', ConfigurationViewSet)
router.register(r'vars', VarsViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'inventories', InventoryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('user', UserDetailView.as_view()),
    path('login', FLoginView.as_view()),
    path('logout', FLogoutView.as_view()),
    path('host_group/content', HostGroupContentView.as_view()),
    path('deploy', do_deploy),
    path('debug', debug),
    path('test', test),
    url(r'', TemplateViewWithCsrf.as_view(template_name="index.html")),
]
