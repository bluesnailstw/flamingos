from django.contrib.auth.models import Group
from deploy.models import Task, TASK_STATUS
from deploy.serializers import TaskSerializer
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from deploy.tasks import deploy_async
from rest_framework.decorators import api_view, permission_classes
from users.views import IsSuperUser


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Task.objects.all().order_by('date_created')
    serializer_class = TaskSerializer


@api_view(['POST'])
@permission_classes([IsSuperUser])
def do_deploy(request):
    if request.method == 'POST':
        t_id = request.data['task_id']
        # self_vars = request.data['vars']
        self_vars = {}
        job_id = deploy_async(t_id, request.user, self_vars)
        return JsonResponse({"message": "ok", "data": job_id})
