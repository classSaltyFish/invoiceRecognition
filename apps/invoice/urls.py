#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from apps.invoice.views.recognize import RecognizeInvoice
from apps.invoice.views.create import CreateInvoice


urlpatterns =[
	path('recognizeInvoice/', RecognizeInvoice.as_view(), name='recognizeInvoice'),
	path('createInvoice/', CreateInvoice.as_view(), name='createInvoice'),
]
