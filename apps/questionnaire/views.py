# _*_ coding:utf-8 _*_
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from questionnaire.models import *
import random
from hashlib import md5


def show_questionnaire(request, questionnaire_id, subject_id=None):
    """
    查找当前问卷并显示出来
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




    # 反解析URL
    return HttpResponseRedirect(reverse('questionnaire.views.questionnaire', kwargs=kwargs))
