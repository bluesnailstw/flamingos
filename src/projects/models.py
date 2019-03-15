from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from users.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from asset.models import Host, HostGroup


class Line(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=u"产品线")
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, null=True)
    user = models.ManyToManyField(User)
    user_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    host_group = models.ForeignKey(HostGroup, null=True, on_delete=models.SET_NULL)
    sls = models.FilePathField(path=settings.SALT_STATE_DIRECTORY,
                               allow_files=False, allow_folders=True, recursive=True)
    description = models.TextField(null=True)
    tags = ArrayField(models.CharField(max_length=255), default=list)
    status = models.IntegerField(null=True)
    line = models.ForeignKey(Line, null=True, related_name=u"business", verbose_name=u"产品线",
                             on_delete=models.SET_NULL)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return self.name
