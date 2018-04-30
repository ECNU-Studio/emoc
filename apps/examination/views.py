# _*_ coding:utf-8 _*_
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from examination.models import *
from users.models import UserProfile
import random
import json
from hashlib import md5
from datetime import *
import time


class ExaminationShow(View):
    """
    预览试卷
    """
    def get(self, request, course_id=None, preview=1):
        course = get_object_or_404(CourseOld, id=int(course_id))
        examination = get_object_or_404(Examination, course=course)
        if examination:
            questions = examination.questions_use()
            for question in questions:
                question.choices = question.choices()
                question.template = "question_type/exam-%s.html" % question.type

        # 反解析URL
        return render(request, 'show_examination.html',
                  {'course': course,
                   'examination': examination,
                   'questions': questions, 'preview': preview}
                      )


class StatisticsShow(View):
    """
    查找当前问卷的统计信息并显示出来
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(CourseOld, id=int(course_id))
        examination = get_object_or_404(Examination, course=course)
        if examination:
            questions = examination.questions_use()
            for question in questions:
                if question.type == 'text':
                    question.answer_texts = question.get_answer_texts()
                else:
                    question.statistics = question.statistics()
                question.template = "statistics_type/%s.html" % question.type

            takeinfos = TakeInfo.objects.filter(examination=examination).order_by('score')

        # 反解析URL
        return render(request, 'examination_statistics.html', {
            'examination': examination,
            'questions': questions,
            'takeinfos': takeinfos
        })


class ShowTakeinfoDetail(View):
    """
    查找一个问卷的答案显示
    """
    def get(self, request, takeinfo_id=None):
        takeinfo = get_object_or_404(TakeInfo, id=int(takeinfo_id))
        examination = get_object_or_404(Examination, id=takeinfo.examination_id)
        if examination:
            questions = examination.questions_use()
            questions.count = questions.count()
            for question in questions:
                choices = question.choices()
                for choice in choices:
                    if Answer.objects.filter(takeinfo=takeinfo.id, question=question.id, choice=choice.id).exists():
                        choice.checked = True
                question.choices = choices
                question.template = "takeinfo_detail_type/%s.html" % question.type
                # 反解析URL  
        return render(request, 'show_takeinfo_detail.html', {
            'takeinfo': takeinfo,
            'questions': questions,
            'examination': examination
        })

class QuestionEdit(View):
    """
    编辑试卷
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(CourseOld, id=int(course_id))
        examination_set = Examination.objects.filter(course=course)[0:1]
        if not examination_set:
            examination = Examination()
            examination.course = course
            examination.is_published = False
            examination.take_nums = 0
            examination.save()
        else:
            examination = list(examination_set)[0]
        questions = examination.questions()
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
                option['checked'] = choice.is_answer
                options.append(option)
            question_obj['field_options']['options'] = options

            question_list.append(question_obj)

        return render(request, 'edit_examination.html', {
            'course': course,
            'examination': examination,
            'question_list': json.dumps(question_list)
        })


class SaveQuestion(View):
    """
    保存试卷时候，根据随机卷或者固定卷进行保存
    """
    def post(self, request):
        res = dict()
        examination_id = int(request.POST.get('examination_id', 0))
        examination = Examination.objects.get(id=examination_id)
        if examination:
            # 删除原有的问题记录
            payload = json.loads(request.POST.get('payload'))
            question_list = payload['fields']
            question_count = int(request.POST.get('question_count', 0))
            is_random = request.POST.get('is_random')

            examination.is_random = is_random
            examination.question_count = question_count
            examination.save()

            Question.objects.filter(examination=examination).delete()
            for index1, value1 in enumerate(question_list):
                question = Question()
                question.examination = examination
                question.sortnum = index1 + 1
                question.type = value1['field_type']
                question.text = value1['label']
                question.save()
                # 有选项，则更新选项表
                if 'options' in value1['field_options'].keys():
                    for index2, value2 in enumerate(value1['field_options']['options']):
                        choice_obj = Choice()
                        choice_obj.question = question
                        choice_obj.is_answer = value2['checked']
                        choice_obj.sortnum = index2 + 1
                        choice_obj.text = value2['label']
                        choice_obj.save()
            if is_random == 'false':
                # 生成固定卷
                questions = Question.objects.filter(examination=examination).order_by('sortnum')[:question_count]
            else:
                # 生成随机卷
                questionAll = list(Question.objects.filter(examination=examination))
                questions = random.sample(questionAll, question_count)

            for question in questions:
                question.is_use = True
                question.save()
            res['status'] = 'success'
            res['msg'] = '保存成功'
        else:
            res = dict()
            res['status'] = 'failed'
            res['msg'] = '课程未创建'
        return HttpResponse(json.dumps(res), content_type='application/json')


class CancelExamination(View):
    def post(self, request):
        examination_id = int(request.POST.get('examination_id', 0))
        examination = get_object_or_404(Examination, id=int(examination_id))
        if examination:
            examination.is_published = False
            examination.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '已取消'
        return HttpResponse(json.dumps(res), content_type='application/json')


class PublishExamination(View):
    def post(self, request):
        examination_id = int(request.POST.get('examination_id', 0))
        examination = get_object_or_404(Examination, id=int(examination_id))
        if examination:
            examination.is_published = True
            examination.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '发布成功'
        return HttpResponse(json.dumps(res), content_type='application/json')


class SubmitExamination(View):
    # 保存记录
    def save_takeinfo(self, examination, user, start_time, end_time):
        takeinfo = TakeInfo()
        takeinfo.user = user
        takeinfo.examination = examination
        takeinfo.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        takeinfo.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        takeinfo.save()
        return takeinfo

    def post(self, request):
        # 获取调查者
        # 根据userid获取
        user_id = int(request.POST.get('user_id', 1))
        user = get_object_or_404(UserOld, id=user_id)
        examination_id = int(request.POST.get('examination_id', 0))
        examination = get_object_or_404(Examination, id=int(examination_id))
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        if examination:
            takeinfo = self.save_takeinfo(examination, user, start_time, end_time)
            # 未处理好
            answers = json.loads(request.POST.get('answerStr'))
            right_num = 0
            for answer_obj in answers:
                question_id = answer_obj["question_id"]
                choices = answer_obj["choice"].split(',')
                answerObjs = Choice.objects.filter(question_id=int(question_id), is_answer=True).values('id')
                answers = []
                for answerObj in answerObjs:
                    answers.append(str(answerObj.get('id')))
                if answers == choices:
                    right_num = right_num + 1
                for choice in choices:
                    answer = Answer()
                    answer.question = question_id
                    # 去除空格
                    if choice.strip():
                        answer.choice = int(choice)
                    answer.text = answer_obj["text"]
                    answer.takeinfo = takeinfo
                    answer.save()

            takeinfo.score = (100/examination.question_count)*right_num
            takeinfo.save()
            examination.take_nums += 1
            examination.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '完成'
        return HttpResponse(json.dumps(res), content_type='application/json')