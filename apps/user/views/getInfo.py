#!/usr/bin/env python3
import json

from rest_framework import status
from rest_framework.permissions import AllowAny
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
