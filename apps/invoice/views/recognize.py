#!/usr/bin/env python3
from rest_framework.views import APIView
from rest_framework.response import Response


class RecognizeInvoice(APIView):
	def post(self, request):
		img = request.FILE.get('image')
		img_bytes = img.read()  # 转为bytes形式
		# start recognize
		result = {}  # 识别结果保存在result中
		# end recognize
		data = {
			"invoiceCode": result.get("invoiceCode", ""),
			"invoiceNum": result.get("invoiceNum", ""),
			"invoiceDate": result.get("invoiceDate", ""),
			"invoiceType": result.get("invoiceType", ""),
			"sellerInfo": result.get("sellerInfo", ""),
			"purchaserInfo": result.get("purchaserInfo", ""),
			"commodityInfo": result.get("commodityInfo", "")
		}
		return Response({"result": data})


