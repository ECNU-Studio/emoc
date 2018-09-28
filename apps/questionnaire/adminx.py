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
    list_display = ['course', 'edit_questionnaire', 'show_questionnaire']
    search_fields = ['course']
    list_filter = ['course']
    # 列表页直接编辑
    list_editable = ['course']
    model_icon = 'fas fa-clipboard-list'
    # 不显示字段
    exclude = ['take_nums']
    # 根据更新时间倒序
    ordering = ['-update_time']

    def queryset(self):
        # super调用方法
        qs = super(QuestionnaireAdmin, self).queryset()
        qs = qs.filter(is_published=False)
        return qs


class PublishedQuestionnaireAdmin(object):
    list_display = ['name', 'show_statistics']
    search_fields = ['name']
    list_filter = ['name']
    # 不显示字段
    exclude = ['is_published']
    # 只读字段
    readonly_fields = ['name', 'take_nums']
    # 列表页直接编辑
    model_icon = 'fas fa-clipboard-list'
    # 根据更新时间倒序
    ordering = ['-update_time']

    def queryset(self):
        # super调用方法
        qs = super(PublishedQuestionnaireAdmin, self).queryset()
        qs = qs.filter(is_published=True)
        return qs


class QuestionAdmin(object):
    list_display = ['questionnaire', 'text', 'type']
    search_fields = ['text']
    # list_filter = ['type']
    # 只读字段
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
    list_display = ['question']
    search_fields = ['question']
    list_filter = ['question']
    model_icon = 'far fa-chart-bar'


xadmin.site.register(Questionnaire, QuestionnaireAdmin)
# xadmin.site.register(PublishedQuestionnaire, PublishedQuestionnaireAdmin)
# xadmin.site.register(Question, QuestionAdmin)
# xadmin.site.register(Choice, ChoiceAdmin)
xadmin.site.register(RunInfo, RunInfoAdmin)

# xadmin.site.register(QuestionnaireStatistics, QuestionnaireStatisticsAdmin)


