# _*_ coding:utf-8 _*_

import xadmin
from .models import Courses
# from teacheres.models import Teacheres


# class TeachersChoice(object):
#     model = Teacheres
#     extra = 0

#课程
class CoursesAdmin(object):
    list_display = ['name', 'coursesAbstract', 'teacherid']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fa fa-graduation-cap'
    # inlines = [TeachersChoice]

xadmin.site.register(Courses, CoursesAdmin)
