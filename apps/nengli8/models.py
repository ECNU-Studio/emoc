# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class companys(models.Model):
    name = models.CharField(max_length=45, verbose_name=_(u"名称"))
    account = models.CharField(max_length=45, verbose_name=_("账户"))
    password = models.CharField(max_length=45, verbose_name=_("密码"))
    email = models.CharField(max_length=45, verbose_name=_(u"邮箱"))
    legalperson = models.CharField(max_length=45, verbose_name=_("法人"))
    address = models.CharField(max_length=45, verbose_name=_("企业地址"))
    cover = models.CharField(max_length=45, verbose_name=_(u"企业封面"))
    memo = models.CharField(max_length=45, verbose_name=_("备注"))
    state = models.CharField(max_length=45, verbose_name=_("是否有效"))

    class Meta:
        verbose_name = '企业'
        verbose_name_plural = verbose_name

