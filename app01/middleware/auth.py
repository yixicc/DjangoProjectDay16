# -*- coding: utf-8 -*-
# @Time : 2025/8/18 11:42
# @Author : zhou
# @File : auth.py
# @Software: PyCharm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):

        if request.path_info in ['/login/','/image/code/']:
            return

        # 如果方法无返回值，则继续往后走
        # 如果有返回值，  HttpResponse
        # 1. 获取当前访问用户的session信息，如果能读到，说明已登录过，可以继续往后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 2.没有登录过，返回登录页面
        return redirect('/login/')


    def process_response(self, request, response):
        return response
