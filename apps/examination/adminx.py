# _*_ coding:utf-8 _*_
import xadmin
from .models import *



# _*_ coding:utf-8 _*_
import xadmin
from .models import CourseOld, Question, Choice


class ChoiceInline(object):
    model = Choice
    extra = 0


class CourseOldAdmin(object):
    list_display = ['name', 'manage_question', 'show_examination', 'show_statistics']
    search_fields = ['name']
    list_filter = ['name']
    # 只读字段
    readonly_fields = ['name']
    model_icon = 'fa fa-calendar'


class ExaminationAdmin(object):
    list_display = ['course', 'show_examination']
    search_fields = []
    list_filter = []
    # 不显示字段
    exclude = ['take_nums']
    relfield_style = 'fk_ajax'
    model_icon = 'far fa-calendar-check'
    # 根据更新时间倒序
    ordering = ['-update_time']

    def queryset(self):
        # super调用方法
        qs = super(ExaminationAdmin, self).queryset()
        qs = qs.filter(is_published=False)
        return qs


class PublishedExaminationAdmin(object):
    list_display = ['course', 'show_statistics']
    search_fields = []
    list_filter = []
    # 不显示字段
    exclude = ['is_published']
    # 只读字段
    readonly_fields = ['course', 'type', 'question_nums', 'take_nums']
    # 列表页直接编辑
    model_icon = 'fas fa-clipboard-list'
    # 根据更新时间倒序
    ordering = ['-update_time']

    def queryset(self):
        # super调用方法
        qs = super(PublishedExaminationAdmin, self).queryset()
        qs = qs.filter(is_published=True)
        return qs


class QuestionAdmin(object):
    list_display = ['course', 'text', 'type']
    search_fields = ['text']
    # list_filter = ['type']
    # 只读字段
    readonly_fields = ['sortnum']
    model_icon = 'fas fa-question'
    # 不显示字段
    # exclude = ['sortnum']
    relfield_style = 'fk_ajax'
    inlines = [ChoiceInline]


xadmin.site.register(CourseOld, CourseOldAdmin)

# xadmin.site.register(Examination, ExaminationAdmin)

# xadmin.site.register(PublishedExamination, PublishedExaminationAdmin)

# xadmin.site.register(Question, QuestionAdmin)