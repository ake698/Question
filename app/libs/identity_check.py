#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : QS
# @File    : identity_check.py
'''
检查登录状态
'''
from django.shortcuts import redirect


def login_need(func):
    def wra(req,*arg,**kwargs):
        identity = req.session.get('username')
        if identity:
            return func(req,*arg,**kwargs)
        else:
            return redirect("/login_register_page/")
    return wra
