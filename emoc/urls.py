# _*_ coding:utf-8 _*_
"""emoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.views.generic import TemplateView
from django.views.static import serve #处理静态文件

import xadmin

# users应用
from users.views import user_login

# questionnaire应用
from questionnaire.views import QuestionnaireView, AddQuestionnaire

# 遍历 INSTALLED_APPS里面的设置，发现有admin.py,就会执行其中的代码
# admin.autodiscover()

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),

    url(r'^login/$', user_login, name="login"),

    # questionnaire应用
    url(r'^questionnaire/take/(?P<questionnaire_id>[0-9]+)/$', QuestionnaireView.as_view(), name='questionnaire'),
    url(r'^questionnaire/add/$', AddQuestionnaire.as_view(), name='add_questionnaire'),


]
