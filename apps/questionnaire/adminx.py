# _*_ coding:utf-8 _*_
import xadmin
from .models import Questionnaire, Question, RunInfo, Choice


class QuestionInline(object):
    model = Question
    extra = 0


class ChoiceInline(object):
    model = Choice
    extra = 0


class QuestionnaireAdmin(object):
    list_display = ['name', 'edit_questionnaire', 'show_questionnaire']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'
    # inlines = [QuestionInline]
    # 根据更新时间倒序
    ordering = ['-update_time']


class QuestionAdmin(object):
    list_display = ['questionnaire', 'text', 'type']
    search_fields = ['text']
    # list_filter = ['type']
    readonly_fields = ['sortnum']
    model_icon = 'fas fa-question'
    # 不显示字段
    # exclude = ['sortnum']
    relfield_style = 'fk_ajax'
    inlines = [ChoiceInline]


# class ChoiceAdmin(object):
#     list_display = ['question', 'text']
#     search_fields = ['text']
#     # list_filter = ['question', 'text']
#     readonly_fields = ['sortnum']
#     model_icon = 'fas fa-question'
#     # 不显示字段
#     # exclude = ['sortnum']
#     relfield_style = 'fk_ajax'


class RunInfoAdmin(object):
    list_display = ['questionnaire', 'user', 'create_time']
    search_fields = ['questionnaire', 'user']
    list_filter = ['questionnaire', 'user', 'create_time']
    model_icon = 'fas fa-history'   #far fa-chart-bar'
    readonly_fields = ['questionnaire', 'user', 'create_time']


# 效率统计
class QuestionnaireStatisticsAdmin(object):
    list_display = ['name', 'show_questionnaire']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    readonly_fields = ['name']
    model_icon = 'far fa-chart-bar'
    inlines = [QuestionInline]


xadmin.site.register(Questionnaire, QuestionnaireAdmin)
# xadmin.site.register(Question, QuestionAdmin)
# xadmin.site.register(Choice, ChoiceAdmin)
xadmin.site.register(RunInfo, RunInfoAdmin)

# xadmin.site.register(Questionnaire, QuestionnaireStatisticsAdmin)


