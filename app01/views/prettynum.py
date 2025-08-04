# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:07
# @Author : zhou
# @File : prettynumm.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from app01 import models
from app01.utils.form import PrettyNumModelForm, PrettyNumEditModelForm
from app01.utils.pagination import Pagination


def prettynum_list(request):

    search_dict = {}
    search_word = request.GET.get('q')
    if search_word:
        search_dict["mobile__contains"] = search_word

    queryset = models.PrettyNum.objects.filter(**search_dict).order_by("-level")
    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_word,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request,'prettynum_list.html',{'context':context})

def prettynum_add(request):
    if request.method == 'GET':
        form = PrettyNumModelForm()
        return render(request,'prettynum_add.html', {"form":form})

    form = PrettyNumModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    else:
        return render(request, 'prettynum_add.html', {"form": form})



def prettynum_edit(request,nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyNumEditModelForm(instance=row_object)
        return render(request, 'prettynum_edit.html', {"form": form, "nid": nid})

    form = PrettyNumEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    else:
        return render(request, 'prettynum_edit.html', {"form": form, "nid": nid})



def prettynum_delete(request):
    nid = request.GET.get('nid')
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')