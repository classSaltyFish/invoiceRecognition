from apps.invoice.models import Invoice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, InvalidPage


# 管理端视图
#url:invoice/list
class InvoiceList(APIView):
    '''分页显示发票信息'''

    def get(self, request):
        '''
        GET请求
        :param request:
        key:   'all'  # 请求所有发票
                'wait'  # 请求待审核发票
                'record'  #请求已审核的发票
        current:  '1'  # 当前页码
        pageSize: '9'  # 每页显示条目数
        :return:
        '''
        page_size = request.GET.get('pagesize')
        current_page = request.GET.get("page")
        key = request.GET.get('key')
        if key == 'wait':
            queryset = Invoice.objects.filter(status__in=[0])
        elif key == 'record':
            queryset = Invoice.objects.filter(status__in=[1])
        else:
            queryset = Invoice.objects.all()
        total = queryset.count()

        data = []
        # 把url取出来,然后把发票数据取成json格式
        for e in queryset:
            temp = dict()
            urls = []

            # 多张图片的url的取法
            # imageset = e.image.all()
            # for image in imageset:
            #     urls.append(image.img.url)
            # temp['imgUrl'] = urls

            # 单张图片的用户的url的取法
            image = e.image.first()#这里是避免有多张图片时，出现错误
            if image is None:
                temp['imgUrl'] = ''
            else:
                temp['imgUrl'] = image.img.url
            temp['id'] = e.id
            temp['invoiceCode'] = e.invoiceCode
            temp['invoiceDate'] = e.invoiceDate
            temp['invoiceNum'] = e.invoiceNum
            temp['invoiceType'] = e.invoiceType
            temp['commodityInfo'] = e.commodityInfo
            temp['status'] = e.status
            temp['processDate'] = e.processDate
            temp['processor'] = e.processer
            temp['purchaseInfo'] = e.purchaserInfo
            temp['sellerInfo'] = e.sellerInfo
            temp['uploader'] = e.uploader_id
            temp['uploadDate'] = e.uploadDate
            data.append(temp)

        # 对分页进行处理，并且捕获异常和处理异常
        try:
            p = Paginator(data, page_size)
            contacts = p.page(current_page).object_list
        except InvalidPage:
            return Response({"msg": "页码有错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        context = {
            "results": contacts,
            "msg": True,
            "pagination": {
                "total": total,
                "pageSize": page_size,
                "current": current_page
            }
        }
        return Response(context, status=status.HTTP_200_OK)
