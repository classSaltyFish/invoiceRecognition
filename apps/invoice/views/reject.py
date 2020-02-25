from apps.invoice.models import Invoice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

#管理端视图
#url:invoice/reject
class InvoiceReject(APIView):
    '''驳回发票'''
    def post(self,request):
        '''
        post请求
        :param request:invoice请求
        :return:
        '''
        data=json.load(request)
        invoice_code=data['invoiceCode']
        invoice=Invoice.objects.get(invoiceCode=invoice_code)
        if invoice is None:
            return Response({'msg':'发票不存在'},status=status.HTTP_404_NOT_FOUND)
        invoice.status=2
        invoice.save()
        return Response({'msg':'ok'},status=status.HTTP_200_OK)