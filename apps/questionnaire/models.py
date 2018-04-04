# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile
from django.utils.translation import ugettext as _

CHOICES_TYPE = [('radio', u'单选'), ('checkbox', u'多选'), ('star', u'打星'), ('text', u'问答')]


class Questionnaire(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u"问卷标题"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def questions(self):
        return Question.objects.filter(questionnaire=self).order_by('sortnum')

    def edit_questionnaire(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/questionnaire/edit/%s' target='_blank'>编辑问卷</a>" % self.id)

    edit_questionnaire.short_description = u"编辑"

    def show_questionnaire(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/questionnaire/take/%s/0' target='_blank'>预览问卷</a>" % self.id)

    show_questionnaire.short_description = u"预览"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '问卷'
        verbose_name_plural = verbose_name
        permissions = (
            ("export", "Can export questionnaire answers"),
            ("management", "Management Tools")
        )


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, verbose_name=_(u"问卷"))
    sortnum = models.IntegerField(default=1, verbose_name=_(u"序号"))
    type = models.CharField(max_length=32, choices=CHOICES_TYPE, verbose_name=_(u"题型"))
    text = models.CharField(max_length=128, verbose_name=_(u"问题"))
    chice_text = models.TextField(editable=False, blank=True, null=True, verbose_name=_(u"选项"), help_text=_(u"每个选项输入后请换行"))
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def choices(self):
        return Choice.objects.filter(question=self).order_by('sortnum')

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'[%s] (%d) %s' % (self.questionnaire, self.sortnum, self.text)


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
    subject = models.ForeignKey(UserProfile, verbose_name=_(u"问卷用户"))
    questionnaire = models.ForeignKey(Questionnaire, verbose_name=_(u"问卷"))
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_(u"问卷时间"))

    def __unicode__(self):
        return "%s, %s: %s" % (self.subject.first_name, self.subject.last_name, self.questionnaire.name)

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name


class Answer(models.Model):
    runinfo = models.ForeignKey(RunInfo)
    question = models.ForeignKey(Question)
    text = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.sortnum, self.subject.surname, self.subject.givenname)
