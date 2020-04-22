#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 20:31
# @Author  : QS
# @File    : urls.py

import app.views as v
from django.urls import path

urlpatterns = [
    path('index/', v.index),
    path('detail/', v.detail),
    path('questions/', v.questions),
    path('add_question/', v.add_question),
]
