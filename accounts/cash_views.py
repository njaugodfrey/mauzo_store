import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.db.models import Sum

from .forms import CashReceiptForm, ReceiptItemsForm
from .cash_models import CashReceipt, CashReceiptItems


def create_cash_receipt(request):
    form = CashReceiptForm
