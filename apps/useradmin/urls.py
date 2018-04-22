# _*_ coding:utf-8 _*_
from django.conf.urls import *
from .views import *


urlpatterns = [
    # 后台管理首页
    url(r'manage/courses$', manage_courses),

]
