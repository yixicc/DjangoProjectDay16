from django.shortcuts import render, redirect

from app01 import models


# Create your views here.

def depart_List(request):
    '''部门列表'''

    '''数据库中获取所有的部门列表'''
    query_set = models.Department.objects.all()

    return render(request,'depart_list.html',{'query_set':query_set})


def depart_add(request):
    if request.method == 'GET':
        return render(request,'depart_add.html')

    departname = request.POST.get("departname")
    models.Department.objects.create(title=departname)
    return redirect('/depart/list/')


def depart_update(request,nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_update.html',{"row_object":row_object})

    departname = request.POST.get("departname")
    models.Department.objects.filter(id=nid).update(title=departname)
    return redirect('/depart/list/')

def depart_delete(request,nid):
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def user_List(request):
    '''部门列表'''

    '''数据库中获取所有的用户列表'''
    query_set = models.UserInfo.objects.all()

    return render(request,'user_list.html',{'query_set':query_set})


def user_add(request):
    if request.method == 'GET':
        return render(request,'user_add.html')

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    creatime = request.POST.get("creatime")
    gender = request.POST.get("gender")
    departname = request.POST.get("departname")

    models.UserInfo.objects.create(name=name,password=password,age=age,account=account,creatime=creatime,gender=gender,departname=departname)
    return redirect('/user/list/')


def user_update(request,nid):
    if request.method == 'GET':
        row_object = models.UserInfo.objects.filter(id=nid).first()
        gender_choices = models.UserInfo.gender_choices,
        depart_list = models.Department.objects.all(),
        return render(request,'user_update.html',{"row_object":row_object,"gender_choices":gender_choices,"depart_list":depart_list})

    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    creatime = request.POST.get("creatime")
    gender = request.POST.get("gender")
    departname = request.POST.get("departname")

    models.Department.objects.filter(id=nid).update(name=name,password=password,age=age,account=account,creatime=creatime,gender=gender,departname=departname)
    return redirect('/user/list/')

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

