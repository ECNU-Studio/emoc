# -*- coding: utf-8 -*-
from django.db import models
from users.models import UserProfile


class Questionnaire(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ("export", "Can export questionnaire answers"),
            ("management", "Management Tools")
        )


class RunInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    subject = models.ForeignKey(UserProfile)
    random = models.CharField(max_length=32) # probably a randomized md5sum
    runid = models.CharField(max_length=32)
    questionnaire = models.ForeignKey(Questionnaire, blank=True, null=True) # or straight int?
    emailcount = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    emailsent = models.DateTimeField(null=True, blank=True)

    lastemailerror = models.CharField(max_length=64, null=True, blank=True)

    state = models.CharField(max_length=16, null=True, blank=True)
    cookies = models.TextField(null=True, blank=True)

    tags = models.TextField(
            blank=True,
            help_text=u"Tags active on this run, separated by commas"
        )

    skipped = models.TextField(
            blank=True,
            help_text=u"A comma sepearted list of questions to skip"
        )


    def __unicode__(self):
        return "%s: %s, %s" % (self.runid, self.subject.surname, self.subject.givenname)

    class Meta:
        verbose_name_plural = 'Run Info'


class RunInfoHistory(models.Model):
    subject = models.ForeignKey(UserProfile)
    runid = models.CharField(max_length=32)
    completed = models.DateField()
    tags = models.TextField(
            blank=True,
            help_text=u"Tags used on this run, separated by commas"
        )
    skipped = models.TextField(
            blank=True,
            help_text=u"A comma sepearted list of questions skipped by this run"
        )
    questionnaire = models.ForeignKey(Questionnaire)

    def __unicode__(self):
        return "%s: %s on %s" % (self.runid, self.subject, self.completed)

    class Meta:
        verbose_name_plural = 'Run Info History'


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    number = models.CharField(max_length=8)
    sort_id = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)
    type = models.CharField(u"Type of question", max_length=32,
        choices = (
            ('choice', u'单选'), ('multi', u'多选'), ('star', u'打星'), ('ask', u'问答'),
        ))

    def __unicode__(self):
        return u'{%s} (%s) %s' % (unicode(self.questionnaire), self.number, self.text)

class Choice(models.Model):
    question = models.ForeignKey(Question)
    sortid = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=64)
    text = models.TextField(u"Choice Text")
    tags = models.CharField(u"Tags", max_length=64, blank=True)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.sortid, self.text)


class Answer(models.Model):
    subject = models.ForeignKey(UserProfile, help_text = u'The user who supplied this answer')
    question = models.ForeignKey(Question, help_text = u"The question that this is an answer to")
    runid = models.CharField(u'RunID', help_text = u"The RunID (ie. year)", max_length=32)
    answer = models.TextField()

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.number, self.subject.surname, self.subject.givenname)

