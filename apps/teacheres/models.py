# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models

# Create your models here.

#培训师表单
class Teacheres(models.Model):
    username = models.CharField(max_length=45, verbose_name=_(u"教师登录名"))
    password = models.CharField(max_length=45, verbose_name=_(u"密码"))
    name = models.CharField(max_length=45, verbose_name=_(u"教师姓名"))
    email = models.CharField(max_length=45, verbose_name=_(u"邮箱"))
    phone = models.CharField(max_length=45, verbose_name=_(u"手机"))
    weixin = models.CharField(max_length=45, verbose_name=_(u"微信"))
    header = models.CharField(max_length=1000, verbose_name=_(u"头像"))
    introduce = models.CharField(max_length=500, verbose_name=_(u"介绍"))
    cv = models.CharField(max_length=500, verbose_name=_(u"简历"))
    openid = models.CharField(max_length=45, verbose_name=_(u"openid"))
    state = models.BooleanField(choices=(("true", "有效"), ("false", "无效")), verbose_name=_(u"是否有效"))
    notice_wenda = models.CharField(max_length=45, verbose_name=_(u"问答通知"))
    notice_pinglun = models.CharField(max_length=45, verbose_name=_(u"评论通知"))
    notice_sendmail = models.CharField(max_length=45, verbose_name=_(u"问答评论发送邮箱"))
    new_ans = models.CharField(max_length=45, verbose_name=_(u"回复"))
    language = models.CharField(max_length=45, verbose_name=_(u"语言（1中文，2英文）"))

    class Meta:
        verbose_name = '培训师'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'teacheres'
    def __unicode__(self):
        return self.name
