# _*_ coding:utf-8 _*_
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from questionnaire.models import *
from users.models import UserProfile
import random
import json
from hashlib import md5


class QuestionnaireView(View):
    """
    查找当前问卷并显示出来
    """
    def get(self, request, questionnaire_id):
        questionnaire = get_object_or_404(Questionnaire, id=int(questionnaire_id))
        if questionnaire:
            questions = questionnaire.questions()
            for question in questions:
                choices = question.chices()
                question.choices = choices
                question.template = "question/%s.html" % question.type

        # 判断用户登录状态
        # res = dict()
        # if not request.user.is_authenticated():
        #     res['status'] = 'fail'
        #     res['msg'] = u'用户未登录'
        #     return HttpResponse(json.dumps(res), content_type='application/json')
        # if qu:
        #     # 生成唯一key
        #     str_to_hash = "".join(map(lambda i: chr(random.randint(0, 255)), range(16)))
        #     str_to_hash += settings.SECRET_KEY
        #     key = md5(str_to_hash).hexdigest()
        #
        #     run = RunInfo()
        #     # run.subject = request.user
        #     run.random = key
        #     run.runid = key
        #     run.questionnaire = qu
        #     run.save()

        # 反解析URL
        return render(request, 'questionnaire.html', {
            'questionnaire': questionnaire,
            'questions': questions
        })
