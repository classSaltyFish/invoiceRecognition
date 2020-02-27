import json

from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        # depth = 1 深度控制，可以查到关联对象得具体信息


class MySerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField(read_only=True)
    commodityInfo = serializers.SerializerMethodField(read_only=True)
    purchaseInfo = serializers.SerializerMethodField(read_only=True)
    sellerInfo = serializers.SerializerMethodField(read_only=True)
    uploader = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = ('id', 'invoiceCode', 'invoiceDate', 'invoiceNum', 'invoiceType',
                  'invoiceMoney', 'uploadDate', 'processDate', 'status', 'processer', 'uploader',
                  'commodityInfo', 'sellerInfo', 'purchaseInfo', 'imgUrl'
                  )
        # fields = '__all__'

    def get_imgUrl(self, obj):
        image = obj.image.first()
        if image is None:
            return ''
        else:
            return image.img.url

    def get_commodityInfo(self, obj):
        return json.loads(obj.commodityInfo)

    def get_purchaseInfo(self, obj):
        return json.loads(obj.purchaserInfo)

    def get_sellerInfo(self, obj):
        return json.loads(obj.sellerInfo)

    def get_uploader(self, obj):
        return obj.uploader.nickname
