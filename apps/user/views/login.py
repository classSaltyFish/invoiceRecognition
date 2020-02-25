#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests

from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.models import User
from invoiceRecognition.local_setting import APP_ID, APP_SECRETKEY


# 小程序登录视图
class Login(APIView):
	"""
		微信登录逻辑
	"""
	permission_classes = (AllowAny,)

	def post(self, request):
		# 前端发送code到后端,后端发送网络请求到微信服务器换取openid
		code = request.data.get('code')
		if not code:
			return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
		url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
			.format(APP_ID, APP_SECRETKEY, code)
		r = requests.get(url)
		res = json.loads(r.text)
		openid = res['openid'] if 'openid' in res else None
		# 判断调用是否成功
		if not openid:
			return Response({'message': '微信调用失败'}, status=status.HTTP_503)

		# 如果用户是第一次登录，则自动创建账户
		# 如果用户不是第一次登录，则不会自动创建账户
		try:
			user = User.objects.get(openId=openid)
		except User.DoesNotExist:
			user = User()
			user.openId = openid
			user.save()

		# 返回openId和状态码,其实感觉还需要一个token
		resp_data = {
			"user_id": user.openId,
			"status": status.HTTP_200_OK,
		}

		return Response(resp_data)


# 管理系统登录视图
class AdminLogin(APIView):
	permission_classes = (AllowAny,)

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
			return Response({"mag": "传入数据格式错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		admin = auth.authenticate(username=username, password=password)
		if not admin:
			return Response({"msg": "密码或用户名不正确", "status": "error"})
		else:
			# 删除原有的Token
			old_token = Token.objects.filter(user=admin)
			old_token.delete()
			# 创建新的Token
			token = Token.objects.create(user=admin)
			return Response({
				"status": "ok",
				"msg": "登录成功",
				"username": username,
				"token": token.key,
				"currentAuthority": "admin"
			})
