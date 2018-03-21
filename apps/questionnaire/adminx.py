# _*_ coding:utf-8 _*_
import xadmin
from .models import Questionnaire, Question, Choice, Answer


class QuestionnaireAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fas fa-clipboard-list'


class QuestionAdmin(object):
    list_display = ['text', 'type']
    search_fields = ['text']
    list_filter = ['type']
    model_icon = 'fas fa-question'


class ChoiceAdmin(object):
    list_display = ['text', 'tags', 'question']
    search_fields = ['text', 'tags', 'question']
    list_filter = ['text', 'tags', 'question']
    model_icon = 'fas fa-list-ol'


# class AnswerAdmin(object):
#     list_display = ['answer']
#     search_fields = ['answer']
#     list_filter = ['answer']


xadmin.site.register(Questionnaire, QuestionnaireAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Choice, ChoiceAdmin)
# xadmin.site.register(Answer, AnswerAdmin)

