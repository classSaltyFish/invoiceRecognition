from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.invoice.models import Invoice
from apps.invoice.serializers import MySerializer

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
                'openId': openId,
                'msg': '用户不存在'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        queryset = Invoice.objects.filter(uploader__openId=openId, status__in=[0, 2])

        data = MySerializer(instance=queryset, many=True).data
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
        data = MySerializer(instance=queryset, many=True).data
        context = {
            'msg': 'ok',
            'results': data
        }
        return Response(context, status=status.HTTP_200_OK)
