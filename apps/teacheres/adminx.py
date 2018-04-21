# _*_ coding:utf-8 _*_
import xadmin
from .models import Teacheres
from courses.models import Courses

class AddCourses(object):
    model = Courses
    extra = 0


#培训师
class TeacheresAdmin(object):
    list_display = ['name', 'username', 'email', 'phone', 'weixin', 'password']
    search_fields = ['name']
    list_filter = ['name']
    # 列表页直接编辑
    list_editable = ['name']
    model_icon = 'fa fa-user'
    inlines = [AddCourses]

xadmin.site.register(Teacheres, TeacheresAdmin)