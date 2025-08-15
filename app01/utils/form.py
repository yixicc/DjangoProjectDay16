# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:08
# @Author : zhou
# @File : form.py
# @Software: PyCharm
from os.path import exists

from django.core.exceptions import ValidationError

from app01 import models
from django import forms

from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class MyForm(forms.Form):
    name = forms.CharField(label='name',widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='password',widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.CharField(label='age',widget=forms.TextInput(attrs={'class':'form-control'}))
    account = forms.CharField(label='account',widget=forms.TextInput(attrs={'class':'form-control'}))
    creatime = forms.CharField(label='creatime',widget=forms.TextInput(attrs={'class':'form-control'}))
    # 性别字段
    gender_choices = models.UserInfo.gender_choices
    gender = forms.ChoiceField(
        label='性别',
        choices=gender_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # 部门字段
    depart = forms.ModelChoiceField(
        label='部门',
        queryset=models.Department.objects.all(),  # 获取所有部门
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class MyModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ('name', 'password', 'age', 'account', 'create_time', 'gender', 'depart')
        # widgets = {
        #     "name": forms.TextInput(attrs={'class':'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class PrettyNumModelForm(forms.ModelForm):
    # # 验证方式一：基于正则表达式
    # mobile = forms.CharField(
    #     label='mobile',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误")],
    # )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"
        # fields = ('mobile','price','level','status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    #验证方式二：基于钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise forms.ValidationError("格式错误")
        return txt_mobile


class PrettyNumEditModelForm(forms.ModelForm):

    # mobile = forms.CharField(label='手机号',disabled=True)

    class Meta:
        model = models.PrettyNum
        fields = ('mobile','price','level','status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    #验证方式二：基于钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise forms.ValidationError("格式错误")
        return txt_mobile


class AdminModelForm(BootStrapModelForm):

    confirm_password = forms.CharField(
        label='确认密码',
        disabled=False,
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ('username','password','confirm_password')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        print("password 是：",password)
        confirm_password = md5(self.cleaned_data['confirm_password'])
        if password != confirm_password:
            raise ValidationError("密码不一致")
        return confirm_password


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

class AdminResetModelForm(BootStrapModelForm):

    confirm_password = forms.CharField(
        label='确认密码',
        disabled=False,
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ('password','confirm_password',)
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    def clean_password(self):
        password = self.cleaned_data['password']
        md5_password = md5(password)
        # 和数据库中的密码比较，不能相同
        exists = models.Admin.objects.filter(id = self.instance.pk,password=md5_password).exists()
        if exists:
            raise forms.ValidationError("新密码不能和之前的密码相同")
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        print("pwd是：",password)
        confirm_password = md5(self.cleaned_data['confirm_password'])
        if password != confirm_password:
            raise forms.ValidationError("密码不一致")
        return confirm_password