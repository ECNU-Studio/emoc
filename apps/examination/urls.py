# _*_ coding:utf-8 _*_
from django.conf.urls import *
from examination.views import *


urlpatterns = [
    # examination
    url(r'edit/(?P<course_id>[0-9]+)/$', QuestionEdit.as_view(), name='edit_question'),
    url(r'take/(?P<course_id>[0-9]+)/(?P<preview>[0|1])/$', ExaminationShow.as_view(), name='show_examination'),
    url(r'statistics/(?P<course_id>[0-9]+)/$', StatisticsShow.as_view(), name='show_statistics'),
    url(r'submit/$', SubmitExamination.as_view(), name='submit_examination'),
    url(r'publish/$', PublishExamination.as_view(), name='publish_examination'),
    url(r'cancel/$', CancelExamination.as_view(), name='cancel_examination'),
    url(r'save/$', SaveQuestion.as_view(), name='save_question'),
    url(r'show/(?P<takeinfo_id>[0-9]+)/$', ShowTakeinfoDetail.as_view(), name='show_takeinfo_detail'),
]
