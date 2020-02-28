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

	def post(self, request):
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
			user = invoice.uploader
		except :
			return Response({"msg": "发票信息错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		if operation == 'pass':
			invoice.status = 1
			user.reimbursement += invoice.invoiceMoney
		elif operation == 'reject':
			invoice.status = 2
			user.no_reimbursement -= invoice.invoiceMoney
		else:
			return Response({"msg": "操作错误错误", "status": "error"}, status=status.HTTP_400_BAD_REQUEST)
		invoice.processer = administrator.username
		invoice.save()
		user.save()
		return Response({"msg": "success", "status": "ok"})
