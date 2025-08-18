# -*- coding: utf-8 -*-
# @Time : 2025/8/18 17:14
# @Author : zhou
# @File : task.py
# @Software: PyCharm
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def task_list(request):
    '''任务列表'''
    return render(request, 'task_list.html')

@csrf_exempt
def task_ajax(request):
    print("request.GET",request.GET)
    print("request.POST",request.POST)
    data_dict = {"status":"success","data":[11,22,33]}
    return HttpResponse(json.dumps(data_dict))

