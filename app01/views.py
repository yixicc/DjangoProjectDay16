from datetime import datetime

from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from dateutil.parser import parse
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

    departname = request.POST.get("title")
    models.Department.objects.create(title=departname)
    return redirect('/depart/list/')


def depart_update(request,nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_update.html',{"row_object":row_object})

    departname = request.POST.get("departname")
    models.Department.objects.filter(id=nid).update(title=departname)
    return redirect('/depart/list/')

def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


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


########################################################################

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


def prettynum_list(request):
    search_dict = {}
    search_word = request.GET.get('q')
    if search_word:
        search_dict["mobile__contains"] = search_word

    '''数据库中获取所有的靓号列表'''
    query_set = models.PrettyNum.objects.filter(**search_dict).order_by("-level")
    return render(request,'prettynum_list.html',{'query_set':query_set,'search_value':search_word})

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