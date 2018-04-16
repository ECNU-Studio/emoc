# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile
from django.utils.translation import ugettext as _

CHOICES_TYPE = [('radio', u'单选'), ('checkbox', u'多选'), ('star', u'打星'), ('text', u'问答')]

Examination_TYPE = [('fixed', u'固定'), ('random', u'随机')]

class CourseOld(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=52, verbose_name='课程名字')

    def questions(self):
        return Question.objects.filter(course=self).order_by('sortnum')

    def __unicode__(self):
        return self.name

    def manage_question(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/examination/edit/%s' target='_blank'>编辑</a>" % self.id)

    manage_question.short_description = u"试题库"

    class Meta:
        verbose_name = '课程试题库'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'courses'

class Examination(models.Model):
    course = models.ForeignKey(CourseOld, verbose_name=_(u"试卷"))
    is_published = models.BooleanField(default=False, verbose_name=u'是否发布')
    take_nums = models.IntegerField(default=0, verbose_name=u'参与人数')
    type = models.CharField(max_length=32, choices=Examination_TYPE, verbose_name=_(u"类型"))
    question_nums = models.IntegerField(default=0, verbose_name=u'试题数')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.course

    class Meta:
        verbose_name = '课程试题'
        verbose_name_plural = verbose_name


class PublishedExamination(Examination):
    class Meta:
        verbose_name = '统计'
        verbose_name_plural = verbose_name
        proxy = True


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
        return ExaminationStatistics.objects.values('choice', 'choice_text', 'num').filter(question=self.id).order_by('csort')

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


class RunInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    user = models.ForeignKey(UserProfile, verbose_name=_(u"用户"), related_name='examination_user_id')
    examination = models.ForeignKey(Examination, verbose_name=_(u"测试"))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u"测试时间"))

    def __unicode__(self):
        return "%s, %s: %s" % (self.user.first_name, self.user.last_name, self.examination.course)

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name


class Answer(models.Model):
    runinfo = models.ForeignKey(RunInfo)
    question = models.IntegerField()
    choice = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.sortnum, self.question.text, self.text)


# 效率统计
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
    num = models.IntegerField()

    class Meta:
        managed = False
        db_table = "examination_statistics"