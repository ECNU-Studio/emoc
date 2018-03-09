# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import Signal
import imp

__all__ = ['question_proc', 'answer_proc', 'add_type', 'AnswerException', 'questionset_done', 'questionnaire_done',]

QuestionChoices = []
QuestionProcessors = {}  # supply additional information to the templates
Processors = {}  # for processing answers

questionnaire_start = Signal(providing_args=["runinfo", "questionnaire"])
questionset_start = Signal(providing_args=["runinfo", "questionset"])
questionset_done = Signal(providing_args=["runinfo", "questionset"])
questionnaire_done = Signal(providing_args=["runinfo", "questionnaire"])


class AnswerException(Exception):
    """Thrown from an answer processor to generate an error message"""
    pass

def question_proc(*names):
    """
    装饰器为一个或多个问题类型创建问题处理器
    Usage:
    @question_proc('typename1', 'typename2')
    def qproc_blah(request, question):
        ...
    """

    def decorator(func):
        global QuestionProcessors
        for name in names:
            QuestionProcessors[name] = func
        return func

    return decorator


def answer_proc(*names):
    """
   装饰器为一个或多个问题类型创建答案处理器

    Usage:
    @question_proc('typename1', 'typename2')
    def qproc_blah(request, question):
        ...
    """

    def decorator(func):
        global Processors
        for name in names:
            Processors[name] = func
        return func

    return decorator


def add_type(id, name):
    """
    在管理界面中注册一个新的问题类型。

    Usage:
        add_type('mysupertype', 'My Super Type [radio]')
    """
    global QuestionChoices
    QuestionChoices.append((id, name))

add_type('sameas', 'Same as Another Question (put sameas=question.number in checks or sameasid=question.id)')

# import questionnaire.qprocessors  # make sure ours are imported first
#
# for app in settings.INSTALLED_APPS:
#     try:
#         app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
#     except AttributeError:
#         continue
#
#     try:
#         imp.find_module('qprocessors', app_path)
#     except ImportError:
#         continue
#
#     __import__("%s.qprocessors" % app)
