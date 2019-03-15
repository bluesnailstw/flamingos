from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from inventory.models import Inventory


class Configuration(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=255, unique=True)
    tags = ArrayField(models.CharField(max_length=255), default=list)
    extra_data = JSONField(default=dict)
    description = models.TextField(verbose_name=u'描述', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return self.name


class Vars(models.Model):
    configure = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='vars')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='vars')
    value = models.TextField(verbose_name=u'值', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    class Meta:
        unique_together = (('configure', 'inventory'),)

    def __str__(self):
        return '%s:%s' % (self.configure.name, self.inventory.name)
