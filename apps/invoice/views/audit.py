#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.invoice.models import Invoice


# 管理系统审核发票类视图
class AuditInvoice(APIView):
	# 测试用
	# permission_classes = (AllowAny,)

	# 运行使用
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		postbody = request.body
		json_result = json.loads(postbody)
		administrator = request.user

		try:
			invoiceCode = json_result['invoiceCode']
			operation = json_result['operation']
		except KeyError:
			return Response({"msg": "传入数据格式错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		try:
			invoice = Invoice.objects.get(invoiceCode=invoiceCode)
		except Invoice.DoesNotExist:
			return Response({"msg": "发票代码错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		if operation == 'pass':
			invoice.status = 1
			invoice.processer = administrator.username
			invoice.save()
		elif operation == 'reject':
			invoice.status = 2
			invoice.processer = administrator.username
			invoice.save()
		else:
			return Response({"msg": "操作错误错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		return Response({"msg": "success", "status": "ok"})
