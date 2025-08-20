# -*- coding: utf-8 -*-
# @Time : 2025/8/18 17:14
# @Author : zhou
# @File : task.py
# @Software: PyCharm
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination


def task_list(request):
    '''任务列表'''
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": queryset,
        "page_string": page_object.html()
    }
    return render(request, 'task_list.html',context)

@csrf_exempt
def task_ajax(request):
    print("request.GET",request.GET)
    print("request.POST",request.POST)
    data_dict = {"status":"success","data":[11,22,33]}
    return HttpResponse(json.dumps(data_dict))

@csrf_exempt
def task_add(request):

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status":True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status":False,'error':form.errors}
    return HttpResponse(json.dumps(data_dict,ensure_ascii=False))
