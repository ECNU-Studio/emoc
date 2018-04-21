# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile
from django.utils.translation import ugettext as _
from nengli8.models import *

CHOICES_TYPE = [('radio', u'单选'), ('checkbox', u'多选'), ('star', u'打星'), ('text', u'问答')]

Examination_TYPE = [('fixed', u'固定卷'), ('random', u'随机卷')]

class Examination(models.Model):
    course = models.ForeignKey(CourseOld, verbose_name=_(u"课程"), related_name='examination_course_id')
    is_published = models.BooleanField(default=False, verbose_name=u'是否发布')
    take_nums = models.IntegerField(default=0, verbose_name=u'参与人数')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self

    def get_questions(self):
        return Question.objects.get(course=self.course)



class Question(models.Model):
    course = models.ForeignKey(CourseOld, verbose_name=_(u"课程"))
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    type = models.CharField(max_length=32, choices=CHOICES_TYPE, verbose_name=_(u"题型"))
    text = models.CharField(max_length=128, verbose_name=_(u"问题"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def choices(self):
        return Choice.objects.filter(question=self).order_by('sortnum')

    def statistics(self):
        return ExaminationStatistics.objects.values('choice', 'choice_text', 'sum', 'percent').filter(question=self.id).order_by('csort')

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'[%s] (%d) %s' % (self.course, self.sortnum, self.text)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    text = models.CharField(max_length=128, verbose_name=_(u"选项"))
    tags = models.CharField(u"Tags", max_length=64, blank=True, editable=False)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.sortnum, self.sortnum, self.text)





class TakeInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    user = models.ForeignKey(UserProfile, verbose_name=_(u"用户"), related_name='examination_user_id')
    course = models.ForeignKey(CourseOld, verbose_name=_(u"课程"))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u"测试时间"))

    def __unicode__(self):
        return "%s, %s: %s" % (self.user.first_name, self.user.last_name, self.course.name)

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name


class Answer(models.Model):
    takeinfo = models.ForeignKey(TakeInfo)
    question = models.IntegerField()
    choice = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.sortnum, self.question.text, self.text)


# 效率统计
class ExaminationStatistics(models.Model):
    course = models.IntegerField()
    name = models.CharField(max_length=128, verbose_name=_(u"标题"))
    question = models.IntegerField()
    question_text = models.CharField(max_length=128, verbose_name=_(u"问题"))
    qsort = models.IntegerField()
    type = models.CharField(max_length=32)
    choice = models.IntegerField()
    choice_text = models.CharField(max_length=128, verbose_name=_(u"选项"))
    csort = models.IntegerField()
    sum = models.IntegerField()
    percent = models.IntegerField()

    class Meta:
        managed = False
        db_table = "examination_statistics"