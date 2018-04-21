# _*_ coding:utf-8 _*_

import xadmin
from .models import Companys,Users

class UsersChoice(object):
    model = Users
    extra = 0

#企业
class CompanysAdmin(object):
    list_display = ['name', 'account', 'email', 'legalperson', 'address']
    search_fields = ['name']
    # list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'
    inlines = [UsersChoice]
xadmin.site.register(Companys, CompanysAdmin)
# class DemoAdmin(object):
#     list_display = ['name']
#     search_fields = ['name']
#     model_icon = 'fas fa-clipboard-list'
#users
class UsersAdmin(object):
    list_display = ['name', 'username', 'password', 'tel', 'department', 'position', 'email', 'total_class']
    search_fields = ['name']
    # list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'

xadmin.site.register(Users, UsersAdmin)