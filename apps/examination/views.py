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


class ExaminationEdit(View):
    """
    编辑问卷
    """
    def get(self, request, examination_id=None):
        examination = get_object_or_404(Examination, id=int(examination_id))
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
                option['checked'] = False
                options.append(option)
            question_obj['field_options']['options'] = options

            question_list.append(question_obj)


        return render(request, 'edit_questionnaire.html', {
            'questionnaire': questionnaire,
            'question_list': json.dumps(question_list)
        })
