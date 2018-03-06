# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from transmeta import TransMeta
from django.utils.translation import ugettext_lazy as _


from django.db import models

# Create your models here.


class Subject(models.Model):
    state = models.CharField(max_length=16, default="inactive", choices=(("active", "Active"), ("inactive", "Inactive")), verbose_name='状态')
    surname = models.CharField(max_length=64, blank=True, null=True, verbose_name='姓')
    givenname = models.CharField(max_length=64, blank=True, null=True, verbose_name='名')
    email = models.EmailField(null=True, blank=True, verbose_name='电子邮箱')
    gender = models.CharField(max_length=8, default="unset", blank=True, verbose_name='性别', choices=(("unset", " - "), ("m", "男"), ("f", "女"),))
    nextrun = models.DateField(verbose_name='下一步', blank=True, null=True)
    formtype = models.CharField(max_length=16, default='email', verbose_name='形式',
                                choices=(("email", "接收邮件"), ("paperform", "纸质",)))

    class Meta:
        verbose_name = '调查者'
        verbose_name_plural = verbose_name


# 问卷
class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    redirect_url = models.CharField(max_length=128, help_text="", default="/static/complete.html")

    class Meta:
        verbose_name = '问卷'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

# 问题集
class QuestionSet(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    sort = models.IntegerField()
    heading = models.CharField(max_length=64)
    checks = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=256)

    def __unicode__(self):
        return self.questionnaire.name

    class Meta:
        verbose_name = '问题集'
        verbose_name_plural = verbose_name


# 问题
class Question(models.Model):
    questionset = models.ForeignKey(QuestionSet)
    number = models.CharField(max_length=4)
    sort_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=256, verbose_name="题目")
    questiontype = models.CharField("题型", max_length=32, choices=(
        ('single', '单选'), ('mutle', '多选'), ('star', '打星'), ('answer', '问答'),
    ))

    def __unicode__(self):
        return '{%s} (%s) %s' % (unicode(self.questionset), self.number, self.title)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name


# 选项
class Choice(models.Model):
    question = models.ForeignKey(Question)
    sort = models.IntegerField()
    value = models.CharField("值", max_length=64)
    title = models.CharField("文本", max_length=128)
    tags = models.CharField("标签", max_length=64, null=True, blank=True)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.sort, self.title)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = verbose_name


# 答案
class Answer(models.Model):
    subject = models.ForeignKey(Subject, help_text='The user who supplied this answer')
    question = models.ForeignKey(Question, help_text="The question that this is an answer to")
    runid = models.CharField('RunID', help_text="The RunID (ie. year)", max_length=32, null=True, blank=True)
    answer = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = '答案'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.number, self.subject.surname, self.subject.givenname)





