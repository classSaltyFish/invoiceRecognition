#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.models import User
from apps.invoice.models import Invoice, Image


class UploadImg(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		img = request.FILES.get('image', '')
		user, _ = User.objects.get_or_create(openId='007', nickname='user7')
		sellerInfo = {
			"sellerName": "hust"
		}
		purchaseInfo = {
			"purchaseName": "huster007"
		}
		commodityInfo = [
			{
				"commodityName": "键盘233 机械",
				"commodityNum": 1,
				"commodityPrice": 799.00,
				"commodityAmount": 799.00,
				"commodityTax": 878.90
			},
			{
				"commodityName": "键盘233 普通",
				"commodityNum": 2,
				"commodityPrice": 199.00,
				"commodityAmount": 398.00,
				"commodityTax": 437.80
			}
		]
		totalAmount = 0.00
		for item in commodityInfo:
			totalAmount = totalAmount + item["commodityAmount"] + item["commodityTax"]
		invoice = Invoice(
			invoiceCode='048',
			invoiceMoney=totalAmount,
			sellerInfo=json.dumps(sellerInfo),
			purchaserInfo=json.dumps(purchaseInfo),
			commodityInfo=json.dumps(commodityInfo),
			uploader=user
		)
		invoice.save()
		user.no_reimbursement += totalAmount
		user.save()
		image = Image(img=img, invoice=invoice)
		image.save()
		return Response("success")
