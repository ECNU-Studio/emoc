#!/usr/bin/python
# vim: set fileencoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.db import transaction
from django.conf import settings
from datetime import datetime
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from questionnaire import QuestionProcessors
from questionnaire import questionnaire_start, questionset_start, questionset_done, questionnaire_done
from questionnaire import AnswerException
from questionnaire import Processors
from questionnaire.models import *
from questionnaire.parsers import *
from questionnaire.emails import _send_email, send_emails
from questionnaire.utils import numal_sort, split_numal
from questionnaire.request_cache import request_cache
from questionnaire.dependency_checker import dep_check
from questionnaire import profiler
from compat import commit_on_success, commit, rollback
import logging
import random
import json
from hashlib import md5
import re


try:
    use_session = settings.QUESTIONNAIRE_USE_SESSION
except AttributeError:
    use_session = False

try:
    debug_questionnaire = settings.QUESTIONNAIRE_DEBUG
except AttributeError:
    debug_questionnaire = False


def r2r(tpl, request, **contextdict):
    "Shortcut to use RequestContext instead of Context in templates"
    contextdict['request'] = request
    return render_to_response(tpl, contextdict, context_instance=RequestContext(request))


def get_runinfo(random):
    """
    通过使用提供的随机密钥返回RunInfo实体
    """
    res = RunInfo.objects.filter(random=random.lower())
    return res and res[0] or None


def get_question(number, questionnaire):
    "Return the specified Question (by number) from the specified Questionnaire"
    res = Question.objects.filter(number=number, questionset__questionnaire=questionnaire)
    return res and res[0] or None


def delete_answer(question, subject, runid):
    "Delete the specified question/subject/runid combination from the Answer table"
    Answer.objects.filter(subject=subject, runid=runid, question=question).delete()


def add_answer(runinfo, question, answer_dict):
    """
    Add an Answer to a Question for RunInfo, given the relevant form input

    answer_dict contains the POST'd elements for this question, minus the
    question_{number} prefix.  The question_{number} form value is accessible
    with the ANSWER key.
    """
    answer = Answer()
    answer.question = question
    answer.subject = runinfo.subject
    answer.runid = runinfo.runid

    type = question.get_type()

    if "ANSWER" not in answer_dict:
        answer_dict['ANSWER'] = None

    if type in Processors:
        answer.answer = Processors[type](question, answer_dict) or ''
    else:
        raise AnswerException("No Processor defined for question type %s" % type)

    # first, delete all existing answers to this question for this particular user+run
    delete_answer(question, runinfo.subject, runinfo.runid)

    # then save the new answer to the database
    answer.save(runinfo)

    return True


def check_parser(runinfo, exclude=[]):
    depparser = BooleanParser(dep_check, runinfo, {})
    tagparser = BooleanParser(has_tag, runinfo)

    fnmap = {
        "maleonly": lambda v: runinfo.subject.gender == 'male',
        "femaleonly": lambda v: runinfo.subject.gender == 'female',
        "shownif": lambda v: v and depparser.parse(v),
        "iftag": lambda v: v and tagparser.parse(v)
    }

    for ex in exclude:
        del fnmap[ex]

    @request_cache()
    def satisfies_checks(checks):
        if not checks:
            return True

        checks = parse_checks(checks)

        for check, value in checks.items():
            if check in fnmap:
                value = value and value.strip()
                if not fnmap[check](value):
                    return False

        return True

    return satisfies_checks


@request_cache()
def skipped_questions(runinfo):
    if not runinfo.skipped:
        return []

    return [s.strip() for s in runinfo.skipped.split(',')]


@request_cache()
def question_satisfies_checks(question, runinfo, checkfn=None):
    if question.number in skipped_questions(runinfo):
        return False

    checkfn = checkfn or check_parser(runinfo)
    return checkfn(question.checks)


@request_cache(keyfn=lambda *args: args[0].id)
def questionset_satisfies_checks(questionset, runinfo, checks=None):
    """Return True if the runinfo passes the checks specified in the QuestionSet

    Checks is an optional dictionary with the keys being questionset.pk and the
    values being the checks of the contained questions.

    This, in conjunction with fetch_checks allows for fewer
    db roundtrips and greater performance.

    Sadly, checks cannot be hashed and therefore the request cache is useless
    here. Thankfully the benefits outweigh the costs in my tests.
    """

    passes = check_parser(runinfo)

    if not passes(questionset.checks):
        return False

    if not checks:
        checks = dict()
        checks[questionset.id] = []

        for q in questionset.questions():
            checks[questionset.id].append((q.checks, q.number))

    # questionsets that pass the checks but have no questions are shown
    # (comments, last page, etc.)
    if not checks[questionset.id]:
        return True

    # if there are questions at least one needs to be visible
    for check, number in checks[questionset.id]:
        if number in skipped_questions(runinfo):
            continue

        if passes(check):
            return True

    return False


def get_progress(runinfo):
    position, total = 0, 0

    current = runinfo.questionset
    sets = current.questionnaire.questionsets()

    checks = fetch_checks(sets)

    # fetch the all question checks at once. This greatly improves the
    # performance of the questionset_satisfies_checks function as it
    # can avoid a roundtrip to the database for each question

    for qs in sets:
        if questionset_satisfies_checks(qs, runinfo, checks):
            total += 1

        if qs.id == current.id:
            position = total

    if not all((position, total)):
        progress = 1
    else:
        progress = float(position) / float(total) * 100.00

        # progress is always at least one percent
        progress = progress >= 1.0 and progress or 1

    return int(progress)


def get_async_progress(request, *args, **kwargs):
    """ Returns the progress as json for use with ajax """

    if 'runcode' in kwargs:
        runcode = kwargs['runcode']
    else:
        session_runcode = request.session.get('runcode', None)
        if session_runcode is not None:
            runcode = session_runcode

    runinfo = get_runinfo(runcode)
    response = dict(progress=get_progress(runinfo))

    cache.set('progress' + runinfo.random, response['progress'])
    response = HttpResponse(json.dumps(response), content_type='application/javascript')
    response["Cache-Control"] = "no-cache"
    return response


def fetch_checks(questionsets):
    ids = [qs.pk for qs in questionsets]

    query = Question.objects.filter(questionset__pk__in=ids)
    query = query.values('questionset_id', 'checks', 'number')

    checks = dict()
    for qsid in ids:
        checks[qsid] = list()

    for result in (r for r in query):
        checks[result['questionset_id']].append(
            (result['checks'], result['number'])
        )

    return checks


def redirect_to_qs(runinfo, request=None):
    "Redirect to the correct and current questionset URL for this RunInfo"

    # cache current questionset
    qs = runinfo.questionset

    # skip questionsets that don't pass
    if not questionset_satisfies_checks(runinfo.questionset, runinfo):

        next = runinfo.questionset.next()

        while next and not questionset_satisfies_checks(next, runinfo):
            next = next.next()

        runinfo.questionset = next
        runinfo.save()

        hasquestionset = bool(next)
    else:
        hasquestionset = True

    # empty ?
    if not hasquestionset:
        logging.warn('no questionset in questionnaire which passes the check')
        return finish_questionnaire(request, runinfo, qs.questionnaire)

    if not use_session:
        args = [runinfo.random, runinfo.questionset.sortid]
        urlname = 'questionset'
    else:
        args = []
        request.session['qs'] = runinfo.questionset.sortid
        request.session['runcode'] = runinfo.random
        urlname = 'questionnaire'
    url = reverse(urlname, args=args)
    return HttpResponseRedirect(url)


def redirect_to_prev_questionnaire(request):
    """
    Used only when ```QUESTIONNAIRE_USE_SESSION``` is True.
    Takes the questionnaire set in the session and redirects to the
    previous questionnaire if any.
    """
    runcode = request.session.get('runcode', None)
    if runcode is not None:
        runinfo = get_runinfo(runcode)
        prev_qs = runinfo.questionset.prev()
        if runinfo and prev_qs:
            request.session['runcode'] = runinfo.random
            request.session['qs'] = prev_qs.sortid
            return HttpResponseRedirect(reverse('questionnaire'))

    return HttpResponseRedirect('/')


@commit_on_success
def questionnaire(request, runcode=None, qs=None):
    """
    进程提交答案（如果存在）并重定向到下一页
    如果这是POST请求，可以解析提交的数据以便存储所有提交的答案。然后返回到下一个问卷集或返回已完成请求。
    如果不是POST请求，则返回main page
    我们只关注成功，来保持一致。如果有错误处理这个问题集的答案，我们也会特别回滚。
    """
    if use_session:
        session_runcode = request.session.get('runcode', None)
        if session_runcode is not None:
            runcode = session_runcode

        session_qs = request.session.get('qs', None)
        if session_qs is not None:
            qs = session_qs

    # if runcode provided as query string, redirect to the proper page
    if not runcode:
        runcode = request.GET.get('runcode')
        if not runcode:
            return HttpResponseRedirect("/")
        else:
            if not use_session:
                args = [runcode, ]
            else:
                request.session['runcode'] = runcode
                args = []
            return HttpResponseRedirect(reverse("questionnaire", args=args))

    runinfo = get_runinfo(runcode)

    if not runinfo:
        commit()
        return HttpResponseRedirect('/')

    # 让runinfo在请求有一个备份
    # 所以我们可以很容易地在像问题处理器这样的地方使用runinfo
    # 没有通过它
    request.runinfo = runinfo

    if not qs:
        # 只需要将语言更改为调查者最初的
        # 问卷页 (may be a direct link from an email)
        if hasattr(request, 'session'):
            request.session['django_language'] = runinfo.subject.language
            translation.activate(runinfo.subject.language)

    if 'lang' in request.GET:
        return set_language(request, runinfo, request.path)

    # --------------------------------
    # ---      处理非POST请求       ---
    # --------------------------------

    if request.method != "POST":
        if qs is not None:
            qs = get_object_or_404(QuestionSet, sortid=qs, questionnaire=runinfo.questionset.questionnaire)
            if runinfo.random.startswith('test:'):
                pass  # ok for testing
            elif qs.sortid > runinfo.questionset.sortid:
                # you may jump back, but not forwards
                return redirect_to_qs(runinfo, request)
            runinfo.questionset = qs
            runinfo.save()
            commit()
        # no questionset id in URL, so redirect to the correct URL
        if qs is None:
            return redirect_to_qs(runinfo, request)
        questionset_start.send(sender=None, runinfo=runinfo, questionset=qs)
        return show_questionnaire(request, runinfo)

    # -------------------------------------
    # --- Process POST with QuestionSet ---
    # -------------------------------------

    # if the submitted page is different to what runinfo says, update runinfo
    # XXX - do we really want this?
    qs = request.POST.get('questionset_id', qs)
    try:
        qsobj = QuestionSet.objects.filter(pk=qs)[0]
        if qsobj.questionnaire == runinfo.questionset.questionnaire:
            if runinfo.questionset != qsobj:
                runinfo.questionset = qsobj
                runinfo.save()
    except:
        pass

    questionnaire = runinfo.questionset.questionnaire
    questionset = runinfo.questionset

    # to confirm that we have the correct answers
    expected = questionset.questions()

    items = request.POST.items()
    extra = {}  # question_object => { "ANSWER" : "123", ... }

    # this will ensure that each question will be processed, even if we did not receive
    # any fields for it. Also works to ensure the user doesn't add extra fields in
    for x in expected:
        items.append((u'question_%s_Trigger953' % x.number, None))

    # generate the answer_dict for each question, and place in extra
    for item in items:
        key, value = item[0], item[1]
        if key.startswith('question_'):
            answer = key.split("_", 2)
            question = get_question(answer[1], questionnaire)
            if not question:
                logging.warn("Unknown question when processing: %s" % answer[1])
                continue
            extra[question] = ans = extra.get(question, {})
            if (len(answer) == 2):
                ans['ANSWER'] = value
            elif (len(answer) == 3):
                ans[answer[2]] = value
            else:
                logging.warn("Poorly formed form element name: %r" % answer)
                continue
            extra[question] = ans

    errors = {}
    for question, ans in extra.items():
        if not question_satisfies_checks(question, runinfo):
            continue
        if u"Trigger953" not in ans:
            logging.warn("User attempted to insert extra question (or it's a bug)")
            continue
        try:
            cd = question.getcheckdict()
            # requiredif is the new way
            depon = cd.get('requiredif', None) or cd.get('dependent', None)
            if depon:
                depparser = BooleanParser(dep_check, runinfo, extra)
                if not depparser.parse(depon):
                    # if check is not the same as answer, then we don't care
                    # about this question plus we should delete it from the DB
                    delete_answer(question, runinfo.subject, runinfo.runid)
                    if cd.get('store', False):
                        runinfo.set_cookie(question.number, None)
                    continue
            add_answer(runinfo, question, ans)
            if cd.get('store', False):
                runinfo.set_cookie(question.number, ans['ANSWER'])
        except AnswerException, e:
            errors[question.number] = e
        except Exception:
            logging.exception("Unexpected Exception")
            rollback()
            raise

    if len(errors) > 0:
        res = show_questionnaire(request, runinfo, errors=errors)
        rollback()
        return res

    questionset_done.send(sender=None, runinfo=runinfo, questionset=questionset)

    next = questionset.next()
    while next and not questionset_satisfies_checks(next, runinfo):
        next = next.next()
    runinfo.questionset = next
    runinfo.save()
    if use_session:
        request.session['prev_runcode'] = runinfo.random

    if next is None:  # we are finished
        return finish_questionnaire(request, runinfo, questionnaire)

    commit()
    return redirect_to_qs(runinfo, request)


def finish_questionnaire(request, runinfo, questionnaire):
    hist = RunInfoHistory()
    hist.subject = runinfo.subject
    hist.runid = runinfo.runid
    hist.completed = datetime.now()
    hist.questionnaire = questionnaire
    hist.tags = runinfo.tags
    hist.skipped = runinfo.skipped
    hist.save()

    questionnaire_done.send(sender=None, runinfo=runinfo,
                            questionnaire=questionnaire)

    redirect_url = questionnaire.redirect_url
    for x, y in (('$LANG', translation.get_language()),
                 ('$SUBJECTID', runinfo.subject.id),
                 ('$RUNID', runinfo.runid),):
        redirect_url = redirect_url.replace(x, str(y))

    if runinfo.runid in ('12345', '54321') \
            or runinfo.runid.startswith('test:'):
        runinfo.questionset = QuestionSet.objects.filter(questionnaire=questionnaire).order_by('sortid')[0]
        runinfo.save()
    else:
        runinfo.delete()
    commit()
    if redirect_url:
        return HttpResponseRedirect(redirect_url)
    return r2r("questionnaire/complete.$LANG.html", request)


def show_questionnaire(request, runinfo, errors={}):
    """
    Return the QuestionSet template

    Also add the javascript dependency code.
    """

    request.runinfo = runinfo

    if request.GET.get('show_all') == '1':  # for debugging purposes.
        questions = runinfo.questionset.questionnaire.questions()
    else:
        questions = runinfo.questionset.questions()

    show_all = request.GET.get('show_all') == '1'  # for debugging purposes in some cases we may want to show all questions on one screen.
    questionset = runinfo.questionset
    questions = questionset.questionnaire.questions() if show_all else questionset.questions()

    qlist = []
    jsinclude = []  # js files to include
    cssinclude = []  # css files to include
    jstriggers = []
    qvalues = {}

    # initialize qvalues
    cookiedict = runinfo.get_cookiedict()

    for k, v in cookiedict.items():
        qvalues[k] = v

    substitute_answer(qvalues, runinfo.questionset)

    for question in questions:
        # if we got here the questionset will at least contain one question
        # which passes, so this is all we need to check for
        question_visible = question_satisfies_checks(question, runinfo) or show_all

        Type = question.get_type()
        _qnum, _qalpha = split_numal(question.number)

        qdict = {
            'css_style': '' if question_visible else 'display:none;',
            'template': 'questionnaire/%s.html' % (Type),
            'qnum': _qnum,
            'qalpha': _qalpha,
            'qtype': Type,
            'qnum_class': (_qnum % 2 == 0) and " qeven" or " qodd",
            'qalpha_class': _qalpha and (ord(_qalpha[-1]) % 2 \
                                         and ' alodd' or ' aleven') or '',
        }

        # substitute answer texts
        substitute_answer(qvalues, question)

        # add javascript dependency checks
        cd = question.getcheckdict()
        depon = cd.get('requiredif', None) or cd.get('dependent', None)
        if depon:
            # extra args to BooleanParser are not required for toString
            parser = BooleanParser(dep_check)
            qdict['checkstring'] = ' checks="%s"' % parser.toString(depon)
            jstriggers.append('qc_%s' % question.number)
        if 'default' in cd and not question.number in cookiedict:
            qvalues[question.number] = cd['default']
        if Type in QuestionProcessors:
            qdict.update(QuestionProcessors[Type](request, question))
            if 'jsinclude' in qdict:
                if qdict['jsinclude'] not in jsinclude:
                    jsinclude.extend(qdict['jsinclude'])
            if 'cssinclude' in qdict:
                if qdict['cssinclude'] not in cssinclude:
                    cssinclude.extend(qdict['jsinclude'])
            if 'jstriggers' in qdict:
                jstriggers.extend(qdict['jstriggers'])
            if 'qvalue' in qdict and not question.number in cookiedict:
                qvalues[question.number] = qdict['qvalue']

        qlist.append((question, qdict))

    try:
        has_progress = settings.QUESTIONNAIRE_PROGRESS in ('async', 'default')
        async_progress = settings.QUESTIONNAIRE_PROGRESS == 'async'
    except AttributeError:
        has_progress = True
        async_progress = False

    if has_progress:
        if async_progress:
            progress = cache.get('progress' + runinfo.random, 1)
        else:
            progress = get_progress(runinfo)
    else:
        progress = 0

    if request.POST:
        for k, v in request.POST.items():
            if k.startswith("question_"):
                s = k.split("_")
                if len(s) == 4:
                    qvalues[s[1] + '_' + v] = '1'  # evaluates true in JS
                elif len(s) == 3 and s[2] == 'comment':
                    qvalues[s[1] + '_' + s[2]] = v
                else:
                    qvalues[s[1]] = v

    if use_session:
        prev_url = reverse('redirect_to_prev_questionnaire')
    else:
        prev_url = 'javascript:history.back();'

    current_answers = []
    if debug_questionnaire:
        current_answers = Answer.objects.filter(subject=runinfo.subject, runid=runinfo.runid).order_by('id')

    r = r2r("questionnaire/questionset.html", request,
            questionset=runinfo.questionset,
            runinfo=runinfo,
            errors=errors,
            qlist=qlist,
            progress=progress,
            triggers=jstriggers,
            qvalues=qvalues,
            jsinclude=jsinclude,
            cssinclude=cssinclude,
            async_progress=async_progress,
            async_url=reverse('progress', args=[runinfo.random]),
            prev_url=prev_url,
            current_answers=current_answers,
    )
    r['Cache-Control'] = 'no-cache'
    r['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    return r


def substitute_answer(qvalues, obj):
    """Objects with a 'text/text_xx' attribute can contain magic strings
    referring to the answers of other questions. This function takes
    any such object, goes through the stored answers (qvalues) and replaces
    the magic string with the actual value. If this isn't possible the
    magic string is removed from the text.

    Only answers with 'store' in their check will work with this.

    """

    if qvalues and obj.text:
        magic = 'subst_with_ans_'
        regex = r'subst_with_ans_(\S+)'

        replacements = re.findall(regex, obj.text)
        text_attributes = [a for a in dir(obj) if a.startswith('text_')]

        for answerid in replacements:

            target = magic + answerid
            replacement = qvalues.get(answerid.lower(), '')

            for attr in text_attributes:
                oldtext = getattr(obj, attr)
                newtext = oldtext.replace(target, replacement)

                setattr(obj, attr, newtext)


def set_language(request, runinfo=None, next=None):
    """
    改变语言，如果有的话，把它保存到runinfo，重定向到提供的URL（或最近的URL）
    也可以使用url处理程序， w/o runinfo & next.
    """
    if not next:
        next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
        if not next:
            next = '/'
    response = HttpResponseRedirect(next)
    response['Expires'] = "Thu, 24 Jan 1980 00:00:00 GMT"
    if request.method == 'GET':
        lang_code = request.GET.get('lang', None)
        if lang_code and translation.check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            if runinfo:
                runinfo.subject.language = lang_code
                runinfo.subject.save()
    return response


def _table_headers(questions):
    """
    Return the header labels for a set of questions as a list of strings.

    This will create separate columns for each multiple-choice possiblity
    and freeform options, to avoid mixing data types and make charting easier.
    """
    ql = list(questions)
    ql.sort(lambda x, y: numal_sort(x.number, y.number))
    columns = []
    for q in ql:
        if q.type == 'choice-yesnocomment':
            columns.extend([q.number, q.number + "-freeform"])
        elif q.type == 'choice-freeform':
            columns.extend([q.number, q.number + "-freeform"])
        elif q.type.startswith('choice-multiple'):
            cl = [c.value for c in q.choice_set.all()]
            cl.sort(numal_sort)
            columns.extend([q.number + '-' + value for value in cl])
            if q.type == 'choice-multiple-freeform':
                columns.append(q.number + '-freeform')
        else:
            columns.append(q.number)
    return columns


@permission_required("questionnaire.export")
def export_csv(request, qid):  # questionnaire_id
    """
    For a given questionnaire id, generaete a CSV containing all the
    answers for all subjects.
    """
    import tempfile, unicodecsv, cStringIO, codecs
    from django.core.servers.basehttp import FileWrapper

    questionnaire = get_object_or_404(Questionnaire, pk=int(qid))
    headings, answers = answer_export(questionnaire)

    response = HttpResponse(content_type="text/csv")

    writer = unicodecsv.writer(response)
    writer.writerow([u'subject', u'runid'] + headings)
    for subject, runid, answer_row in answers:
        row = ["%s/%s" % (subject.id, subject.state), runid] + [
            a if a else '--' for a in answer_row]
        writer.writerow(row)

    response['Content-Disposition'] = 'attachment; filename="export-%s.csv"' % qid
    return response


def answer_export(questionnaire, answers=None):
    """
    questionnaire -- questionnaire model for export
    answers -- query set of answers to include in export, defaults to all

    Return a flat dump of column headings and all the answers for a
    questionnaire (in query set answers) in the form (headings, answers)
    where headings is:
        ['question1 number', ...]
    and answers is:
        [(subject1, 'runid1', ['answer1.1', ...]), ... ]

    The headings list might include items with labels like
    'questionnumber-freeform'.  Those columns will contain all the freeform
    answers for that question (separated from the other answer data).

    Multiple choice questions will have one column for each choice with
    labels like 'questionnumber-choice'.

    The items in the answers list are unicode strings or empty strings
    if no answer was given.  The number of elements in each answer list will
    always match the number of headings.
    """
    if answers is None:
        answers = Answer.objects.all()
    answers = answers.filter(
        question__questionset__questionnaire=questionnaire).order_by(
        'subject', 'runid', 'question__questionset__sortid', 'question__number')
    answers = answers.select_related()
    questions = Question.objects.filter(
        questionset__questionnaire=questionnaire)
    headings = _table_headers(questions)

    coldict = {}
    for num, col in enumerate(headings):  # use coldict to find column indexes
        coldict[col] = num
    # collect choices for each question
    qchoicedict = {}
    for q in questions:
        qchoicedict[q.id] = [x[0] for x in q.choice_set.values_list('value')]

    runid = subject = None
    out = []
    row = []
    for answer in answers:
        if answer.runid != runid or answer.subject != subject:
            if row:
                out.append((subject, runid, row))
            runid = answer.runid
            subject = answer.subject
            row = [""] * len(headings)
        ans = answer.split_answer()
        if type(ans) == int:
            ans = str(ans)
        for choice in ans:
            col = None
            if type(choice) == list:
                # freeform choice
                choice = choice[0]
                col = coldict.get(answer.question.number + '-freeform', None)
            if col is None:  # look for enumerated choice column (multiple-choice)
                col = coldict.get(answer.question.number + '-' + unicode(choice), None)
            if col is None:  # single-choice items
                if ((not qchoicedict[answer.question.id]) or
                            choice in qchoicedict[answer.question.id]):
                    col = coldict.get(answer.question.number, None)
            if col is None:  # last ditch, if not found throw it in a freeform column
                col = coldict.get(answer.question.number + '-freeform', None)
            if col is not None:
                row[col] = choice
    # and don't forget about the last one
    if row:
        out.append((subject, runid, row))
    return headings, out


def answer_summary(questionnaire, answers=None):
    """
    questionnaire -- questionnaire model for summary
    answers -- query set of answers to include in summary, defaults to all

    Return a summary of the answer totals in answer_qs in the form:
    [('q1', 'question1 text',
        [('choice1', 'choice1 text', num), ...],
        ['freeform1', ...]), ...]

    questions are returned in questionnaire order
    choices are returned in question order
    freeform options are case-insensitive sorted
    """

    if answers is None:
        answers = Answer.objects.all()
    answers = answers.filter(question__questionset__questionnaire=questionnaire)
    questions = Question.objects.filter(
        questionset__questionnaire=questionnaire).order_by(
        'questionset__sortid', 'number')

    summary = []
    for question in questions:
        q_type = question.get_type()
        if q_type.startswith('choice-yesno'):
            choices = [('yes', _('Yes')), ('no', _('No'))]
            if 'dontknow' in q_type:
                choices.append(('dontknow', _("Don't Know")))
        elif q_type.startswith('choice'):
            choices = [(c.value, c.text) for c in question.choices()]
        else:
            choices = []
        choice_totals = dict([(k, 0) for k, v in choices])
        freeforms = []
        for a in answers.filter(question=question):
            ans = a.split_answer()
            for choice in ans:
                if type(choice) == list:
                    freeforms.extend(choice)
                elif choice in choice_totals:
                    choice_totals[choice] += 1
                else:
                    # be tolerant of improperly marked data
                    freeforms.append(choice)
        freeforms.sort(numal_sort)
        summary.append((question.number, question.text, [
            (n, t, choice_totals[n]) for (n, t) in choices], freeforms))
    return summary


def has_tag(tag, runinfo):
    """ Returns true if the given runinfo contains the given tag. """
    return tag in (t.strip() for t in runinfo.tags.split(','))


@permission_required("questionnaire.management")
def send_email(request, runinfo_id):
    if request.method != "POST":
        return HttpResponse("This page MUST be called as a POST request.")
    runinfo = get_object_or_404(RunInfo, pk=int(runinfo_id))
    successful = _send_email(runinfo)
    return r2r("emailsent.html", request, runinfo=runinfo, successful=successful)


def generate_run(request, questionnaire_id, subject_id=None):
    """
    可以匿名生成RunID实例的视图，然后重定位到问卷
    使用'Anonymous'（匿名）调查者，如果不存在，则创建。
    URL模式：
    (r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    """
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    if subject_id is not None:
        su = get_object_or_404(Subject, pk=subject_id)
    else:
        su = Subject.objects.filter(givenname='Anonymous', surname='User')[0:1]
        if su:
            su = su[0]
        else:
            su = Subject(givenname='Anonymous', surname='User')
            su.save()

    str_to_hash = "".join(map(lambda i: chr(random.randint(0, 255)), range(16)))
    str_to_hash += settings.SECRET_KEY
    key = md5(str_to_hash).hexdigest()

    run = RunInfo(subject=su, random=key, runid=key, questionset=qs)
    run.save()
    if not use_session:
        kwargs = {'runcode': key}
    else:
        kwargs = {}
        request.session['runcode'] = key

    questionnaire_start.send(sender=None, runinfo=run, questionnaire=qu)
    return HttpResponseRedirect(reverse('questionnaire', kwargs=kwargs))
