#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 20:31
# @Author  : QS
# @File    : urls.py

import app.views as v
from django.urls import path,re_path

urlpatterns = [
    path('index/', v.index),
    re_path(r'^detail/(?P<id>\d+)/$', v.detail),
    path('questions/', v.questions),
    path('add_question/', v.add_question),
    path('set_top/', v.set_top),
    path('delete_question/', v.delete_question),
    path('collection_question/', v.collection_question),
    path('delete_answer/', v.delete_answer),
    path('like_answer/', v.like_answer),
    path('select_answer/', v.select_answer),
    path('',v.index)
]
