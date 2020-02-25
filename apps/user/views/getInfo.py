#!/usr/bin/env python3
import json

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.models import User


# 小程序端类视图
class GetUseInfo(APIView):
	permission_classes = (AllowAny,)

	def get(self, request):
		postbody = request.body
		json_result = json.loads(postbody)
		openId = json_result['openId']

		try:
			user = User.objects.get(openId=openId)
		except User.DoesNotExist as e:
			return Response(data={"mag": "error"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			data = {
				"status": user.status,
				"reimbursement": user.reimbursement,
				"no_reimbursement": user.no_reimbursement
			}
			return Response({"use_info": data})


# 管理系统类视图
class GetAdminInfo(APIView):
	# 测试用
	# permission_classes = (AllowAny,)

	# 运行使用
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		administrator = request.user
		data = {
			"msg": "success",
			"name": administrator.username,
			"userid": administrator.id
		}
		return Response(data)
