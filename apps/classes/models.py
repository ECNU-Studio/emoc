# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext as _
#from courses.models import Courses
# Create your models here.


#班级
class Classes(models.Model):
    companyid = models.CharField(max_length=45, verbose_name=_(u"公司id"))
    coursesid = models.CharField(max_length=45, verbose_name=_(u"课程id"))
    schoolTime = models.DateTimeField( verbose_name=_(u"上课时间"))
    address = models.CharField(max_length=100, verbose_name=_(u"上课地点"))
    state = models.BooleanField(max_length=1, verbose_name=_(u"状态"))
    period = models.CharField(max_length=45, verbose_name=_(u"周期"))
    hour = models.IntegerField(default=0 , verbose_name=_(u"学时"))
    # classStudent = models.ForeignKey(ClassStudent, verbose_name=_(u"上次课程的学生"))
    # courses = models.ForeignKey(Courses, verbose_name=_(u"此班级要上的课程"))
    # companys = models.ForeignKey(Companys, verbose_name=_(u"上此课程的公司"))
    # classModels = models.ForeignKey(ClassModels, verbose_name=_(u"课程模块"))
    # comment = models.ForeignKey(Comment, verbose_name=_(u"评论"))
    # classAddress = models.ForeignKey(ClassAddress, default="", verbose_name=_(u"班级地址"))
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = verbose_name
        # managed = False
        # db_table = 'class'


    # def teacher(self):
    #     course = Courses.objects.filter(id=self.coursesid)
    #     return course.teacher

    def __unicode__(self):
        return self.coursesid