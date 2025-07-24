from django.shortcuts import render

from app01 import models


# Create your views here.

def depart_List(request):
    '''部门列表'''

    '''数据库中获取所有的部门列表'''
    query_set = models.Department.objects.all()

    return render(request,'depart_list.html',{'query_set':query_set})
