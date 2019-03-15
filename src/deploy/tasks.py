from salt.salt_api import Pepper
from asset.models import Host, HostGroup
from deploy.models import Task, TASK_STATUS, History
from django.conf import settings
from users.models import User
from pillars.models import Vars, Configuration
from redis import StrictRedis


def get_all_hosts(task: Task):
    hosts = set()

    def travel(node: HostGroup):
        if node is None:
            return
        for host in node.hosts.filter(inventory=task.inventory):
            hosts.add(host.host_name)
        for child in node.children.all():
            travel(child)
    if task.target:
        travel(task.target)
    else:
        travel(task.project.host_group)
    return list(hosts)


def deploy_async(t_id: int, user: User, self_vars: dict):
    task = Task.objects.get(id=t_id)
    sls = task.project.sls.replace(settings.SALT_STATE_DIRECTORY, '')
    hosts = get_all_hosts(task)
    values = {**{value.configure.name: value.value
                 for value in Vars.objects.filter(inventory=task.inventory)}, **self_vars}
    pipe = StrictRedis(host=settings.REDIS_HOST_SERVER,
                       port=settings.REDIS_HOST_PORT,
                       db=settings.REDIS_DB).pipeline()
    for hostname in hosts:
        pipe.delete(hostname)
        pipe.hmset(hostname, values)
        responses = pipe.execute()
        print("sync values to redis for hostname[%s], result: %s" % (hostname, str(responses)))
    print("project %s deployed on hosts; %s" % (task.project.name, hosts))
    p = Pepper().login()
    result = p.local_async(tgt=hosts, fun='state.sls',
                           arg=[sls], tgt_type='list')
    # {'return': [{'jid': '20190301083447106122', 'minions': ['074cda43674f']}]}
    task.status = TASK_STATUS[1][0]
    job_id = result['return'][0]['jid']
    task.barn = result['return'][0]['minions']
    task.occupy = job_id
    task.operator = user
    task.save()
    return job_id
