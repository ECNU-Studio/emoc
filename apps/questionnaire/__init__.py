# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import Signal
import imp

QuestionChoices = []


def add_type(id, name):
    global QuestionChoices
    QuestionChoices.append((id, name))
