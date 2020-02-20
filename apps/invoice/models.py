from django.db import models
from django.utils import timezone

from apps.user.models import User


# Create your models here.
class Invoice(models.Model):
	STATUS_ITEMS = [
		(0, '待审批'),
		(1, '审批通过'),
		(2, '退回'),
	]
	invoiceCode = models.CharField(max_length=30, blank=False, verbose_name='发票代码')
	invoiceNum = models.CharField(max_length=30, blank=True, default='', verbose_name='发票号码')
	invoiceDate = models.DateField(blank=True, default=timezone.now, verbose_name='开票日期')
	invoiceType = models.CharField(max_length=30, blank=True, default='', verbose_name='发票类型')
	sellerInfo = models.TextField(blank=True, default='', verbose_name='卖家信息')  # 存储形式为json_string
	purchaserInfo = models.TextField(blank=True, default='', verbose_name='买家信息')  # 存储形式为json_string
	commodityInfo = models.TextField(blank=True, default='', verbose_name='商品信息')  # 存储形式为json_string
	uploadDate = models.DateField(auto_now_add=True, verbose_name='上传时间')
	processDate = models.DateField(auto_now=True, verbose_name='审批时间')
	status = models.IntegerField(choices=STATUS_ITEMS, default=0, verbose_name='审批状态')
	processer = models.CharField(max_length=30, blank=True, default='', verbose_name='审批人')
	uploader = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='invoice', verbose_name='上传者')

	def __str__(self):
		return self.invoiceCode

	class Meta:
		db_table = 'invoice'


class Image(models.Model):
	img = models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='图片')
	invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE, related_name='image', verbose_name='所属发票')

	class Meta:
		db_table = 'image'
