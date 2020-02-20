#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.models import User
from apps.invoice.models import Invoice, Image


class CreateInvoice(APIView):
	def post(self, request):
		postbody = request.body
		json_result = json.loads(postbody)
		try:
			openId = json_result['openId']
			user = User.objects.get(openId=openId)

			invoice_info = json_result['invoice_info']
			invoiceCode = invoice_info['invoiceCode']
			if Invoice.objects.filter(invoiceCode=invoiceCode).count() != 0:
				return Response({"mag": "exist"})
			new_invoice = Invoice(
				invoiceCode=invoiceCode,
				invoiceNum=invoice_info['invoiceNum'],
				invoiceDate=invoice_info['invoiceDate'],
				invoiceType=invoice_info['invoiceType'],
				sellerInfo=invoice_info['sellerInfo'],
				purchaserInfo=invoice_info['purchaserInfo'],
				commodityInfo=invoice_info['commodityInfo'],
				uploader=user
			)
			new_invoice.save()

			new_img = Image(
				img=request.FILES.get('image', ''),
				invoice=new_invoice
			)
		except KeyError:
			return Response({"mag": "传入数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)
		except User.DoesNotExist:
			return Response({"mag": "openId错误"}, status=status.HTTP_400_BAD_REQUEST)
		return Response({"mag": "success"})
