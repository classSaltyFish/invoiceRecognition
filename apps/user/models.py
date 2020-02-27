from django.db import models


# Create your models here.
from django.utils import timezone


class User(models.Model):
	STATUS_ITEMS = [
		(0, '冻结'),
		(1, '正常')
	]
	openId = models.CharField(max_length=30, blank=False, verbose_name='用户id',unique=True)
	nickname = models.CharField(max_length=30, blank=True, default='', verbose_name='昵称')
	status = models.IntegerField(choices=STATUS_ITEMS, default=1, verbose_name='状态')
	reimbursement = models.FloatField(default=0.0, verbose_name='已报销金额')
	no_reimbursement = models.FloatField(default=0.0, verbose_name='待报销金额')
	latestSubmit = models.DateTimeField(blank=True, default=timezone.now, verbose_name='最新提交时间')

	def __str__(self):
		return self.nickname

	class Meta:
		db_table = 'user'
