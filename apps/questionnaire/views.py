# _*_ coding:utf-8 _*_
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from questionnaire.models import *
# from users.models import UserProfile
from nengli8.models import *
import json
from hashlib import md5


class QuestionnaireEdit(View):
    """
    编辑问卷
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(CourseOld, id=int(course_id))
        questionnaire_set = Questionnaire.objects.filter(course=course)[0:1]
        if not questionnaire_set:
            questionnaire = Questionnaire()
            questionnaire.course = course
            questionnaire.is_published = False
            questionnaire.take_nums = 0
            questionnaire.save()
        else:
            questionnaire = list(questionnaire_set)[0]
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
    def get(self, request, course_id=None):
        course = get_object_or_404(CourseOld, id=int(course_id))
        questionnaire = get_object_or_404(Questionnaire, course=course)
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

class ShowRuninfoDetail(View):
    """
    查找一个问卷的答案显示
    """
    def get(self, request, runinfo_id=None):
        runinfo = get_object_or_404(RunInfo, id=int(runinfo_id))
        questionnaire = get_object_or_404(Questionnaire, id=runinfo.questionnaire_id)
        if questionnaire:
            questions = questionnaire.questions()
            for question in questions:
                choices = question.choices()
                for choice in choices:
                    if Answer.objects.filter(runinfo=runinfo.id, question=question.id, choice=choice.id).exists():
                        choice.checked = True
                question.choices = choices
                question.template = "runinfo_detail_type/%s.html" % question.type
                # 反解析URL
        return render(request, 'show_runinfo_detail.html', {
            'questions': questions
        })



class QuestionnaireShow(View):
    """
    查找当前问卷并显示出来
    """
    def get(self, request, course_id=None, preview=1):
        course = get_object_or_404(CourseOld, id=int(course_id))
        questionnaire = get_object_or_404(Questionnaire, course=course)
        if questionnaire:
            questions = questionnaire.questions()
            questions.count = questions.count()
            for question in questions:
                question.choices = question.choices()
                question.template = "question_type/%s.html" % question.type

        # 反解析URL
        return render(request, 'show_questionnaire.html', {
            'course': course,
            'questionnaire': questionnaire,
            'questions': questions,
            'preview': preview
        })


class CancelQuestionnaire(View):
    def post(self, request):
        questionnaire_id = int(request.POST.get('questionnaire_id', 0))
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        if questionnaire:
            questionnaire.is_published = False
            questionnaire.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '已取消 '
        return HttpResponse(json.dumps(res), content_type='application/json')


class PublishQuestionnaire(View):
    def post(self, request):
        questionnaire_id = int(request.POST.get('questionnaire_id', 0))
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        if questionnaire:
            questionnaire.is_published = True
            questionnaire.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '发布成功'
        return HttpResponse(json.dumps(res), content_type='application/json')


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
        # 根据userid获取
        user_id = int(request.POST.get('user_id', 1))
        user = get_object_or_404(UserOld, id=user_id)
        questionnaire_id = int(request.POST.get('questionnaire_id', 0))
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
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

