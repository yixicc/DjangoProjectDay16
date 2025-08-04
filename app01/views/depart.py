# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:06
# @Author : zhou
# @File : depart.py
# @Software: PyCharm
from django.shortcuts import render, redirect

from app01 import models


def depart_List(request):
    '''部门列表'''

    '''数据库中获取所有的部门列表'''
    query_set = models.Department.objects.all()

    return render(request,'depart_list.html',{'query_set':query_set})


def depart_add(request):
    if request.method == 'GET':
        return render(request,'depart_add.html')

    departname = request.POST.get("title")
    models.Department.objects.create(title=departname)
    return redirect('/depart/list/')


def depart_update(request,nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_update.html',{"row_object":row_object})

    departname = request.POST.get("departname")
    models.Department.objects.filter(id=nid).update(title=departname)
    return redirect('/depart/list/')

def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')

