# _*_ coding:utf-8 _*_
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def manage_courses(request):
    return render(request, 'admin_courses.html')
