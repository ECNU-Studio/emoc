# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.


# 企业表单
class Companys(models.Model):
    name = models.CharField(max_length=45, verbose_name=_(u"名称"))
    account = models.CharField(max_length=45, verbose_name=_(u"账户"))
    password = models.CharField(max_length=45, verbose_name=_(u"密码"))
    email = models.CharField(max_length=45,blank=True, null=True, verbose_name=_(u"邮箱"))
    legalperson = models.CharField(max_length=45, blank=True, null=True,verbose_name=_(u"法人"))
    address = models.CharField(max_length=45,blank=True, null=True, verbose_name=_(u"企业地址"))
    cover = models.CharField(max_length=45, blank=True, null=True,verbose_name=_(u"企业封面"))
    memo = models.CharField(max_length=45, blank=True, null=True,verbose_name=_(u"备注"))
    state = models.BooleanField(max_length=45, default=0, verbose_name=_(u"是否有效"))
    # add_time = models.DateTimeField(default=datetime.now, verbose_name=_(u"添加时间"))

    class Meta:
        # managed = False
        # db_table = 'companys'
        verbose_name = '企业'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name