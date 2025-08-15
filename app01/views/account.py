# -*- coding: utf-8 -*-
# @Time : 2025/8/15 15:51
# @Author : zhou
# @File : account.py
# @Software: PyCharm
from cProfile import label

from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5


class LoginView(BootStrapForm):
    username = forms.CharField(
        label = "用户名",
        widget =forms.TextInput,
        required = True,
    )

    password =forms.CharField(
        label = "密码",
        widget = forms.PasswordInput,
        required = True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def account_login(request):
    if request.method == "GET":
        # 展示页面
        form = LoginView
        return render(request,'login.html',{'form':form})

    form = LoginView(data = request.POST)
    if form.is_valid():
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request,'login.html',{'form':form})

        return redirect('/admin/list')

    return render(request, 'login.html', {'form': form})

