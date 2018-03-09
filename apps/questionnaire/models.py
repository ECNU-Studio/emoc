# -*- coding: utf-8 -*-
from django.db import models
from transmeta import TransMeta
from django.utils.translation import ugettext_lazy as _
from questionnaire import QuestionChoices
import re
from utils import split_numal
import json
from parsers import parse_checks, ParseException
from django.conf import settings

_numre = re.compile("(\d+)([a-z]+)", re.I)


class Subject(models.Model):
    STATE_CHOICES = [
        ("active", _("Active")),
        ("inactive", _("Inactive")),
        # Can be changed from elsewhere with
        # Subject.STATE_CHOICES[:] = [ ('blah', 'Blah') ]
    ]
    state = models.CharField(max_length=16, default="inactive",
        choices = STATE_CHOICES, verbose_name=_('State'))
    surname = models.CharField(max_length=64, blank=True, null=True,
        verbose_name=_('Surname'))
    givenname = models.CharField(max_length=64, blank=True, null=True,
        verbose_name=_('Given name'))
    email = models.EmailField(null=True, blank=True, verbose_name=_('Email'))
    gender = models.CharField(max_length=8, default="unset", blank=True,
        verbose_name=_('Gender'),
        choices = ( ("unset", _("Unset")),
                    ("male", _("Male")),
                    ("female", _("Female")),
        )
    )
    nextrun = models.DateField(verbose_name=_('Next Run'), blank=True, null=True)
    formtype = models.CharField(max_length=16, default='email',
        verbose_name = _('Form Type'),
        choices = (
            ("email", _("Subject receives emails")),
            ("paperform", _("Subject is sent paper form"),))
    )
    language = models.CharField(max_length=8, default=settings.LANGUAGE_CODE,
        verbose_name = _('Language'), choices = settings.LANGUAGES)

    def __unicode__(self):
        return u'%s, %s (%s)' % (self.surname, self.givenname, self.email)

    def next_runid(self):
        "Return the string form of the runid for the upcoming run"
        return str(self.nextrun.year)

    def last_run(self):
        "Returns the last completed run or None"
        try:
            query = RunInfoHistory.objects.filter(subject=self)
            return query.order_by('-completed')[0]
        except IndexError:
            return None

    def history(self):
        return RunInfoHistory.objects.filter(subject=self).order_by('runid')

    def pending(self):
        return RunInfo.objects.filter(subject=self).order_by('runid')

    class Meta:
        verbose_name = '调查者'
        verbose_name_plural = verbose_name

class Questionnaire(models.Model):
    name = models.CharField(max_length=128)
    redirect_url = models.CharField(max_length=128, help_text="URL to redirect to when Questionnaire is complete. Macros: $SUBJECTID, $RUNID, $LANG", default="/static/complete.html")

    def __unicode__(self):
        return self.name

    def questionsets(self):
        if not hasattr(self, "__qscache"):
            self.__qscache = \
              QuestionSet.objects.filter(questionnaire=self).order_by('sortid')
        return self.__qscache

    def questions(self):
        questions = []
        for questionset in self.questionsets():
            questions += questionset.questions()
        return questions

    class Meta:
        verbose_name = '问卷'
        verbose_name_plural = verbose_name
        permissions = (
            ("export", "Can export questionnaire answers"),
            ("management", "Management Tools")
        )


class QuestionSet(models.Model):
    __metaclass__ = TransMeta

    "Which questions to display on a question page"
    questionnaire = models.ForeignKey(Questionnaire)
    sortid = models.IntegerField() # used to decide which order to display in
    heading = models.CharField(max_length=64)
    checks = models.TextField(blank=True,
        help_text = """Current options are 'femaleonly' or 'maleonly' and shownif="QuestionNumber,Answer" which takes the same format as <tt>requiredif</tt> for questions.""")
    text = models.TextField(u'Text', help_text="This is interpreted as Textile: <a href='http://en.wikipedia.org/wiki/Textile_%28markup_language%29' target='_blank'>http://en.wikipedia.org/wiki/Textile_(markup_language)</a>")

    def questions(self):
        if not hasattr(self, "__qcache"):
            def numeric_number(val):
                matches = re.findall(r'^\d+', val)
                return int(matches[0]) if matches else 0

            questions_with_sort_id = sorted(Question.objects.filter(questionset=self.id).exclude(sort_id__isnull=True), key=lambda q: q.sort_id)

            questions_with_out_sort_id = sorted(Question.objects.filter(questionset=self.id, sort_id__isnull=True), key=lambda q: (numeric_number(q.number), q.number))
            self.__qcache = questions_with_sort_id + questions_with_out_sort_id
        return self.__qcache

    def next(self):
        qs = self.questionnaire.questionsets()
        retnext = False
        for q in qs:
            if retnext:
                return q
            if q == self:
                retnext = True
        return None

    def prev(self):
        qs = self.questionnaire.questionsets()
        last = None
        for q in qs:
            if q == self:
                return last
            last = q

    def is_last(self):
        try:
            return self.questionnaire.questionsets()[-1] == self
        except NameError:
            # should only occur if not yet saved
            return True

    def is_first(self):
        try:
            return self.questionnaire.questionsets()[0] == self
        except NameError:
            # should only occur if not yet saved
            return True

    def __unicode__(self):
        return u'%s: %s' % (self.questionnaire.name, self.heading)

    class Meta:
        verbose_name = '问题集'
        verbose_name_plural = verbose_name
        # translate = ('text',)


class RunInfo(models.Model):
    "Store the active/waiting questionnaire runs here"
    subject = models.ForeignKey(Subject)
    random = models.CharField(max_length=32) # probably a randomized md5sum
    runid = models.CharField(max_length=32)
    # questionset should be set to the first QuestionSet initially, and to null on completion
    # ... although the RunInfo entry should be deleted then anyway.
    questionset = models.ForeignKey(QuestionSet, blank=True, null=True) # or straight int?
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

    def save(self, **kwargs):
        self.random = (self.random or '').lower()
        super(RunInfo, self).save(**kwargs)

    def add_tags(self, tags):
        for tag in tags:
            if self.tags:
                self.tags += ','
            self.tags += tag

    def remove_tags(self, tags):
        if not self.tags:
            return

        current_tags = self.tags.split(',')

        for tag in tags:
            try:
                current_tags.remove(tag)
            except ValueError:
                pass
        self.tags = ",".join(current_tags)

    def set_cookie(self, key, value):
        "runinfo.set_cookie(key, value). If value is None, delete cookie"
        key = key.lower().strip()
        cookies = self.get_cookiedict()
        if type(value) not in (int, float, str, unicode, type(None)):
            raise Exception("Can only store cookies of type integer or string")
        if value is None:
            if key in cookies:
                del cookies[key]
        else:
            if type(value) in ('int', 'float'):
                value=str(value)
            cookies[key] = value
        cstr = json.dumps(cookies)
        self.cookies=cstr
        self.save()
        self.__cookiecache = cookies

    def get_cookie(self, key, default=None):
        if not self.cookies:
            return default
        d = self.get_cookiedict()
        return d.get(key.lower().strip(), default)

    def get_cookiedict(self):
        if not self.cookies:
            return {}
        if not hasattr(self, '__cookiecache'):
            self.__cookiecache = json.loads(self.cookies)
        return self.__cookiecache

    def __unicode__(self):
        return "%s: %s, %s" % (self.runid, self.subject.surname, self.subject.givenname)

    class Meta:
        verbose_name = '运行信息'
        verbose_name_plural = verbose_name


class RunInfoHistory(models.Model):
    subject = models.ForeignKey(Subject)
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

    def answers(self):
        "Returns the query for the answers."
        return Answer.objects.filter(subject=self.subject, runid=self.runid)

    class Meta:
        verbose_name = '历史记录'
        verbose_name_plural = verbose_name


class Question(models.Model):
    __metaclass__ = TransMeta

    questionset = models.ForeignKey(QuestionSet)
    number = models.CharField(max_length=8, help_text=
        "eg. <tt>1</tt>, <tt>2a</tt>, <tt>2b</tt>, <tt>3c</tt><br /> "
        "Number is also used for ordering questions.")
    sort_id = models.IntegerField(null=True, blank=True, help_text="Questions within a questionset are sorted by sort order first, question number second")
    text = models.TextField(blank=True, verbose_name=_("Text"))
    type = models.CharField(u"Type of question", max_length=32,
        choices = QuestionChoices,
        help_text = u"Determines the means of answering the question. " \
        "An open question gives the user a single-line textfield, " \
        "multiple-choice gives the user a number of choices he/she can " \
        "choose from. If a question is multiple-choice, enter the choices " \
        "this user can choose from below'.")
    extra = models.TextField(u"Extra information", blank=True, null=True, help_text=u"Extra information (use  on question type)")
    checks = models.TextField(u"Additional checks", blank=True,
        null=True, help_text="Additional checks to be performed for this "
        "value (space separated)  <br /><br />"
        "For text fields, <tt>required</tt> is a valid check.<br />"
        "For yes/no choice, <tt>required</tt>, <tt>required-yes</tt>, "
        "and <tt>required-no</tt> are valid.<br /><br />"
        "If this question is required only if another question's answer is "
        'something specific, use <tt>requiredif="QuestionNumber,Value"</tt> '
        'or <tt>requiredif="QuestionNumber,!Value"</tt> for anything but '
        "a specific value.  "
        "You may also combine tests appearing in <tt>requiredif</tt> "
        "by joining them with the words <tt>and</tt> or <tt>or</tt>, "
        'eg. <tt>requiredif="Q1,A or Q2,B"</tt>')
    footer = models.TextField(u"Footer", help_text="Footer rendered below the question interpreted as textile", blank=True)

    def questionnaire(self):
        return self.questionset.questionnaire

    def getcheckdict(self):
        """getcheckdict returns a dictionary of the values in self.checks"""
        if(hasattr(self, '__checkdict_cached')):
            return self.__checkdict_cached
        try:
            self.__checkdict_cached = d = parse_checks(self.sameas().checks or '')
        except ParseException:
            raise Exception("Error Parsing Checks for Question %s: %s" % (
                self.number, self.sameas().checks))
        return d

    def __unicode__(self):
        return u'{%s} (%s) %s' % (unicode(self.questionset), self.number, self.text)

    def sameas(self):
        if self.type == 'sameas':
            try:
                kwargs = {}
                for check, value in parse_checks(self.checks):
                    if check == 'sameasid':
                        kwargs['id'] = value
                        break
                    elif check == 'sameas':
                        kwargs['number'] = value
                        kwargs['questionset__questionnaire'] = self.questionset.questionnaire
                        break

                self.__sameas = res = getattr(self, "__sameas", Question.objects.get(**kwargs))
                return res
            except Question.DoesNotExist:
                return Question(type='comment') # replace with something benign
        return self

    def display_number(self):
        "Return either the number alone or the non-number part of the question number indented"
        m = _numre.match(self.number)
        if m:
            sub = m.group(2)
            return "&nbsp;&nbsp;&nbsp;" + sub
        return self.number

    def choices(self):
        if self.type == 'sameas':
            return self.sameas().choices()
        res = Choice.objects.filter(question=self).order_by('sortid')
        return res

    def is_custom(self):
        return "custom" == self.sameas().type

    def get_type(self):
        "Get the type name, treating sameas and custom specially"
        t = self.sameas().type
        if t == 'custom':
            cd = self.sameas().getcheckdict()
            if 'type' not in cd:
                raise Exception("When using custom types, you must have type=<name> in the additional checks field")
            return cd.get('type')
        return t

    def questioninclude(self):
        return "questionnaire/" + self.get_type() + ".html"

    @property
    def is_comment(self):
        return self.type == 'comment'

#     def __cmp__(a, b):
#         anum, astr = split_numal(a.number)
#         bnum, bstr = split_numal(b.number)
#         cmpnum = cmp(anum, bnum)
#         return cmpnum or cmp(astr, bstr)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        # translate = ('text', 'extra', 'footer')


class Choice(models.Model):
    __metaclass__ = TransMeta

    question = models.ForeignKey(Question)
    sortid = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=64)
    text = models.TextField(u"Choice Text")
    tags = models.CharField(u"Tags", max_length=64, blank=True)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.sortid, self.text)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = verbose_name
        # translate = ('text',)


class Answer(models.Model):
    subject = models.ForeignKey(Subject, help_text = u'The user who supplied this answer')
    question = models.ForeignKey(Question, help_text = u"The question that this is an answer to")
    runid = models.CharField(u'RunID', help_text = u"The RunID (ie. year)", max_length=32)
    answer = models.TextField()

    def __unicode__(self):
        return "Answer(%s: %s, %s)" % (self.question.number, self.subject.surname, self.subject.givenname)

    def split_answer(self):
        """
        Decode stored answer value and return as a list of choices.
        Any freeform value will be returned in a list as the last item.

        Calling code should be tolerant of freeform answers outside
        of additional [] if data has been stored in plain text format
        """
        try:
            return json.loads(self.answer)
        except ValueError:
            # this was likely saved as plain text, try to guess what the
            # value(s) were
            if 'multiple' in self.question.type:
                return self.answer.split('; ')
            else:
                return [self.answer]

    def check_answer(self):
        "Confirm that the supplied answer matches what we expect"
        return True

    def save(self, runinfo=None, **kwargs):
        self._update_tags(runinfo)
        super(Answer, self).save(**kwargs)

    def _update_tags(self, runinfo):
        if not runinfo:
            return

        tags_to_add = []

        for choice in self.question.choices():
            tags = choice.tags
            if not tags:
                continue
            tags = tags.split(',')
            runinfo.remove_tags(tags)

            for split_answer in self.split_answer():
                if unicode(split_answer) == choice.value:
                    tags_to_add.extend(tags)

        runinfo.add_tags(tags_to_add)
        runinfo.save()
