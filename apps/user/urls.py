#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from apps.user.views.login import AdminLogin, Login
from apps.user.views.getInfo import GetUseInfo, GetAdminInfo
from apps.user.views.delete import DeleteUser
from apps.user.views.suspendAccount import SuspendUser, UnSuspendUser
from apps.user.views.list import UserList

urlpatterns = [
    # 小程序端接口
    path('login/', Login.as_view(), name='login'),
    path('getUserInfo/', GetUseInfo.as_view(), name='getUserInfo'),

    # 管理系统端接口
    path('adminLogin/', AdminLogin.as_view(), name='admin_login'),
    path('delete/', DeleteUser.as_view(), name='delete'),
    path('suspend/', SuspendUser.as_view(), name='suspend'),
    path('unsuspend/', UnSuspendUser.as_view(), name='unsuspend'),
    path('list/', UserList.as_view(), name='list'),
    path('currentUser/', GetAdminInfo.as_view())
]
