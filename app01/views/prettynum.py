# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:07
# @Author : zhou
# @File : prettynumm.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from app01 import models
from app01.utils.form import PrettyNumModelForm, PrettyNumEditModelForm


def prettynum_list(request):

    search_dict = {}
    search_word = request.GET.get('q')
    if search_word:
        search_dict["mobile__contains"] = search_word

    #根据用户想要访问的页面计算起止位置
    page = int(request.GET.get('page',1))

    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    #   数据总条数
    total_count = models.PrettyNum.objects.filter(**search_dict).count()
    # 总页码数
    total_pages,div = divmod(total_count,page_size)
    if div:
        total_pages = total_pages + 1

    # 计算当前页的前5页和后5页
    plus = 5
    # 总页数小于11页
    if total_pages <= 2 * plus + 1 :
        start_page = 1
        end_page = total_pages
    else:
        # 总页数大于11页
        if page <= plus:
            # 当前页小于5
            start_page = 1
            end_page = 2 * plus + 1
        elif page >= total_pages - plus:
            # 当前页大于5
            start_page = page - plus
            end_page = total_pages
        else:
            start_page = page - plus
            end_page = page + plus

    #页码
    page_str_list = []

    #首页
    page_str_list.append('<li class="active"><a href="?page={}">首页</a></li>'.format(1))

    # 上一页
    if page > 1:
        ele = '<li class="active"><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        ele = '<li class="active"><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(ele)

    for i in range (start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_str_list.append(ele)

    # 下一页
    if page < total_pages:
        ele = '<li class="active"><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        ele = '<li class="active"><a href="?page={}">下一页</a></li>'.format(total_pages)
    page_str_list.append(ele)

    #尾页
    page_str_list.append('<li class="active"><a href="?page={}">尾页</a></li>'.format(total_pages))

    page_string = mark_safe("".join(page_str_list))

    '''数据库中获取所有的靓号列表'''
    query_set = models.PrettyNum.objects.filter(**search_dict).order_by("-level")[start:end]
    return render(request,'prettynum_list.html',{'query_set':query_set,'search_value':search_word,"page_string":page_string})

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