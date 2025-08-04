# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:06
# @Author : zhou
# @File : users.py
# @Software: PyCharm
from ast import parse
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import MyForm, MyModelForm


def user_List(request):
    '''部门列表'''

    '''数据库中获取所有的用户列表'''
    query_set = models.UserInfo.objects.all()
    return render(request,'user_list.html',{'query_set':query_set})


def user_add(request):
    if request.method == 'GET':
        gender_choices = models.UserInfo.gender_choices
        depart_list =  models.Department.objects.all()
        return render(request,'user_add.html', {"gender_choices":gender_choices,"depart_list":depart_list})

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    create_time = request.POST.get("create_time")
    gender = request.POST.get("gender")
    depart = request.POST.get("depart")

    models.UserInfo.objects.create(name=name,password=password,age=age,account=account,create_time=create_time,gender=gender,depart_id=depart)
    return redirect('/user/list/')


def user_update(request,nid):
    if request.method == 'GET':
        row_object = models.UserInfo.objects.filter(id=nid).first()
        departments =  models.Department.objects.values('id', 'title')  # 显式指定字段
        return render(request,'user_update.html',{"row_object":row_object,"depart_list":list(departments)})

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    creatime = request.POST.get("creatime")
    # 将各种格式的日期转换为标准格式
    formatted_date = parse(creatime)
    gender = request.POST.get("gender")
    depart = request.POST.get("depart")

    models.UserInfo.objects.filter(id=nid).update(name=name,password=password,age=age,account=account,create_time=formatted_date,gender=gender,depart_id=depart)
    return redirect('/user/list/')

def user_delete(request):
    nid = request.GET.get('nid')
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')



def user_add_form(request):
    if request.method == 'GET':
        form = MyForm()
        return render(request,'user_add_form.html', {"form":form})

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    creatime = request.POST.get("creatime")
    gender = request.POST.get("gender")
    depart = request.POST.get("depart")

    models.UserInfo.objects.create(name=name,password=password,age=age,account=account,create_time=creatime,gender=gender,depart_id=depart)
    return redirect('/user/list/')


########################################################################


def user_add_modelform(request):
    if request.method == 'GET':
        form = MyModelForm()
        return render(request,'user_add_modelform.html', {"form":form})

    form = MyModelForm(data = request.POST)
    if form.is_valid():
        print('-----------------')
        print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add_modelform.html', {"form": form})

def user_edit(request,nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        # 使用实例数据初始化表单（用于回显）
        form = MyModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form, "nid": nid})

    form = MyModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 验证通过，保存表单数据
        form.save()
        return redirect('/user/list/')
    else:
        # 验证失败，重新显示表单（带错误信息）
        return render(request, 'user_edit.html', {"form": form, "nid": nid})