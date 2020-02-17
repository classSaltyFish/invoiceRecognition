# Generated by Django 3.0.3 on 2020-02-17 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openId', models.CharField(max_length=30, verbose_name='用户id')),
                ('nickname', models.CharField(blank=True, default='', max_length=30, verbose_name='昵称')),
                ('status', models.IntegerField(choices=[(0, '冻结'), (1, '正常')], default=1, verbose_name='状态')),
                ('reimbursement', models.FloatField(default=0.0, verbose_name='已报销金额')),
                ('no_reimbursement', models.FloatField(default=0.0, verbose_name='待报销金额')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
