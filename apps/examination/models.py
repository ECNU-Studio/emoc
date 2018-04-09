# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile
from django.utils.translation import ugettext as _

CHOICES_TYPE = [('radio', u'单选'), ('checkbox', u'多选'), ('star', u'打星'), ('text', u'问答')]

class Examination(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u"问卷标题"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '测试'
        verbose_name_plural = verbose_name


class ExamQuestion(models.Model):
    examination = models.ForeignKey(Examination, verbose_name=_(u"测试"))
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    type = models.CharField(max_length=32, choices=CHOICES_TYPE, verbose_name=_(u"题型"))
    text = models.CharField(max_length=128, verbose_name=_(u"问题"))
    chice_text = models.TextField(editable=False, blank=True, null=True, verbose_name=_(u"选项"),
                                  help_text=_(u"每个选项输入后请换行"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class ExamChoice(models.Model):
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    text = models.CharField(max_length=128, verbose_name=_(u"选项"))
    tags = models.CharField(u"Tags", max_length=64, blank=True, editable=False)


class ExamRunInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    user = models.ForeignKey(UserProfile, verbose_name=_(u"问卷用户"))
    examination = models.ForeignKey(ExamQuestion, verbose_name=_(u"问卷"))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u"问卷时间"))


class ExamAnswer(models.Model):
    exam_runinfo = models.ForeignKey(ExamRunInfo)
    exam_question = models.ForeignKey(ExamQuestion)
    text = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)








