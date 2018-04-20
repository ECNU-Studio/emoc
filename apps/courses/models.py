# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

#课程
class Courses(models.Model):
    name = models.CharField(max_length=45, verbose_name=_(u"课程名称"))
    coursesAbstract = models.TextField(max_length=45, verbose_name=_(u"课程简介"))
    cover = models.ImageField(max_length=45, verbose_name=_(u"封面"))
    teacherid = models.IntegerField(default=0,  verbose_name=_(u"讲师id"))
    # state = models.CharField(max_length=45, verbose_name=_(u"是否有效"))
    # honor = models.CharField(max_length=45, verbose_name=_(u"勋章图"))
    # abstractFile = models.CharField(max_length=1000,blank=True, null=True, verbose_name=_(u"简介附件"))
    # abstractFileSize = models.CharField(max_length=500, verbose_name=_(u"简介附件文件大小"))
    # abstractFileName = models.CharField(max_length=500, verbose_name=_(u"简介附件名称"))
    # teacher = models.ForeignKey(Teacheres , verbose_name=_(u"此课程的上课教师"))
    # classes = models.ForeignKey(Classes, verbose_name=_(u"上此课程的班级"))
    # catalog = models.ForeignKey(Catalog , verbose_name=_(u"课程目录"))

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'courses'

    def __unicode__(self):
        return self.name
