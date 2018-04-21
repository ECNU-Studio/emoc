# _*_ coding:utf-8 _*_

import xadmin
from .models import Companys

#企业
class CompanysAdmin(object):
    list_display = ['name', 'account', 'email', 'legalperson', 'address']
    search_fields = ['name']
    # list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fas fa-clipboard-list'

# class DemoAdmin(object):
#     list_display = ['name']
#     search_fields = ['name']
#     model_icon = 'fas fa-clipboard-list'



xadmin.site.register(Companys, CompanysAdmin)