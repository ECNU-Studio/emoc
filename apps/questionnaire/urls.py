# _*_ coding:utf-8 _*_
from django.conf.urls import *
from questionnaire.views import *


urlpatterns = [
    # questionnaire应用
    url(r'edit/(?P<questionnaire_id>[0-9]+)/$', QuestionnaireEdit.as_view(), name='edit_questionnaire'),
    url(r'take/(?P<questionnaire_id>[0-9]+)/(?P<preview>[0|1])/$', QuestionnaireShow.as_view(), name='show_questionnaire'),
    url(r'statistics/(?P<questionnaire_id>[0-9]+)/$', StatisticsShow.as_view(), name='show_statistics'),
    url(r'submit/$', SubmitQuestionnaire.as_view(), name='submit_questionnaire'),
    url(r'save/$', SaveQuestionnaire.as_view(), name='save_questionnaire'),
]
