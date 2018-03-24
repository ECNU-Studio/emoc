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
    def get(self, request, questionnaire_id=None):
        questionnaire = get_object_or_404(Questionnaire, id=int(questionnaire_id))
        if questionnaire:
            questions = questionnaire.questions()
            for question in questions:
                choices = question.chices()
                question.choices = choices
                question.template = "question_type/%s.html" % question.type

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


class AddQuestionnaire(View):
    # 保存记录
    def save_runinfo(self, questionnaire, user):
        runinfo = RunInfo()
        runinfo.subject = user
        runinfo.questionnaire = questionnaire
        runinfo.save()
        return runinfo

    def post(self, request):
        # 获取调查者
        if not request.user.is_authenticated():
            user = UserProfile.objects.filter(username='Anonymous')[0:1]
        else:
            user = request.user

        questionnaire_id = int(request.POST.get('questionnaire_id', 0))

        questionnaire = Questionnaire.objects.get(id=questionnaire_id)

        if questionnaire:
            runinfo = self.save_runinfo(questionnaire, user)
            # 未处理好
            answer_list = json.loads(request.POST.get('answerStr'))
            for answer_obj in answer_list:
                answer = Answer()
                answer.text = answer_obj["answer"]
                question = Question.objects.get(id=answer_obj["question_id"])
                answer.question = question
                answer.runinfo = runinfo
                answer.save()

            res = dict()
            res['status'] = 'success'
            res['msg'] = '完成'
        return HttpResponse(json.dumps(res), content_type='application/json')

