# _*_ coding:utf-8 _*_
from django.conf.urls import *
from examination.views import *


urlpatterns = [
    # questionnaire应用
    url(r'edit/(?P<course_id>[0-9]+)/$', QuestionEdit.as_view(), name='edit_question'),
    url(r'take/(?P<course_id>[0-9]+)/(?P<preview>[0|1])/$', ExaminationShow.as_view(), name='show_examination'),
    # url(r'statistics/(?P<questionnaire_id>[0-9]+)/$', StatisticsShow.as_view(), name='show_statistics'),
    # url(r'submit/$', SubmitQuestionnaire.as_view(), name='submit_questionnaire'),
    url(r'save/$', SaveQuestion.as_view(), name='save_question'),
]
