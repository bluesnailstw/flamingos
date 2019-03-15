from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from users.models import User
from django.contrib.auth.models import Group


class Inventory(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=255, unique=True)
    user = models.ManyToManyField(User)
    user_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    tags = ArrayField(models.CharField(max_length=255), default=list)
    reserved = models.TextField(blank=True, null=True)
    description = models.TextField(verbose_name=u'描述', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return self.name
