# Generated by Django 3.0.3 on 2020-02-17 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoiceCode', models.CharField(max_length=30, verbose_name='发票代码')),
                ('invoiceNum', models.CharField(blank=True, default='', max_length=30, verbose_name='发票号码')),
                ('invoiceData', models.DateField(blank=True, default='', verbose_name='开票日期')),
                ('invoiceType', models.CharField(blank=True, default='', max_length=30, verbose_name='发票类型')),
                ('sellerInfo', models.TextField(blank=True, default='', verbose_name='卖家信息')),
                ('purchaserInfo', models.TextField(blank=True, default='', verbose_name='买家信息')),
                ('commodityInfo', models.TextField(blank=True, default='', verbose_name='商品信息')),
                ('uploadData', models.DateField(auto_now_add=True, verbose_name='上传时间')),
                ('processData', models.DateField(auto_now=True, verbose_name='审批时间')),
                ('status', models.IntegerField(choices=[(0, '待审批'), (1, '审批通过'), (2, '退回')], default=0, verbose_name='审批状态')),
                ('processer', models.CharField(blank=True, default='', max_length=30, verbose_name='审批人')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='user.User', verbose_name='上传者')),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='图片')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='invoice.Invoice', verbose_name='所属发票')),
            ],
            options={
                'db_table': 'image',
            },
        ),
    ]