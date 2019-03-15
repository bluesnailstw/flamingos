from django.db import models
from users.models import User
from django.contrib.postgres.fields import JSONField, ArrayField
from inventory.models import Inventory

idc_type = (
    (0, u"CDN"),
    (1, u"核心")
)

idc_operator = (
    (0, u"电信"),
    (1, u"联通"),
    (2, u"移动"),
    (3, u"铁通"),
    (4, u"小带宽"),
)

SERVER_STATUS = (
    (0, u"未知"),
    (1, u"正常"),
    (2, u"禁用"),
    (3, u"报废"),
)
USE_STATUS = (
    (0, u"保留"),
    (1, u"未分配"),
    (2, u"已分配"),
)

ENVIRONMENT = (
    (0, u"保留"),
    (1, u"未分配"),
    (2, u"已分配"),
)

ENVIRONMENT_CHOICES = (
    (0, u"未指定"),
    (1, u"测试环境"),
    (2, u"预发布环境"),
    (3, u"生产环境"),
)


class IDC(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=u'机房名称')
    bandwidth = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'机房带宽')
    phone = models.CharField(max_length=255, verbose_name=u'联系电话')
    linkman = models.CharField(max_length=255, null=True, verbose_name=u'联系人')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, verbose_name=u"IP地址段")
    operator = models.IntegerField(verbose_name=u"运营商", choices=idc_operator, blank=True, null=True)
    type = models.IntegerField(verbose_name=u"机房类型", choices=idc_type, blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name=u"备注")
    date_created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    minion_id = models.CharField(max_length=255, unique=True, verbose_name=u"minion 唯一标识")
    host_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"主机名")
    machine_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"主机ID")
    manufacturer = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'硬件厂商')
    serialnumber = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'序列号')
    oscodename = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'系统代号')
    osrelease = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'系统版本')
    cpu_model = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'cpu型号')
    disks = ArrayField(models.CharField(max_length=255), default=list, verbose_name=u'磁盘')
    mem_total = models.IntegerField(default=0, verbose_name=u'物理内存MB')
    swap_total = models.IntegerField(default=0, verbose_name=u'交换内存MB')
    num_cpus = models.IntegerField(default=0, verbose_name=u'cpu核心数')
    ip4_interfaces = JSONField(default=dict)
    virtual = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'硬件虚拟化类型')
    virtual_subtype = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'内核虚拟化类型')

    father = models.ForeignKey("self", blank=True, null=True, verbose_name=u"父主机",
                               related_name='children', on_delete=models.PROTECT)

    idc = models.ForeignKey(IDC, blank=True, null=True, verbose_name=u'机房',
                            related_name='hosts', on_delete=models.SET_NULL)
    guarantee_date = models.DateField(blank=True, null=True, verbose_name=u'保修时间')
    cabinet = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'机柜号')
    server_cabinet_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'机器位置')
    number = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'资产编号')
    room_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"房间号")
    server_sn = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"SN编号")

    inventory = models.ForeignKey(Inventory, null=True, verbose_name=u'环境',
                                  related_name='hosts', on_delete=models.SET_NULL)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    idle = models.IntegerField(choices=USE_STATUS, default=1, verbose_name=u'使用状态')
    status = models.IntegerField(choices=SERVER_STATUS, default=1, verbose_name=u"管理状态")
    comment = models.TextField(blank=True, null=True, verbose_name=u'备注')

    salt_raw = JSONField(default=dict)

    def __str__(self):
        return self.host_name


class HostGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=u'组名')
    hosts = models.ManyToManyField(Host)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='children')
    comment = models.TextField(blank=True, null=True, verbose_name=u'备注')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    date_updated = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __str__(self):
        return self.name
