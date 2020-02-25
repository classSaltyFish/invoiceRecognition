#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from apps.invoice.views.recognize import RecognizeInvoice
from apps.invoice.views.create import CreateInvoice
from apps.invoice.views.show import ReimburseInvoice,ShowInvoices
from apps.invoice.views.list import InvoiceList
from apps.invoice.views.passby import InvoicePass
from apps.invoice.views.reject import InvoiceReject

urlpatterns =[
	path('recognizeInvoice/', RecognizeInvoice.as_view(), name='recognizeInvoice'),
	path('createInvoice/', CreateInvoice.as_view(), name='createInvoice'),
	path('showInvoice/',ShowInvoices.as_view()),
	path('reimburseInvoice/',ReimburseInvoice.as_view()),

	#管理端视图
	path('list/',InvoiceList.as_view()),
	path('pass/',InvoicePass.as_view()),
	path('reject/',InvoiceReject.as_view())
]
