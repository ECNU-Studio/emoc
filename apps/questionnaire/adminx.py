# _*_ coding:utf-8 _*_
import xadmin
from .models import Questionnaire, Question


class QuestionInline(object):
    model = Question
    extra = 0


class QuestionnaireAdmin(object):
    list_display = ['name', 'show_questionnaire']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'
    inlines = [QuestionInline]
    # 根据更新时间倒序
    # ordering = ['-update_time']


class QuestionAdmin(object):
    list_display = ['text', 'type']
    search_fields = ['text']
    list_filter = ['type']
    readonly_fields = ['sortnum']
    model_icon = 'fas fa-question'
    # 不显示字段
    # exclude = ['sortnum']
    relfield_style = 'fk_ajax'



# class ChoiceAdmin(object):
#     list_display = ['text', 'question', 'sortnum']
#     search_fields = ['text', 'question']
#     list_filter = ['text', 'question']
#     model_icon = 'fas fa-list-ol'
#     # 不显示字段
#     exclude = ['sortnum']


# class AnswerAdmin(object):
#     list_display = ['answer']
#     search_fields = ['answer']
#     list_filter = ['answer']


xadmin.site.register(Questionnaire, QuestionnaireAdmin)
xadmin.site.register(Question, QuestionAdmin)
# xadmin.site.register(Answer, AnswerAdmin)

