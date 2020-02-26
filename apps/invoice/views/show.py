from rest_framework.permissions import AllowAny

from apps.invoice.models import Invoice
from apps.invoice.serializers import InvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


# Create your views here.


# 小程序端视图
class ShowInvoices(APIView):
    """
    显示用户未得到报销和未通过的发票
    url：/invoice/showInvoice

    get：
    返回用户的发票信息
    请求参数：用户id
    返回参数：json数据

    """
    permission_classes = (AllowAny,)

    def get(self, request):
        # 获得该用户的待审批和退回的发票信息
        openId = request.GET.get('openId')
        user = Invoice.objects.filter(uploader__openId=openId)
        if user.count() == 0:
            context = {
                'status': status.HTTP_404_NOT_FOUND,
                'msg': '用户不存在'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        queryset = Invoice.objects.filter(uploader__openId=openId, status__in=[0, 2])

        data = []
        # 把url取出来,然后把发票数据取成json格式
        for e in queryset:
            temp = dict()
            # 单张图片的用户的url的取法
            image = e.image.first()  # 这里是避免有多张图片时，出现错误
            if image is None:
                temp['imgUrl'] = ''
            else:
                temp['imgUrl'] = image.img.url
            temp['id'] = e.id
            temp['invoiceCode'] = e.invoiceCode
            temp['invoiceDate'] = e.invoiceDate
            temp['invoiceNum'] = e.invoiceNum
            temp['invoiceType'] = e.invoiceType
            temp['commodityInfo'] = json.loads(e.commodityInfo)
            temp['status'] = e.status
            temp['processDate'] = e.processDate
            temp['processor'] = e.processer
            temp['purchaseInfo'] = json.loads(e.purchaserInfo)
            temp['sellerInfo'] = json.loads(e.sellerInfo)
            temp['uploader'] = e.uploader_id
            temp['uploadDate'] = e.uploadDate
            temp['invoiceMoney'] = e.invoiceMoney
            data.append(temp)

        context = {
            'msg': 'ok',
            'results': data
        }
        return Response(context, status=status.HTTP_200_OK)


# 小程序端视图
class ReimburseInvoice(APIView):
    """
    显示得到报销的发票
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        :param request:openId
        :return: json格式的已通过的发票信息
        """
        openId = request.GET.get('openId')
        user = Invoice.objects.filter(uploader__openId=openId)
        if user.count() == 0:
            context = {
                'msg': '用户不存在'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        queryset = Invoice.objects.filter(uploader__openId=openId, status__in=[1])
        data = []
        # 把url取出来,然后把发票数据取成json格式
        for e in queryset:
            temp = dict()
            # 单张图片的用户的url的取法
            image = e.image.first()  # 这里是避免有多张图片时，出现错误
            if image is None:
                temp['imgUrl'] = ''
            else:
                temp['imgUrl'] = image.img.url
            temp['id'] = e.id
            temp['invoiceCode'] = e.invoiceCode
            temp['invoiceDate'] = e.invoiceDate
            temp['invoiceNum'] = e.invoiceNum
            temp['invoiceType'] = e.invoiceType
            temp['commodityInfo'] = json.loads(e.commodityInfo)
            temp['status'] = e.status
            temp['processDate'] = e.processDate
            temp['processor'] = e.processer
            temp['purchaseInfo'] = json.loads(e.purchaserInfo)
            temp['sellerInfo'] = json.loads(e.sellerInfo)
            temp['uploader'] = e.uploader_id
            temp['uploadDate'] = e.uploadDate
            temp['invoiceMoney'] = e.invoiceMoney
            data.append(temp)

        context = {
            'msg': 'ok',
            'results': data
        }
        return Response(context, status=status.HTTP_200_OK)
