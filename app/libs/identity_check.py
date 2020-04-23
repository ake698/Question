#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : QS
# @File    : identity_check.py
'''
检查登录状态
'''
from django.shortcuts import redirect
from functools import wraps

def login_need():
    def decorator(func):
        def wra(req,*arg,**kwargs):
            identity = req.session.get('username')
            if not identity:
                redirect("/login_register_page/")
            return func(req,*arg,**kwargs)
        return wra
    return decorator