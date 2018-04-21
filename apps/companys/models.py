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


#用户基本信息表
class Users(models.Model):
    username = models.CharField(max_length=45, verbose_name=_(u"用户账号"))
    name = models.CharField(max_length=45, verbose_name=_(u"姓名"))
    # photo = models.CharField(max_length=1000, verbose_name=_(u"头像"))
    password = models.CharField(max_length=45, verbose_name=_(u"密码"))
    # companyID = models.IntegerField(default=0,  verbose_name=_(u"公司ID"))
    department = models.CharField(max_length=45, blank=True, null=True , verbose_name=_(u"部门"))
    position = models.CharField(max_length=45,blank=True, null=True , verbose_name=_(u"职位"))
    # openid = models.CharField(max_length=45, verbose_name=_(u"微信openid"))
    # qq = models.CharField(max_length=45, verbose_name=_(u"QQ"))
    tel = models.CharField(max_length=45, blank=True, null=True ,verbose_name=_(u"电话"))
    email = models.CharField(max_length=45,blank=True, null=True , verbose_name=_(u"邮箱"))
    # notice_wenda = models.BooleanField(max_length=45, verbose_name=_(u"问答通知"))
    # notice_pinglun = models.BooleanField(max_length=45, verbose_name=_(u"评论通知"))
    # notice_sendmail = models.BooleanField(max_length=45, verbose_name=_(u"问答评论发送邮箱"))
    # total_hours = models.IntegerField(default=0,  verbose_name=_(u"累计学时"))
    total_class = models.IntegerField(default=0, blank=True, null=True , verbose_name=_(u"学习课程"))
    # total_day = models.IntegerField(default=0,  verbose_name=_(u"累计天数"))
    # classID = models.IntegerField(default=0,  verbose_name=_(u"班级id"))
    # dayBefor = models.DateTimeField( verbose_name=_(u"上次时间"))
    # dayFirst = models.DateTimeField( verbose_name=_(u"连续登陆，第一次登陆"))
    # total_score = models.FloatField(max_length=12, verbose_name=_(u"总成绩"))
    # class_finish = models.IntegerField(default=0,  verbose_name=_(u"已完成课程"))
    # state = models.BooleanField(max_length=1, verbose_name=_(u"是否有效"))
    # new_ans = models.BooleanField(max_length=1, verbose_name=_(u"是否有新的回复"))
    # classStudent = models.CharField(max_length=45, verbose_name=_(u"班级"))
    companyid = models.ForeignKey(Companys, default=0, to_field='id',verbose_name=_(u"公司"))
    # language = models.CharField(max_length=45, verbose_name=_(u"语言（1中文，2英文）"))
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class ComtoUsers(models.Model):
    companys = models.ForeignKey(Companys, to_field='id',verbose_name= _(u"公司"))
    users = models.ForeignKey(Users,  to_field='id', verbose_name=_(u"用户"))