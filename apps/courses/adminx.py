# _*_ coding:utf-8 _*_
import xadmin
from .models import Course


class CourseAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
    style_fields = {"detail": "ueditor"}


xadmin.site.register(Course, CourseAdmin)
