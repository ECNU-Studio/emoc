# _*_ coding:utf-8 _*_
import xadmin

from .models import Subject, Questionnaire, QuestionSet, Question, Choice, Answer


class SubjectAdmin(object):
    list_display = ['surname', 'givenname', 'gender']
    search_fields = ['surname', 'givenname', 'gender']
    list_filter = ['surname', 'givenname', 'gender']


class QuestionnaireAdmin(object):
    list_display = ['name', 'redirect_url']
    search_fields = ['name', 'redirect_url']
    list_filter = ['name', 'redirect_url']


class QuestionSetAdmin(object):
    list_display = ['heading', 'text']
    search_fields = ['heading', 'text']
    list_filter = ['heading', 'text']


class QuestionAdmin(object):
    list_display = ['type', 'text']
    search_fields = ['type', 'text']
    list_filter = ['type', 'text']


class ChoiceAdmin(object):
    list_display = ['tags', 'text']
    search_fields = ['tags', 'text']
    list_filter = ['tags', 'text']


# class AnswerAdmin(object):
#     list_display = ['answer']
#     search_fields = ['answer']
#     list_filter = ['answer']


xadmin.site.register(Subject, SubjectAdmin)
xadmin.site.register(Questionnaire, QuestionnaireAdmin)
xadmin.site.register(QuestionSet, QuestionSetAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Choice, ChoiceAdmin)
# xadmin.site.register(Answer, AnswerAdmin)

