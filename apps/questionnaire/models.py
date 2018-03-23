# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile

CHOICES_TYPE = [('choice', u'单选'), ('multi', u'多选'), ('star', u'打星'), ('ask', u'问答')]


class Questionnaire(models.Model):
    name = models.CharField(max_length=128)

    def questions(self):
        return Question.objects.filter(questionnaire=self).order_by('sortnum')

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ("export", "Can export questionnaire answers"),
            ("management", "Management Tools")
        )


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    sortnum = models.IntegerField()
    text = models.TextField(blank=True)
    type = models.CharField(u"Type of question", max_length=32, choices=CHOICES_TYPE)

    def chices(self):
        return Choice.objects.filter(question=self).order_by('sortnum')

    def __unicode__(self):
        return u'[%s] (%s) %s' % (self.questionnaire, self.sortnum, self.text)


class Choice(models.Model):
    question = models.ForeignKey(Question)
    sortnum = models.IntegerField()
    text = models.TextField(u"Choice Text")
    tags = models.CharField(u"Tags", max_length=64, blank=True)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.sortnum, self.sortnum, self.text)


class RunInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    subject = models.ForeignKey(UserProfile)
    questionnaire = models.ForeignKey(Questionnaire, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s, %s" % (self.runid, self.subject.surname, self.subject.givenname)

    class Meta:
        verbose_name_plural = 'Run Info'


class Answer(models.Model):
    runinfo = models.ForeignKey(RunInfo)
    question = models.ForeignKey(Question)
    text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.sortnum, self.subject.surname, self.subject.givenname)
