from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from apps.invoice.models import Invoice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, InvalidPage

from apps.invoice.serializers import MySerializer


# 管理端视图
# url:invoice/list
class InvoiceList(APIView):
    """分页显示发票信息"""
    # # 测试用
    # permission_classes = (AllowAny,)

    # # 运行使用
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        GET请求
        :param request:
        key:   'all'  # 请求所有发票
                'wait'  # 请求待审核发票
                'record'  #请求已审核的发票
        current:  '1'  # 当前页码
        pageSize: '9'  # 每页显示条目数
        :return:
        """
        page_size = request.GET.get('pageSize')
        current_page = request.GET.get("current")
        key = request.GET.get('key')

        if key == 'wait':
            queryset = Invoice.objects.filter(status__in=[0])
        elif key == 'record':
            queryset = Invoice.objects.filter(status__in=[1,2])
        else:
            queryset = Invoice.objects.all()
        total = queryset.count()

        # 对分页进行处理，并且捕获异常和处理异常
        try:
            p = Paginator(queryset, page_size)
            contacts = p.page(current_page)
            result = MySerializer(instance=contacts, many=True)
        except InvalidPage:
            return Response({"msg": "页码有错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        context = {
            "results": result.data,
            "msg": True,
            "pagination": {
                "total": total,
                "pageSize": page_size,
                "current": current_page
            }
        }
        return Response(context, status=status.HTTP_200_OK)
