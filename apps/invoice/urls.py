#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from apps.invoice.views.recognize import RecognizeInvoice
from apps.invoice.views.create import CreateInvoice
from apps.invoice.views.show import ReimburseInvoice, ShowInvoices
from apps.invoice.views.list import InvoiceList
from apps.invoice.views.audit import AuditInvoice

urlpatterns = [
	path('recognizeInvoice/', RecognizeInvoice.as_view(), name='recognizeInvoice'),
	path('createInvoice/', CreateInvoice.as_view(), name='createInvoice'),
	path('showInvoice/', ShowInvoices.as_view()),
	path('reimburseInvoice/', ReimburseInvoice.as_view()),

	# 管理端视图
	path('list/', InvoiceList.as_view()),
	path('auditInvoice/', AuditInvoice.as_view()),
]
