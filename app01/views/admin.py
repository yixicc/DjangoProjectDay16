# -*- coding: utf-8 -*-
# @Time : 2025/8/13 11:00
# @Author : zhou
# @File : admin.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from app01 import models
from app01.utils.form import AdminModelForm, AdminEditModelForm
from app01.utils.pagination import Pagination


def admin_List(request):
    '''管理员列表'''
    search_dict = {}
    search_word = request.GET.get('q')
    if search_word:
        search_dict["username__contains"] = search_word

    '''数据库中获取所有的管理员'''
    query_set = models.Admin.objects.filter(**search_dict).order_by("id")
    page_object = Pagination(request, query_set)
    context = {
        "search_data": search_word,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request,'admin_list.html',{'context':context})


def admin_add(request):
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request,'add.html', {"form":form,title:'新建管理员'})

    form = AdminModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    else:
        return render(request, 'add.html', {"form": form})


def admin_edit(request, nid):

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request,'error.html',{"msg":"数据不存在"})
        return redirect('/admin/list/')

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request,'add.html', {"form":form,"title":title})

    form = AdminEditModelForm(data = request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'add.html', {"form":form,"title":title})