# -*- coding: utf-8 -*-
# @Time : 2025/8/4 11:08
# @Author : zhou
# @File : form.py
# @Software: PyCharm


from app01 import models
from django import forms

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