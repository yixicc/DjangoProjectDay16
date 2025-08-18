# -*- coding: utf-8 -*-
# @Time : 2025/8/18 17:14
# @Author : zhou
# @File : task.py
# @Software: PyCharm
from django.http import HttpResponse
from django.shortcuts import render


def task_list(request):
    '''任务列表'''
    return render(request, 'task_list.html')


def task_ajax(request):
    print("request.GET",request.GET)
    return HttpResponse("成功了")

