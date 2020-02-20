#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from rest_framework.authtoken.models import Token

from apps.user.models import User
from apps.user.serializers import UserSerializer


# 小程序登录视图
class Login(APIView):
	def post(self, request):
		postbody = request.body
		json_result = json.loads(postbody)
		try:
			user_info = json_result['user_info']
			openId = user_info['openId']
			nickname = user_info['nickname']
		except KeyError:
			return Response({"mag": "传入数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)
		user, created = User.objects.get_or_create(openId=openId)
		user.nickname = nickname
		if not user:
			return Response({"mag": "error"})
		else:
			return Response({"mag": "success"})


# 管理系统登录视图
class AdminLogin(APIView):
	def post(self, request):
		# 从请求的body中获得想要的信息

		postbody = request.body
		json_result = json.loads(postbody)

		# 对拿到的信息进行操作
		try:
			admin_info = json_result['user_info']
			username = admin_info['username']
			password = admin_info['password']
		except KeyError:
			return Response({"mag": "传入数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)
		admin = auth.authenticate(username=username, password=password)
		if not admin:
			return Response({'msg': '密码或用户名不正确'})
		else:
			# 删除原有的Token
			old_token = Token.objects.filter(user=admin)
			old_token.delete()
			# 创建新的Token
			token = Token.objects.create(user=admin)
			return Response({
				"msg": "登录成功",
				"username": username,
				"token": token.key
			})
