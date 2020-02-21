from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        # depth = 1 深度控制，可以查到关联对象得具体信息
