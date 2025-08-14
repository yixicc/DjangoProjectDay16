# -*- coding: utf-8 -*-
# @Time : 2025/8/14 11:13
# @Author : zhou
# @File : encrypt.py
# @Software: PyCharm
import hashlib
from django.conf import settings


def md5(data_string):
    m = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    m.update(data_string.encode('utf-8'))
    return m.hexdigest()
