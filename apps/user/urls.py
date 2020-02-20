#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from apps.user.views.login import AdminLogin, Login
from apps.user.views.getInfo import GetUseInfo


urlpatterns = [
	# 小程序端接口
	path('login/', Login.as_view(), name='login'),
	path('getUserInfo/', GetUseInfo.as_view(), name='getUserInfo'),


	# 管理系统端接口
	path('adminLogin/', AdminLogin.as_view(), name='admin_login'),
]
