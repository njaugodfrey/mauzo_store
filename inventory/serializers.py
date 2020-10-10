from rest_framework import serializers
from drf_writable_nested import serializers as writable
from .models import Stock, GoodsReceipt, ReceivedGoods


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class ReceivedGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceivedGoods
        fields = [
            'document_ref', 'stock', 'quantity',
            'price', 'amount'
        ]


class GoodsReceiptSerializer(serializers.ModelSerializer):
    receipt_note = ReceivedGoodsSerializer(many=True)
    class Meta:
        model = GoodsReceipt
        fields = [
            'receipt_date', 'receipt_number', 'input_by', 'receipt_note'
        ]
