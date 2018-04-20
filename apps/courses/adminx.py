# _*_ coding:utf-8 _*_

import xadmin
from .models import Courses


#课程
class CoursesAdmin(object):
    list_display = ['name', 'coursesAbstract', 'teacherid']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fa fa-graduation-cap'

xadmin.site.register(Courses, CoursesAdmin)
