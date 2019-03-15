from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from asset.models import Host, HostGroup
from projects.models import Project
from users.models import User
from inventory.models import Inventory

TASK_STATUS = (
    ("standby", "待命中"),
    ("running", "运行中"),
    ("stopped", "已停止"),
)


class Task(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    target = models.ForeignKey(HostGroup, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name=u"状态", choices=TASK_STATUS, default=TASK_STATUS[0][0])
    tags = ArrayField(models.CharField(max_length=255), default=list)
    occupy = models.CharField(max_length=255, unique=True, verbose_name=u"job id", null=True)
    barn = ArrayField(models.CharField(max_length=255), verbose_name=u'待处理主机', default=list)
    operator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return '%s:%s' % (self.project.name, self.inventory.name)


class History(models.Model):
    job_id = models.CharField(max_length=255, verbose_name=u"状态", null=True)
    minion_id = models.CharField(max_length=255, verbose_name=u"状态", null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
    result = JSONField(default=dict)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        unique_together = (('job_id', 'minion_id'),)

    def __str__(self):
        return '%s:%s' % (self.job_id, self.minion_id)
