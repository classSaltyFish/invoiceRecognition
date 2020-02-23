from apps.invoice.models import Invoice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, InvalidPage



class InvoiceList(APIView):
    def get(self, request):
        page_size = request.GET.get('pagesize')
        current_page = request.GET.get("page")

        queryset = Invoice.objects.all()
        total = queryset.count()

        data = []
        # 把url取出来,然后把发票数据取成json格式
        for e in queryset:
            temp = dict()
            urls = []

            imageset = e.image.all()
            for image in imageset:
                urls.append(image.img.url)
            temp['imgUrl'] = urls

            temp['id']=e.id
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

        #对分页进行处理，并且捕获异常和处理异常
        try:
            p = Paginator(data, page_size)
            contacts = p.page(current_page).object_list
        except InvalidPage:
            return Response({"msg":"页码有错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        context = {
            "results": contacts,
            "msg": True,
            "pagination":{
                "total": total,
                "pageSize": page_size,
                "current": current_page
            }
        }
        return Response(context, status=status.HTTP_200_OK)
