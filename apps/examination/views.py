# _*_ coding:utf-8 _*_
from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from examination.models import *
import random
import json
from hashlib import md5


class ExaminationShow(View):
    """
    预览试卷
    """
    def get(self, request, course_id=None, preview=1):
        course = get_object_or_404(Course, id=int(course_id))
        examination = course.examination()
        questions = []
        for exam in examination:
            question = Question.objects.get(id=exam.question_id)
            question.choices = question.choices()
            question.template = "question_type/%s.html" % question.type
            questions.append(question)

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
        return render(request, 'show_examination.html',
                      {'course': course, 'questions': questions, 'preview': preview})


class StatisticsShow(View):
    """
    查找当前问卷的统计信息并显示出来
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(Course, id=int(course_id))
        examination = course.examination()
        questions = []
        for exam in examination:
            question = Question.objects.get(id=exam.question_id)
            if question.type == 'text':
                question.answer_texts = question.get_answer_texts()
            else:
                question.statistics = question.statistics()
            question.template = "statistics_type/%s.html" % question.type
            questions.append(question)
        takeinfos = TakeInfo.objects.filter(course=course)[:10]

        # 反解析URL
        return render(request, 'examination_statistics.html', {
            'course': course,
            'questions': questions,
            'takeinfos': takeinfos
        })


class QuestionEdit(View):
    """
    编辑试卷
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(Course, id=int(course_id))
        questions = course.questions()
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

        return render(request, 'edit_examination.html', {
            'course': course,
            'question_list': json.dumps(question_list)
        })


class SaveQuestion(View):
    """
    保存试卷时候，根据随机卷或者固定卷进行保存
    """
    def post(self, request):
        res = dict()
        course_id = int(request.POST.get('course_id', 0))
        course = Course.objects.get(id=course_id)
        if course:
            # 删除原有的问题记录
            Question.objects.filter(course=course).delete()
            # 删除原有的试卷
            Examination.objects.filter(course=course).delete()
            payload = json.loads(request.POST.get('payload'))
            question_list = payload['fields']
            question_count = int(request.POST.get('question_count', 0))
            is_random = request.POST.get('is_random')
            for index1, value1 in enumerate(question_list):
                question = Question()
                question.course = course
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

            if is_random == 'false':
                # 生成固定卷
                questions = Question.objects.filter(course=course).order_by('sortnum')[:question_count]
            else:
                # 生成随机卷
                questionAll = list(Question.objects.filter(course=course))
                questions = random.sample(questionAll, question_count)

            for question in questions:
                examination = Examination()
                examination.question = question
                examination.course = course
                examination.save()
            res['status'] = 'success'
            res['msg'] = '保存成功'
        else:
            res = dict()
            res['status'] = 'failed'
            res['msg'] = '课程未创建'
        return HttpResponse(json.dumps(res), content_type='application/json')


class SubmitExamination(View):
    # 保存记录
    def save_takeinfo(self, course, user):
        takeinfo = TakeInfo()
        takeinfo.user = user
        takeinfo.course = course
        takeinfo.save()
        return takeinfo

    def post(self, request):
        # 获取调查者
        if not request.user.is_authenticated():
            user = User.objects.filter(username='Anonymous')[0:1]
        else:
            user = request.user
        course_id = int(request.POST.get('course_id', 0))
        course = Course.objects.get(id=course_id)
        if course:
            takeinfo = self.save_takeinfo(course, user)
            answers = json.loads(request.POST.get('answerStr'))
            for answer_obj in answers:
                choices = answer_obj["choice"].split(',')
                for choice in choices:
                    answer = Answer()
                    answer.question = answer_obj["question_id"]
                    if choice.strip():
                        answer.choice = int(choice)
                    answer.text = answer_obj["text"]
                    answer.takeinfo = takeinfo
                    answer.save()
            if course.take_nums:
                course.take_nums += 1
            else:
                course.take_nums = 1
            course.save()
            res = dict()
            res['status'] = 'success'
            res['msg'] = '完成'
        return HttpResponse(json.dumps(res), content_type='application/json')