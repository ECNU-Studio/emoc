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


class QuestionnaireEdit(View):
    """
    编辑问卷
    """
    def get(self, request, questionnaire_id=None):
        questionnaire = get_object_or_404(Questionnaire, id=int(questionnaire_id))
        questions = questionnaire.questions()
        question_list = []
        for question in questions:
            question_obj = {}
            question_obj['label'] = question.text
            question_obj['field_type'] = question.type
            question_obj['field_options'] = {}

            choices = question.choices()
            options = []
            for choice in choices:
                option = {}
                option['label'] = choice.text
                option['checked'] = False
                options.append(option)
            question_obj['field_options']['options'] = options

            question_list.append(question_obj)


        return render(request, 'edit_questionnaire.html', {
            'questionnaire': questionnaire,
            'question_list': json.dumps(question_list)
        })


class StatisticsShow(View):
    """
    查找当前问卷的统计信息并显示出来
    """
    def get(self, request, questionnaire_id=None):
        questionnaire = get_object_or_404(Questionnaire, id=int(questionnaire_id))
        if questionnaire:
            questions = questionnaire.questions()
            for question in questions:
                if question.type == 'text':
                    question.answer_texts = question.get_answer_texts()
                else:
                    question.statistics = question.statistics()
                question.template = "statistics_type/%s.html" % question.type

            runinfos = RunInfo.objects.filter(questionnaire=questionnaire)[:10]

        # 反解析URL
        return render(request, 'questionnaire_statistics.html', {
            'questionnaire': questionnaire,
            'questions': questions,
            'runinfos': runinfos
        })




class QuestionnaireShow(View):
    """
    查找当前问卷并显示出来
    """
    def get(self, request, questionnaire_id=None, preview=1):
        questionnaire = get_object_or_404(Questionnaire, id=int(questionnaire_id))
        if questionnaire:
            questions = questionnaire.questions()
            for question in questions:
                question.choices = question.choices()
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
        return render(request, 'show_questionnaire.html', {
            'questionnaire': questionnaire,
            'questions': questions,
            'preview': preview
        })


class SubmitQuestionnaire(View):
    # 保存记录
    def save_runinfo(self, questionnaire, user):
        runinfo = RunInfo()
        runinfo.user = user
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
            answers = json.loads(request.POST.get('answerStr'))
            for answer_obj in answers:
                choices = answer_obj["choice"].split(',')
                for choice in choices:
                    answer = Answer()
                    answer.question = answer_obj["question_id"]
                    if choice.strip():
                        answer.choice = int(choice)
                    answer.text = answer_obj["text"]
                    answer.runinfo = runinfo
                    answer.save()
            questionnaire.take_nums += 1
            questionnaire.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '完成'
        return HttpResponse(json.dumps(res), content_type='application/json')


class SaveQuestionnaire(View):
    def post(self, request):
        res = dict()

        questionnaire_id = int(request.POST.get('questionnaire_id', 0))
        questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        if questionnaire:
            # 删除原有的问题记录
            Question.objects.filter(questionnaire=questionnaire).delete()
            payload = json.loads(request.POST.get('payload'))
            question_list = payload['fields']
            for index1, value1 in enumerate(question_list):
                question = Question()
                question.questionnaire = questionnaire
                question.sortnum = index1 + 1
                # question.type = value1['field_type'].split('-')[0]
                question.type = value1['field_type']
                question.text = value1['label']
                question.save()
                # 有选项，则更新选项表
                if 'options' in value1['field_options'].keys():
                    for index2, value2 in enumerate(value1['field_options']['options']):
                        choice_obj = Choice()
                        choice_obj.question = question
                        choice_obj.sortnum = index2 + 1
                        choice_obj.text = value2['label']
                        choice_obj.save()

            res['status'] = 'success'
            res['msg'] = '保存成功'
        else:
            res = dict()
            res['status'] = 'failed'
            res['msg'] = '问卷未创建'
        return HttpResponse(json.dumps(res), content_type='application/json')

