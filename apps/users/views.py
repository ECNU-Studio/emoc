# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # render方法的三个参数
        return render(request, 'login.html', {})
