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
    list_display = ['name','manage_question']
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fa fa-calendar'


class ExaminationAdmin(object):
    list_display = ['course', 'is_published']
    search_fields = ['course']
    list_filter = ['course']
    # 不显示字段
    # exclude = ['take_nums']
    relfield_style = 'fk_ajax'
    model_icon = 'far fa-calendar-check'


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

xadmin.site.register(Examination, ExaminationAdmin)


# xadmin.site.register(Question, QuestionAdmin)