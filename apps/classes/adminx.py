# _*_ coding:utf-8 _*_
import xadmin
from .models import Classes

#班级
class ClassesAdmin(object):
    list_display = ['companyid', 'coursesid']
    search_fields = ['companyid']
    list_filter = ['companyid']
    # 列表页直接编辑
    list_editable = ['companyid']
    model_icon = 'fa fa-users'

xadmin.site.register(Classes, ClassesAdmin)

