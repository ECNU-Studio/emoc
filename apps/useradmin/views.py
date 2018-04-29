# _*_ coding:utf-8 _*_
import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from courses.models import *

class manage_courses(View):
    def get(self, request, courses_id=None, preview=1):
        all_courses = courses.objects.all()
        org_nums = courses.count()
        # 反解析URL
        return render(request, 'templates/admin_courses.html', {
             'org_nums': org_nums,
            'all_courses': all_courses,
             'preview': preview
         })
