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


class QuestionEdit(View):
    """
    编辑问卷
    """
    def get(self, request, course_id=None):
        course = get_object_or_404(CourseOld, id=int(course_id))
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


        return render(request, 'edit_question.html', {
            'course': course,
            'question_list': json.dumps(question_list)
        })



class SaveQuestion(View):
    def post(self, request):
        res = dict()
        course_id = int(request.POST.get('course_id', 0))
        course = CourseOld.objects.get(id=course_id)
        if course:
            # 删除原有的问题记录
            Question.objects.filter(course=course).delete()
            payload = json.loads(request.POST.get('payload'))
            question_list = payload['fields']
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

            res['status'] = 'success'
            res['msg'] = '保存成功'
        else:
            res = dict()
            res['status'] = 'failed'
            res['msg'] = '课程未创建'
        return HttpResponse(json.dumps(res), content_type='application/json')