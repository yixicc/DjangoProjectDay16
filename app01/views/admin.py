# -*- coding: utf-8 -*-
# @Time : 2025/8/13 11:00
# @Author : zhou
# @File : admin.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from app01 import models
from app01.utils.form import AdminModelForm
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
        print(form.cleaned_data)
        form.save()
        return redirect('/admin/list/')
    else:
        return render(request, 'add.html', {"form": form})