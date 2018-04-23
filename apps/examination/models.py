# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile
from django.utils.translation import ugettext as _
from nengli8.models import *

CHOICES_TYPE = [('radio', u'单选'), ('checkbox', u'多选'), ('star', u'打星'), ('text', u'问答')]

class Examination(models.Model):
    course = models.ForeignKey(CourseOld, verbose_name=_(u"问卷"), related_name='examination_course_id')
    is_published = models.BooleanField(default=False, verbose_name=u'是否发布')
    take_nums = models.IntegerField(default=0, verbose_name=u'参与人数')
    is_random = models.BooleanField(default=False, verbose_name=u'是否随机')
    question_count = models.IntegerField(default=0, verbose_name=u'题目数量')

    def questions(self):
        return Question.objects.filter(examination=self).order_by('sortnum')

    def questions_use(self):
        return Question.objects.filter(examination=self, is_use=True).order_by('sortnum')

    def statistics(self):
        return ExaminationStatistics.objects.filter(questionnaire=self.id).order_by('qsort')

    def __unicode__(self):
        return self.course.name

    class Meta:
        verbose_name = '问卷'
        verbose_name_plural = verbose_name


class Question(models.Model):
    examination = models.ForeignKey(Examination, verbose_name=_(u"试卷"))
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    type = models.CharField(max_length=32, choices=CHOICES_TYPE, verbose_name=_(u"题型"))
    text = models.CharField(max_length=128, verbose_name=_(u"问题"))
    is_use = models.BooleanField(default=False, verbose_name=u'是否使用')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def choices(self):
        return Choice.objects.filter(question=self).order_by('sortnum')

    def statistics(self):
        return ExaminationStatistics.objects.values('choice', 'choice_text', 'sum', 'percent').filter(question=self.id).order_by('csort')

    def get_answer_texts(self):
        return Answer.objects.values('text').filter(question=self.id).order_by('id')[:5]

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'[%s] (%d) %s' % (self.examination, self.sortnum, self.text)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    is_answer = models.BooleanField(default=False, verbose_name=u'是否正确答案')
    text = models.CharField(max_length=128, verbose_name=_(u"选项"))
    tags = models.CharField(u"Tags", max_length=64, blank=True, editable=False)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.sortnum, self.sortnum, self.text)


class TakeInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    user = models.ForeignKey(UserOld, verbose_name=_(u"问卷用户"))
    examination = models.ForeignKey(Examination, verbose_name=_(u"课程"))
    score = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True, verbose_name=_(u"开始时间"))
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_(u"结束时间"))

    def __unicode__(self):
        return "%s: %s" % (self.user.username, self.examination.course.name)

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


# 统计
class ExaminationStatistics(models.Model):
    examination = models.IntegerField()
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